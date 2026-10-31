/*
 * prime_kernel.c -- prime-by-prime kernel for Erdős #288, Cluster C0, Impl 2.
 *
 * Mathematical representation (per prime p, per interval [a,b]):
 *   Let V_p = max_{n in [a,b]} v_p(n)  (the largest p-adic valuation in the
 *   interval) and define S_p = (p^{V_p} * H(a,b)) mod p^{V_p+1}, taken in the
 *   ring of p-adic integers.  H(a,b) = p^{-V_p} * S_p in Z_(p), and the stored
 *   residue S_p (mod p^{V_p+1}) determines everything needed locally:
 *     - Write t = v_p(S_p) when S_p != 0 (then t <= V_p).
 *       If S_p == 0 or t >= V_p, the reduced denominator of H(a,b) is NOT
 *       divisible by p: e_p = 0.
 *       Otherwise e_p = V_p - t > 0 and the unit part
 *       u_p = (S_p / p^t) mod p^{e_p}  satisfies  p^{e_p} * H(a,b) = u_p
 *       in Z_(p) modulo p^{e_p}.
 *     - The global reduced denominator is B = prod_p p^{e_p}, and
 *       A mod p^{e_p} = u_p * (B / p^{e_p} mod p^{e_p}) mod p^{e_p},
 *       so the singleton condition A = -1 (mod B) is the conjunction over p
 *       of the prime-power conditions u_p * R_p = -1 (mod p^{e_p}), where
 *       R_p := (B / p^{e_p}) mod p^{e_p}.
 *
 * Incremental update when a term 1/n is appended (n = b, v = v_p(n),
 * w = (n / p^v)^{-1} mod p^{v+1}, precomputed):
 *   v <= V_p :  S_p += p^{V_p - v} * w          (mod p^{V_p+1})
 *   v >  V_p :  S_p  = p^{v - V_p} * S_p + w    (mod p^{v+1}),  V_p := v
 * In both cases each summand is < the modulus, so one conditional
 * subtraction implements the reduction, and the stored precision
 * p^{V_p+1} is exactly what the transition formulas consume.
 *
 * Sparsity facts used (proved in census2.py's documentation / RESULTS.md):
 *   (1) e_p and u_p can change only when p | n: if v_p(n) = 0 then the added
 *       term changes S_p only by a multiple of p^{V_p}, which leaves
 *       S_p mod p^{V_p} -- hence t, e_p and u_p -- unchanged; if
 *       0 < v_p(n) <= V_p etc., only primes dividing n are touched by the
 *       recomputation branch anyway.
 *   (2) Therefore B changes only at "delta events" (some e_p for p | n
 *       changes).  At a delta event, B_new = B_old * Fn / Fd with
 *       Fn = prod_{delta>0} p^{delta}, Fd = prod_{delta<0} p^{-delta}
 *       (64-bit integers).  Quantities that depend on B multiplicatively
 *       (R_f for a small filter set of primes f, and B modulo a set of
 *       auxiliary primes > 2000 used as a quadratic-residue prefilter for
 *       the pronic test B = c(c+1)) are updated at delta events only:
 *       multiplied by Fn and by the modular inverse of Fd (invertible:
 *       Fd's prime factors are <= 2000 and differ from the modulus prime).
 *       If a filter prime's own exponent changed, its R_f is recomputed
 *       from the full exponent vector.
 *
 * The sweep therefore maintains NO global fraction A/B and never uses
 * floating point.  Final exact decisions for candidate intervals are made
 * outside this kernel (Python big integers) from per-prime data that this
 * kernel recomputes from scratch per interval via pk_interval(), an
 * independent accumulation path (strata sum at fixed V_p, not the
 * incremental transition rules).
 */

#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#define MAXN 2000
#define MAXP 512
#define NFILTER 5          /* filter primes: 2,3,5,7,11 (first five primes) */
#define NQR 12             /* auxiliary QR moduli: first 12 primes > 2000    */

static int NP = 0;
static int primes_arr[MAXP];
static int p_pow_arr[MAXP][16];
static int p_maxexp[MAXP];
static uint8_t vp_table[MAXP][MAXN + 1];
static uint32_t w_table[MAXP][MAXN + 1];
static int initialized = 0;

static int qr_mod[NQR];
static uint8_t *qr_table[NQR];   /* qr_table[j][d] = 1 iff d is a square mod qr_mod[j] */

