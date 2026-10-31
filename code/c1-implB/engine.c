/*
 * Erdős #288, Cycle 1, Cluster C1, Implementation B.
 * Independent multi-modular engine, written from scratch for this task.
 * (No code from c0-impl1, c0-impl2 or c1-implA is used or adapted.)
 *
 * Method
 * ------
 * For fixed b, sweep a = b, b-1, ..., 1 maintaining the reduced fraction
 * H(a,b) = A/B exactly as a custom bignum pair.  Only mul-by-small,
 * add, mod-by-small and div-by-small are needed in the sweep, by:
 *
 * Lemma L1 (step gcd is small and structured).  Stepping from [a+1,b]
 * to [a,b] with a' = a: N' = A*a' + B, M' = B*a', g' = gcd(N', M'),
 * A_new = N'/g', B_new = M'/g'.  Every prime dividing g' divides a':
 * if p | g' and p does not divide a', then p | M' forces p | B, and
 * N' = A*a' + B = A*a' (mod p) != 0 since gcd(A,B)=1 and p does not
 * divide a'.  Hence g' | D' := prod_{p|a'} p^{v_p(M')} and indeed
 * g' = gcd(N', D') because D' | M'.  Also D' = a' * prod p^{e_p}
 * <= 20000 * 20000^5 < 2^86 and each factor p^{v_p(M')} < 2^32.
 * So g' comes from mod-by-small passes (direct when D' < 2^32,
 * per-prime-power otherwise), and the divisions are div-by-small.
 *
 * Multi-modular filter (the decision gate for recording candidates).
 * For large primes P_0,P_1,P_2 (all > N, hence coprime to every A, B
 * and every g'), maintain transported residues
 *     At_j = A*Gamma (mod P_j), Bt_j = B*Gamma (mod P_j),
 *     Gamma = product of all step gcds in this b-sweep.
 * Since A_new = N'/g' and Gamma_new = Gamma*g', the division cancels:
 *     At' = At*a' + Bt,  Bt' = Bt*a',  Gamma' = Gamma*g'  (mod P_j),
 * so no modular inverse is ever needed.  A singleton solution obeys
 * A + 1 = t*B over the integers for a unique t in [1,11] (because
 * 0 < H(a,b) <= H(1,20000) < 10.49 and t = floor(H)+1), hence
 *     At_j + Gamma_j = t * Bt_j (mod P_j) for every j.
 * The filter tests t = 1..12 on P_0 (12 is harmless over-admission)
 * and confirms hits on P_1, P_2.  Soundness: a true solution always
 * passes, by induction on the sweep (integer equality implies the
 * congruences).  Every candidate is then decided by an independent
 * exact Python computation (see verify_candidates.py).
 *
 * L = 2 branch (forced denominator).  H(c,c+1) = (2c+1)/(c(c+1)) is
 * in lowest terms (gcd(2c+1, c) = gcd(2c+1, c+1) = 1), and integrality
 * of H(a,b) + H(c,c+1) forces den H(a,b) = c(c+1) (background fact,
 * CENSUS0.md).  So an L=2 solution needs B pronic with root c > b.
 * Prefilter: 4B+1 must be a perfect square, so its reduction must be
 * a square modulo m for m in {64} u {primes <= 47}: reject on any
 * non-residue.  B mod m is tracked exactly, not through Gamma (Gamma
 * accumulates small prime factors and would trivialise the test):
 * for each small prime p, B mod p is 0 when e_p >= 1, else it is the
 * unit part u_p = (B / p^{e_p}) mod p, maintained by the exact update
 * u_p <- u_p * w_a * w_g^{-1} (mod p), where w_a is a' with its
 * p-part removed, w_g is g' with its p-part removed (a p-unit, hence
 * invertible mod p), and similarly for the odd part of B modulo 64.
 * Survivors additionally need 4B+1 to be a quadratic residue modulo
 * each large prime P_j (Legendre symbol of the transported value,
 * which differs from 4B+1 by the square factor Gamma^2).  Final
 * exact pronic test: integer sqrt of 4B+1 by Newton iteration on a
 * Knuth-D bignum division, verified by exact multiplication
 * s*s == 4B+1 (the multiplication is the decision).  Near-misses
 * (B = c(c+1), c > b) are recorded and decided exactly in Python.
 *
 * No floating point is used anywhere.  All decisions are exact.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

typedef unsigned __int128 u128;
typedef int64_t i64;
typedef uint64_t u64;
typedef uint32_t u32;

/* ================= bignum (little-endian u64 limbs) ================= */
typedef struct { u64 *d; int n; int cap; } bn_t;

