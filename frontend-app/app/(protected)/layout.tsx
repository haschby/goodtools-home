import MainSideBar from "@/components/atoms/sidebar/MainSideBar";

export default function ProtectedLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <section className="flex flex-row h-screen">
      <MainSideBar />
      <div className="w-full min-w-0 bg-red-500">
        {children}
      </div>
    </section>
  );
}