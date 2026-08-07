const facets = [
  { className: "facet facet-tall", label: "Form" },
  { className: "facet facet-round", label: "Light" },
  { className: "facet facet-small", label: "Detail" },
];

export default function Home() {
  return (
    <main>
      <header className="site-header">
        <a className="wordmark" href="#top" aria-label="Grace Mar home">
          Grace Mar
        </a>
        <nav aria-label="Primary navigation">
          <a href="#grace-gems">Grace Gems</a>
          <a href="#approach">Our approach</a>
          <a href="#contact">Contact</a>
        </nav>
      </header>

      <section className="hero" id="top">
        <div className="hero-copy">
          <p className="eyebrow">A considered commercial house</p>
          <h1>
            Made to carry
            <span>meaning.</span>
          </h1>
          <p className="hero-intro">
            Grace Mar is home to thoughtfully built brands, beginning with
            Grace Gems—our flagship jewelry brand.
          </p>
          <a className="text-link" href="#grace-gems">
            Discover Grace Gems <span aria-hidden="true">↓</span>
          </a>
        </div>

        <div className="hero-art" aria-hidden="true">
          <div className="orbit orbit-one" />
          <div className="orbit orbit-two" />
          <div className="gem gem-main">
            <i />
          </div>
          <div className="gem gem-small" />
          <p>Grace<br />Gems</p>
        </div>

        <p className="vertical-note" aria-hidden="true">EST. WITH INTENTION</p>
      </section>

      <section className="gems-section" id="grace-gems">
        <div className="section-number" aria-hidden="true">01</div>
        <div className="gems-heading">
          <p className="eyebrow">The flagship brand</p>
          <h2>Jewelry for the stories we choose to keep.</h2>
        </div>
        <p className="gems-copy">
          Grace Gems is taking shape as the first expression of Grace Mar: a
          jewelry brand guided by beauty, significance, and care in the details.
        </p>

        <div className="facet-row" aria-label="Grace Gems design study">
          {facets.map((facet) => (
            <div className={facet.className} key={facet.label}>
              <div className="facet-shape" aria-hidden="true" />
              <p>{facet.label}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="approach-section" id="approach">
        <p className="eyebrow">Our approach</p>
        <div className="principles">
          <article>
            <span>01</span>
            <h3>Thoughtful design</h3>
            <p>Every choice begins with purpose and earns its place.</p>
          </article>
          <article>
            <span>02</span>
            <h3>Clear promises</h3>
            <p>We say what we mean and grow trust through clarity.</p>
          </article>
          <article>
            <span>03</span>
            <h3>Deliberate growth</h3>
            <p>We build carefully, one enduring expression at a time.</p>
          </article>
        </div>
      </section>

      <section className="contact-section" id="contact">
        <p className="eyebrow">Coming soon</p>
        <h2>A new chapter is being set.</h2>
        <p>Grace Mar and Grace Gems are preparing for their next expression.</p>
        <div className="contact-rule" />
        <p className="contact-note">Contact details will be available here soon.</p>
      </section>

      <footer>
        <a className="wordmark" href="#top">Grace Mar</a>
        <p>Grace Gems is the flagship jewelry brand of Grace Mar.</p>
        <p>© 2026 Grace Mar</p>
      </footer>
    </main>
  );
}
