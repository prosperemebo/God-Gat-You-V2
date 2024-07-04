import type { Metadata } from "next";

export const metadata: Metadata = {
  title: 'God Gat You - Wallpapers',
  description:
    'We bring motivating and inspirating wallpapers every week to help, inspire and change people’s perspectives towards the world and life. And we do this in order of His coming.',
  icons: {
    icon: ['/favicon.png?v=4'],
    apple: ['/favicon.png?v=4'],
    shortcut: ['/favicon.png'],
  },
};

function WallpaperPage() {
  return <div>WallpaperPage</div>;
}

export default WallpaperPage;
