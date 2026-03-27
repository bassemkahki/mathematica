import { Artwork } from '@/data/artworks'
import { VideoPlayer } from './VideoPlayer'
import { PaperColumn } from './PaperColumn'

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
        </div>

        {/* Paper Column */}
        <PaperColumn paperSlug={artwork.paperSlug} />
      </div>
    </section>
  )
}