static void bn_init(bn_t *x, int cap) {
    x->d = (u64 *)calloc((size_t)cap, sizeof(u64));
    if (!x->d) { fprintf(stderr, "oom\n"); exit(3); }
    x->n = 0; x->cap = cap;
}
static void bn_free(bn_t *x) { free(x->d); x->d = NULL; x->n = x->cap = 0; }
static void bn_norm(bn_t *x) { while (x->n > 0 && x->d[x->n - 1] == 0) x->n--; }
static void bn_set_ui(bn_t *x, u64 v) { x->d[0] = v; x->n = (v != 0) ? 1 : 0; }
static void bn_copy(bn_t *dst, const bn_t *src) {
    memcpy(dst->d, src->d, sizeof(u64) * (size_t)src->n);
    dst->n = src->n;
}
static int bn_cmp(const bn_t *a, const bn_t *b) {
    if (a->n != b->n) return a->n < b->n ? -1 : 1;
    for (int i = a->n - 1; i >= 0; i--)
        if (a->d[i] != b->d[i]) return a->d[i] < b->d[i] ? -1 : 1;
    return 0;
}
static void bn_add_to(bn_t *dst, const bn_t *a, const bn_t *b) { /* dst != a,b */
    int n = a->n > b->n ? a->n : b->n;
    u128 carry = 0;
    for (int i = 0; i < n; i++) {
        u128 cur = carry + (i < a->n ? a->d[i] : 0) + (i < b->n ? b->d[i] : 0);
        dst->d[i] = (u64)cur; carry = cur >> 64;
    }
    int i = n;
    if (carry) { dst->d[i] = (u64)carry; i++; }
    dst->n = i; bn_norm(dst);
}
/* dst = src * m + add (add may be NULL); dst != src, dst != add */
static void bn_mul_ui_add(bn_t *dst, const bn_t *src, u64 m, const bn_t *add) {
    u128 carry = 0;
    int an = add ? add->n : 0, n = src->n;
    for (int i = 0; i < n; i++) {
        u128 cur = (u128)src->d[i] * m + carry + (i < an ? add->d[i] : 0);
        dst->d[i] = (u64)cur; carry = cur >> 64;
    }
    int i = n;
    while (carry || i < an) {
        u128 cur = carry + (i < an ? add->d[i] : 0);
        dst->d[i] = (u64)cur; carry = cur >> 64; i++;
    }
    dst->n = i; bn_norm(dst);
}
static void bn_mul_ui(bn_t *dst, const bn_t *src, u64 m) { bn_mul_ui_add(dst, src, m, NULL); }
/* x mod d, 0 < d < 2^32 */
static u64 bn_mod_u32d(const bn_t *x, u64 d) {
    u64 rem = 0;
    for (int i = x->n - 1; i >= 0; i--) {
        u64 limb = x->d[i];
        rem = ((rem << 32) | (limb >> 32)) % d;
        rem = ((rem << 32) | (limb & 0xffffffffULL)) % d;
    }
    return rem;
}
/* x /= d in place, 0 < d < 2^32; returns remainder */
static u64 bn_div_ui(bn_t *x, u64 d) {
    u64 rem = 0;
    for (int i = x->n - 1; i >= 0; i--) {
        u64 limb = x->d[i];
        u64 hi = (rem << 32) | (limb >> 32);
        u64 qhi = hi / d; rem = hi % d;
        u64 lo = (rem << 32) | (limb & 0xffffffffULL);
        u64 qlo = lo / d; rem = lo % d;
        x->d[i] = (qhi << 32) | qlo;
    }
    bn_norm(x);
    return rem;
}
/* x /= d in place, any u64 d > 0 (uses __int128); returns remainder */
static u64 bn_div_ui64(bn_t *x, u64 d) {
    u64 rem = 0;
    for (int i = x->n - 1; i >= 0; i--) {
        u128 cur = ((u128)rem << 64) | x->d[i];
        x->d[i] = (u64)(cur / d);
        rem = (u64)(cur % d);
    }
    bn_norm(x);
    return rem;
}
/* schoolbook mul; dst != a, dst != b */
static void bn_mul(bn_t *dst, const bn_t *a, const bn_t *b) {
    int n = a->n + b->n;
    for (int i = 0; i < n; i++) dst->d[i] = 0;
    dst->n = n;
    for (int i = 0; i < a->n; i++) {
        if (a->d[i] == 0) continue;
        u128 carry = 0;
        for (int j = 0; j < b->n; j++) {
            u128 cur = (u128)a->d[i] * b->d[j] + dst->d[i + j] + carry;
            dst->d[i + j] = (u64)cur; carry = cur >> 64;
        }
        int k = i + b->n;
        while (carry) { u128 cur = (u128)dst->d[k] + carry; dst->d[k] = (u64)cur; carry = cur >> 64; k++; }
    }
    bn_norm(dst);
}
static int bn_bitlen(const bn_t *x) {
    if (x->n == 0) return 0;
    u64 top = x->d[x->n - 1]; int b = 0;
    while (top) { b++; top >>= 1; }
    return (x->n - 1) * 64 + b;
}
static void bn_shl_bits(bn_t *dst, const bn_t *src, int shift) { /* dst != src */
    int limbs = shift / 64, bits = shift % 64;
    int n = src->n + limbs + (bits ? 1 : 0);
    for (int i = 0; i < n; i++) dst->d[i] = 0;
    for (int i = src->n - 1; i >= 0; i--) {
        dst->d[i + limbs] |= src->d[i] << bits;
        if (bits) dst->d[i + limbs + 1] |= src->d[i] >> (64 - bits);
    }
    dst->n = n; bn_norm(dst);
}
static void bn_shr_bits(bn_t *dst, const bn_t *src, int shift) { /* dst != src */
    int limbs = shift / 64, bits = shift % 64;
    if (limbs >= src->n) { dst->n = 0; return; }
    int n = src->n - limbs;
    for (int i = 0; i < n; i++) {
        u64 lo = src->d[i + limbs] >> bits;
        u64 hi = bits && (i + limbs + 1 < src->n) ? src->d[i + limbs + 1] << (64 - bits) : 0;
        dst->d[i] = lo | hi;
    }
    dst->n = n; bn_norm(dst);
}
/* general divmod (Knuth Algorithm D); q, r, a, b all distinct, b > 0 */
static void bn_divmod(bn_t *q, bn_t *r, const bn_t *a, const bn_t *b) {
    if (bn_cmp(a, b) < 0) { bn_set_ui(q, 0); bn_copy(r, a); return; }
    if (b->n == 1) {
        bn_copy(q, a);
        u64 rem = bn_div_ui64(q, b->d[0]);
        bn_set_ui(r, rem);
        return;
    }
    int n = b->n, m = a->n - n;
    int shift = __builtin_clzll(b->d[n - 1]);
    bn_t u, v;
    bn_init(&u, a->cap + 2); bn_init(&v, b->cap + 2);
    bn_shl_bits(&u, a, shift);
    bn_shl_bits(&v, b, shift);
    /* ensure u has m+n+1 limbs worth of storage/indexing (zeros above n) */
    if (u.n < a->n + 1) { for (int i = u.n; i <= a->n; i++) u.d[i] = 0; }
    q->n = m + 1;
    for (int j = m; j >= 0; j--) {
        u64 top2 = u.d[j + n]; /* may be 0 */
        u128 num = ((u128)top2 << 64) | u.d[j + n - 1];
        u64 qhat; u128 rhat;
        if (top2 >= v.d[n - 1]) {
            qhat = UINT64_MAX;
            rhat = num - (u128)qhat * v.d[n - 1];
        } else {
            qhat = (u64)(num / v.d[n - 1]);
            rhat = num % v.d[n - 1];
        }
        while (1) {
            u128 left = (u128)qhat * v.d[n - 2];
            u128 right = (rhat << 64) | u.d[j + n - 2];
            if (left <= right) break;
            qhat--; rhat += v.d[n - 1];
            if (rhat >= ((u128)1 << 64)) break;
        }
        /* multiply and subtract */
        u128 carry = 0; u64 borrow = 0;
        for (int i = 0; i < n; i++) {
            u128 p = (u128)qhat * v.d[i] + carry;
            carry = p >> 64;
            u64 plow = (u64)p;
            __int128 sub = (__int128)u.d[j + i] - (__int128)borrow - (__int128)plow;
            u.d[j + i] = (u64)sub;
            borrow = sub < 0 ? (u64)(((-sub - 1) >> 64) + 1) : 0;
        }
        __int128 sub = (__int128)u.d[j + n] - (__int128)borrow - (__int128)carry;
        u.d[j + n] = (u64)sub;
        if (sub < 0) { /* add back */
            qhat--;
            u128 c2 = 0;
            for (int i = 0; i < n; i++) {
                u128 s = (u128)u.d[j + i] + v.d[i] + c2;
                u.d[j + i] = (u64)s; c2 = s >> 64;
            }
            u.d[j + n] = u.d[j + n] + (u64)c2;
        }
        q->d[j] = qhat;
    }
    bn_norm(q);
    bn_shr_bits(r, &u, shift);
    bn_free(&u); bn_free(&v);
}
/* integer sqrt: out = floor(sqrt(T)); T, out distinct; scratch q, tmp */
static void bn_isqrt(bn_t *out, const bn_t *T, bn_t *qs, bn_t *rs, bn_t *tmp) {
    if (T->n == 0) { bn_set_ui(out, 0); return; }
    int bits = bn_bitlen(T);
    /* start x = 2^{floor(bits/2)+1} > sqrt(T) */
    memset(out->d, 0, sizeof(u64) * (size_t)out->cap);
    int e = bits / 2 + 1;
    out->d[e / 64] = 1ULL << (e % 64);
    out->n = e / 64 + 1;
    for (;;) {
        bn_divmod(qs, rs, T, out);
        bn_add_to(tmp, out, qs);
        /* tmp >>= 1 */
        {
            u64 carry = 0;
            for (int i = tmp->n - 1; i >= 0; i--) {
                u64 nc = tmp->d[i] & 1;
                tmp->d[i] = (tmp->d[i] >> 1) | (carry << 63);
                carry = nc;
            }
            bn_norm(tmp);
        }
        if (bn_cmp(tmp, out) >= 0) break;
        bn_copy(out, tmp);
    }
    /* exact adjustment (at most a couple of steps) */
    for (;;) {
        bn_mul(tmp, out, out);
        if (bn_cmp(tmp, T) <= 0) break;
        /* out -= 1 */
        int i = 0; u64 bor = 1;
        while (bor) { u64 v = out->d[i]; out->d[i] = v - bor; bor = (v == 0); i++; }
        bn_norm(out);
    }
    for (;;) {
        /* (out+1)^2 <= T ? */
        bn_copy(tmp, out);
        { u128 c = 1; int i = 0; while (c) { u128 cur = (u128)tmp->d[i] + c; tmp->d[i] = (u64)cur; c = cur >> 64; i++; if (i > tmp->n) tmp->n = i; } bn_norm(tmp); }
        bn_t sq; bn_init(&sq, tmp->cap + 2);
        bn_mul(&sq, tmp, tmp);
        int le = bn_cmp(&sq, T) <= 0;
        bn_free(&sq);
        if (!le) break;
        bn_copy(out, tmp);
    }
}
/* decimal string (malloc'd) */
static char *bn_to_dec(const bn_t *x) {
    bn_t tmp; bn_init(&tmp, x->cap + 2); bn_copy(&tmp, x);
    int maxgroups = x->n * 3 + 2;
    u32 *g = (u32 *)malloc(sizeof(u32) * (size_t)maxgroups);
    int ng = 0;
    if (tmp.n == 0) g[ng++] = 0;
    while (tmp.n > 0) g[ng++] = (u32)bn_div_ui(&tmp, 1000000000ULL);
    char *buf = (char *)malloc((size_t)ng * 9 + 2);
    int pos = sprintf(buf, "%u", g[ng - 1]);
    for (int i = ng - 2; i >= 0; i--) pos += sprintf(buf + pos, "%09u", g[i]);
    free(g); bn_free(&tmp);
    return buf;
}

