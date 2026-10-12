import MainSideBar from "@/components/atoms/sidebar/MainSideBar";
import { requireSession } from "@/lib/auth/session";

export default async function ProtectedLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  // Défense en profondeur : le proxy protège déjà les routes,
  // mais on revérifie la session côté serveur.
  await requireSession();

  return (
    <section className="flex flex-row h-screen">
      <MainSideBar />
      <div className="w-full min-w-0 bg-red-500">
        {children}
      </div>
    </section>
  );
}
