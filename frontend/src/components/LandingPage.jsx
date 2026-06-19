export default function LandingPage({ onOpenLogin, onOpenRegister }) {
  return (
    <div className="landing">
      <div className="landing-glow landing-glow--left" aria-hidden="true" />
      <div className="landing-glow landing-glow--right" aria-hidden="true" />

      <header className="landing-nav">
        <div className="brand">
          <span className="brand-mark" aria-hidden="true">
            <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
              <circle cx="11" cy="11" r="9" stroke="currentColor" strokeWidth="1.5" />
              <path d="M7 11.5c1 2 2.5 3.2 4 3.2s3-1.2 4-3.2" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
            </svg>
          </span>
          <span className="brand-name">Petasight</span>
        </div>
        <div className="landing-nav-actions">
          <button type="button" className="btn btn-ghost" onClick={onOpenLogin}>
            Sign in
          </button>
          <button type="button" className="btn btn-primary" onClick={onOpenRegister}>
            Get started
          </button>
        </div>
      </header>

      <main className="landing-main">
        <section className="hero">
          <p className="hero-eyebrow">Color-aware AI chat</p>
          <h1 className="hero-title">
            Every reply paints
            <br />
            <span className="hero-gradient">its own mood</span>
          </h1>
          <p className="hero-lead">
            Type a city and temperature, a decimal, or anything else — the bot responds in
            conversation and colors each bubble from what you wrote.
          </p>
          <div className="hero-actions">
            <button type="button" className="btn btn-primary btn-lg" onClick={onOpenRegister}>
              Create free account
            </button>
            <button type="button" className="btn btn-outline btn-lg" onClick={onOpenLogin}>
              Sign in
            </button>
          </div>
        </section>

        <section className="feature-grid" aria-label="How coloring works">
          <article className="feature-card feature-card--temp">
            <span className="feature-badge">Rule 1</span>
            <h3>City + temperature</h3>
            <p>Deep blue at freezing, purple near 15°C, bright red at 35°C and above.</p>
            <code>Mumbai 32</code>
          </article>
          <article className="feature-card feature-card--decimal">
            <span className="feature-badge">Rule 2</span>
            <h3>Standalone decimal</h3>
            <p>Sepia ramp from the first two digits — lighter at .00, darker at .99.</p>
            <code>0.42</code>
          </article>
          <article className="feature-card feature-card--panic">
            <span className="feature-badge">Rule 3</span>
            <h3>Everything else</h3>
            <p>AI reads urgency — violet for panic, magenta in the middle, pale yellow when calm.</p>
            <code>HELP ME NOW</code>
          </article>
        </section>
      </main>

      <footer className="landing-footer">
        <p>Petasight team members only · @petasight.com</p>
      </footer>
    </div>
  );
}