static u64 ugcd(u64 a, u64 b) { while (b) { u64 t = a % b; a = b; b = t; } return a; }
static u64 modpow_u64(u64 a, u64 e, u64 mod) {
    u64 r = 1 % mod; a %= mod;
    while (e) {
        if (e & 1) r = (u64)((u128)r * a % mod);
        a = (u64)((u128)a * a % mod);
        e >>= 1;
    }
    return r;
}
static int is_prime_u32(u32 n) {
    if (n < 2) return 0;
    static const u32 small[] = {2,3,5,7,11,13,17,19,23,29,31,37};
    for (size_t i = 0; i < sizeof(small)/sizeof(small[0]); i++) {
        if (n == small[i]) return 1;
        if (n % small[i] == 0) return 0;
    }
    u32 d = n - 1; int r = 0; while ((d & 1) == 0) { d >>= 1; r++; }
    static const u32 bases[] = {2, 7, 61}; /* deterministic for n < 2^32 */
    for (size_t i = 0; i < 3; i++) {
        u32 a = bases[i] % n; if (a == 0) continue;
        u64 x = modpow_u64(a, d, n);
        if (x == 1 || x == n - 1) continue;
        int comp = 1;
        for (int j = 1; j < r; j++) { x = (x * x) % n; if (x == n - 1) { comp = 0; break; } }
        if (comp) return 0;
    }
    return 1;
}
/* Extra Legendre primes: PX[0..6] maintained in the sweep (transported),
 * PD[0..19] applied to survivors from the bignum directly.  All are
 * primes in (998244353, 10^9), distinct from LP0..LP2, generated and
 * Miller-Rabin verified at startup. */
