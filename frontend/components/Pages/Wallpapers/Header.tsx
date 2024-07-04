import { secondaryFont } from '@/app/layout';
import classes from './Wallpapers.module.scss';

function Header() {
  return (
    <header className={classes.header}>
      <h1 className={`heading-secondary ${secondaryFont}`}>Wallpapers</h1>
    </header>
  );
}

export default Header;
