/*
 * prime_kernel.c -- prime-by-prime kernel for Erdos #288, Cluster C1,
 * Implementation A.  Scaled adaptation of the C0 Implementation 2 kernel
 * (same prime-by-prime mathematics, same (V_p, S_p) representation, same
 * filter / QR-prefilter architecture), restructured so the sweep costs
 * O(#distinct prime divisors of b) per interval step instead of O(#primes):
 *
 * Sparsity lemma used (in addition to the C0 facts documented in
 * ../c0-impl2/prime_kernel.c): for an ODD prime p, terms 1/n with
 * v_p(n) = 0 contribute p^{V_p} * (n^{-1} mod p) to S_p.  Over any complete
 * block of p consecutive integers the residues n mod p run through
 * 1..p-1,0 and sum_r r^{-1} = sum_r r = p(p-1)/2 = 0 (mod p), so complete
 * blocks contribute 0 to S_p mod p^{V_p+1}.  Between two consecutive
 * multiples of p the non-multiples form exactly one complete block, hence
 * S_p (and so e_p, u_p) for odd p only needs updating when p | n -- with
 * one exception: the partial block from the interval start a to the first
 * multiple of p, whose contribution (mod p, the only precision the
 * V-increase formula consumes) is the precomputed prefix sum
 * sum_{r=a mod p}^{p-1} r^{-1} (mod p).  The prime 2 (where the block sum
 * is 1, not 0) is updated directly at every step; that is O(1).
 * Therefore the sweep maintains e_p, u_p exactly while touching, per step,
 * only the distinct prime divisors of the new index.
 *
 * R_f maintenance: R_f = (B / f^{e_f}) mod f^{e_f}.  We maintain
 * C_f = (B / f^{e_f}) mod f^{Vmax_f} directly: C_f is the product over
 * p != f of p^{e_p} modulo f^{Vmax_f}; it changes only when some OTHER
 * prime's exponent changes (multiplication by a unit power / its inverse,
 * both precomputed), and is invariant when f's own exponent changes.
 * R_f = C_f mod f^{e_f} is refreshed at each delta event.
 *
 * QR prefilter moduli are the first 24 primes > MAXN (the C0 kernel used
 * primes > 2000; at MAXN = 20000 the moduli must exceed 20000 so that
 * Fd, whose prime factors are <= MAXN, stays coprime to each modulus).
 * Filter primes are the first 12 primes (C0 used 5; the extra primes make
 * the singleton filter far more selective at this scale, at the cost of
 * 12 modular updates per delta event).
 *
 * pk_interval() is the independent scratch path (fixed-V strata sum, now
 * grouped by valuation strata with the same complete-block identity used
 * only to evaluate the v=0 stratum sum in O(1) per prime via the prefix
 * table: sum_{n<=X, p not | n} n^{-1} mod p = pref[X mod p]).
 */

#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#define MAXN 20000
#define MAXP 3000
#define NFILTER 12         /* filter primes: first 12 primes 2..37        */
#define NQR 24             /* auxiliary QR moduli: first 24 primes > MAXN */

static int NP = 0;
static int primes_arr[MAXP];
static uint32_t p_pow_arr[MAXP][16];
static int p_maxexp[MAXP];
static int spf_arr[MAXN + 1];
static int val_to_pi[MAXN + 1];
static uint16_t *pref_inv[MAXP];   /* pref_inv[pi][r] = sum_{s=1}^r s^{-1} mod p */
static int initialized = 0;

static int qr_mod[NQR];
static uint8_t *qr_table[NQR];
static uint32_t inv_p_qr[NQR][MAXP];
static uint32_t inv_p_modf[NFILTER][MAXP];
static uint32_t modf_arr[NFILTER];          /* f^{Vmax_f} */

static uint32_t modinv_u32(uint32_t a, uint32_t mod) {
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
    int64_t inv = s0 % (int64_t)mod;
    if (inv < 0) inv += mod;
    return (uint32_t)inv;
}

