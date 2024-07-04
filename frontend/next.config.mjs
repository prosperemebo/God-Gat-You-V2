/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    BACKEND_URL: process.env.BACKEND_URL,
    WEBSITE_URL: process.env.WEBSITE_URL,
    S3_BUCKET_URL_PREFIX: process.env.S3_BUCKET_URL_PREFIX,
  },
  images: {
    domains: [process.env.S3_BUCKET_URL_HOST],
  },
};

export default nextConfig;
