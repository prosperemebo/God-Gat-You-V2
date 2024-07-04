import Link from 'next/link';
import Image from 'next/image';
import logo from '@/assets/logo/logo.png';

import classes from './Layouts.module.scss';

function MainNav() {
  return (
    <nav className={`${classes.navigation} center-content`}>
      <Link className={classes.logo} href='/'>
        <Image
          src={logo}
          alt='God Gat You'
          width={100}
          height={100}
          objectFit='contain'
        />
      </Link>
      <ul className={classes.navLinks}>
        <li>
          <Link href='/' className={classes.active}>
            Home
          </Link>
        </li>
        <li>
          <Link href='/wallpapers'>Wallpapers</Link>
        </li>
        <li>
          <Link href='/about'>About</Link>
        </li>
      </ul>
    </nav>
  );
}

export default MainNav;
