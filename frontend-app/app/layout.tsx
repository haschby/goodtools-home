import type { Metadata } from "next";
import "./globals.css";
import MainSideBar from "@/components/atoms/sidebar/MainSideBar";

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
        <section className="flex flex-row h-screen">
          <MainSideBar />
          <div className="w-full min-w-0 bg-gray-50">
              {children}
          </div>
        </section>
      </body>
    </html>
  );
}