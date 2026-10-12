import { NextRequest, NextResponse } from "next/server";
import {
    AUTH_COOKIE_NAME,
    DEFAULT_AUTHENTICATED_PATH,
    SIGNIN_PATH,
    isPublicPath,
} from "@/lib/auth/config";
import { verifySessionToken } from "@/lib/auth/jwt";

export default async function proxy(request: NextRequest) {
    const { pathname, search } = request.nextUrl;
    const token = request.cookies.get(AUTH_COOKIE_NAME)?.value;
    const session = await verifySessionToken(token);

    // Déjà connecté -> pas besoin de revoir la page de login
    if (isPublicPath(pathname)) {
        if (session) {
            return NextResponse.redirect(new URL(DEFAULT_AUTHENTICATED_PATH, request.url));
        }
        return NextResponse.next();
    }

    // Non connecté (ou token expiré / invalide) -> /signin
    if (!session) {
        const signinUrl = new URL(SIGNIN_PATH, request.url);
        if (pathname !== "/") {
            signinUrl.searchParams.set("callbackUrl", `${pathname}${search}`);
        }
        const response = NextResponse.redirect(signinUrl);
        if (token) response.cookies.delete(AUTH_COOKIE_NAME); // nettoie un token invalide
        return response;
    }

    return NextResponse.next();
}

export const config = {
    // Tout le site, sauf les assets statiques de Next et les fichiers publics
    matcher: [
        "/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp|ico|pdf)$).*)",
    ],
};