static uint32_t modinv_u32(uint32_t a, uint32_t mod) {
    /* inverse of a modulo mod, gcd(a,mod)=1, mod >= 2; a is reduced first */
    int64_t r0, r1, s0, s1;
    if (mod == 1) return 0;
    a %= mod;
    r0 = (int64_t)a; r1 = (int64_t)mod;
    s0 = 1; s1 = 0;
    while (r1 != 0) {
        int64_t q = r0 / r1;
        int64_t r2 = r0 - q * r1; r0 = r1; r1 = r2;
        int64_t s2 = s0 - q * s1; s0 = s1; s1 = s2;
    }
    /* r0 should be 1 */
    int64_t inv = s0 % (int64_t)mod;
    if (inv < 0) inv += mod;
    return (uint32_t)inv;
}

int pk_init(int nmax) {
    if (initialized) return NP;
    if (nmax > MAXN) return -1;
    /* sieve primes up to nmax */
    static uint8_t is_composite[MAXN + 1];
    memset(is_composite, 0, sizeof(is_composite));
    NP = 0;
    for (int i = 2; i <= nmax; i++) {
        if (!is_composite[i]) {
            primes_arr[NP++] = i;
            if ((int64_t)i * i <= nmax)
                for (int j = i * i; j <= nmax; j += i) is_composite[j] = 1;
        }
    }
    for (int pi = 0; pi < NP; pi++) {
        int p = primes_arr[pi];
        int64_t val = 1;
        int k = 0;
        while (k < 16) {
            p_pow_arr[pi][k] = (int)val;
            if (val > (int64_t)INT32_MAX / p) break;
            val *= p; k++;
        }
        /* max exponent of p in any n <= nmax */
        int me = 0; int64_t pw = p;
        while (pw <= nmax) { me++; if (pw > nmax / p) break; pw *= p; }
        p_maxexp[pi] = me;
        for (int n = 1; n <= nmax; n++) {
            int t = n, v = 0;
            while (t % p == 0) { t /= p; v++; }
            vp_table[pi][n] = (uint8_t)v;
            uint32_t mod = (uint32_t)p_pow_arr[pi][v + 1];
            w_table[pi][n] = (mod <= 1) ? 0 : modinv_u32((uint32_t)(t % (int)mod), mod);
        }
    }
    /* QR moduli: first NQR primes > 2000 (sieve up to 10000) */
    static uint8_t comp2[10001];
    memset(comp2, 0, sizeof(comp2));
    for (int i = 2; (int64_t)i * i <= 10000; i++)
        if (!comp2[i]) for (int j = i * i; j <= 10000; j += i) comp2[j] = 1;
    int cnt = 0;
    for (int i = 2001; i <= 10000 && cnt < NQR; i++) {
        if (!comp2[i]) {
            qr_mod[cnt] = i;
            qr_table[cnt] = (uint8_t *)calloc((size_t)i, 1);
            for (int x = 0; x < i; x++) qr_table[cnt][(x * x) % i] = 1;
            cnt++;
        }
    }
    initialized = 1;
    return NP;
}

int pk_num_primes(void) { return NP; }
int pk_prime_at(int idx) { return primes_arr[idx]; }
int pk_filter_count(void) { return NFILTER; }
int pk_qr_count(void) { return NQR; }
void pk_get_qr_mods(uint32_t *out) { for (int j = 0; j < NQR; j++) out[j] = (uint32_t)qr_mod[j]; }
void pk_get_filter_primes(uint32_t *out) { for (int f = 0; f < NFILTER; f++) out[f] = (uint32_t)primes_arr[f]; }

/* ---------------- interval prime data from scratch ---------------- */
/* For one interval [a,b]: for every prime p <= b compute V_p directly,
 * then S_p as the strata sum sum_n p^{V_p - v_p(n)} * w_p(n) mod p^{V_p+1},
 * then e_p, u_p.  Independent of the incremental sweep machinery. */
