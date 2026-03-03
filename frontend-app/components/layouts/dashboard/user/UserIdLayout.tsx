import { ReactNode } from "react";

interface UsersPageIdLayoutProps {
    children: ReactNode;
}

export default function UsersPageIdLayout(
    { children }: UsersPageIdLayoutProps
) {
    return (
        <section className="flex flex-col items-start w-full text-slate-800 h-screen">
            {children}
        </section>
    )
}