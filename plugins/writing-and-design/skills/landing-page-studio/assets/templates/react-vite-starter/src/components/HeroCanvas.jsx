export default function HeroCanvas() {
  return <>
    <svg id="hero-svg" viewBox="0 0 1200 700" preserveAspectRatio="none" aria-hidden="true">
      <defs><linearGradient id="hero-gradient"><stop stopColor="#00e5ff" stopOpacity=".5" /><stop offset="1" stopColor="#7c3aed" stopOpacity=".3" /></linearGradient></defs>
      <path fill="url(#hero-gradient)" d="M0,350 C220,180 420,520 680,340 C890,210 1050,420 1200,260 L1200,700 L0,700 Z" />
    </svg>
    <canvas id="hero-canvas" hidden aria-hidden="true" />
  </>;
}