static u32 PX[7], PD[20];
static void extra_primes_init(void) {
    int nx = 0, nd = 0;
    u32 cand = 999999999u;
    while (nx < 7 || nd < 20) {
        if (is_prime_u32(cand)) {
            if (nx < 7) PX[nx++] = cand; else PD[nd++] = cand;
        }
        cand -= 2;
    }
}
/* (u128 v) mod m for small m < 2^32, hardware divisions only */
static u64 mod_u128_small(u128 v, u64 m) {
    u64 hi = (u64)(v >> 64), lo = (u64)v;
    u64 r = (hi % m) * ((u64)(((u128)1 << 64) % m)) % m;
    r = (r + lo % m) % m;
    return r;
}

/* ================= sieve ================= */
#define NMAX 20000
static int spf[NMAX + 1];
static int primes_list[NMAX + 1];
static int nprimes = 0;
static void sieve(void) {
    for (int i = 2; i <= NMAX; i++) {
        if (!spf[i]) { spf[i] = i; primes_list[nprimes++] = i; }
        for (int j = 0; j < nprimes && primes_list[j] <= spf[i] && (long)i * primes_list[j] <= NMAX; j++)
            spf[i * primes_list[j]] = primes_list[j];
    }
    spf[1] = 1;
}
static int factor_distinct(int x, int *ps, int *es) {
    int c = 0;
    while (x > 1) { int p = spf[x], e = 0; while (x % p == 0) { x /= p; e++; } ps[c] = p; es[c] = e; c++; }
    return c;
}
static u64 ipow_limit(int p, int e) { u64 r = 1; while (e-- > 0) r *= (u64)p; return r; }

/* ================= QR prefilter tables ================= */
/* moduli, in check order (lowest pass density first) */
static const u32 QMS[15] = {64,47,43,41,37,31,29,23,19,17,13,11,7,5,3};
static unsigned char qr_ok[15][64];
/* small primes for unit-part tracking, index j = 0..13 */
static const int SP[14] = {3,5,7,11,13,17,19,23,29,31,37,41,43,47};
static int prime_idx[NMAX + 1];
static unsigned char POWT[2262][29][14]; /* POWT[qi][f][j] = primes_list[qi]^f mod SP[j] */
static unsigned char Wtab[NMAX + 1][14]; /* Wtab[x][j] = (x with SP[j]-part removed) mod SP[j] */
static unsigned char W64tab[NMAX + 1];   /* odd part of x mod 64 */
static unsigned char inv64tab[64];       /* inverse of odd residues mod 64 */
static unsigned char inv_3[3], inv_5[5], inv_7[7], inv_11[11], inv_13[13], inv_17[17], inv_19[19],
                     inv_23[23], inv_29[29], inv_31[31], inv_37[37], inv_41[41], inv_43[43], inv_47[47];
