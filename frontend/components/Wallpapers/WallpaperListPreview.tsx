import { cormorant, secondaryFont } from '@/app/layout';
import classes from './Wallpapers.module.scss';
import WallpaperService from '@/services/api/WallpaperService';
import WallpaperCatalog from './WallpaperCatalog';
import Link from 'next/link';

async function WallpaperListPreview() {
  const wallpapers = await WallpaperService.getWallpapers(1, 12);

  return (
    <section className={`${classes.wallpapers} center-content`}>
      <div className={classes.header}>
        <h2 className={secondaryFont + ' heading-tertiary'}>Wallpapers</h2>
      </div>
      <WallpaperCatalog wallpapers={wallpapers.data} />
      <div className={classes.foot}>
        <Link href='/wallpapers' className={secondaryFont + ' text-link'}>
          View All Wallpapers
        </Link>
      </div>
    </section>
  );
}

export default WallpaperListPreview;
