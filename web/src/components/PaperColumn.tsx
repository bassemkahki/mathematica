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
          background: '#141414',
          color: '#888',
          fontSize: '16px',
          fontStyle: 'italic',
          padding: '16px',
          overflowY: 'auto',
          maxHeight: '90vh',
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
        background: '#141414',
        color: '#C8C8C8',
        fontSize: '16px',
        fontWeight: 400,
        lineHeight: 1.6,
        maxHeight: '90vh',
        padding: '24px',
      }}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  )
}
