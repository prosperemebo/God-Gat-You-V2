import type { Metadata } from 'next';
import { Inter } from 'next/font/google';

import '../sass/main.scss';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'God Gat You - Welcome to God God You',
  description:
    'We bring motivating and inspirating wallpapers every week to help, inspire and change people’s perspectives towards the world and life. And we do this in order of His coming.',
  icons: {
    icon: ['/favicon.png?v=4'],
    apple: ['/favicon.png?v=4'],
    shortcut: ['/favicon.png'],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang='en'>
      <body className={inter.className}>{children}</body>
    </html>
  );
}
