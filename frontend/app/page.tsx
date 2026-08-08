const steps = [
  ["01", "Describe the issue", "Tell us what happened and where. Add a photo when it helps."],
  ["02", "Review the details", "CivicFix will help organize your report before you submit it."],
  ["03", "Track progress", "Follow the report from submission through resolution."],
];

export default function Home() {
  return (
    <main>
      <nav className="mx-auto flex max-w-6xl items-center justify-between px-6 py-6" aria-label="Main navigation">
        <a href="#top" className="text-xl font-bold tracking-tight text-emerald-950">CivicFix</a>
        <a href="#how-it-works" className="text-sm font-semibold text-slate-700 hover:text-emerald-800">How it works</a>
      </nav>

      <section id="top" className="mx-auto grid max-w-6xl gap-12 px-6 pb-20 pt-16 lg:grid-cols-[1.2fr_.8fr] lg:items-center lg:pt-24">
        <div>
          <p className="mb-5 text-sm font-bold uppercase tracking-[0.18em] text-emerald-700">Better streets start with clear reports</p>
          <h1 className="max-w-3xl text-5xl font-bold leading-[1.04] tracking-[-0.04em] text-emerald-950 sm:text-7xl">Make community problems visible.</h1>
          <p className="mt-7 max-w-2xl text-lg leading-8 text-slate-600">CivicFix helps residents report damaged roads, broken streetlights, waste problems, water leaks, and other public infrastructure issues—then track what happens next.</p>
          <div className="mt-9 flex flex-wrap gap-4">
            <a href="#phase-one" className="rounded-full bg-emerald-800 px-7 py-3.5 font-bold text-white shadow-sm hover:bg-emerald-900 focus:outline-none focus:ring-4 focus:ring-emerald-200">Report an issue</a>
            <a href="#how-it-works" className="rounded-full border border-slate-300 bg-white px-7 py-3.5 font-bold text-slate-800 hover:border-emerald-700">See how it works</a>
          </div>
        </div>
        <aside className="rounded-[2rem] bg-emerald-950 p-8 text-white shadow-xl shadow-emerald-950/10 sm:p-10">
          <p className="text-sm font-bold uppercase tracking-widest text-emerald-300">Built for follow-through</p>
          <p className="mt-6 text-3xl font-bold leading-tight">One clear place to report, review, and track local issues.</p>
          <div className="mt-10 grid grid-cols-2 gap-4 border-t border-white/15 pt-7">
            <div><p className="text-3xl font-bold">5</p><p className="mt-1 text-sm text-emerald-100">clear status stages</p></div>
            <div><p className="text-3xl font-bold">1</p><p className="mt-1 text-sm text-emerald-100">shared report record</p></div>
          </div>
        </aside>
      </section>

      <section id="how-it-works" className="bg-white py-20">
        <div className="mx-auto max-w-6xl px-6">
          <p className="text-sm font-bold uppercase tracking-[0.18em] text-emerald-700">How it works</p>
          <h2 className="mt-3 text-4xl font-bold tracking-tight text-emerald-950">From observation to action</h2>
          <div className="mt-12 grid gap-5 md:grid-cols-3">
            {steps.map(([number, title, description]) => (
              <article key={number} className="rounded-3xl border border-slate-200 bg-[#fbfcf9] p-7">
                <span className="text-sm font-bold text-emerald-700">{number}</span>
                <h3 className="mt-8 text-xl font-bold">{title}</h3>
                <p className="mt-3 leading-7 text-slate-600">{description}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section id="phase-one" className="mx-auto max-w-6xl px-6 py-20">
        <div className="rounded-3xl border border-amber-200 bg-amber-50 px-7 py-8 sm:flex sm:items-center sm:justify-between sm:gap-8">
          <div><h2 className="text-2xl font-bold text-amber-950">Reporting is coming in the next phase</h2><p className="mt-2 text-amber-900/80">This first foundation includes the public landing page and a working API health check. No reports are accepted or invented yet.</p></div>
          <span className="mt-5 inline-block shrink-0 rounded-full bg-amber-200 px-4 py-2 text-sm font-bold text-amber-950 sm:mt-0">Phase 1</span>
        </div>
      </section>

      <footer className="border-t border-slate-200 px-6 py-8 text-center text-sm text-slate-500">CivicFix — clear community issue reporting.</footer>
    </main>
  );
}