int pk_init(int nmax) {
    if (initialized) return NP;
    if (nmax > MAXN) return -1;
    /* spf sieve */
    for (int i = 0; i <= nmax; i++) { spf_arr[i] = i; val_to_pi[i] = -1; }
    NP = 0;
    for (int i = 2; i <= nmax; i++) {
        if (spf_arr[i] == i) {
            primes_arr[NP] = i;
            val_to_pi[i] = NP;
            NP++;
            if ((int64_t)i * i <= nmax)
                for (int j = i * i; j <= nmax; j += i)
                    if (spf_arr[j] == j) spf_arr[j] = i;
        }
    }
    for (int pi = 0; pi < NP; pi++) {
        int p = primes_arr[pi];
        uint64_t val = 1;
        for (int k = 0; k < 16; k++) {
            p_pow_arr[pi][k] = (val <= 0xFFFFFFFFull) ? (uint32_t)val : 0;
            val *= (uint64_t)p;
        }
        int me = 0; uint64_t pw = (uint64_t)p;
        while (pw <= (uint64_t)nmax) { me++; if (pw > (uint64_t)nmax / (uint64_t)p) break; pw *= (uint64_t)p; }
        p_maxexp[pi] = me;
        /* prefix sums of modular inverses of residues, odd primes only */
        if (p > 2) {
            uint16_t *pref = (uint16_t *)malloc(sizeof(uint16_t) * (size_t)p);
            uint32_t *inv = (uint32_t *)malloc(sizeof(uint32_t) * (size_t)p);
            pref[0] = 0;
            if (p > 1) inv[1] = 1;
            uint32_t acc = 0;
            for (int r = 1; r < p; r++) {
                if (r > 1) inv[r] = (uint32_t)((uint64_t)(p - p / r) * inv[p % r] % (uint32_t)p);
                acc += inv[r]; if (acc >= (uint32_t)p) acc -= (uint32_t)p;
                pref[r] = (uint16_t)acc;
            }
            free(inv);
            pref_inv[pi] = pref;
        } else {
            pref_inv[pi] = NULL;
        }
    }
    /* QR moduli: first NQR primes > MAXN */
    {
        static uint8_t comp2[200001];
        memset(comp2, 0, sizeof(comp2));
        for (int i = 2; (int64_t)i * i <= 200000; i++)
            if (!comp2[i]) for (int j = i * i; j <= 200000; j += i) comp2[j] = 1;
        int cnt = 0;
        for (int i = MAXN + 1; i <= 200000 && cnt < NQR; i++) {
            if (!comp2[i]) {
                qr_mod[cnt] = i;
                qr_table[cnt] = (uint8_t *)calloc((size_t)i, 1);
                for (int x = 0; x < i; x++) qr_table[cnt][(x * x) % i] = 1;
                cnt++;
            }
        }
    }
    for (int j = 0; j < NQR; j++)
        for (int pi = 0; pi < NP; pi++)
            inv_p_qr[j][pi] = modinv_u32((uint32_t)(primes_arr[pi] % qr_mod[j]),
                                         (uint32_t)qr_mod[j]);
    for (int f = 0; f < NFILTER; f++) {
        modf_arr[f] = p_pow_arr[f][p_maxexp[f]];
        for (int pi = 0; pi < NP; pi++) {
            if (pi == f) { inv_p_modf[f][pi] = 0; continue; }
            inv_p_modf[f][pi] = modinv_u32((uint32_t)(primes_arr[pi] % (int)modf_arr[f]),
                                           modf_arr[f]);
        }
    }
    initialized = 1;
    return NP;
}

int pk_num_primes(void) { return NP; }
int pk_filter_count(void) { return NFILTER; }
int pk_qr_count(void) { return NQR; }
void pk_get_qr_mods(uint32_t *out) { for (int j = 0; j < NQR; j++) out[j] = (uint32_t)qr_mod[j]; }
void pk_get_filter_primes(uint32_t *out) { for (int f = 0; f < NFILTER; f++) out[f] = (uint32_t)primes_arr[f]; }

