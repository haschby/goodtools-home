"use server";

import { BaseResponse } from "@/lib/types/base";
import { gatewayService } from "@/lib/services/gateway";

interface WorkflowProps {
    provider?: string;
    id: string;
    workflowName?: string;
}

export async function startWorkflow({ provider, id, workflowName }: WorkflowProps): Promise<BaseResponse<unknown>> {
    const api_url = `/client/workflow/${provider}/${id}/start`;
    const response: BaseResponse<unknown> = await gatewayService(api_url, {
        method: "POST",
        cache: 'no-store',
        headers: { 'Content-Type': 'application/json', 'workflow-name': workflowName || 'syncPennyLaneWorkflow' }
    });
    return response;
}

export async function pollWorkflow({ id }: { id: string }): Promise<BaseResponse<unknown>> {
    const api_url = `/client/workflow/poll/${id}`;
    const response: BaseResponse<unknown> = await gatewayService(api_url, {
        method: "GET",
        cache: 'no-store',
        headers: { 'Content-Type': 'application/json' }
    });
    return response;
}

export async function getWorkflows(): Promise<BaseResponse<unknown>> {
    const api_url = `/client/workflow/`;
    const response: BaseResponse<unknown> = await gatewayService(api_url, {
        method: "GET",
        cache: 'no-store',
        headers: { 'Content-Type': 'application/json' }
    });
    return response;
}