void pk_interval(int a, int b, uint8_t *e_out, uint32_t *u_out) {
    for (int pi = 0; pi < NP; pi++) {
        e_out[pi] = 0; u_out[pi] = 0;
        int p = primes_arr[pi];
        if (p > b) continue;
        int Vv = 0;
        for (int n = a; n <= b; n++) { int v = vp_table[pi][n]; if (v > Vv) Vv = v; }
        uint32_t mod = (uint32_t)p_pow_arr[pi][Vv + 1];
        uint32_t S = 0;
        for (int n = a; n <= b; n++) {
            int v = vp_table[pi][n];
            uint32_t term = (uint32_t)p_pow_arr[pi][Vv - v] * w_table[pi][n];
            S += term; if (S >= mod) S -= mod;
        }
        if (S != 0) {
            uint32_t tmp = S; int t = 0;
            while (tmp % (uint32_t)p == 0) { tmp /= (uint32_t)p; t++; }
            if (t < Vv) {
                e_out[pi] = (uint8_t)(Vv - t);
                u_out[pi] = tmp % (uint32_t)p_pow_arr[pi][Vv - t];
            }
        }
    }
}

/* ---------------- incremental state ---------------- */
typedef struct {
    uint8_t V[MAXP];
    uint32_t S[MAXP];
    uint8_t E[MAXP];
    uint32_t U[MAXP];
    uint32_t RF[NFILTER];
    uint32_t Bres[NQR];
    int changed_pi[16];
    int changed_delta[16];
    int changed_cnt;
} State;

static void state_reset(State *st) {
    memset(st->V, 0, sizeof(st->V));
    memset(st->S, 0, sizeof(st->S));
    memset(st->E, 0, sizeof(st->E));
    memset(st->U, 0, sizeof(st->U));
    memset(st->RF, 0, sizeof(st->RF));
    for (int j = 0; j < NQR; j++) st->Bres[j] = 1; /* B = 1 for the empty sum */
    st->changed_cnt = 0;
}

static void state_add(State *st, int n) {
    st->changed_cnt = 0;
    for (int pi = 0; pi < NP; pi++) {
        int p = primes_arr[pi];
        int v = vp_table[pi][n];
        if (v == 0) {
            int Vv = st->V[pi];
            uint32_t mod = (uint32_t)p_pow_arr[pi][Vv + 1];
            uint32_t term = (uint32_t)p_pow_arr[pi][Vv] * w_table[pi][n];
            uint32_t s = st->S[pi] + term;
            if (s >= mod) s -= mod;
            st->S[pi] = s;
            continue;
        }
        int Vv = st->V[pi];
        uint32_t w = w_table[pi][n];
        if (v <= Vv) {
            uint32_t mod = (uint32_t)p_pow_arr[pi][Vv + 1];
            uint32_t term = (uint32_t)p_pow_arr[pi][Vv - v] * w;
            uint32_t s = st->S[pi] + term;
            if (s >= mod) s -= mod;
            st->S[pi] = s;
        } else {
            uint32_t newmod = (uint32_t)p_pow_arr[pi][v + 1];
            uint32_t s = (uint32_t)p_pow_arr[pi][v - Vv] * st->S[pi] + w;
            if (s >= newmod) s -= newmod;
            st->S[pi] = s;
            st->V[pi] = (uint8_t)v;
            Vv = v;
        }
        /* recompute e_p, u_p for this prime (p | n) */
        uint8_t e_old = st->E[pi];
        uint8_t e_new = 0; uint32_t u_new = 0;
        uint32_t sval = st->S[pi];
        if (sval != 0) {
            uint32_t tmp = sval; int t = 0;
            while (tmp % (uint32_t)p == 0) { tmp /= (uint32_t)p; t++; }
            if (t < Vv) {
                e_new = (uint8_t)(Vv - t);
                u_new = tmp % (uint32_t)p_pow_arr[pi][Vv - t];
            }
        }
        st->E[pi] = e_new; st->U[pi] = u_new;
        if (e_new != e_old && st->changed_cnt < 16) {
            st->changed_pi[st->changed_cnt] = pi;
            st->changed_delta[st->changed_cnt] = (int)e_new - (int)e_old;
            st->changed_cnt++;
        }
    }
    if (st->changed_cnt == 0) return;
    uint64_t Fn = 1, Fd = 1;
    for (int i = 0; i < st->changed_cnt; i++) {
        int pi = st->changed_pi[i], d = st->changed_delta[i];
        if (d > 0) Fn *= (uint64_t)p_pow_arr[pi][d];
        else Fd *= (uint64_t)p_pow_arr[pi][-d];
    }
    /* B modulo the QR auxiliary primes */
    for (int j = 0; j < NQR; j++) {
        uint32_t mod = (uint32_t)qr_mod[j];
        uint32_t br = st->Bres[j];
        br = (uint32_t)((uint64_t)br * (Fn % mod) % mod);
        br = (uint32_t)((uint64_t)br * modinv_u32((uint32_t)(Fd % mod), mod) % mod);
        st->Bres[j] = br;
    }
    /* R_f for the filter primes */
    for (int f = 0; f < NFILTER; f++) {
        int pif = f; /* filter primes are primes_arr[0..NFILTER-1] */
        if (st->E[pif] == 0) { st->RF[f] = 0; continue; }
        uint32_t qf = (uint32_t)p_pow_arr[pif][st->E[pif]];
        int is_changed = 0;
        for (int i = 0; i < st->changed_cnt; i++) if (st->changed_pi[i] == pif) is_changed = 1;
        if (is_changed) {
            uint64_t prod = 1 % qf;
            for (int s = 0; s < NP; s++) {
                if (s == pif || st->E[s] == 0) continue;
                prod = prod * ((uint64_t)p_pow_arr[s][st->E[s]] % qf) % qf;
            }
            st->RF[f] = (uint32_t)prod;
        } else {
            uint32_t r = st->RF[f];
            r = (uint32_t)((uint64_t)r * (Fn % qf) % qf);
            r = (uint32_t)((uint64_t)r * modinv_u32((uint32_t)(Fd % qf), qf) % qf);
            st->RF[f] = r;
        }
    }
}

