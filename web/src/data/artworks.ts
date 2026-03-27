export interface Artwork {
  slug: string
  title: string
  videoSrc: string   // e.g. '/videos/fibonacci.mp4'
  posterSrc: string  // e.g. '/posters/fibonacci.png'
  paperSlug: string  // maps to public/papers/{paperSlug}.html
}

export const artworks: Artwork[] = [
  {
    slug: 'fibonacci',
    title: 'Fibonacci Spiral',
    videoSrc: '/videos/fibonacci.mp4',
    posterSrc: '/posters/fibonacci.png',
    paperSlug: 'fibonacci',
  },
]
