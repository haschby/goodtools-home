import "server-only";

import { scrypt, timingSafeEqual, createHash, type ScryptOptions } from "node:crypto";

/* ------------------------------------------------------------------ */
/* Mot de passe : hash scrypt stocké dans AUTH_PASSWORD_HASH           */
/* Format : scrypt:<N>:<r>:<p>:<salt base64url>:<hash base64url>        */
/* Génération : `npm run auth:hash -- "<mot de passe>"`                 */
/* ------------------------------------------------------------------ */

function scryptAsync(password: string, salt: Buffer, keylen: number, options: ScryptOptions): Promise<Buffer> {
    return new Promise((resolve, reject) => {
        scrypt(password, salt, keylen, options, (err, derivedKey) => {
            if (err) reject(err);
            else resolve(derivedKey);
        });
    });
}

async function verifyPasswordHash(password: string, storedHash: string): Promise<boolean> {
    const parts = storedHash.split(":");
    if (parts.length !== 6 || parts[0] !== "scrypt") {
        throw new Error("AUTH_PASSWORD_HASH invalide (format attendu : scrypt:N:r:p:salt:hash).");
    }
    const [, n, r, p, saltB64, hashB64] = parts;
    const expected = Buffer.from(hashB64, "base64url");
    const N = Number(n);
    const derived = await scryptAsync(password, Buffer.from(saltB64, "base64url"), expected.length, {
        N,
        r: Number(r),
        p: Number(p),
        maxmem: 256 * N * Number(r),
    });
    return timingSafeEqual(derived, expected);
}

function sha256(value: string): Buffer {
    return createHash("sha256").update(value, "utf8").digest();
}

/**
 * Vérifie les identifiants contre AUTH_USERNAME / AUTH_PASSWORD_HASH (.env).
 */
export async function verifyCredentials(username: string, password: string): Promise<boolean> {
    const expectedUsername = process.env.AUTH_USERNAME;
    const passwordHash = process.env.AUTH_PASSWORD_HASH;

    if (!expectedUsername || !passwordHash) {
        throw new Error("AUTH_USERNAME / AUTH_PASSWORD_HASH non définis dans l'environnement.");
    }

    // Les deux vérifications sont toujours exécutées (temps constant, pas de court-circuit).
    const usernameOk = timingSafeEqual(
        sha256(username.trim().toLowerCase()),
        sha256(expectedUsername.trim().toLowerCase())
    );
    const passwordOk = await verifyPasswordHash(password, passwordHash);
    return usernameOk && passwordOk;
}

/* ------------------------------------------------------------------ */
/* Rate limiting en mémoire contre le brute force.                      */
/*  - par IP : uniquement si l'IP est fiable (AUTH_TRUST_PROXY=true)    */
/*  - global : plafond de tentatives toutes IP confondues, impossible   */
/*    à contourner en changeant de header / d'IP.                       */
/* Mémoire locale : à remplacer par Redis si plusieurs instances.       */
/* ------------------------------------------------------------------ */

const WINDOW_MS = 15 * 60 * 1000;
const MAX_ATTEMPTS_PER_IP = 5;
const MAX_ATTEMPTS_GLOBAL = 30;
const GLOBAL_KEY = "__global__";

const attempts = new Map<string, { count: number; firstAttempt: number }>();

function getCount(key: string): number {
    const entry = attempts.get(key);
    if (!entry) return 0;
    if (Date.now() - entry.firstAttempt > WINDOW_MS) {
        attempts.delete(key);
        return 0;
    }
    return entry.count;
}

function increment(key: string): void {
    const entry = attempts.get(key);
    if (!entry || Date.now() - entry.firstAttempt > WINDOW_MS) {
        attempts.set(key, { count: 1, firstAttempt: Date.now() });
        return;
    }
    entry.count += 1;
}

/**
 * IP du client. On ne fait confiance à `x-forwarded-for` que si l'app est
 * derrière un reverse proxy de confiance (AUTH_TRUST_PROXY=true). Dans ce
 * cas on prend la DERNIÈRE valeur : celle ajoutée par notre proxy, que le
 * client ne peut pas falsifier (les premières valeurs, elles, le peuvent).
 */
export function getClientIp(headerStore: Headers): string | null {
    if (process.env.AUTH_TRUST_PROXY !== "true") return null;
    const forwardedFor = headerStore.get("x-forwarded-for");
    if (forwardedFor) {
        const ips = forwardedFor.split(",").map((ip) => ip.trim()).filter(Boolean);
        return ips.at(-1) ?? null;
    }
    return headerStore.get("x-real-ip");
}

export function isRateLimited(ip: string | null): boolean {
    if (getCount(GLOBAL_KEY) >= MAX_ATTEMPTS_GLOBAL) return true;
    return ip !== null && getCount(`ip:${ip}`) >= MAX_ATTEMPTS_PER_IP;
}

export function registerFailedAttempt(ip: string | null): void {
    increment(GLOBAL_KEY);
    if (ip) increment(`ip:${ip}`);
}

export function resetAttempts(ip: string | null): void {
    if (ip) attempts.delete(`ip:${ip}`);
}

/** Ralentit les échecs (≈ 0.5–1s) pour freiner les scripts automatisés. */
export function failureDelay(): Promise<void> {
    const ms = 500 + Math.floor(Math.random() * 500);
    return new Promise((resolve) => setTimeout(resolve, ms));
}
