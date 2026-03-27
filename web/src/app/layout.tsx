import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Mathematica — Mathematical Art Gallery',
  description: 'Mathematical truth made visible through high-fidelity digital art.',
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap"
          rel="stylesheet"
        />
        <script
          dangerouslySetInnerHTML={{
            __html: \`
              window.MathJax = {
                tex: {
                  inlineMath: [['\\\\\\\\(', '\\\\\\\\)']],
                  displayMath: [['\\\\\\\\[', '\\\\\\\\\\]']]
                },
                options: {
                  skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre']
                }
              };
            \`,
          }}
        />
        <script
          defer
          src="https://cdn.jsdelivr.net/npm/mathjax@4/tex-chtml.js"
        />
      </head>
      <body className="antialiased">
        {children}
      </body>
    </html>
  )
}
