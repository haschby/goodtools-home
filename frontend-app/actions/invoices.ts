"use server";

import { gatewayService } from "@/lib/services/gateway";
import { BaseResponse } from "@/lib/types/base";
import { Invoice, StatusInput } from "@/lib/types/invoice";

interface GetInvoicesProps extends StatusInput {
    options?: {
        cursor?: string | null;
        limit?: number;
        id?: string | null;
    };
}

export async function getInvoices({ label, options }: GetInvoicesProps): Promise<BaseResponse<Invoice[]>> {

    const params = new URLSearchParams({
        status: label!, 
        cursor: options?.cursor ?? '', 
        id: options?.id ?? ''
    });

    const api_url = `/client/invoice/all?${params.toString()}`;
    const response: BaseResponse<Invoice[]> = await gatewayService(
        api_url,
        { 
            cache: 'no-store',
            method: "GET",
            headers: { 'Content-Type': 'application/json' }
        }
    );
    return response;
}