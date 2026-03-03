import Link from "next/link";

interface UsersPageIdProps  {
    params: {
        id: string;
    };
}

export default async function UsersPageId({ params }: UsersPageIdProps) {
    const { id } = await params;
    return (
        <section className="text-slate-800 h-screen">
            <h1>User ID: {id}</h1>
            <Link href="/users" className="text-slate-800 hover:text-slate-600">Back</Link>
        </section>
    )
}