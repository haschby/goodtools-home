import { BaseResponse } from "../types/base";

const GATEWAY_URL = process.env.ENV === 'local' ? process.env.BACKEND_URL : process.env.NEXT_PUBLIC_GATEWAY_API_URL;

export async function gatewayService<T>(
    path: string, 
    options: RequestInit = { 
        method: "GET"
    }
): Promise<BaseResponse<T>> {

    const controller = new AbortController();
    const { signal } = controller;

    try {  
        const response = await fetch(
            `${GATEWAY_URL}${path}`,
            { 
                ...options,
                signal
            },
        );

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status} ${response.statusText}`);
        }

        const data: BaseResponse<T> = await response.json();
        return data;
    } catch (error) {
        throw new Error(`${String(error)}`);
        // return {
        //     message: 'Error fetching data',
        //     error: `${String(error)}`,
        //     status_code: 500,
        //     data: null
        // }
    } finally {
        controller.abort();
    }
}