/* ---------------- interval prime data from scratch ---------------- */
/* Strata sum at fixed V_p, independent of the incremental sweep. */
void pk_interval(int a, int b, uint8_t *e_out, uint32_t *u_out) {
    for (int pi = 0; pi < NP; pi++) {
        e_out[pi] = 0; u_out[pi] = 0;
        int p = primes_arr[pi];
        if (p > b) continue;
        /* V = max v_p(n) over [a,b]: largest k with a multiple of p^k inside */
        int Vv = 0;
        uint64_t pk = (uint64_t)p;
        for (int k = 1; k <= p_maxexp[pi]; k++) {
            if (b / (int64_t)pk - (a - 1) / (int64_t)pk > 0) Vv = k;
            else if (pk > (uint64_t)b) break;
            pk *= (uint64_t)p;
        }
        uint32_t mod = p_pow_arr[pi][Vv + 1];
        uint32_t S = 0;
        /* v >= 1 strata: multiples of p^v with exact valuation v */
        uint64_t pv = 1;
        for (int v = 1; v <= Vv; v++) {
            pv *= (uint64_t)p;                     /* p^v */
            uint32_t modw = p_pow_arr[pi][v + 1];  /* p^{v+1} */
            int64_t step = (int64_t)pv;
            int64_t m0 = ((int64_t)a + step - 1) / step * step;
            for (int64_t m = m0; m <= b; m += step) {
                int64_t mp = m / step;
                if (mp % p == 0) continue;
                uint32_t w = modinv_u32((uint32_t)(mp % modw), modw);
                uint32_t term = (uint32_t)((uint64_t)p_pow_arr[pi][Vv - v] * w % mod);
                S += term; if (S >= mod) S -= mod;
            }
        }
        /* v = 0 stratum */
        if (p == 2) {
            int cnt_odd = (b + 1) / 2 - a / 2;
            if (cnt_odd & 1) {
                S += p_pow_arr[pi][Vv]; if (S >= mod) S -= mod;
            }
        } else {
            /* F(X) = pref[X mod p] because complete blocks sum to 0 mod p */
            int fb = pref_inv[pi][b % p];
            int fa = pref_inv[pi][(a - 1) % p];
            int s0 = fb - fa; if (s0 < 0) s0 += p;
            if (s0) {
                S += (uint32_t)((uint64_t)p_pow_arr[pi][Vv] * (uint32_t)s0 % mod);
                if (S >= mod) S -= mod;
            }
        }
        if (S != 0) {
            uint32_t tmp = S; int t = 0;
            while (tmp % (uint32_t)p == 0) { tmp /= (uint32_t)p; t++; }
            if (t < Vv) {
                e_out[pi] = (uint8_t)(Vv - t);
                u_out[pi] = tmp % p_pow_arr[pi][Vv - t];
            }
        }
    }
}

/* ---------------- incremental state (sparse divisor updates) ---------------- */
typedef struct {
    uint8_t V[MAXP];
    uint32_t S[MAXP];
    uint8_t E[MAXP];
    uint32_t U[MAXP];
    uint8_t first_done[MAXP];
    uint32_t RF[NFILTER];
    uint32_t Cf[NFILTER];
    uint32_t Bres[NQR];
    int run_a;
    int changed_pi[16];
    int changed_delta[16];
    int changed_cnt;
} State;

static void state_reset(State *st, int a) {
    memset(st->V, 0, sizeof(st->V));
    memset(st->S, 0, sizeof(st->S));
    memset(st->E, 0, sizeof(st->E));
    memset(st->U, 0, sizeof(st->U));
    memset(st->first_done, 0, sizeof(st->first_done));
    memset(st->RF, 0, sizeof(st->RF));
    for (int f = 0; f < NFILTER; f++) st->Cf[f] = 1 % modf_arr[f];
    for (int j = 0; j < NQR; j++) st->Bres[j] = 1;
    st->run_a = a;
    st->changed_cnt = 0;
}

