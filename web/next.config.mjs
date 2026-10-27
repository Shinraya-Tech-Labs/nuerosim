/** @type {import('next').NextConfig} */
const config = {
  distDir: process.env.NEXT_DIST_DIR || ".next",
  async rewrites() {
    return [{source:'/api/:path*',destination:`${process.env.NEUROSIM_API_URL || 'http://127.0.0.1:8000'}/:path*`}];
  },
};
export default config;
