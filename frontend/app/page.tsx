import { Fragment } from 'react';
import Header from '@/components/Layouts/Header';
import WallpaperListPreview from '@/components/Wallpapers/WallpaperListPreview';

async function Home() {


  return (
    <Fragment>
      <Header />
      <WallpaperListPreview  />
    </Fragment>
  );
}

export default Home;
