export default function DashboardLayout({ children }: { children: React.ReactNode }) {
    return (
        <aside className="bg-gray-50">
            <section className="text-slate-700 h-screen">
                {children}
            </section>
        </aside>
    )
}