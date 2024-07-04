'use client';

import { secondaryFont } from '@/app/layout';
import { useMemo, useState } from 'react';
import { AiOutlineLoading3Quarters } from 'react-icons/ai';
import WallpaperCatalog from './WallpaperCatalog';
import WallpaperService from '@/services/api/WallpaperService';
import classes from './Wallpapers.module.scss';

interface IPropTypes {
  wallpapers: IWallpaper[];
  page: number;
  totalPages: number;
}

async function getWallpapers(
  page = 1,
  page_size = 100
): Promise<IPaginatedApiResponse<IWallpaper[]>> {
  const options: RequestInit = {
    method: 'GET',
    credentials: 'include',
    headers: {
      cache: 'no-store',
      'Access-Control-Allow-Credentials': 'true',
      'Content-Type': 'application/json',
      Accept: 'application/json',
    } as HeadersInit,
  };

  const uniqueParam = `&_=${new Date().getTime()}`;
  const url = `${process.env.BACKEND_URL_2}/api/v1/wallpapers?page=${page}&page_size=${page_size}${uniqueParam}`;
  const response = await fetch(url, options);

  return response.json();
}

function WallpaperListPagination({ wallpapers, page, totalPages }: IPropTypes) {
  const [loadedWallpapers, setLoadedWallpapers] = useState<IWallpaper[]>([]);
  const [nextPage, setNextPage] = useState(() => page + 1);
  const [isLoadinMore, setIsLoadinMore] = useState(false);

  const allWallpapers = useMemo(
    () => [...wallpapers, ...loadedWallpapers],
    [wallpapers, loadedWallpapers]
  );

  async function loadMore() {
    setIsLoadinMore(true);
    console.log(nextPage)

    try {
      const newWallpapers = await getWallpapers(nextPage, 12);

      setLoadedWallpapers(newWallpapers.data);

      setNextPage(nextPage + 1);
    } catch (err) {
      console.log(err);
    } finally {
      setIsLoadinMore(false);
    }
  }

  return (
    <section className={`${classes.wallpapers} center-content`}>
      <WallpaperCatalog wallpapers={allWallpapers} />
      {/* <div className={classes.foot}>
        {page < totalPages && isLoadinMore ? (
          <span className='loading'>
            <AiOutlineLoading3Quarters />
          </span>
        ) : (
          <button className={secondaryFont + ' text-link'} onClick={loadMore}>
            Load More
          </button>
        )}
      </div> */}
    </section>
  );
}

export default WallpaperListPagination;
