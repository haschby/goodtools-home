"use server";

// import { gatewayService } from "@/lib/services/gateway";
import { BaseResponse } from "@/lib/types/base";
import { User } from "@/lib/types/user";

export async function getUsers(): Promise<BaseResponse<User[]>> {
    return {
        message: 'Users fetched successfully',
        status_code: 200,
        data: []
    };
}