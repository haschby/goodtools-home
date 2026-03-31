"use client";

import Icon from "../Icon";
import { Spinner3Bulk } from "@lineiconshq/free-icons";

export default function SkeletonListViewItem({ nbColumns }: { nbColumns?: number }) {
    
    return (
        <>
            { 
            Array.from({ length: nbColumns ?? 12 }).map(
                (_, index: number) => (
                    <tr key={index} className="border-b border-slate-100 text-gray-800">
                        {Array.from({ length: nbColumns ?? 12 }).map(
                            (_, index: number) => {
                                if (index === 0) {
                                    return (
                                        <td key={index} className="min-w-fit w-fit py-3 px-6">
                                           <Icon
                                                Icon={Spinner3Bulk}
                                                size={20}
                                                strokeWidth={2}
                                                className="animate-spin text-blue-500" />
                                        </td>
                                    )
                                }
                                <td key={index} className="min-w-fit w-fit py-3 px-6">
                                    <span className="flex mb-1 bg-gray-200 w-full rounded-full h-2 animate-pulse"></span>
                                </td>
                            }
                        )}
                    </tr>
                    )
                )
            }
        </>
    );
}