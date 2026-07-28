interface AppLayoutProps {
    children: React.ReactNode;
}

export default function AppLayout({ children }: AppLayoutProps) {
    return (
        <section className="flex flex-col h-screen">
            {children}
        </section>
    )
}