/**
 * Configuration partagée de l'authentification.
 * Ce fichier ne dépend d'aucune API Node : il est utilisable dans le proxy.
 */

export const AUTH_COOKIE_NAME = "gt_session";

/** Durée de vie du token (en secondes). Défaut : 8h. */
export const AUTH_SESSION_DURATION = Number(process.env.AUTH_SESSION_DURATION ?? 60 * 60 * 8);

export const SIGNIN_PATH = "/signin";
export const DEFAULT_AUTHENTICATED_PATH = "/invoices";

/** Routes accessibles sans être connecté. */
export const PUBLIC_PATHS = [SIGNIN_PATH];

export const JWT_ISSUER = "goodtools-frontend";
export const JWT_AUDIENCE = "goodtools-api";

export function isPublicPath(pathname: string): boolean {
    return PUBLIC_PATHS.some(
        (path) => pathname === path || pathname.startsWith(`${path}/`)
    );
}

/**
 * Protège contre les open-redirects : n'accepte que des chemins internes.
 */
export function sanitizeCallbackUrl(callbackUrl: string | null | undefined): string {
    if (
        !callbackUrl ||
        !callbackUrl.startsWith("/") ||
        callbackUrl.startsWith("//") ||
        callbackUrl.startsWith("/\\") ||
        isPublicPath(callbackUrl)
    ) {
        return DEFAULT_AUTHENTICATED_PATH;
    }
    return callbackUrl;
}
