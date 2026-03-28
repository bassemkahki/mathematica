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
      style={{
        aspectRatio: '16/9',
        borderRadius: '2px',
        overflow: 'hidden',
        border: '1px solid #1A1A1A',
      }}
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
        style={{ background: '#080808' }}
      />

      {/* Play overlay */}
      {!playing && !error && (
        <button
          onClick={handlePlay}
          aria-label="Play artwork"
          className="absolute inset-0 flex items-center justify-center transition-opacity duration-300"
          style={{ opacity: loading ? 0.5 : 0.6 }}
          onMouseEnter={e => { (e.currentTarget as HTMLButtonElement).style.opacity = '0.9' }}
          onMouseLeave={e => { (e.currentTarget as HTMLButtonElement).style.opacity = '0.6' }}
        >
          {loading ? (
            <p style={{ color: '#777', fontSize: '14px', fontFamily: 'Inter, sans-serif', fontStyle: 'italic' }}>
              Loading...
            </p>
          ) : (
            <span
              className="flex items-center justify-center rounded-full"
              style={{
                width: '48px',
                height: '48px',
                background: 'rgba(255,255,255,0.08)',
                border: '1px solid rgba(255,255,255,0.12)',
                backdropFilter: 'blur(4px)',
              }}
            >
              <svg
                width="18"
                height="18"
                viewBox="0 0 18 18"
                fill="none"
                aria-hidden="true"
              >
                <polygon points="5,2 16,9 5,16" fill="#D0D0D0" />
              </svg>
            </span>
          )}
        </button>
      )}

      {/* Error state */}
      {error && (
        <div className="absolute inset-0 flex items-end justify-start p-4">
          <p style={{ color: '#555', fontSize: '14px', fontFamily: 'Inter, sans-serif', fontStyle: 'italic' }}>
            Video unavailable
          </p>
        </div>
      )}
    </div>
  )
}
