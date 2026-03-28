import { readFile } from 'fs/promises'
import path from 'path'

interface PaperColumnProps {
  paperSlug: string
}

export async function PaperColumn({ paperSlug }: PaperColumnProps) {
  let html = ''
  let loadError = false

  try {
    const filePath = path.join(process.cwd(), 'public', 'papers', `${paperSlug}.html`)
    html = await readFile(filePath, 'utf-8')
  } catch {
    loadError = true
  }

  if (loadError || !html) {
    return (
      <div
        data-testid="paper-column"
        style={{
          color: '#555',
          fontSize: '14px',
          fontStyle: 'italic',
          fontFamily: 'Inter, sans-serif',
          padding: '24px',
        }}
      >
        <p>Paper unavailable.</p>
      </div>
    )
  }

  return (
    <div
      data-testid="paper-column"
      className="overflow-y-auto"
      style={{
        background: '#0E0E0E',
        border: '1px solid #1A1A1A',
        borderRadius: '3px',
        color: '#A0A0A0',
        fontSize: '15px',
        fontWeight: 400,
        lineHeight: 1.75,
        maxHeight: '85vh',
        padding: '28px 24px',
        fontFamily: 'Inter, sans-serif',
      }}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  )
}
