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
    console.log('@getInvoices', label, options);
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

export async function getInvoiceById(id: string): Promise<BaseResponse<Invoice>> {
    console.log('@getInvoiceById', id);
    const api_url = `/client/invoice/${id}`;
    const response: BaseResponse<Invoice> = await gatewayService(api_url, {
        method: "GET",
        cache: 'force-cache',
        headers: { 'Content-Type': 'application/json' }
    });
    return response;
}

export async function searchInvoices(q: string): Promise<BaseResponse<Invoice[]>> {
    const api_url = `/client/invoice/search?q=${q}`;
    const response: BaseResponse<Invoice[]> = await gatewayService(api_url, {
        method: "POST",
        cache: 'no-store',
        headers: { 'Content-Type': 'application/json' }
    });
    return response;
}

export async function patchInvoice(invoice: Invoice): Promise<BaseResponse<Invoice>> {
    const api_url = `/client/invoice/${invoice.id}`;
    const response: BaseResponse<Invoice> = await gatewayService(api_url, {
        method: "PATCH",
        cache: 'no-store',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(invoice)
    });
    return response;
}