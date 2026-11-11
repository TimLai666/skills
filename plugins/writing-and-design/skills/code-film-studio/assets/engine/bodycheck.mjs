// Bodies that obey the room: joint limits, limb solving toward a contact, and a check that finds every frame where a
// body part passes through the floor, an object, or another body part. Plain arrays ([x, y, z], metres, y up), no
// dependencies, so it runs in the film page and in Node. The same three ideas apply in Blender (limit constraints,
// IK with a pole target, a script that samples frames); see references/building.md.

const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]], add = (a, b) => [a[0] + b[0], a[1] + b[1], a[2] + b[2]];
const mul = (a, k) => [a[0] * k, a[1] * k, a[2] * k], dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const len = (a) => Math.sqrt(dot(a, a)), norm = (a) => { const l = len(a) || 1; return mul(a, 1 / l); };
const clamp = (x, a, b) => Math.min(b, Math.max(a, x));

// 1. Joint limits, in radians. A hinge (elbow, knee) only bends one way: its lower limit is 0, never negative.
export const HUMAN_LIMITS = {
  elbow: [0, 2.55], knee: [0, 2.45],
  shoulderForward: [-0.9, 3.0], shoulderOut: [-0.25, 2.9], shoulderTwist: [-1.4, 1.4],
  hipForward: [-0.45, 2.1], hipOut: [-0.35, 0.8], spineBend: [-0.35, 1.3], spineTwist: [-0.6, 0.6],
  neckYaw: [-1.2, 1.2], neckPitch: [-0.75, 0.75], wristPitch: [-1.2, 1.2], wristRoll: [-0.5, 0.6],
};
// clampPose({ elbow: -0.3, knee: 1.0 }) -> { pose: { elbow: 0, knee: 1.0 }, hits: ['elbow -0.30 -> 0.00'] }
// Clamp every pose before it is applied, and treat a hit as a bug in the animation, not as something to hide.
export function clampPose(pose, limits = HUMAN_LIMITS) {
  const out = {}, hits = [];
  for (const [k, v] of Object.entries(pose)) {
    const key = Object.keys(limits).find((n) => k === n || k.toLowerCase().startsWith(n.toLowerCase()));
    if (key === undefined || typeof v !== 'number') { out[k] = v; continue; }
    const c = clamp(v, limits[key][0], limits[key][1]); out[k] = c;
    if (Math.abs(c - v) > 1e-6) hits.push(`${k} ${v.toFixed(2)} -> ${c.toFixed(2)}`);
  }
  return { pose: out, hits };
}

// 2. Two-bone solve: put the hand (or foot) on a target and decide where the elbow (or knee) points with a pole.
// root: shoulder or hip position; target: where the wrist or ankle must be; pole: a point the middle joint bends toward
// (elbows: behind and outside the body; knees: in front). Returns the middle joint, the end actually reached, and
// whether the target was out of reach (then the limb is straight toward it and the body must move closer).
export function twoBone(root, target, pole, upper, lower) {
  const to = sub(target, root), d0 = len(to), n = norm(to);
  const d = clamp(d0, Math.abs(upper - lower) + 1e-4, upper + lower - 1e-4);
  const x = (upper * upper - lower * lower + d * d) / (2 * d), h = Math.sqrt(Math.max(0, upper * upper - x * x));
  let p = sub(sub(pole, root), mul(n, dot(sub(pole, root), n)));
  if (len(p) < 1e-6) p = Math.abs(n[1]) < 0.9 ? [0, 1, 0] : [0, 0, 1];
  p = norm(p);
  const mid = add(add(root, mul(n, x)), mul(p, h));
  return { mid, end: add(root, mul(n, d)), outOfReach: d0 > upper + lower + 1e-4, flex: Math.PI - Math.acos(clamp((upper * upper + lower * lower - d * d) / (2 * upper * lower), -1, 1)) };
}
// A planted foot: give the ankle the position it had when it landed and solve the leg to it every frame until it lifts.
export const plantFoot = (hip, landed, kneePole, thigh, shin, floorY = 0, ankleHeight = 0.07) =>
  twoBone(hip, [landed[0], Math.max(landed[1], floorY + ankleHeight), landed[2]], kneePole, thigh, shin);

