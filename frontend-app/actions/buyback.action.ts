"use server";

import { GetSearchParams } from "@/lib/types/base";
// import { searchQueryMockData } from "@/mockData/common";
import { Buyback } from "@/lib/types/buyback";
import { PaginatedResponse, GenericResponseAPI } from "@/lib/types/base";
import { gatewayService } from "@/lib/services/gateway";

export async function getBuybacks(
    { status, page, limit, query = null }: GetSearchParams
): Promise<GenericResponseAPI<PaginatedResponse<Buyback>>> {
    
    const params = new URLSearchParams({
        status: status,
        page: page?.toString(),
        limit: limit?.toString(),
        query: query ?? ''
    });
    
    const api_url = `/client/buyback/all?${params.toString()}`;
    const response: GenericResponseAPI<PaginatedResponse<Buyback>> =
        await gatewayService(api_url, {
            method: "GET",
            cache: "no-store",
            headers: { "Content-Type": "application/json" }
            
        }
    );
    return response;
}

export async function getBuybackById(id: string) {
    const api_url = `/client/buyback/${id}`;
    const response: GenericResponseAPI<Buyback> =
        await gatewayService(api_url, {
            method: "GET",
            cache: "no-store",
            headers: { "Content-Type": "application/json" }
        }
    );

    console.log("response", response);
    return response;
}

export async function patchBuyback(
    buyback: Buyback
): Promise<GenericResponseAPI<Buyback>> {
    const api_url = `/client/buyback/${buyback.id}`;
    const response: GenericResponseAPI<Buyback> =
        await gatewayService(api_url, {
            method: "PATCH",
            cache: "no-store",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(buyback)
        }
    );
    return response;
}

export async function createBuybacks(
    formDatas: FormData
): Promise<GenericResponseAPI<Buyback[]>> {
    const api_url = "/client/buyback/creates";
    const response: GenericResponseAPI<Buyback[]> =
        await gatewayService(api_url, {
            method: "POST",
            body: formDatas
        }
    );
    console.log("response", response);
    return response;
}