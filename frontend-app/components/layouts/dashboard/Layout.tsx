"use client";

interface DashBoardLayoutProps {
    title?: string | null;
    children: React.ReactNode;
}

export const DashBoardPageLayout = (
    { title = null, children }: DashBoardLayoutProps
) => {
    return (
        <section className="flex flex-col">
            {children}
        </section>
    );
}