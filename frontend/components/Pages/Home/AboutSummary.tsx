import WallpaperService from '@/services/api/WallpaperService';

import classes from './Home.module.scss'

async function AboutSummary() {
  const wallpapers = await WallpaperService.getMostDownloaded();

  return <section className={classes.aboutSection}>
	
  </section>;
}

export default AboutSummary;
