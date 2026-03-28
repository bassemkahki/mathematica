import { Artwork } from '@/data/artworks'
import { VideoPlayer } from './VideoPlayer'
import { PaperColumn } from './PaperColumn'
import { DownloadButton } from './DownloadButton'

interface ArtworkSectionProps {
  artwork: Artwork
}

export function ArtworkSection({ artwork }: ArtworkSectionProps) {
  return (
    <section
      className="max-w-[1400px] mx-auto px-6 md:px-16 py-20 lg:py-28"
      style={{ borderBottom: '1px solid #1A1A1A' }}
    >
      {/* Section heading */}
      <div className="mb-14">
        <h2
          className="text-3xl md:text-4xl"
          style={{
            fontFamily: "'EB Garamond', Georgia, serif",
            fontWeight: 400,
            color: '#E0E0E0',
            letterSpacing: '0.01em',
          }}
        >
          {artwork.title}
        </h2>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-10 lg:gap-16 items-start">
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
            className="mt-3 flex items-center justify-between"
            style={{
              background: '#111111',
              border: '1px solid #1A1A1A',
              borderRadius: '3px',
              padding: '10px 14px',
            }}
          >
            <div>
              <p
                className="text-sm"
                style={{
                  color: '#A0A0A0',
                  fontWeight: 400,
                  fontFamily: 'Inter, sans-serif',
                }}
              >
                4K Still Frame
              </p>
              <p
                className="text-xs mt-0.5"
                style={{ color: '#555', fontFamily: 'Inter, sans-serif' }}
              >
                3840 x 2160 &middot; PNG &middot; 16-bit RGBA
              </p>
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