static void fill_inv(unsigned char *tab, int p) {
    tab[0] = 0;
    for (int x = 1; x < p; x++) for (int y = 1; y < p; y++) if (x * y % p == 1) { tab[x] = (unsigned char)y; break; }
}
static void qr_init(void) {
    for (int i = 0; i < 15; i++) {
        u32 m = QMS[i];
        for (u32 s = 0; s < m; s++) qr_ok[i][(s * s) % m] = 1;
    }
    for (int i = 0; i <= NMAX; i++) prime_idx[i] = -1;
    for (int i = 0; i < nprimes; i++) prime_idx[primes_list[i]] = i;
    for (int qi = 0; qi < nprimes; qi++) {
        int q = primes_list[qi];
        for (int j = 0; j < 14; j++) {
            u64 cur = 1 % (u64)SP[j];
            POWT[qi][0][j] = (unsigned char)cur;
            for (int f = 1; f <= 28; f++) { cur = cur * (u64)q % (u64)SP[j]; POWT[qi][f][j] = (unsigned char)cur; }
        }
    }
    for (int x = 1; x <= NMAX; x++) {
        for (int j = 0; j < 14; j++) {
            int t = x, p = SP[j];
            while (t % p == 0) t /= p;
            Wtab[x][j] = (unsigned char)(t % p);
        }
        int t = x; while ((t & 1) == 0) t >>= 1;
        W64tab[x] = (unsigned char)(t & 63);
    }
    for (int x = 1; x < 64; x += 2) for (int y = 1; y < 64; y += 2) if (x * y % 64 == 1) { inv64tab[x] = (unsigned char)y; break; }
    fill_inv(inv_3, 3); fill_inv(inv_5, 5); fill_inv(inv_7, 7); fill_inv(inv_11, 11);
    fill_inv(inv_13, 13); fill_inv(inv_17, 17); fill_inv(inv_19, 19); fill_inv(inv_23, 23);
    fill_inv(inv_29, 29); fill_inv(inv_31, 31); fill_inv(inv_37, 37); fill_inv(inv_41, 41);
    fill_inv(inv_43, 43); fill_inv(inv_47, 47);
}

/* ================= self tests ================= */
static u64 rng_state = 0x9E3779B97F4A7C15ULL;
static u64 rng(void) { u64 x = rng_state; x ^= x << 13; x ^= x >> 7; x ^= x << 17; rng_state = x; return x; }

static int selftest(void) {
    /* divmod fuzz: verify a == q*b + r and r < b using mul/add */
    for (int t = 0; t < 4000; t++) {
        int an = 1 + (int)(rng() % 24), bn_ = 1 + (int)(rng() % 12);
        bn_t A, B, Q, R, P, S;
        bn_init(&A, 64); bn_init(&B, 64); bn_init(&Q, 64); bn_init(&R, 64); bn_init(&P, 128); bn_init(&S, 128);
        for (int i = 0; i < an; i++) A.d[i] = rng();
        for (int i = 0; i < bn_; i++) B.d[i] = rng();
        A.n = an; B.n = bn_; bn_norm(&A); bn_norm(&B);
        if (B.n == 0) bn_set_ui(&B, 7);
        bn_divmod(&Q, &R, &A, &B);
        if (bn_cmp(&R, &B) >= 0) { printf("SELFTEST FAIL divmod r<b t=%d\n", t); return 0; }
        bn_mul(&P, &Q, &B);
        bn_add_to(&S, &P, &R);
        if (bn_cmp(&S, &A) != 0) { printf("SELFTEST FAIL divmod identity t=%d an=%d bn=%d\n", t, A.n, B.n); return 0; }
        bn_free(&A); bn_free(&B); bn_free(&Q); bn_free(&R); bn_free(&P); bn_free(&S);
    }
    /* isqrt fuzz */
    for (int t = 0; t < 300; t++) {
        int an = 1 + (int)(rng() % 30);
        bn_t T, S, P, Tp1, S1;
        bn_init(&T, 80); bn_init(&S, 80); bn_init(&P, 160); bn_init(&Tp1, 80); bn_init(&S1, 80);
        for (int i = 0; i < an; i++) T.d[i] = rng();
        T.n = an; bn_norm(&T);
        bn_t q, r, tmp; bn_init(&q, 160); bn_init(&r, 160); bn_init(&tmp, 160);
        bn_isqrt(&S, &T, &q, &r, &tmp);
        bn_mul(&P, &S, &S);
        if (bn_cmp(&P, &T) > 0) { printf("SELFTEST FAIL isqrt low t=%d\n", t); return 0; }
        bn_copy(&S1, &S);
        { u128 c = 1; int i = 0; while (c) { u128 cur = (u128)S1.d[i] + c; S1.d[i] = (u64)cur; c = cur >> 64; i++; if (i > S1.n) S1.n = i; } bn_norm(&S1); }
        bn_mul(&P, &S1, &S1);
        if (bn_cmp(&P, &T) <= 0) { printf("SELFTEST FAIL isqrt high t=%d\n", t); return 0; }
        bn_free(&T); bn_free(&S); bn_free(&P); bn_free(&Tp1); bn_free(&S1);
        bn_free(&q); bn_free(&r); bn_free(&tmp);
    }
    /* exact squares through isqrt */
    for (int t = 0; t < 100; t++) {
        int an = 1 + (int)(rng() % 15);
        bn_t C, T, S;
        bn_init(&C, 40); bn_init(&T, 80); bn_init(&S, 80);
        for (int i = 0; i < an; i++) C.d[i] = rng();
        C.n = an; bn_norm(&C);
        bn_mul(&T, &C, &C);
        bn_t q, r, tmp; bn_init(&q, 160); bn_init(&r, 160); bn_init(&tmp, 160);
        bn_isqrt(&S, &T, &q, &r, &tmp);
        if (bn_cmp(&S, &C) != 0) { printf("SELFTEST FAIL isqrt square t=%d\n", t); return 0; }
        bn_free(&C); bn_free(&T); bn_free(&S); bn_free(&q); bn_free(&r); bn_free(&tmp);
    }
    printf("SELFTEST OK\n");
    return 1;
}

