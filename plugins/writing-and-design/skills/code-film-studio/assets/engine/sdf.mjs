// Signed distance sculpting, meshed once at load with surface nets. Deterministic: no randomness, no time.
import * as THREE from 'three';

const H3 = (x, y, z) => Math.sqrt(x * x + y * y + z * z);
export const smin = (a, b, k) => { const h = Math.max(k - Math.abs(a - b), 0) / k; return Math.min(a, b) - h * h * k * 0.25; };
export const smax = (a, b, k) => -smin(-a, -b, k);
export const sph = (x, y, z, cx, cy, cz, r) => H3(x - cx, y - cy, z - cz) - r;
export const ell = (x, y, z, cx, cy, cz, rx, ry, rz) => {
  const px = (x - cx) / rx, py = (y - cy) / ry, pz = (z - cz) / rz;
  const k0 = H3(px, py, pz), k1 = H3(px / rx, py / ry, pz / rz);
  return k1 > 1e-9 ? k0 * (k0 - 1) / k1 : -Math.min(rx, ry, rz);
};
export const cap = (x, y, z, ax, ay, az, bx, by, bz, ra, rb = ra) => {
  const pax = x - ax, pay = y - ay, paz = z - az, bax = bx - ax, bay = by - ay, baz = bz - az;
  const h = Math.min(1, Math.max(0, (pax * bax + pay * bay + paz * baz) / (bax * bax + bay * bay + baz * baz)));
  return H3(pax - bax * h, pay - bay * h, paz - baz * h) - (ra + (rb - ra) * h);
};
export const box = (x, y, z, cx, cy, cz, hx, hy, hz, r = 0) => {
  const qx = Math.abs(x - cx) - hx + r, qy = Math.abs(y - cy) - hy + r, qz = Math.abs(z - cz) - hz + r;
  return H3(Math.max(qx, 0), Math.max(qy, 0), Math.max(qz, 0)) + Math.min(Math.max(qx, qy, qz), 0) - r;
};
export const gauss = (d, s) => Math.exp(-(d * d) / (s * s));
// value noise, hashed from integers only
const h3 = (i, j, k) => { let n = (Math.imul(i, 374761393) + Math.imul(j, 668265263) + Math.imul(k, 1440662683)) | 0; n = Math.imul(n ^ (n >>> 13), 1274126177); return ((n ^ (n >>> 16)) >>> 0) / 4294967295; };
export const noise3 = (x, y, z) => {
  const i = Math.floor(x), j = Math.floor(y), k = Math.floor(z), fx = x - i, fy = y - j, fz = z - k;
  const u = fx * fx * (3 - 2 * fx), v = fy * fy * (3 - 2 * fy), w = fz * fz * (3 - 2 * fz);
  const l = (a, b, t) => a + (b - a) * t;
  return l(l(l(h3(i, j, k), h3(i + 1, j, k), u), l(h3(i, j + 1, k), h3(i + 1, j + 1, k), u), v),
           l(l(h3(i, j, k + 1), h3(i + 1, j, k + 1), u), l(h3(i, j + 1, k + 1), h3(i + 1, j + 1, k + 1), u), v), w);
};
export const fbm3 = (x, y, z, o = 3) => { let a = 0.5, s = 0, n = 0; for (let i = 0; i < o; i++) { s += a * noise3(x, y, z); n += a; x *= 2.03; y *= 2.03; z *= 2.03; a *= 0.5; } return s / n; };

