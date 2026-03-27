import { artworks } from '@/data/artworks'
import { SiteHeader } from '@/components/SiteHeader'
import { ArtworkSection } from '@/components/ArtworkSection'

export default function GalleryPage() {
  if (!artworks || artworks.length === 0) {
    return (
      <main className="min-h-screen bg-[#0A0A0A] flex flex-col items-center justify-center p-8">
        <h1 className="text-2xl font-semibold text-[#E8E8E8] mb-4">No artworks yet.</h1>
        <p className="text-[#888] italic">
          Rendered artworks will appear here once the pipeline has completed.
        </p>
      </main>
    )
  }

  return (
    <main className="min-h-screen bg-[#0A0A0A]">
      <SiteHeader />
      <div className="divide-y divide-[#141414]">
        {artworks.map((artwork) => (
          <ArtworkSection key={artwork.slug} artwork={artwork} />
        ))}
      </div>
      <footer className="py-24 text-center text-[#444] text-sm">
        &copy; {new Date().getFullYear()} Mathematica Art. All mathematical truths reserved.
      </footer>
    </main>
  )
}
