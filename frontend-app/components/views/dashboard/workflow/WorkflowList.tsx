"use client";
import { useEffect, useState } from "react";
import { getWorkflows } from "@/actions/workflow";
import { ListView } from "@/components/atoms/listview/ListView";
import WorkflowListRowItem from "@/components/views/dashboard/workflow/listview/WorkflowListRowItem";
import { Workflow } from "@/lib/types/workflow";
import TitleInfo from "@/components/atoms/view/TitleInfo";

export default function WorkflowList() {

    const [workflows, setWorkflows] = useState<Workflow[]>([]);

    useEffect(() => {
        const fetchWorkflows = async () => {
            const workflows = await getWorkflows();
            setWorkflows(workflows as unknown as Workflow[]);
        }
        fetchWorkflows();
    }, []);

    const cssHeader = "whitespace-nowrap text-sm font-bold bg-gray-100 text-gray-500";

    return (
        <div className="h-screen bg-white">
            <div className="px-6 flex flex-col h-full text-gray-700 gap-4 w-full">

                <TitleInfo
                    title="Workflows"
                    baseLineText="View detailed workflows by clicking on the row."
                    totalRows={workflows.length}
                />

                <ListView
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
                    paginationActions={undefined}
                    controlTableActions={undefined}
                />
            </div>
        </div>
    )
}