// f(x,y,z) -> distance. Returns a BufferGeometry with position, normal (from the field), color (colorFn) and uv (uvFn).
export function meshSDF(f, min, max, cell, { colorFn = null, uvFn = null, block = 4 } = {}) {
  const nx = Math.ceil((max[0] - min[0]) / cell) + 1, ny = Math.ceil((max[1] - min[1]) / cell) + 1, nz = Math.ceil((max[2] - min[2]) / cell) + 1;
  const V = new Float32Array(nx * ny * nz).fill(1);
  const idx = (i, j, k) => i + nx * (j + ny * k);
  const reach = block * cell * 1.8;
  for (let k0 = 0; k0 < nz; k0 += block) for (let j0 = 0; j0 < ny; j0 += block) for (let i0 = 0; i0 < nx; i0 += block) {
    const h = block * 0.5 * cell;
    const d = f(min[0] + i0 * cell + h, min[1] + j0 * cell + h, min[2] + k0 * cell + h);
    const i1 = Math.min(nx, i0 + block), j1 = Math.min(ny, j0 + block), k1 = Math.min(nz, k0 + block);
    if (Math.abs(d) > reach) { const s = d > 0 ? 1 : -1; for (let k = k0; k < k1; k++) for (let j = j0; j < j1; j++) for (let i = i0; i < i1; i++) V[idx(i, j, k)] = s; continue; }
    for (let k = k0; k < k1; k++) for (let j = j0; j < j1; j++) for (let i = i0; i < i1; i++)
      V[idx(i, j, k)] = f(min[0] + i * cell, min[1] + j * cell, min[2] + k * cell);
  }
  const vid = new Int32Array(nx * ny * nz).fill(-1), pos = [], ind = [];
  const corners = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0], [0, 0, 1], [1, 0, 1], [0, 1, 1], [1, 1, 1]];
  const edges = [[0, 1], [2, 3], [4, 5], [6, 7], [0, 2], [1, 3], [4, 6], [5, 7], [0, 4], [1, 5], [2, 6], [3, 7]];
  const cv = new Float32Array(8);
  for (let k = 0; k < nz - 1; k++) for (let j = 0; j < ny - 1; j++) for (let i = 0; i < nx - 1; i++) {
    let mask = 0;
    for (let c = 0; c < 8; c++) { cv[c] = V[idx(i + corners[c][0], j + corners[c][1], k + corners[c][2])]; if (cv[c] < 0) mask |= 1 << c; }
    if (mask === 0 || mask === 255) continue;
    let sx = 0, sy = 0, sz = 0, n = 0;
    for (const [a, b] of edges) {
      if ((cv[a] < 0) === (cv[b] < 0)) continue;
      const t = cv[a] / (cv[a] - cv[b]);
      sx += corners[a][0] + (corners[b][0] - corners[a][0]) * t; sy += corners[a][1] + (corners[b][1] - corners[a][1]) * t;
      sz += corners[a][2] + (corners[b][2] - corners[a][2]) * t; n++;
    }
    vid[idx(i, j, k)] = pos.length / 3;
    pos.push(min[0] + (i + sx / n) * cell, min[1] + (j + sy / n) * cell, min[2] + (k + sz / n) * cell);
  }
  const quad = (a, b, c, d, flip) => { if (a < 0 || b < 0 || c < 0 || d < 0) return; if (flip) ind.push(a, c, b, a, d, c); else ind.push(a, b, c, a, c, d); };
  for (let k = 1; k < nz - 1; k++) for (let j = 1; j < ny - 1; j++) for (let i = 1; i < nx - 1; i++) {
    const v0 = V[idx(i, j, k)] < 0;
    if (v0 !== (V[idx(i + 1, j, k)] < 0)) quad(vid[idx(i, j - 1, k - 1)], vid[idx(i, j, k - 1)], vid[idx(i, j, k)], vid[idx(i, j - 1, k)], !v0);
    if (v0 !== (V[idx(i, j + 1, k)] < 0)) quad(vid[idx(i - 1, j, k - 1)], vid[idx(i - 1, j, k)], vid[idx(i, j, k)], vid[idx(i, j, k - 1)], !v0);
    if (v0 !== (V[idx(i, j, k + 1)] < 0)) quad(vid[idx(i - 1, j - 1, k)], vid[idx(i, j - 1, k)], vid[idx(i, j, k)], vid[idx(i - 1, j, k)], !v0);
  }
  const P = new Float32Array(pos), N = new Float32Array(P.length), C = colorFn ? new Float32Array(P.length) : null, U = uvFn ? new Float32Array(P.length / 3 * 2) : null;
  const e = cell * 0.6, col = [0, 0, 0], uv = [0, 0];
  for (let v = 0; v < P.length; v += 3) {
    const x = P[v], y = P[v + 1], z = P[v + 2];
    let gx = f(x + e, y, z) - f(x - e, y, z), gy = f(x, y + e, z) - f(x, y - e, z), gz = f(x, y, z + e) - f(x, y, z - e);
    const l = H3(gx, gy, gz) || 1; gx /= l; gy /= l; gz /= l;
    N[v] = gx; N[v + 1] = gy; N[v + 2] = gz;
    if (C) { colorFn(x, y, z, gx, gy, gz, col); C[v] = col[0]; C[v + 1] = col[1]; C[v + 2] = col[2]; }
    if (U) { uvFn(x, y, z, uv); U[v / 3 * 2] = uv[0]; U[v / 3 * 2 + 1] = uv[1]; }
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.BufferAttribute(P, 3));
  g.setAttribute('normal', new THREE.BufferAttribute(N, 3));
  if (C) g.setAttribute('color', new THREE.BufferAttribute(C, 3));
  if (U) g.setAttribute('uv', new THREE.BufferAttribute(U, 2));
  g.setIndex(ind);
  g.computeBoundingSphere();
  return g;
}

