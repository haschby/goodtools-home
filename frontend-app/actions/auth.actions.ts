"use server";

import { headers } from "next/headers";
import { redirect } from "next/navigation";
import { SIGNIN_PATH, sanitizeCallbackUrl } from "@/lib/auth/config";
import {
    failureDelay,
    getClientIp,
    isRateLimited,
    registerFailedAttempt,
    resetAttempts,
    verifyCredentials,
} from "@/lib/auth/credentials";
import { createSession, deleteSession } from "@/lib/auth/session";

export interface SigninState {
    errors: string[];
}

export async function signin(
    _prevState: SigninState,
    formData: FormData
): Promise<SigninState> {
    const username = String(formData.get("username") ?? "");
    const password = String(formData.get("password") ?? "");
    const callbackUrl = sanitizeCallbackUrl(String(formData.get("callbackUrl") ?? ""));

    if (!username || !password || username.length > 256 || password.length > 256) {
        return { errors: ["Invalid username or password"] };
    }

    const clientIp = getClientIp(await headers());

    if (isRateLimited(clientIp)) {
        await failureDelay();
        return { errors: ["Too many attempts, please try again in a few minutes"] };
    }

    if (!(await verifyCredentials(username, password))) {
        registerFailedAttempt(clientIp);
        await failureDelay();
        return { errors: ["Invalid username or password"] };
    }

    resetAttempts(clientIp);
    await createSession(username);
    redirect(callbackUrl);
}

export async function signout(): Promise<void> {
    await deleteSession();
    redirect(SIGNIN_PATH);
}
