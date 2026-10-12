"use server";

import { Suspense } from "react";
import { Workflow } from "@/lib/types/workflow";
import { DataListProvider } from "@/components/providers/DataListProvider";
import { QueryClientProvider } from "@/components/providers/QueryClientProvider";
import { getWorkflows, getWorkflowById } from "@/actions/workflow";
import WorkflowList from "@/components/views/dashboard/workflow/WorkflowList";

export default async function WorkflowPage() {
    return (
        <QueryClientProvider entity="workflow">
            <Suspense fallback={<div>Loading...</div>}>
                <DataListProvider<Workflow>
                    statuses={[]}
                    fetchFunction={getWorkflows}
                    getRecordById={getWorkflowById}
                    refreshRecord={getWorkflowById}
                >
                    <WorkflowList />
                </DataListProvider>
            </Suspense>
        </QueryClientProvider>
    )
}
