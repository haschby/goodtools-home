"use server";

import { gatewayService } from "@/lib/services/gateway";
import { Invoice } from "@/lib/types/invoice";
import { GenericResponseAPI, GetSearchParams, PaginatedResponse } from "@/lib/types/base";

export async function getInvoices(
    { status, page, limit }: GetSearchParams
): Promise<GenericResponseAPI<PaginatedResponse<Invoice[]>>> {

    console.log('@getInvoices', status, page, limit);
    const params = new URLSearchParams({
        status: status,
        page: page?.toString(),
        limit: limit?.toString()
    });

    const api_url = `/client/invoice/all?${params.toString()}`;
    const response: GenericResponseAPI<PaginatedResponse<Invoice[]>> = await gatewayService(
        api_url,
        { 
            cache: 'no-store',
            method: "GET",
            headers: { 'Content-Type': 'application/json' }
        }
    );
    
    return response;
}

export async function getInvoiceById(id: string): Promise<GenericResponseAPI<Invoice>> {
    console.log('@getInvoiceById', id);
    const api_url = `/client/invoice/${id}`;
    const response: GenericResponseAPI<Invoice> = await gatewayService(api_url, {
        method: "GET",
        cache: 'force-cache',
        headers: { 'Content-Type': 'application/json' }
    });

    console.log('@getInvoiceById response : ', response);
    return response;
}

export async function searchInvoices(q: string): Promise<GenericResponseAPI<Invoice[]>> {
    const api_url = `/client/invoice/search?q=${q}`;
    const response: GenericResponseAPI<Invoice[]> = await gatewayService(api_url, {
        method: "POST",
        cache: 'no-store',
        headers: { 'Content-Type': 'application/json' }
    });
    return response;
}

export async function patchInvoice(invoice: Invoice): Promise<GenericResponseAPI<Invoice>> {
    const api_url = `/client/invoice/${invoice.id}`;
    const response: GenericResponseAPI<Invoice> = await gatewayService(api_url, {
        method: "PATCH",
        cache: 'no-store',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(invoice)
    });
    return response;
}

interface InvoiceBulkUpdateSchema {
    ids: string[];
    status: string;
}

export async function bulkUpdateInvoices(payload: InvoiceBulkUpdateSchema): Promise<GenericResponseAPI<Invoice[]>> {
    console.log('@payload : ', payload);
    const api_url = `/client/invoice/bulk/update/${payload.status}`;
    const response: GenericResponseAPI<Invoice[]> = await gatewayService(api_url, {
        method: "PATCH",
        cache: 'no-store',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload.ids)
    });
    return response;
}