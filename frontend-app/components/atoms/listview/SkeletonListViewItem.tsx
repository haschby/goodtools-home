"use client";

export default function SkeletonListViewItem({ nbColumns }: { nbColumns?: number }) {
    
    return (
        <>
            { 
            Array.from({ length: nbColumns ?? 10 }).map(
                (_, index: number) => (
                    <tr key={index} className="border-b border-slate-100 text-gray-800">
                        {Array.from({ length: nbColumns ?? 10 }).map(
                            (_, index: number) => (
                                <td key={index} className="min-w-fit w-fit py-3 px-6">
                                    <span className="flex mb-1 bg-gray-200 w-full rounded-full h-2 animate-pulse"></span>
                                </td>
                            )
                        )}
                    </tr>
                    )
                )
            }
        </>
    );
}