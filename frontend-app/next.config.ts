import type { NextConfig } from "next";

const isDev = process.env.NODE_ENV !== "production";

// Origines autorisées en plus (ex: MinIO/stockage des PDF), séparées par des espaces.
const extraFileOrigins = process.env.CSP_FILE_ORIGINS ?? "";
const devOrigins = isDev ? "http://localhost:* ws://localhost:*" : "";

const contentSecurityPolicy = [
  "default-src 'self'",
  // 'unsafe-inline' requis par les scripts d'hydratation Next (sans nonce) ; 'unsafe-eval' en dev uniquement (HMR)
  `script-src 'self' 'unsafe-inline'${isDev ? " 'unsafe-eval'" : ""}`,
  "style-src 'self' 'unsafe-inline'",
  `img-src 'self' data: blob: ${extraFileOrigins} ${devOrigins}`,
  "font-src 'self' data:",
  `connect-src 'self' ${devOrigins}`,
  // Iframes des factures / buybacks (PDF)
  `frame-src 'self' blob: data: https: ${extraFileOrigins} ${devOrigins}`,
  "worker-src 'self' blob:",
  "object-src 'none'",
  "base-uri 'self'",
  "form-action 'self'",
  "frame-ancestors 'none'",
  ...(isDev ? [] : ["upgrade-insecure-requests"]),
].map((directive) => directive.replace(/\s+/g, " ").trim()).join("; ");

const securityHeaders = [
  { key: "Content-Security-Policy", value: contentSecurityPolicy },
  { key: "X-Frame-Options", value: "DENY" },
  { key: "X-Content-Type-Options", value: "nosniff" },
  { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
  { key: "Permissions-Policy", value: "camera=(), microphone=(), geolocation=(), payment=()" },
  { key: "Cross-Origin-Opener-Policy", value: "same-origin" },
  ...(isDev ? [] : [{ key: "Strict-Transport-Security", value: "max-age=63072000; includeSubDomains" }]),
];

const nextConfig: NextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,
  experimental: {
    serverActions: {
      bodySizeLimit: '100mb',
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
  async headers() {
    return [
      {
        source: "/:path*",
        headers: securityHeaders,
      },
    ];
  },
};

export default nextConfig;
