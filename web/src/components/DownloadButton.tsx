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
      className="flex items-center gap-2 text-xs"
      style={{
        fontFamily: 'Inter, sans-serif',
        fontWeight: 400,
        color: '#888',
        background: 'transparent',
        border: '1px solid #1A1A1A',
        borderRadius: '3px',
        padding: '6px 12px',
        textDecoration: 'none',
        transition: 'color 0.2s, border-color 0.2s',
      }}
      onMouseEnter={e => {
        (e.currentTarget as HTMLAnchorElement).style.color = '#C0C0C0';
        (e.currentTarget as HTMLAnchorElement).style.borderColor = '#333';
      }}
      onMouseLeave={e => {
        (e.currentTarget as HTMLAnchorElement).style.color = '#888';
        (e.currentTarget as HTMLAnchorElement).style.borderColor = '#1A1A1A';
      }}
    >
      <svg
        width="12"
        height="12"
        viewBox="0 0 12 12"
        fill="none"
        aria-hidden="true"
      >
        <path
          d="M6 1v7M3.5 5.5L6 8l2.5-2.5M2 10h8"
          stroke="currentColor"
          strokeWidth="1.2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
      Download
    </a>
  )
}
