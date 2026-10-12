"use server";

import { BaseResponse, GenericResponseAPI, GetSearchParams, PaginatedResponse } from "@/lib/types/base";
import { Workflow } from "@/lib/types/workflow";
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

export async function getWorkflows(
    { status = 'All', page = 1, limit = 30, query = null }: GetSearchParams
): Promise<GenericResponseAPI<PaginatedResponse<Workflow[]>>> {
    const params = new URLSearchParams({
        status: status ?? 'All',
        page: `${page ?? 1}`,
        limit: `${limit ?? 30}`,
        query: query ?? ''
    });
    const api_url = `/client/workflow/?${params.toString()}`;
    const response: GenericResponseAPI<PaginatedResponse<Workflow[]>> = await gatewayService(api_url, {
        method: "GET",
        cache: 'no-store',
        headers: { 'Content-Type': 'application/json' }
    });
    return response;
}

export async function getWorkflowById(id: string): Promise<GenericResponseAPI<Workflow>> {
    const response: GenericResponseAPI<Workflow> = await gatewayService(`/client/workflow/poll/${id}`, {
        method: "GET",
        cache: 'no-store',
        headers: { 'Content-Type': 'application/json' }
    });
    return response;
}