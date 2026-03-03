
export default function DashboardLayout({ children }: { children: React.ReactNode }) {
    return (

        <aside>
            <section className="text-slate-800 h-screen">
                {children}
            </section>
        </aside>
    )
}