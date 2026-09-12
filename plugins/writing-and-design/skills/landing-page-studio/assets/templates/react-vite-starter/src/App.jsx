import { useEffect } from "react";
import { startAnimations } from "./animations";
import { Icon } from "@iconify/react";
import HeroCanvas from "./components/HeroCanvas";

const cards = [
  { icon: "solar:bolt-bold", title: "{{value_prop_1}}", desc: "{{value_prop_1_description}}" },
  { icon: "solar:shield-check-bold", title: "{{value_prop_2}}", desc: "{{value_prop_2_description}}" },
  { icon: "solar:rocket-bold", title: "{{value_prop_3}}", desc: "{{value_prop_3_description}}" },
];

export default function App() {
  useEffect(() => {
    const preference = window.matchMedia("(prefers-reduced-motion: reduce)");
    let disposed = false;
    let loaded = false;
    let cleanup = startAnimations({ ready: false });
    const load = async () => {
      if (preference.matches || loaded) return;
      loaded = true;
      const dependencyErrors = [];
      const failed = name => { dependencyErrors.push(name); return null; };
      const [gsapModule, animeModule, threeModule] = await Promise.all([
        import("gsap").catch(() => failed("GSAP")), import("animejs").catch(() => failed("Anime.js")), import("three").catch(() => failed("Three.js")),
      ]);
      if (disposed) return;
      cleanup();
      cleanup = startAnimations({ gsap: gsapModule?.default, anime: animeModule?.default, THREE: threeModule, dependencyErrors });
    };
    const timer = window.setTimeout(load, 100);
    preference.addEventListener("change", load);
    return () => { disposed = true; window.clearTimeout(timer); preference.removeEventListener("change", load); cleanup(); };
  }, []);

  return (
    <div className="min-h-screen bg-bg text-white font-body">
      <header className="sticky top-0 z-40 border-b border-white/10 bg-black/25 backdrop-blur-md">
        <nav className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <span className="font-display text-2xl">{"{{brand_name}}"}</span>
          <a className="rounded-full bg-accent px-5 py-2 text-sm font-bold text-slate-900" href="#cta">
            {"{{primary_cta}}"}
          </a>
        </nav>
      </header>

      <main>
      <section className="relative overflow-hidden px-6 pb-20 pt-20">
        <HeroCanvas />
        <div className="hero-glow pointer-events-none absolute -top-10 right-0 h-64 w-64 rounded-full bg-cyan-300/20 blur-3xl" />
        <div className="relative mx-auto max-w-6xl">
          <p data-reveal className="mb-3 inline-flex rounded-full border border-cyan-300/70 px-3 py-1 text-xs uppercase tracking-[0.18em] text-cyan-200">
            {"{{audience_or_product_category}}"}
          </p>
          <h1 data-reveal className="max-w-3xl font-display text-4xl leading-tight md:text-6xl">
            {"{{hero_title}}"}
          </h1>
          <p data-reveal className="mt-4 max-w-2xl text-lg text-slate-200">
            {"{{hero_subtitle}}"}
          </p>
          <div data-reveal className="mt-8 flex gap-4">
            <a data-magnetic href="#cta" className="rounded-full bg-accent px-7 py-3 text-sm font-bold text-slate-900">
              {"{{primary_cta}}"}
            </a>
            <a href="#value" className="rounded-full border border-white/50 px-7 py-3 text-sm font-bold">
              了解更多
            </a>
          </div>
        </div>
      </section>

      <section id="value" className="mx-auto grid max-w-6xl gap-6 px-6 pb-20 md:grid-cols-3">
        {cards.map((card) => (
          <article
            key={card.title}
            data-reveal
            className="glass rounded-2xl p-6"
          >
            <Icon icon={card.icon} width={26} />
            <h2 className="mt-4 text-xl font-bold">{card.title}</h2>
            <p className="mt-2 text-sm text-slate-300">{card.desc}</p>
          </article>
        ))}
      </section>

      {/* Populate two distinct verified evidence types before delivery, e.g. a sourced
          case study and an approved customer quotation. Omit unavailable evidence. */}
      <section id="proof" hidden />

      <section id="cta" className="mx-auto max-w-6xl px-6 pb-24">
        <div
          data-reveal
          className="beam-border glass rounded-3xl p-10 text-center"
        >
          <h2 className="font-display text-4xl">{"{{final_cta_title}}"}</h2>
          <p className="mx-auto mt-4 max-w-2xl text-slate-200">{"{{final_cta_subtitle}}"}</p>
          <a data-magnetic href="{{primary_cta_url}}" className="mt-8 inline-flex rounded-full bg-white px-8 py-3 text-sm font-bold text-slate-900">
            {"{{primary_cta}}"}
          </a>
        </div>
      </section>

      </main>
      <footer className="border-t border-white/10 py-8 text-center text-xs text-slate-400">
        © {"{{year}}"} {"{{brand_name}}"}
      </footer>
    </div>
  );
}
