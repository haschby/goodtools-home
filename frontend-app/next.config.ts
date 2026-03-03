import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  env: {
    NEXT_PUBLIC_GATEWAY_API_URL: process.env.NEXT_PUBLIC_GATEWAY_API_URL,
  },
  experimental: {
    serverActions: {
      bodySizeLimit: '10mb',
    }
  },
  images: {
    remotePatterns: [
      {
        protocol: "http",
        hostname: "localhost",
        port: "7770",
        pathname: "/**",
      },
    ],
  },
};

export default nextConfig;
