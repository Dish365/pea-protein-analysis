import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'PEA Protein Analysis Platform | Advanced Process Optimization',
  description: 'Industry-leading platform for comprehensive technical, economic, and environmental analysis of pea protein extraction processes. Optimize your production with data-driven insights.',
  keywords: [
    'pea protein analysis',
    'process optimization',
    'economic analysis',
    'technical analysis',
    'environmental analysis',
    'sustainability metrics',
    'protein extraction',
    'process efficiency',
    'cost optimization',
    'environmental impact',
    'production analytics',
    'protein yield optimization'
  ],
  authors: [{ name: 'PEA Analysis Team' }],
  viewport: 'width=device-width, initial-scale=1',
  themeColor: '#0ea5e9',
  openGraph: {
    type: 'website',
    title: 'PEA Protein Analysis Platform',
    description: 'Advanced analytics and optimization for pea protein extraction processes',
    siteName: 'PEA Analysis',
    locale: 'en_US',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'PEA Protein Analysis Platform',
    description: 'Advanced analytics and optimization for pea protein extraction processes',
  },
  robots: {
    index: true,
    follow: true,
  },
  manifest: '/site.webmanifest',
  icons: {
    icon: '/favicon.ico',
    apple: '/apple-touch-icon.png',
  }
}; 