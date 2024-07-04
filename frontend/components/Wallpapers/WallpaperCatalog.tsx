import Wallpaper from './Wallpaper';
import classes from './Wallpapers.module.scss';

interface IPropTypes {
	wallpapers: IWallpaper[];
}  

function WallpaperCatalog({wallpapers}: IPropTypes) {
  return (
    <ul className={classes.wallpaperCatalog}>
      {wallpapers?.map((wallpaper) => (
        <Wallpaper key={wallpaper.id} wallpaper={wallpaper} />
      ))}
    </ul>
  );
}

export default WallpaperCatalog;
