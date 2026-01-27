"use client";

interface DashBoardHeaderProps {
    title: string;
    description?: string | null;
}

export const DashBoardHeader = (
    { title, description = null }
    : DashBoardHeaderProps
) => {
    return (
        <section className="flex flex-col">
            <h1 className="text-2xl font-bold text-slate-800 pt-6">
                {title}
            </h1>
            { 
                description && 
                <p className="text-sm text-slate-500">
                    {description}
                </p>
            }
        </section>
    );
}