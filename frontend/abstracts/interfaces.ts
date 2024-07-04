interface IWallpaper {
  created_at: string;
  description: string;
  desktop?: string;
  downloads: number;
  id: string;
  is_private: boolean;
  is_public: boolean;
  likes_count: number;
  mobile?: string;
  name: string;
  publish_date: string;
  slug: string;
  tablet?: string;
  thumbnail: string;
  updated_at: string;
}

interface IApiResponse<T> {
  message: string;
  status: ResponseStatus;
  data: T;
}

interface IPaginatedApiResponse<T> {
  message: string;
  page: number;
  page_size: number;
  status: ResponseStatus;
  total_count: number;
  total_pages: number;
  data: T;
}
