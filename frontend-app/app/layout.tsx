import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Goodtools Flow Manager",
  description: "Goodtools Flow Manager",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`antialiased overflow-hidden h-screen`}>
        {children}
      </body>
    </html>
  );
}