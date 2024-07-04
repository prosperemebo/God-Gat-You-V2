import { secondaryFont } from '@/app/layout';
import classes from './Layouts.module.scss';

function Header() {
  return (
    <header className={`${classes.header} `}>
      <h1 className={`heading-primary ${secondaryFont}`}>GOD GAT YOU</h1>
      <p className='paragraph'>
        We bring motivating and inspiring wallpapers every week to help, inspire
        and change people’s perspectives towards the world and life. And we do
        this in order of His coming.
      </p>
    </header>
  );
}

export default Header;
