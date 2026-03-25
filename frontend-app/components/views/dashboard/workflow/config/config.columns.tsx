"use client";

import { Workflow, Workflow_Step } from "@/lib/types/workflow";
import Link from "next/link";
import { ColumnProps } from "@/lib/types/common";
import { StatusRow } from "@/components/atoms/listview/RowItems/StatusRow";

export const workflowsColumns: ColumnProps<Workflow>[] = [
    {
        keyfield: 'id',
        align: 'left',
        maxWidth: '150px',
        isFirst: true,
        renderItem: (item: Workflow) =>
            <Link href={`/workflows/${item.provider}/sync/${item.id}`}>
                <span className="underline bg-gray-100 font-semibold text-gray-800 p-1 rounded-md">
                    #{item.id.toUpperCase()}
                </span>
            </Link>
    },
    {
        keyfield: 'provider',
        align: 'left',
        maxWidth: '150px',
        isNumber: false,
        renderItem: (item: Workflow) =>
            <span className="text-sm font-normal text-gray-500">
                {item.provider}
            </span>
    },
    {
        keyfield: 'status',
        align: 'left',
        maxWidth: '150px',
        isNumber: false,
        renderItem: (item: Workflow) =>
            <StatusRow className="px-2 py-1 rounded-md" status={`${item.status}`} />
    },
    {
        keyfield: 'created_at',
        align: 'left',
        maxWidth: '150px',
        isNumber: false,
        renderItem: (item: Workflow) =>
            <span className="text-sm font-normal text-gray-500">
                {`
                    ${new Date(item.created_at).toLocaleDateString('fr-FR')} - 
                    ${new Date(item.created_at).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
                `}
            </span>
    },
    {
        keyfield: 'ended_at',
        align: 'left',
        maxWidth: '150px',
        isNumber: false,
        renderItem: (item: Workflow) =>
            <span className="text-sm font-normal text-gray-500">
                {`
                    ${new Date(item.ended_at).toLocaleDateString('fr-FR')} - 
                    ${new Date(item.ended_at).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
                `}
            </span>
    },
    {
        keyfield: 'duration',
        align: 'left',
        maxWidth: '150px',
        isNumber: false,
        renderItem: (item: Workflow) => {
            const duration: number = new Date(item.ended_at).getTime() - new Date(item.created_at).getTime();
            const hours: number = Math.floor(duration/3600000);
            const minutes: number = Math.floor((duration%3600000)/60000);
            const seconds: number = Math.floor((duration%60000)/1000);
            if (hours > 0) {
                return `${hours}h ${minutes}m ${seconds}s`;
            } else if (minutes > 0) {
                return `${minutes}m ${seconds}s`;
            } else {
                return `${seconds}s`;
            }
        }
    }
];