// 3. The check. Describe a body as capsules { name, a, b, r, skip?: [names it may touch] } and the set as boxes
// { name, min, max }. penetrations() lists what passes through what at one moment; checkFrames() runs a whole range.
const segPoint = (a, b, t) => add(a, mul(sub(b, a), t));
const boxDist = (p, bx) => { const d = [0, 1, 2].map((i) => Math.max(bx.min[i] - p[i], 0, p[i] - bx.max[i])); return len(d); };
const inBox = (p, bx) => [0, 1, 2].every((i) => p[i] > bx.min[i] && p[i] < bx.max[i]);
function segSeg(a0, a1, b0, b1) {                      // closest distance between two segments
  const u = sub(a1, a0), v = sub(b1, b0), w = sub(a0, b0), A = dot(u, u), B = dot(u, v), C = dot(v, v), D = dot(u, w), E = dot(v, w);
  const den = A * C - B * B; let s = den < 1e-9 ? 0 : clamp((B * E - C * D) / den, 0, 1);
  let t = C < 1e-9 ? 0 : clamp((B * s + E) / C, 0, 1); s = A < 1e-9 ? 0 : clamp((B * t - D) / A, 0, 1);
  return len(sub(segPoint(a0, a1, s), segPoint(b0, b1, t)));
}
export function penetrations(capsules, boxes = [], { floorY = 0, tolerance = 0.01, samples = 7 } = {}) {
  const out = [];
  for (const c of capsules) {
    const low = Math.min(c.a[1], c.b[1]) - c.r;
    if (low < floorY - tolerance && !(c.skip || []).includes('floor')) out.push({ part: c.name, into: 'floor', depth: floorY - low });
    for (const bx of boxes) {
      if ((c.skip || []).includes(bx.name)) continue;
      let worst = 0;
      for (let i = 0; i < samples; i++) { const p = segPoint(c.a, c.b, i / (samples - 1)); const d = inBox(p, bx) ? -1 : boxDist(p, bx); worst = Math.max(worst, d < 0 ? c.r : c.r - d); }
      if (worst > tolerance) out.push({ part: c.name, into: bx.name, depth: worst });
    }
  }
  for (let i = 0; i < capsules.length; i++) for (let j = i + 1; j < capsules.length; j++) {
    const p = capsules[i], q = capsules[j];
    if ((p.skip || []).includes(q.name) || (q.skip || []).includes(p.name)) continue;      // neighbours on the skeleton touch by design
    const over = p.r + q.r - segSeg(p.a, p.b, q.a, q.b);
    if (over > tolerance) out.push({ part: p.name, into: q.name, depth: over });
  }
  return out;
}
// checkFrames((frame) => ({ capsules, boxes }), 0, 7199, 24) -> a list of intervals, worst first, ready to print.
// Run it on every shot before rendering. An empty list is the bar; anything else is fixed in the animation or
// listed for the user as a deliberate contact (a hand resting on a table: add the table to that capsule's skip).
export function checkFrames(sample, start, end, fps = 24, opts = {}) {
  const open = new Map(), done = [];
  for (let f = start; f <= end + 1; f++) {
    const hits = f <= end ? (() => { const s = sample(f); return penetrations(s.capsules, s.boxes || [], opts); })() : [];
    const seen = new Set();
    for (const h of hits) { const k = `${h.part} into ${h.into}`; seen.add(k); const o = open.get(k) || { what: k, from: f, to: f, depth: 0 }; o.to = f; o.depth = Math.max(o.depth, h.depth); open.set(k, o); }
    for (const [k, o] of [...open]) if (!seen.has(k)) { done.push(o); open.delete(k); }
  }
  return done.sort((a, b) => b.depth - a.depth).map((o) => `${o.what}: ${(o.from / fps).toFixed(2)}s to ${(o.to / fps).toFixed(2)}s, up to ${(o.depth * 100).toFixed(1)} cm`);
}
