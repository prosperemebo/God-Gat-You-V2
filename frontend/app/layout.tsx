import type { Metadata } from 'next';
import { Poppins, Cormorant } from 'next/font/google';
import MainNav from '@/components/Layouts/MainNav';
import '../sass/main.scss';

const poppins = Poppins({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-poppins',
  weight: ['100', '200', '300', '400', '500', '600', '700', '800', '900'],
});

export const cormorant = Cormorant({
  subsets: ['latin'],
  display: 'swap',
  weight: ['300', '400', '500', '600', '700'],
});

export const primaryFont = poppins.className;
export const secondaryFont = cormorant.className;

const metadata: Metadata = {
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
      <body className={primaryFont}>
        <MainNav />
        {children}
      </body>
    </html>
  );
}
