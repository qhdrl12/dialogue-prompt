import './globals.css'
import type { Metadata } from 'next'
import { Noto_Sans_KR, Merriweather } from 'next/font/google'

const notoSansKR = Noto_Sans_KR({ 
  subsets: ['latin'],
  weight: ['100', '200', '300', '400', '500', '600', '700', '800', '900'],
  variable: '--font-noto-sans-kr',
  display: 'swap',
})

const merriweather = Merriweather({ 
  subsets: ['latin'],
  weight: ['300', '400', '700', '900'],
  variable: '--font-merriweather',
  display: 'swap',
})

export const metadata: Metadata = {
  title: 'Dialogue Prompt',
  description: '사용자의 간단한 키워드 또는 설명을 바탕으로, 목표 달성에 최적화된 구체적인 프롬프트를 생성하는 AI 기반 프롬프트 생성기',
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="ko" className={`${notoSansKR.variable} ${merriweather.variable}`}>
      <body className="font-sans">
        <div className="min-h-screen">
          {children}
        </div>
      </body>
    </html>
  )
}
