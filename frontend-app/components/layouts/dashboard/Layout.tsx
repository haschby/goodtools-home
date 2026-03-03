"use client";

import { DashBoardHeader } from "./Header";

interface DashBoardLayoutProps {
    title: string;
    children: React.ReactNode;
}

export const DashBoardPageLayout = (
    { title, children }: DashBoardLayoutProps
) => {
    return (
        <section className="flex flex-col">
            <DashBoardHeader title={title} />
            {children}
        </section>
    );
}