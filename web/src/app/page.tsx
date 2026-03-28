import { artworks } from '@/data/artworks'
import { SiteHeader } from '@/components/SiteHeader'
import { ArtworkSection } from '@/components/ArtworkSection'

export default function GalleryPage() {
  if (!artworks || artworks.length === 0) {
    return (
      <main className="min-h-screen flex flex-col items-center justify-center p-8" style={{ background: '#0A0A0A' }}>
        <h1
          className="text-2xl mb-4"
          style={{ fontFamily: "'EB Garamond', Georgia, serif", color: '#E0E0E0' }}
        >
          No artworks yet.
        </h1>
        <p style={{ color: '#555', fontStyle: 'italic', fontFamily: "'EB Garamond', Georgia, serif" }}>
          Rendered artworks will appear here once the pipeline has completed.
        </p>
      </main>
    )
  }

  return (
    <main className="min-h-screen" style={{ background: '#0A0A0A' }}>
      <SiteHeader />
      <div>
        {artworks.map((artwork) => (
          <ArtworkSection key={artwork.slug} artwork={artwork} />
        ))}
      </div>
      <footer
        className="py-28 text-center text-xs"
        style={{
          color: '#333',
          fontFamily: 'Inter, sans-serif',
          letterSpacing: '0.05em',
        }}
      >
        {new Date().getFullYear()} Mathematica
      </footer>
    </main>
  )
}