static void recompute_eu(State *st, int pi) {
    int p = primes_arr[pi];
    int Vv = st->V[pi];
    uint8_t e_old = st->E[pi];
    uint8_t e_new = 0; uint32_t u_new = 0;
    uint32_t sval = st->S[pi];
    if (sval != 0) {
        uint32_t tmp = sval; int t = 0;
        while (tmp % (uint32_t)p == 0) { tmp /= (uint32_t)p; t++; }
        if (t < Vv) {
            e_new = (uint8_t)(Vv - t);
            u_new = tmp % p_pow_arr[pi][Vv - t];
        }
    }
    st->E[pi] = e_new; st->U[pi] = u_new;
    if (e_new != e_old && st->changed_cnt < 16) {
        st->changed_pi[st->changed_cnt] = pi;
        st->changed_delta[st->changed_cnt] = (int)e_new - (int)e_old;
        st->changed_cnt++;
    }
}

static void state_add(State *st, int n) {
    st->changed_cnt = 0;
    if ((n & 1) == 1) {
        /* p = 2, v = 0 term: S_2 += 2^{V_2} * 1 (mod 2^{V_2+1}); e,u unchanged */
        int Vv = st->V[0];
        uint32_t mod = p_pow_arr[0][Vv + 1];
        uint32_t s = st->S[0] + p_pow_arr[0][Vv];
        if (s >= mod) s -= mod;
        st->S[0] = s;
    }
    /* distinct prime divisors of n */
    int m = n;
    while (m > 1) {
        int p = spf_arr[m];
        int pi = val_to_pi[p];
        int v = 0;
        while (m % p == 0) { m /= p; v++; }
        uint32_t modw = p_pow_arr[pi][v + 1];
        int nprime = n / (int)p_pow_arr[pi][v];
        uint32_t w = modinv_u32((uint32_t)(nprime % (int)modw), modw);
        int Vv = st->V[pi];
        if (pi == 0) {
            /* p = 2 divisor term, direct update (S_2 is exact) */
            if (v <= Vv) {
                uint32_t mod = p_pow_arr[0][Vv + 1];
                uint32_t s = st->S[0] + (uint32_t)((uint64_t)p_pow_arr[0][Vv - v] * w % mod);
                if (s >= mod) s -= mod;
                st->S[0] = s;
            } else {
                uint32_t newmod = p_pow_arr[0][v + 1];
                uint32_t s = (uint32_t)((uint64_t)p_pow_arr[0][v - Vv] * st->S[0] % newmod) + w;
                if (s >= newmod) s -= newmod;
                st->S[0] = s;
                st->V[0] = (uint8_t)v;
            }
            recompute_eu(st, 0);
        } else if (!st->first_done[pi]) {
            /* first multiple of p in this run: fold in the partial v=0 block
             * from run_a to n-1 (needed only mod p) */
            int r0 = st->run_a % p;
            int partial = 0;
            if (r0 != 0) {
                int hi = pref_inv[pi][p - 1];
                int lo = (r0 > 1) ? pref_inv[pi][r0 - 1] : 0;
                partial = hi - lo; if (partial < 0) partial += p;
            }
            uint32_t newmod = p_pow_arr[pi][v + 1];
            uint32_t s = (uint32_t)((uint64_t)p_pow_arr[pi][v] * (uint32_t)partial % newmod) + w;
            if (s >= newmod) s -= newmod;
            st->S[pi] = s;
            st->V[pi] = (uint8_t)v;
            st->first_done[pi] = 1;
            recompute_eu(st, pi);
        } else if (v <= Vv) {
            uint32_t mod = p_pow_arr[pi][Vv + 1];
            uint32_t s = st->S[pi] + (uint32_t)((uint64_t)p_pow_arr[pi][Vv - v] * w % mod);
            if (s >= mod) s -= mod;
            st->S[pi] = s;
            recompute_eu(st, pi);
        } else {
            uint32_t newmod = p_pow_arr[pi][v + 1];
            uint32_t s = (uint32_t)((uint64_t)p_pow_arr[pi][v - Vv] * st->S[pi] % newmod) + w;
            if (s >= newmod) s -= newmod;
            st->S[pi] = s;
            st->V[pi] = (uint8_t)v;
            recompute_eu(st, pi);
        }
    }
    if (st->changed_cnt == 0) return;
    /* delta event: update B mod QR primes and C_f, then refresh R_f */
    for (int i = 0; i < st->changed_cnt; i++) {
        int pi = st->changed_pi[i], d = st->changed_delta[i];
        int p = primes_arr[pi];
        int ad = d < 0 ? -d : d;
        for (int j = 0; j < NQR; j++) {
            uint32_t mod = (uint32_t)qr_mod[j];
            uint64_t br = st->Bres[j];
            if (d > 0) { for (int t = 0; t < ad; t++) br = br * (uint32_t)(p % (int)mod) % mod; }
            else { uint32_t iv = inv_p_qr[j][pi]; for (int t = 0; t < ad; t++) br = br * iv % mod; }
            st->Bres[j] = (uint32_t)br;
        }
        for (int f = 0; f < NFILTER; f++) {
            if (f == pi) continue;   /* C_f excludes f itself: unchanged */
            uint32_t mod = modf_arr[f];
            uint64_t cf = st->Cf[f];
            if (d > 0) { for (int t = 0; t < ad; t++) cf = cf * (uint32_t)(p % (int)mod) % mod; }
            else { uint32_t iv = inv_p_modf[f][pi]; for (int t = 0; t < ad; t++) cf = cf * iv % mod; }
            st->Cf[f] = (uint32_t)cf;
        }
    }
    for (int f = 0; f < NFILTER; f++) {
        if (st->E[f] == 0) { st->RF[f] = 0; continue; }
        st->RF[f] = st->Cf[f] % p_pow_arr[f][st->E[f]];
    }
}

