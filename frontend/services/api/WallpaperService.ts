class WallpaperService {
  static endpoints = {
    wallpapers: `${process.env.BACKEND_URL}/api/v1/wallpapers`,
    download: `${process.env.BACKEND_URL}/api/v1/wallpapers/:PAPERID/download`,
    wallpaperImagePrefix: `${process.env.S3_BUCKET_URL_PREFIX}/wallpaper/`,
  };

  static async getWallpapers(
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

    const url = `${this.endpoints.wallpapers}?page=${page}&page_size=${page_size}`;
    const response = await fetch(url, options);

    return response.json();
  }

  static async downloadWallpaper(
    id: string
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

    const url = this.endpoints.download.replace(':PAPERID', id);
    const response = await fetch(url, options);

    return response.json();
  }

  static async getMostDownloaded(
    page = 1,
    page_size = 5
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

    const url = `${this.endpoints.wallpapers}?page=${page}&page_size=${page_size}&sort=downloads`;
    const response = await fetch(url, options);

    return response.json();
  }
}

export default WallpaperService;
