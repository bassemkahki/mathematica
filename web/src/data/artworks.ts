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
  {
    slug: 'primes',
    title: 'Prime Ulam Cylinder',
    videoSrc: '/videos/primes.mp4',
    posterSrc: '/posters/primes.png',
    paperSlug: 'primes',
  },
  {
    slug: 'fractal',
    title: 'L-System Fractal',
    videoSrc: '/videos/fractal.mp4',
    posterSrc: '/posters/fractal.png',
    paperSlug: 'fractal',
  },
]
