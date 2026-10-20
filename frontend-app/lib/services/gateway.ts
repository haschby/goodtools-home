import "server-only";

import { redirect } from "next/navigation";
import { BaseResponse } from "../types/base";
import { SIGNIN_PATH } from "../auth/config";
import { getSessionToken } from "../auth/session";

// Variables serveur uniquement (jamais exposées au navigateur).
const GATEWAY_URL =
    process.env.ENV === 'local' ?
    process.env.BACKEND_URL : 
    process.env.GATEWAY_API_URL;

class UnauthorizedError extends Error {
    constructor() {
        super("Unauthorized");
    }
}

/**
 * Appel au backend. Le JWT de session (cookie httpOnly) est automatiquement
 * ajouté dans le header `Authorization: Bearer <token>`.
 */
export async function gatewayService<T>(
    path: string, 
    options: RequestInit = { 
        method: "GET"
    }
): Promise<BaseResponse<T>> {

    // La session est toujours vérifiée, y compris en local.
    const sessionToken = await getSessionToken();
    if (!sessionToken) {
        redirect(SIGNIN_PATH);
    }

    // En local, le backend attend un token de test.
    const token = process.env.ENV === 'local' ? 'test-token' : sessionToken;

    const headers = new Headers(options.headers);
    headers.set("Authorization", `Bearer ${token}`);

    const controller = new AbortController();
    const { signal } = controller;

    try {  
        const response = await fetch(
            `${GATEWAY_URL}${path}`,
            { 
                ...options,
                headers,
                signal
            },
        );

        if (response.status === 401) {
            throw new UnauthorizedError();
        }

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status} ${response.statusText}`);
        }

        const data: BaseResponse<T> = await response.json();
        return data;
    } catch (error) {
        if (error instanceof UnauthorizedError) {
            redirect(SIGNIN_PATH);
        }
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