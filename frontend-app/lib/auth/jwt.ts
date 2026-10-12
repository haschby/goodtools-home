import { SignJWT, jwtVerify, type JWTPayload } from "jose";
import { AUTH_SESSION_DURATION, JWT_AUDIENCE, JWT_ISSUER } from "./config";

export interface SessionPayload extends JWTPayload {
    sub: string;
}

function getSecretKey(): Uint8Array {
    const secret = process.env.AUTH_SECRET;
    if (!secret || secret.length < 32) {
        throw new Error("AUTH_SECRET manquant ou trop court (32 caractères minimum).");
    }
    return new TextEncoder().encode(secret);
}

export async function signSessionToken(username: string): Promise<string> {
    return new SignJWT({})
        .setProtectedHeader({ alg: "HS256", typ: "JWT" })
        .setSubject(username)
        .setIssuer(JWT_ISSUER)
        .setAudience(JWT_AUDIENCE)
        .setIssuedAt()
        .setExpirationTime(`${AUTH_SESSION_DURATION}s`)
        .sign(getSecretKey());
}

/** Retourne le payload si le token est valide, sinon `null`. */
export async function verifySessionToken(
    token: string | undefined | null
): Promise<SessionPayload | null> {
    if (!token) return null;
    try {
        const { payload } = await jwtVerify<SessionPayload>(token, getSecretKey(), {
            algorithms: ["HS256"],
            issuer: JWT_ISSUER,
            audience: JWT_AUDIENCE,
        });
        return payload.sub ? payload : null;
    } catch {
        return null;
    }
}
