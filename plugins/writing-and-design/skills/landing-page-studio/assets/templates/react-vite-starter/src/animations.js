function startAnimations({ gsap, anime, THREE, ready = true, heroEffect = "webgl", dependencyErrors = [] } = {}) {
  let alert;
  const report = message => {
    if (!alert) {
      alert = document.createElement("p");
      alert.setAttribute("role", "alert");
      alert.style.cssText = "position:relative;z-index:50;margin:1rem;padding:1rem;border:1px solid #fca5a5;background:#450a0a;color:white";
      document.querySelector("main")?.prepend(alert);
    }
    alert.textContent = [alert.textContent, message].filter(Boolean).join(" ");
    console.error(message);
  };
  const preference = window.matchMedia("(prefers-reduced-motion: reduce)");
  let stop = () => {};
  const refresh = () => {
    stop();
    alert?.remove(); alert = null;
    const cleanups = [];
    const reveal = [...document.querySelectorAll("[data-reveal]")];
    document.body.dataset.motion = preference.matches ? "reduced" : "full";
    reveal.forEach(el => { el.style.opacity = "1"; el.style.transform = "none"; });
    const heroSvg = document.getElementById("hero-svg");
    if (heroSvg) heroSvg.style.display = "none";
    if (preference.matches || !ready) { stop = () => {}; return; }
    if (dependencyErrors.length) report(`動畫工具 ${dependencyErrors.join("、")} 載入失敗，效果尚未完成。請檢查網路並重新載入。`);
    if (!gsap && !dependencyErrors.includes("GSAP")) report("動畫工具 GSAP 載入失敗，進場與互動效果尚未完成。");
    if (gsap && "IntersectionObserver" in window) {
      const observer = new IntersectionObserver(entries => entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        gsap.fromTo(entry.target, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: .8, overwrite: true });
        observer.unobserve(entry.target);
      }), { threshold: .12 });
      reveal.filter(el => el.getBoundingClientRect().top >= window.innerHeight).forEach(el => observer.observe(el));
      cleanups.push(() => { observer.disconnect(); gsap.killTweensOf(reveal); });
    }
    document.querySelectorAll("[data-magnetic]").forEach(el => {
      if (!gsap) return;
      const move = e => { if (e.pointerType === "touch") return; const r = el.getBoundingClientRect(); gsap.to(el, { x: (e.clientX-r.left-r.width/2)*.12, y: (e.clientY-r.top-r.height/2)*.12, duration: .2, overwrite: true }); };
      const leave = () => gsap.to(el, { x: 0, y: 0, duration: .25, overwrite: true });
      el.addEventListener("pointermove", move); el.addEventListener("pointerleave", leave);
      cleanups.push(() => { el.removeEventListener("pointermove", move); el.removeEventListener("pointerleave", leave); gsap.killTweensOf(el); el.style.transform = "none"; });
    });
    const canvas = document.getElementById("hero-canvas");
    const svg = document.getElementById("hero-svg");
    const startSvg = () => {
      if (svg) svg.style.display = "";
      if (!anime || !svg) { if (svg) svg.style.display = "none"; report("SVG 動畫無法啟動，請檢查動畫工具與圖層。"); return; }
      const animation = anime({ targets: svg, translateY: [0, -18], direction: "alternate", loop: true, easing: "easeInOutSine", duration: 4000 });
      cleanups.push(() => { animation.pause(); anime.remove(svg); svg.style.transform = "none"; });
    };
    let renderer, geometry, material, raf = 0;
    let resize, lost;
    const disposeWebGL = () => {
      cancelAnimationFrame(raf);
      if (resize) window.removeEventListener("resize", resize);
      if (lost && canvas) canvas.removeEventListener("webglcontextlost", lost);
      geometry?.dispose(); material?.dispose(); renderer?.dispose();
      if (canvas) canvas.hidden = true;
      if (svg) svg.style.display = "none";
    };
    if (heroEffect === "svg") {
      startSvg();
      stop = () => cleanups.reverse().forEach(fn => fn());
      return;
    }
    try {
      if (!THREE || !canvas) throw new Error("WebGL unavailable");
      canvas.hidden = false;
      renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(55, 1, .1, 100); camera.position.z = 6;
      geometry = new THREE.BufferGeometry();
      const positions = new Float32Array(850 * 3);
      for (let i = 0; i < positions.length; i++) positions[i] = (Math.random()-.5)*10;
      geometry.setAttribute("position", new THREE.BufferAttribute(positions, 3));
      material = new THREE.PointsMaterial({ color: 0x00e5ff, size: .03, transparent: true, opacity: .72 });
      const points = new THREE.Points(geometry, material); scene.add(points);
      resize = () => { const w = canvas.clientWidth || 1, h = canvas.clientHeight || 1; renderer.setSize(w, h, false); camera.aspect = w/h; camera.updateProjectionMatrix(); };
      resize(); window.addEventListener("resize", resize);
      lost = event => { event.preventDefault(); disposeWebGL(); report("WebGL 連線中斷，主視覺動畫尚未完成。"); };
      canvas.addEventListener("webglcontextlost", lost);
      let lastFrame = 0;
      const tick = (time = 0) => {
        const visible = !document.hidden && canvas.getBoundingClientRect().bottom > 0;
        if (visible && time-lastFrame >= 1000/30) { points.rotation.y += .0018; renderer.render(scene, camera); lastFrame = time; }
        raf = requestAnimationFrame(tick);
      };
      tick(); if (svg) svg.style.display = "none";
      cleanups.push(disposeWebGL);
    } catch (error) { disposeWebGL(); if (!dependencyErrors.includes("Three.js")) report("WebGL 無法啟動，主視覺動畫尚未完成。請檢查瀏覽器與圖形支援。"); }
    stop = () => { cleanups.reverse().forEach(fn => fn()); };
  };
  refresh(); preference.addEventListener("change", refresh);
  return () => { preference.removeEventListener("change", refresh); stop(); alert?.remove(); delete document.body.dataset.motion; };
}

export { startAnimations };
