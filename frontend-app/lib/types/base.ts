import { StatusInput } from "./invoice";

export interface BaseResponse<T> {
    message: string;
    error?: string | null;
    status_code: number;
    data?: T | null;
}

export interface BaseEntity {
    id: string;
}

export interface PaginatedResponse<T> {
    items: T[];
    limit: number;
    page: number;
    total_pages: number;
    total: number;
}

export interface GetSearchParams extends StatusInput {
    status: string;
    page: number;
    limit: number;
}

export type GenericResponseAPI<T> = BaseResponse<PaginatedResponse<T> | T> | BaseResponse<T>;