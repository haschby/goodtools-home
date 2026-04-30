interface UsersPageIdMetricsProps {
    params: {
        id: string;
    };
}

export default async function UsersPageIdMetrics({ params }: UsersPageIdMetricsProps) {
    const { id } = await params;
    return (
        <section className="text-slate-800 h-screen">
            <h1>User Metrics ID: {id}</h1>
        </section>
    )
}