/* ================= sweep ================= */
static double now_sec(void) {
    struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

#define LP0 1000000007ULL
#define LP1 1000000009ULL
#define LP2 998244353ULL

int main(int argc, char **argv) {
    if (argc >= 2 && strcmp(argv[1], "--selftest") == 0) {
        sieve(); qr_init(); extra_primes_init();
        return selftest() ? 0 : 1;
    }
    if (argc < 4) { fprintf(stderr, "usage: engine b_lo b_hi outfile.json\n"); return 2; }
    int b_lo = atoi(argv[1]), b_hi = atoi(argv[2]);
    const char *outpath = argv[3];
    sieve(); qr_init(); extra_primes_init();

    FILE *outf = fopen(outpath, "w");
    if (!outf) { perror("fopen"); return 2; }

    double t_start = now_sec();
    long long intervals = 0, p1_passes = 0, sing_cand = 0, l2_pre = 0, l2_leg = 0, l2_legx = 0, l2_legd = 0, l2_nm = 0, l2_pronic_le = 0;

    int fps[8], fes[8];
    static int ep[NMAX + 1];

    int cap = (int)(1.5 * b_hi / 64.0) + 64;
    bn_t A, B, Nn, Pp;
    bn_init(&A, cap); bn_init(&B, cap); bn_init(&Nn, cap); bn_init(&Pp, cap);
    /* pronic scratch */
    bn_t T, S, Qs, Rs, Tm, Prod;
    bn_init(&T, cap + 8); bn_init(&S, cap); bn_init(&Qs, cap); bn_init(&Rs, cap); bn_init(&Tm, cap + 8); bn_init(&Prod, cap + 8);

    fprintf(outf, "{\"b_lo\":%d,\"b_hi\":%d,\"moduli\":[1000000007,1000000009,998244353],\"singleton_candidates\":[", b_lo, b_hi);
    int first_rec = 1;

    typedef struct { int a, b; char *c; } nm_t;
    nm_t *nms = NULL; int nnm = 0, nmcap = 0;

    for (int b = b_lo; b <= b_hi; b++) {
        bn_set_ui(&A, 1);
        bn_set_ui(&B, (u64)b);
        memset(ep, 0, sizeof(int) * (size_t)(b + 1));
        {
            int c = factor_distinct(b, fps, fes);
            for (int i = 0; i < c; i++) ep[fps[i]] = fes[i];
        }
        u64 At0 = 1 % LP0, Bt0 = (u64)b % LP0, Gm0 = 1;
        u64 At1 = 1 % LP1, Bt1 = (u64)b % LP1, Gm1 = 1;
        u64 At2 = 1 % LP2, Bt2 = (u64)b % LP2, Gm2 = 1;
        u64 BtX[7], GmX[7];
        for (int k = 0; k < 7; k++) { BtX[k] = (u64)b % PX[k]; GmX[k] = 1; }
        /* unit parts of B modulo small primes / 64 (B itself is b) */
        u64 U_3, U_5, U_7, U_11, U_13, U_17, U_19, U_23, U_29, U_31, U_37, U_41, U_43, U_47, U_64;
        {
            int tb = b; while ((tb & 1) == 0) tb >>= 1; U_64 = (u64)(tb & 63);
#define UINIT(P, UV) { int t = b; while (t % P == 0) t /= P; UV = (u64)(t % P); }
            UINIT(3, U_3) UINIT(5, U_5) UINIT(7, U_7) UINIT(11, U_11) UINIT(13, U_13)
            UINIT(17, U_17) UINIT(19, U_19) UINIT(23, U_23) UINIT(29, U_29) UINIT(31, U_31)
            UINIT(37, U_37) UINIT(41, U_41) UINIT(43, U_43) UINIT(47, U_47)
#undef UINIT
        }

        for (int a = b; a >= 1; a--) {
            if (a < b) {
                u64 ap = (u64)a;
                bn_mul_ui(&Pp, &B, ap);
                bn_mul_ui_add(&Nn, &A, ap, &B);
                int nf = factor_distinct(a, fps, fes);
                u128 Dp = 1; int big = 0;
                u64 p_pow_vM[8]; int vM[8];
                for (int i = 0; i < nf; i++) {
                    int v = ep[fps[i]] + fes[i];
                    vM[i] = v;
                    p_pow_vM[i] = ipow_limit(fps[i], v);
                    Dp *= (u128)p_pow_vM[i];
                    if (Dp >= ((u128)1 << 32)) big = 1;
                }
                u128 gp = 1;
                int fv[8] = {0,0,0,0,0,0,0,0};
                if (nf > 0 && Dp > 1) {
                    if (!big) {
                        u64 D64 = (u64)Dp;
                        u64 r = bn_mod_u32d(&Nn, D64);
                        u64 g = ugcd(r, D64);
                        gp = g;
                        for (int i = 0; i < nf; i++) {
                            u64 gg = g; int f = 0;
                            while (gg % (u64)fps[i] == 0) { gg /= (u64)fps[i]; f++; }
                            fv[i] = f;
                        }
                    } else {
                        gp = 1;
                        for (int i = 0; i < nf; i++) {
                            u64 r = bn_mod_u32d(&Nn, p_pow_vM[i]);
                            int f;
                            if (r == 0) f = vM[i];
                            else { f = 0; u64 rr = r; while (rr % (u64)fps[i] == 0) { rr /= (u64)fps[i]; f++; } }
                            fv[i] = f;
                            gp *= (u128)ipow_limit(fps[i], f);
                        }
                    }
                }
                if (gp > 1) {
                    if (gp < ((u128)1 << 32)) {
                        bn_div_ui(&Nn, (u64)gp);
                        bn_div_ui(&Pp, (u64)gp);
                    } else {
                        for (int i = 0; i < nf; i++) if (fv[i] > 0) {
                            u64 d = ipow_limit(fps[i], fv[i]);
                            bn_div_ui(&Nn, d);
                            bn_div_ui(&Pp, d);
                        }
                    }
                }
                bn_copy(&A, &Nn);
                bn_copy(&B, &Pp);
                for (int i = 0; i < nf; i++) ep[fps[i]] += fes[i] - fv[i];
                /* ---- transported modular state ---- */
                int gp1 = (gp == 1);
                u64 gp64 = gp1 ? 1 : (gp < ((u128)1 << 64) ? (u64)gp : 0);
                if (gp1) {
                    At0 = (At0 * ap + Bt0) % LP0; Bt0 = Bt0 * ap % LP0;
                    At1 = (At1 * ap + Bt1) % LP1; Bt1 = Bt1 * ap % LP1;
                    At2 = (At2 * ap + Bt2) % LP2; Bt2 = Bt2 * ap % LP2;
                    for (int k = 0; k < 7; k++) BtX[k] = BtX[k] * ap % PX[k];
                } else if (gp64) {
                    At0 = (At0 * ap + Bt0) % LP0; Bt0 = Bt0 * ap % LP0; Gm0 = Gm0 * (gp64 % LP0) % LP0;
                    At1 = (At1 * ap + Bt1) % LP1; Bt1 = Bt1 * ap % LP1; Gm1 = Gm1 * (gp64 % LP1) % LP1;
                    At2 = (At2 * ap + Bt2) % LP2; Bt2 = Bt2 * ap % LP2; Gm2 = Gm2 * (gp64 % LP2) % LP2;
                    for (int k = 0; k < 7; k++) { BtX[k] = BtX[k] * ap % PX[k]; GmX[k] = GmX[k] * (gp64 % PX[k]) % PX[k]; }
                } else {
                    At0 = (At0 * ap + Bt0) % LP0; Bt0 = Bt0 * ap % LP0; Gm0 = Gm0 * mod_u128_small(gp, LP0) % LP0;
                    At1 = (At1 * ap + Bt1) % LP1; Bt1 = Bt1 * ap % LP1; Gm1 = Gm1 * mod_u128_small(gp, LP1) % LP1;
                    At2 = (At2 * ap + Bt2) % LP2; Bt2 = Bt2 * ap % LP2; Gm2 = Gm2 * mod_u128_small(gp, LP2) % LP2;
                    for (int k = 0; k < 7; k++) { BtX[k] = BtX[k] * ap % PX[k]; GmX[k] = GmX[k] * mod_u128_small(gp, PX[k]) % PX[k]; }
                }
                /* ---- unit parts of the new B modulo small primes / 64 ---- */
                {
                    U_64 = U_64 * W64tab[a] & 63;
                    if (!gp1) {
                        u64 h64 = 1;
                        for (int i = 0; i < nf; i++) if (fv[i] > 0 && (fps[i] & 1)) {
                            u64 pw = 1; for (int k = 0; k < fv[i]; k++) pw = pw * (u64)(fps[i] & 63) & 63;
                            h64 = h64 * pw & 63;
                        }
                        if (h64 != 1) U_64 = U_64 * inv64tab[h64] & 63;
                    }
#define UPDU(P, UV, J, INVTAB) \
                    { u64 h_ = 1; \
                      if (!gp1) { for (int i2 = 0; i2 < nf; i2++) if (fv[i2] > 0 && fps[i2] != P) h_ = h_ * POWT[prime_idx[fps[i2]]][fv[i2]][J] % P; } \
                      UV = UV * Wtab[a][J] % P; \
                      if (h_ != 1) UV = UV * INVTAB[h_] % P; }
                    UPDU(3, U_3, 0, inv_3)
                    UPDU(5, U_5, 1, inv_5)
                    UPDU(7, U_7, 2, inv_7)
                    UPDU(11, U_11, 3, inv_11)
                    UPDU(13, U_13, 4, inv_13)
                    UPDU(17, U_17, 5, inv_17)
                    UPDU(19, U_19, 6, inv_19)
                    UPDU(23, U_23, 7, inv_23)
                    UPDU(29, U_29, 8, inv_29)
                    UPDU(31, U_31, 9, inv_31)
                    UPDU(37, U_37, 10, inv_37)
                    UPDU(41, U_41, 11, inv_41)
                    UPDU(43, U_43, 12, inv_43)
                    UPDU(47, U_47, 13, inv_47)
#undef UPDU
                }
            }
            intervals++;
            /* ---- singleton filter ---- */
            {
                u64 lhs = At0 + Gm0; if (lhs >= LP0) lhs -= LP0;
                int tfound = 0;
                u64 rhs = 0;
                for (int t = 1; t <= 12; t++) {
                    rhs += Bt0; if (rhs >= LP0) rhs -= LP0;
                    if (lhs == rhs) { tfound = t; break; }
                }
                if (tfound) {
                    p1_passes++;
                    u64 l1 = At1 + Gm1; if (l1 >= LP1) l1 -= LP1;
                    u64 l2 = At2 + Gm2; if (l2 >= LP2) l2 -= LP2;
                    if (l1 == Bt1 * (u64)tfound % LP1 && l2 == Bt2 * (u64)tfound % LP2) {
                        sing_cand++;
                        fprintf(outf, "%s{\"a\":%d,\"b\":%d,\"t\":%d}", first_rec ? "" : ",", a, b, tfound);
                        first_rec = 0;
                    }
                }
            }
            /* ---- L2 pronic prefilter ---- */
            {
                int pass = 1;
                if (pass) { u64 bm = ep[2] >= 6 ? 0 : ((U_64 << ep[2]) & 63); u64 val = (4 * bm + 1) & 63; if (!qr_ok[0][val]) pass = 0; }
#define CHK(IDX, P, UV) \
                if (pass) { u64 bm = ep[P] ? 0 : UV; u64 val = (4 * bm + 1) % P; if (!qr_ok[IDX][val]) pass = 0; }
                CHK(1, 47, U_47)
                CHK(2, 43, U_43)
                CHK(3, 41, U_41)
                CHK(4, 37, U_37)
                CHK(5, 31, U_31)
                CHK(6, 29, U_29)
                CHK(7, 23, U_23)
                CHK(8, 19, U_19)
                CHK(9, 17, U_17)
                CHK(10, 13, U_13)
                CHK(11, 11, U_11)
                CHK(12, 7, U_7)
                CHK(13, 5, U_5)
                CHK(14, 3, U_3)
#undef CHK
                if (pass) {
                    l2_pre++;
                    /* Legendre stage on the large primes (transported value) */
                    int lok = 1;
                    {
                        u64 v0 = Gm0 * ((4 * Bt0 + Gm0) % LP0) % LP0;
                        if (v0 != 0 && modpow_u64(v0, (LP0 - 1) / 2, LP0) != 1) lok = 0;
                        if (lok) { u64 v1 = Gm1 * ((4 * Bt1 + Gm1) % LP1) % LP1;
                            if (v1 != 0 && modpow_u64(v1, (LP1 - 1) / 2, LP1) != 1) lok = 0; }
                        if (lok) { u64 v2 = Gm2 * ((4 * Bt2 + Gm2) % LP2) % LP2;
                            if (v2 != 0 && modpow_u64(v2, (LP2 - 1) / 2, LP2) != 1) lok = 0; }
                    }
                    if (lok) {
                        l2_leg++;
                        /* stage C: Legendre on the 7 extra transported primes */
                        for (int k = 0; k < 7 && lok; k++) {
                            u64 p = PX[k];
                            u64 v = GmX[k] * ((4 * BtX[k] + GmX[k]) % p) % p;
                            if (v != 0 && modpow_u64(v, (p - 1) / 2, p) != 1) lok = 0;
                        }
                        if (lok) {
                            l2_legx++;
                            /* stage D: Legendre on 20 primes, B read from the bignum */
                            for (int k = 0; k < 20 && lok; k++) {
                                u64 p = PD[k];
                                u64 bm = bn_mod_u32d(&B, p);
                                u64 v = (4 * bm + 1) % p;
                                if (v != 0 && modpow_u64(v, (p - 1) / 2, p) != 1) lok = 0;
                            }
                            if (lok) l2_legd++;
                        }
                    }
                    if (lok) {
                        /* exact pronic test: T = 4B+1, s = isqrt(T), s*s == T */
                        bn_mul_ui(&T, &B, 4);
                        { /* T += 1 */
                            u128 c = 1; int i = 0;
                            if (T.n == 0) { T.d[0] = 1; T.n = 1; }
                            else while (c && i < T.n) { u128 cur = (u128)T.d[i] + c; T.d[i] = (u64)cur; c = cur >> 64; i++; }
                            if (c) { T.d[T.n] = 1; T.n++; }
                        }
                        bn_isqrt(&S, &T, &Qs, &Rs, &Tm);
                        bn_mul(&Prod, &S, &S);
                        if (bn_cmp(&Prod, &T) == 0) {
                            /* c = (S-1)/2 */
                            bn_copy(&Tm, &S);
                            { int i = 0; u64 bor = 1; while (bor) { u64 v = Tm.d[i]; Tm.d[i] = v - bor; bor = (v == 0); i++; } bn_norm(&Tm); }
                            bn_div_ui(&Tm, 2);
                            bn_t bb; bn_init(&bb, 4); bn_set_ui(&bb, (u64)b);
                            int cmpb = bn_cmp(&Tm, &bb);
                            bn_free(&bb);
                            if (cmpb > 0) {
                                l2_nm++;
                                if (nnm == nmcap) { nmcap = nmcap ? nmcap * 2 : 64; nms = (nm_t *)realloc(nms, sizeof(nm_t) * (size_t)nmcap); }
                                nms[nnm].a = a; nms[nnm].b = b; nms[nnm].c = bn_to_dec(&Tm); nnm++;
                            } else {
                                l2_pronic_le++;
                            }
                        }
                    }
                }
            }
        }
    }

    double elapsed = now_sec() - t_start;
    fprintf(outf, "],\"l2_nearmisses\":[");
    for (int i = 0; i < nnm; i++) {
        fprintf(outf, "%s{\"a\":%d,\"b\":%d,\"c\":%s}", i ? "," : "", nms[i].a, nms[i].b, nms[i].c);
        free(nms[i].c);
    }
    free(nms);
    fprintf(outf, "],\"stats\":{\"intervals\":%lld,\"p1_passes\":%lld,\"singleton_candidates\":%lld,\"l2_prefilter_passes\":%lld,\"l2_legendre_passes\":%lld,\"l2_legendreX_passes\":%lld,\"l2_legendreD_passes\":%lld,\"l2_nearmisses\":%lld,\"l2_pronic_c_le_b\":%lld},\"seconds\":%.3f}\n",
            intervals, p1_passes, sing_cand, l2_pre, l2_leg, l2_legx, l2_legd, l2_nm, l2_pronic_le, elapsed);
    fclose(outf);
    bn_free(&A); bn_free(&B); bn_free(&Nn); bn_free(&Pp);
    bn_free(&T); bn_free(&S); bn_free(&Qs); bn_free(&Rs); bn_free(&Tm); bn_free(&Prod);
    return 0;
}