/* debug: incremental sweep for a single a up to b, dump state */
void pk_debug_state(int a, int b, uint8_t *e_out, uint32_t *u_out,
                    uint32_t *rf_out, uint32_t *bres_out) {
    State *st = (State *)malloc(sizeof(State));
    state_reset(st, a);
    for (int n = a; n <= b; n++) state_add(st, n);
    for (int pi = 0; pi < NP; pi++) { e_out[pi] = st->E[pi]; u_out[pi] = st->U[pi]; }
    for (int f = 0; f < NFILTER; f++) rf_out[f] = st->RF[f];
    for (int j = 0; j < NQR; j++) bres_out[j] = st->Bres[j];
    free(st);
}

/* ---------------- the sweep over a chunk of a-values ---------------- */
int pk_sweep_chunk(int a0, int a1, int N,
                   uint16_t *out_single, uint64_t cap_single,
                   uint16_t *out_l2, uint64_t cap_l2,
                   uint64_t *stats) {
    State *st = (State *)malloc(sizeof(State));
    uint64_t ns = 0, nl = 0;
    for (int i = 0; i < 6; i++) stats[i] = 0;
    for (int a = a0; a <= a1; a++) {
        state_reset(st, a);
        for (int b = a; b <= N; b++) {
            state_add(st, b);
            stats[0]++;
            if (st->changed_cnt > 0) { stats[1]++; stats[2] += (uint64_t)st->changed_cnt; }
            int spass = 1;
            for (int f = 0; f < NFILTER; f++) {
                if (st->E[f] == 0) continue;
                uint32_t qf = p_pow_arr[f][st->E[f]];
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