/* debug: run the incremental sweep for a single a up to b and dump state */
void pk_debug_state(int a, int b, uint8_t *e_out, uint32_t *u_out,
                    uint32_t *rf_out, uint32_t *bres_out) {
    State *st = (State *)malloc(sizeof(State));
    state_reset(st);
    for (int n = a; n <= b; n++) state_add(st, n);
    for (int pi = 0; pi < NP; pi++) { e_out[pi] = st->E[pi]; u_out[pi] = st->U[pi]; }
    for (int f = 0; f < NFILTER; f++) rf_out[f] = st->RF[f];
    for (int j = 0; j < NQR; j++) bres_out[j] = st->Bres[j];
    free(st);
}

/* ---------------- the sweep over a chunk of a-values ---------------- */
/* For every a in [a0,a1] and b in [a,N]: update the prime state, then test
 *   (S) singleton filter: for every filter prime f with e_f > 0,
 *       u_f * R_f = -1 (mod f^{e_f}) must hold;
 *   (L) pronic prefilter: for every QR modulus m_j, 4B+1 must be a square
 *       modulo m_j (necessary for B = c(c+1)).
 * Intervals passing (S) are written to out_single, those passing (L) to
 * out_l2, as (uint16 a, uint16 b) pairs.
 * stats: [0]=intervals, [1]=delta events, [2]=changed-prime records,
 *        [3]=single passes, [4]=l2 passes, [5]=overflow flag.            */
int pk_sweep_chunk(int a0, int a1, int N,
                   uint16_t *out_single, uint64_t cap_single,
                   uint16_t *out_l2, uint64_t cap_l2,
                   uint64_t *stats) {
    State *st = (State *)malloc(sizeof(State));
    uint64_t ns = 0, nl = 0;
    for (int i = 0; i < 6; i++) stats[i] = 0;
    for (int a = a0; a <= a1; a++) {
        state_reset(st);
        for (int b = a; b <= N; b++) {
            state_add(st, b);
            stats[0]++;
            if (st->changed_cnt > 0) { stats[1]++; stats[2] += (uint64_t)st->changed_cnt; }
            int spass = 1;
            for (int f = 0; f < NFILTER; f++) {
                if (st->E[f] == 0) continue;
                uint32_t qf = (uint32_t)p_pow_arr[f][st->E[f]];
                if ((uint64_t)st->U[f] * st->RF[f] % qf != qf - 1) { spass = 0; break; }
            }
            if (spass) {
                stats[3]++;
                if (ns < cap_single) { out_single[2 * ns] = (uint16_t)a; out_single[2 * ns + 1] = (uint16_t)b; ns++; }
                else stats[5] = 1;
            }
            int lpass = 1;
            for (int j = 0; j < NQR; j++) {
                uint32_t mod = (uint32_t)qr_mod[j];
                uint32_t d = (4 * st->Bres[j] + 1) % mod;
                if (!qr_table[j][d]) { lpass = 0; break; }
            }
            if (lpass) {
                stats[4]++;
                if (nl < cap_l2) { out_l2[2 * nl] = (uint16_t)a; out_l2[2 * nl + 1] = (uint16_t)b; nl++; }
                else stats[5] = 1;
            }
        }
    }
    free(st);
    return 0;
}
