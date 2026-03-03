"use server";

import { gatewayService } from "@/lib/services/gateway";
import { BaseResponse } from "@/lib/types/base";
import { searchQueryMockData } from "@/mockData/common";

interface GetTotalRecordsByEntityProps {
    entity: string;
}

export async function getTotalRecordsByEntity(
    { entity }:GetTotalRecordsByEntityProps
): Promise<BaseResponse<unknown>> {
    
    const apiPath = `/client/${entity}/count`;
    const response: BaseResponse<unknown> = await gatewayService(
        apiPath, {
        method: "GET",
        cache: 'no-store' });

    return { message: 'Total records found', status_code: 201, data: response ?? 0 };
} 

interface SearchQueryProps {
    entity: string;
    query: string;
}

export async function searchQuery<T>(
    { entity, query }: SearchQueryProps
): Promise<BaseResponse<T[]>> {
    // const apiPath = `/client/invoice/search?query=${query}`;
    // const response: BaseResponse<unknown> = await gatewayService(
    //     apiPath, {
    //     method: "POST",
    //     cache: 'no-store',
    //     body: JSON.stringify({ query })
    // });

    // console.log('@RESPONSE', response);

    return {
        message: 'Search query',
        status_code: 201,
        data: searchQueryMockData[entity as keyof typeof searchQueryMockData] as T[]
    };
}