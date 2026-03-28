'use client'

interface DownloadButtonProps {
  href: string
  filename: string
  label: string
}

export function DownloadButton({ href, filename, label }: DownloadButtonProps) {
  return (
    <a
      href={href}
      download={filename}
      aria-label={label}
      className="flex items-center gap-2 text-[#E8E8E8] text-sm"
      style={{
        background: '#1E1E1E',
        border: '1px solid #2A2A2A',
        borderRadius: '4px',
        padding: '8px 14px',
        textDecoration: 'none',
        transition: 'background 0.15s',
      }}
      onMouseEnter={e => { (e.currentTarget as HTMLAnchorElement).style.background = '#2A2A2A' }}
      onMouseLeave={e => { (e.currentTarget as HTMLAnchorElement).style.background = '#1E1E1E' }}
    >
      <svg
        width="14"
        height="14"
        viewBox="0 0 14 14"
        fill="none"
        aria-hidden="true"
      >
        <path
          d="M7 1v8M4 6l3 3 3-3M2 11h10"
          stroke="#E8E8E8"
          strokeWidth="1.5"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
      Download 4K
    </a>
  )
}
