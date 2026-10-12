"use client";
import { useMemo } from "react";
import { ListView } from "@/components/atoms/listview/ListView";
import WorkflowListRowItem from "@/components/views/dashboard/workflow/listview/WorkflowListRowItem";
import WorkflowListViewTableControl from "@/components/views/dashboard/workflow/listview/WorkflowListViewTableControl";
import { Workflow } from "@/lib/types/workflow";
import { useDataTable } from "@/lib/contexts/DataTableCustomContext";
import TitleInfo from "@/components/atoms/view/TitleInfo";

export default function WorkflowList() {

    const { pagination, error } = useDataTable<Workflow>();
    const workflows = useMemo(
        () => (pagination?.items ?? []) as Workflow[],
        [pagination?.items]
    );

    const TableControl = useMemo(() => <WorkflowListViewTableControl />, []);

    const cssHeader = "whitespace-nowrap text-sm font-bold bg-gray-100 text-gray-500";

    return (
        <div className="h-screen bg-white">
            <div className="flex flex-col h-full text-gray-700 gap-4 w-full">

                <TitleInfo
                    title="Workflows"
                    baseLineText="View detailed workflows by clicking on the row."
                    totalRows={pagination?.total ?? 0}
                />

                { error && (
                    <p className="text-sm text-red-700 bg-red-400/10 border border-red-200 rounded-md p-2">
                        {error}
                    </p>
                )}

                <ListView
                    filters={ <></> }
                    data={ <WorkflowListRowItem data={workflows} /> }
                    headers={
                        <>
                            <th key={0} style={{ width: '180px' }} className={cssHeader}>
                                <span className="px-6 border-r border-gray-50 pl-6 flex py-4 w-full h-full border-b border-gray-200">
                                    {'Workflow ID'} 
                                </span>
                            </th>
                            <th key={1} style={{ width: '180px' }} className={cssHeader}>
                                <span className="px-6 border-r border-gray-50 pl-6 flex py-4 justify-start w-full h-full border-b border-gray-200">
                                    {'Provider'} 
                                </span>
                            </th>
                            <th key={2} style={{ width: '150px' }} className={cssHeader}>
                                <span className="px-6 border-r border-gray-50 pl-6 flex py-4 justify-start w-full h-full border-b border-gray-200">
                                    {'Status'} 
                                </span>
                            </th>
                            <th key={3} style={{ width: '180px' }} className={cssHeader}>
                                <span className="px-6 border-r border-gray-50 pl-6 flex py-4 justify-start w-full h-full border-b border-gray-200">
                                    {'Started At'} 
                                </span>
                            </th>
                            <th key={4} style={{ width: '180px' }} className={cssHeader}>
                                <span className="px-6 border-r border-gray-50 pl-6 flex py-4 justify-start w-full h-full border-b border-gray-200">
                                    {'Ended At'} 
                                </span>
                            </th>
                            <th key={5} style={{ width: 'auto' }} className={cssHeader}>
                                <span className="px-6 border-r border-gray-50 pl-6 flex py-4 justify-start w-full h-full border-b border-gray-200">
                                    {'Time Consumed'} 
                                </span>
                            </th>
                        </>
                    }
                    paginationActions={ TableControl }
                    controlTableActions={undefined}
                />
            </div>
        </div>
    )
}
