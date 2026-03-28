import { Artwork } from '@/data/artworks'
import { VideoPlayer } from './VideoPlayer'
import { PaperColumn } from './PaperColumn'
import { DownloadButton } from './DownloadButton'

interface ArtworkSectionProps {
  artwork: Artwork
}

export function ArtworkSection({ artwork }: ArtworkSectionProps) {
  return (
    <section className="max-w-[1440px] mx-auto px-6 md:px-12 py-16 lg:py-24 border-b border-[#141414] last:border-0">
      <div className="mb-12">
        <h2 className="text-2xl font-semibold text-[#E8E8E8] tracking-tight">
          {artwork.title}
        </h2>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-12 items-start">
        {/* Video Column */}
        <div data-testid="video-column-wrapper">
          <VideoPlayer
            src={artwork.videoSrc}
            poster={artwork.posterSrc}
            title={artwork.title}
          />

          {/* 4K Photo Download Frame */}
          <div
            data-testid="download-frame"
            className="mt-4 flex items-center justify-between"
            style={{
              background: '#141414',
              border: '1px solid #1E1E1E',
              borderRadius: '4px',
              padding: '12px 16px',
            }}
          >
            <div>
              <p className="text-[#E8E8E8] text-sm font-semibold">4K Still Frame</p>
              <p className="text-[#555] text-xs mt-0.5">3840 × 2160 · PNG · 16-bit RGBA</p>
            </div>
            <DownloadButton
              href={artwork.posterSrc}
              filename={`${artwork.slug}-4k.png`}
              label={`Download 4K photo of ${artwork.title}`}
            />
          </div>
        </div>

        {/* Paper Column */}
        <PaperColumn paperSlug={artwork.paperSlug} />
      </div>
    </section>
  )
}
