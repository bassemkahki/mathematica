export function SiteHeader() {
  return (
    <header
      className="py-20 md:py-28 text-center"
      style={{ borderBottom: '1px solid #1A1A1A' }}
    >
      <p
        className="text-xs tracking-[0.3em] uppercase mb-6"
        style={{ color: '#555', fontFamily: 'Inter, sans-serif', fontWeight: 400 }}
      >
        A Gallery of
      </p>
      <h1
        className="text-5xl md:text-7xl mb-4"
        style={{
          fontFamily: "'EB Garamond', Georgia, serif",
          fontWeight: 400,
          color: '#E0E0E0',
          letterSpacing: '0.02em',
        }}
      >
        Mathematica
      </h1>
      <p
        className="text-lg md:text-xl mt-6"
        style={{
          fontFamily: "'EB Garamond', Georgia, serif",
          fontStyle: 'italic',
          fontWeight: 400,
          color: '#777',
          letterSpacing: '0.01em',
        }}
      >
        Mathematical truth made visible
      </p>
    </header>
  )
}
