"use server";

import { gatewayService } from "@/lib/services/gateway";
import { Invoice } from "@/lib/types/invoice";
import { BaseResponse, GenericResponseAPI, GetSearchParams, PaginatedResponse } from "@/lib/types/base";

export async function getInvoices(
    { status, page, limit, query = null }: GetSearchParams
): Promise<GenericResponseAPI<PaginatedResponse<Invoice[]>>> {

    console.log('@getInvoices', status, page, limit);
    const params = new URLSearchParams({
        status: status,
        page: page?.toString(),
        limit: limit?.toString(),
        query: query ?? ''
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
    status?: string;
    gc_booking?: string;
}

export async function bulkUpdateInvoices(payload: InvoiceBulkUpdateSchema): Promise<GenericResponseAPI<Invoice[]>> {
    console.log('@payload : ', payload);

    const status = payload.status ?? 'none';
    const query = payload.gc_booking
        ? `?${new URLSearchParams({ gc_booking: payload.gc_booking }).toString()}`
        : '';

    const api_url = `/client/invoice/bulk/update/${status}${query}`;
    const response: GenericResponseAPI<Invoice[]> = await gatewayService(api_url, {
        method: "PATCH",
        cache: 'no-store',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload.ids)
    });
    return response;
}


export interface RentabilitiesResponse {
    bookingId?: string;
    isMonthly?: boolean;
    isExternal?: boolean;
    isManualInvoice?: boolean;
    items?: Rentability[];
    ca?: number;
    profit?: number;
    charges?: number;
    margin?: number;
}

export interface Rentability {
    id?: string;
    priceHT?: number;
    bookingId?: string;
    assetId?: string;
    type?: string;
    totalPriceHT?: number;
}

export async function getRentabilitiesByBookingId(bookingId: number): Promise<RentabilitiesResponse> {
    const api_url = `/client/gc/booking/${bookingId}/rentabilities`;
    const response: BaseResponse<RentabilitiesResponse> = await gatewayService<RentabilitiesResponse>(api_url, {
        method: "GET",
        cache: 'no-store',
        headers: { 'Content-Type': 'application/json' }
    });
    console.log('Response rentabilities : ', response);
    return { ...response.data } as RentabilitiesResponse;
}