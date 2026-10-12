#!/usr/bin/env node
/**
 * Génère la valeur de AUTH_PASSWORD_HASH à partir d'un mot de passe.
 * Usage : npm run auth:hash -- "mon-mot-de-passe"
 */
import { randomBytes, scryptSync } from "node:crypto";

const password = process.argv[2];

if (!password) {
    console.error('Usage : npm run auth:hash -- "<mot de passe>"');
    process.exit(1);
}
if (password.length < 12) {
    console.error("Le mot de passe doit faire au moins 12 caractères.");
    process.exit(1);
}

const N = 16384, r = 8, p = 1, keylen = 64;
const salt = randomBytes(16);
const hash = scryptSync(password, salt, keylen, { N, r, p, maxmem: 256 * N * r });

console.log(`AUTH_PASSWORD_HASH=scrypt:${N}:${r}:${p}:${salt.toString("base64url")}:${hash.toString("base64url")}`);