// A tileable noise normal map and roughness map drawn once on canvases (pores, weave, grain of a surface).
export function noiseMaps(size, { scale = 24, strength = 1, octaves = 3, stretch = [1, 1], seed = 0 } = {}) {
  const hgt = new Float32Array(size * size);
  const tn = (x, y) => {                                  // tileable by blending four shifted samples
    const u = x / size, v = y / size, s = scale;
    const a = fbm3(u * s * stretch[0], v * s * stretch[1], seed, octaves), b = fbm3((u - 1) * s * stretch[0], v * s * stretch[1], seed, octaves);
    const c = fbm3(u * s * stretch[0], (v - 1) * s * stretch[1], seed, octaves), d = fbm3((u - 1) * s * stretch[0], (v - 1) * s * stretch[1], seed, octaves);
    return (a * (1 - u) + b * u) * (1 - v) + (c * (1 - u) + d * u) * v;
  };
  for (let y = 0; y < size; y++) for (let x = 0; x < size; x++) hgt[x + y * size] = tn(x, y);
  const mk = () => { const c = document.createElement('canvas'); c.width = c.height = size; return c; };
  const nc = mk(), rc = mk(), ng = nc.getContext('2d'), rg = rc.getContext('2d');
  const nd = ng.createImageData(size, size), rd = rg.createImageData(size, size);
  for (let y = 0; y < size; y++) for (let x = 0; x < size; x++) {
    const i = x + y * size, hx = hgt[(x + 1) % size + y * size] - hgt[(x + size - 1) % size + y * size];
    const hy = hgt[x + ((y + 1) % size) * size] - hgt[x + ((y + size - 1) % size) * size];
    const nxv = -hx * strength * 40, nyv = -hy * strength * 40, l = H3(nxv, nyv, 1);
    nd.data[i * 4] = 127.5 + 127.5 * nxv / l; nd.data[i * 4 + 1] = 127.5 + 127.5 * nyv / l; nd.data[i * 4 + 2] = 127.5 + 127.5 / l; nd.data[i * 4 + 3] = 255;
    const r = 255 * Math.min(1, Math.max(0, 0.5 + (hgt[i] - 0.5) * 1.6));
    rd.data[i * 4] = rd.data[i * 4 + 1] = rd.data[i * 4 + 2] = r; rd.data[i * 4 + 3] = 255;
  }
  ng.putImageData(nd, 0, 0); rg.putImageData(rd, 0, 0);
  const tex = (c, srgb) => { const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.anisotropy = 8; if (srgb) t.colorSpace = THREE.SRGBColorSpace; return t; };
  return { normal: tex(nc, false), rough: tex(rc, false), height: hgt };
}
