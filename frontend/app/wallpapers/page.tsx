import Header from '@/components/Pages/Wallpapers/Header';
import WallpaperListPagination from '@/components/Wallpapers/WallpaperListPagination';
import WallpaperService from '@/services/api/WallpaperService';
import { Fragment } from 'react';

async function WallpapersPage() {
  const wallpapers = await WallpaperService.getWallpapers();

  return (
    <Fragment>
      <Header />
      <WallpaperListPagination
        wallpapers={wallpapers.data}
        page={wallpapers.page}
        totalPages={wallpapers.total_pages}
      />
    </Fragment>
  );
}

export default WallpapersPage;
