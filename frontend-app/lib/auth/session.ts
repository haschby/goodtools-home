import "server-only";

import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { AUTH_COOKIE_NAME, AUTH_SESSION_DURATION, SIGNIN_PATH } from "./config";
import { signSessionToken, verifySessionToken, type SessionPayload } from "./jwt";

export async function createSession(username: string): Promise<void> {
    const token = await signSessionToken(username);
    const cookieStore = await cookies();

    cookieStore.set(AUTH_COOKIE_NAME, token, {
        httpOnly: true,                                  // inaccessible au JS client (XSS)
        secure: process.env.NODE_ENV === "production",   // HTTPS uniquement en prod
        sameSite: "lax",                                 // protection CSRF
        path: "/",
        maxAge: AUTH_SESSION_DURATION,
    });
}

export async function deleteSession(): Promise<void> {
    const cookieStore = await cookies();
    cookieStore.delete(AUTH_COOKIE_NAME);
}

export async function getSessionToken(): Promise<string | null> {
    const cookieStore = await cookies();
    const token = cookieStore.get(AUTH_COOKIE_NAME)?.value;
    const payload = await verifySessionToken(token);
    return payload ? token! : null;
}

export async function getSession(): Promise<SessionPayload | null> {
    const cookieStore = await cookies();
    return verifySessionToken(cookieStore.get(AUTH_COOKIE_NAME)?.value);
}

/**
 * À utiliser dans les server components / server actions sensibles
 * (défense en profondeur, en plus du proxy).
 */
export async function requireSession(): Promise<SessionPayload> {
    const session = await getSession();
    if (!session) redirect(SIGNIN_PATH);
    return session;
}
