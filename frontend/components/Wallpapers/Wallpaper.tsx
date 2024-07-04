import Image from 'next/image';
import classes from './Wallpapers.module.scss';
import WallpaperService from '@/services/api/WallpaperService';

interface IPropTypes {
  wallpaper: IWallpaper;
}

function Wallpaper({ wallpaper }: IPropTypes) {
  const imageUrl =
    WallpaperService.endpoints.wallpaperImagePrefix + wallpaper.thumbnail;

  return (
    <figure className={classes.wallpaper}>
      <Image alt={wallpaper.name} src={imageUrl} width={400} height={450} />
    </figure>
  );
}

export default Wallpaper;
