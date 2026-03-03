import Link from "next/link"

const UserListLink = () => {
    return (
        <aside className="flex flex-col items-start w-full">
            <Link href="/users/12345" className="text-slate-800 hover:text-slate-600">12345</Link>
            <Link href="/users/12346" className="text-slate-800 hover:text-slate-600">12346</Link>
            <Link href="/users/12347" className="text-slate-800 hover:text-slate-600">12347</Link>
            <Link href="/users/12348" className="text-slate-800 hover:text-slate-600">12348</Link>
            <Link href="/users/12349" className="text-slate-800 hover:text-slate-600">12349</Link>
            <Link href="/users/12350" className="text-slate-800 hover:text-slate-600">12350</Link>
        </aside>
    )
}

export default function UserLayout({ children }: { children: React.ReactNode }) {
    return (
        <section className="flex items-start w-full text-slate-800 h-screen">
            <UserListLink />
            <section className="flex flex-col items-start w-full">
                {children}
            </section>
        </section>
    )
}