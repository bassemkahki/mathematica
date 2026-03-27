'use client'

import { useRef, useState } from 'react'

interface VideoPlayerProps {
  src: string
  poster: string
  title: string
}

export function VideoPlayer({ src, poster, title }: VideoPlayerProps) {
  const videoRef = useRef<HTMLVideoElement>(null)
  const [playing, setPlaying] = useState(false)
  const [error, setError] = useState(false)
  const [loading, setLoading] = useState(false)

  function handlePlay() {
    if (!videoRef.current) return
    setLoading(true)
    videoRef.current.play().then(() => {
      setPlaying(true)
      setLoading(false)
    }).catch(() => {
      setError(true)
      setLoading(false)
    })
  }

  return (
    <div
      className="relative w-full"
      style={{ aspectRatio: '16/9' }}
      data-testid="video-column"
    >
      <video
        ref={videoRef}
        src={src}
        poster={poster}
        preload="none"
        controls={playing}
        aria-label={title}
        onError={() => setError(true)}
        onWaiting={() => setLoading(true)}
        onPlaying={() => setLoading(false)}
        className="w-full h-full object-cover"
      />

      {/* Play overlay — visible by default, fades out when playing */}
      {!playing && !error && (
        <button
          onClick={handlePlay}
          aria-label="Play artwork"
          className="absolute inset-0 flex items-center justify-center transition-opacity duration-200"
          style={{ opacity: loading ? 0.5 : 0.7 }}
          onMouseEnter={e => { (e.currentTarget as HTMLButtonElement).style.opacity = '1' }}
          onMouseLeave={e => { (e.currentTarget as HTMLButtonElement).style.opacity = '0.7' }}
        >
          {loading ? (
            <p className="italic" style={{ color: '#888', fontSize: '16px' }}>Loading...</p>
          ) : (
            <span
              className="flex items-center justify-center rounded-full"
              style={{
                width: '44px',
                height: '44px',
                background: 'rgba(255,255,255,0.15)',
              }}
            >
              {/* SVG play triangle — white, 20px */}
              <svg
                width="20"
                height="20"
                viewBox="0 0 20 20"
                fill="none"
                aria-hidden="true"
              >
                <polygon points="5,3 17,10 5,17" fill="#E8E8E8" />
              </svg>
            </span>
          )}
        </button>
      )}

      {/* Error state */}
      {error && (
        <div className="absolute inset-0 flex items-end justify-start p-4">
          <p className="italic" style={{ color: '#888', fontSize: '16px' }}>
            Video unavailable — file may still be rendering.
          </p>
        </div>
      )}
    </div>
  )
}
