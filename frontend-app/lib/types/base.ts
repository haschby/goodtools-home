export interface BaseResponse<T> {
    message: string;
    error?: string | null;
    status_code: number;
    data?: T | null;
}

export interface BaseEntity {
    id: string;
}