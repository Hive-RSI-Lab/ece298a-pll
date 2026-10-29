// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table implementation internals

#include "Vtop__pch.h"

extern const VlVarTableEntry Vtop___024root__VpiVarTable0[];
extern const VlVarTableEntry Vtop___024root__VpiVarTable1[];
extern const VlVarTableEntry Vtop___024root__VpiVarTable2[];
extern const VlVarTableEntry Vtop___024root__VpiVarTable3[];
extern const VlVarTableEntry Vtop___024root__VpiVarTable4[];
extern const VlVarTableEntry Vtop___024root__VpiVarTable5[];
extern const VlVarTableEntry Vtop___024root__VpiVarTable6[];
extern const VlScopeTableEntry Vtop__Syms__VpiScopeTable[];


// VPI VARIABLE/SCOPE TABLES
#if defined(__GNUC__)
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Winvalid-offsetof"
#endif
extern const VlVarTableEntry Vtop___024root__VpiVarTable0[] = {
    {"clk", offsetof(Vtop___024root, clk), VLVT_UINT8, (VLVD_IN|VLVF_PUB_RW|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"clk_fb", offsetof(Vtop___024root, clk_fb), VLVT_UINT8, (VLVD_OUT|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"cp_trim0", offsetof(Vtop___024root, cp_trim0), VLVT_UINT8, (VLVD_OUT|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"cp_trim1", offsetof(Vtop___024root, cp_trim1), VLVT_UINT8, (VLVD_OUT|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"cp_trim_in", offsetof(Vtop___024root, cp_trim_in), VLVT_UINT8, (VLVD_IN|VLVF_PUB_RW|VLVF_NET), 0, 1, {1, 0, 0, 0, 0, 0}},
    {"lock", offsetof(Vtop___024root, lock), VLVT_UINT8, (VLVD_OUT|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"n_sel", offsetof(Vtop___024root, n_sel), VLVT_UINT8, (VLVD_IN|VLVF_PUB_RW|VLVF_NET), 0, 1, {2, 0, 0, 0, 0, 0}},
    {"obs_out", offsetof(Vtop___024root, obs_out), VLVT_UINT8, (VLVD_OUT|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"obs_sel", offsetof(Vtop___024root, obs_sel), VLVT_UINT8, (VLVD_IN|VLVF_PUB_RW|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"pfd_dn", offsetof(Vtop___024root, pfd_dn), VLVT_UINT8, (VLVD_OUT|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"pfd_up", offsetof(Vtop___024root, pfd_up), VLVT_UINT8, (VLVD_OUT|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"pll_en", offsetof(Vtop___024root, pll_en), VLVT_UINT8, (VLVD_OUT|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"pll_en_in", offsetof(Vtop___024root, pll_en_in), VLVT_UINT8, (VLVD_IN|VLVF_PUB_RW|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"rst_n", offsetof(Vtop___024root, rst_n), VLVT_UINT8, (VLVD_IN|VLVF_PUB_RW|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"vco_out", offsetof(Vtop___024root, vco_out), VLVT_UINT8, (VLVD_IN|VLVF_PUB_RW|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
};
extern const VlVarTableEntry Vtop___024root__VpiVarTable1[] = {
    {"clk", offsetof(Vtop___024root, ihsan_sa_pll__DOT__clk), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"clk_fb", offsetof(Vtop___024root, ihsan_sa_pll__DOT__clk_fb), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"clk_fb_int", offsetof(Vtop___024root, ihsan_sa_pll__DOT__clk_fb_int), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"clk_pre", offsetof(Vtop___024root, ihsan_sa_pll__DOT__clk_pre), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"cp_trim0", offsetof(Vtop___024root, ihsan_sa_pll__DOT__cp_trim0), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"cp_trim1", offsetof(Vtop___024root, ihsan_sa_pll__DOT__cp_trim1), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"cp_trim_in", offsetof(Vtop___024root, ihsan_sa_pll__DOT__cp_trim_in), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 1, {1, 0, 0, 0, 0, 0}},
    {"lock", offsetof(Vtop___024root, ihsan_sa_pll__DOT__lock), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"n_sel", offsetof(Vtop___024root, ihsan_sa_pll__DOT__n_sel), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 1, {2, 0, 0, 0, 0, 0}},
    {"obs_int", offsetof(Vtop___024root, ihsan_sa_pll__DOT__obs_int), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"obs_out", offsetof(Vtop___024root, ihsan_sa_pll__DOT__obs_out), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"obs_q3", offsetof(Vtop___024root, ihsan_sa_pll__DOT__obs_q3), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"obs_sel", offsetof(Vtop___024root, ihsan_sa_pll__DOT__obs_sel), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"pfd_dn", offsetof(Vtop___024root, ihsan_sa_pll__DOT__pfd_dn), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"pfd_dn_q", offsetof(Vtop___024root, ihsan_sa_pll__DOT__pfd_dn_q), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"pfd_up", offsetof(Vtop___024root, ihsan_sa_pll__DOT__pfd_up), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"pfd_up_q", offsetof(Vtop___024root, ihsan_sa_pll__DOT__pfd_up_q), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"pll_en", offsetof(Vtop___024root, ihsan_sa_pll__DOT__pll_en), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"pll_en_in", offsetof(Vtop___024root, ihsan_sa_pll__DOT__pll_en_in), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"recover", offsetof(Vtop___024root, ihsan_sa_pll__DOT__recover), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"rst_n", offsetof(Vtop___024root, ihsan_sa_pll__DOT__rst_n), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"vco_out", offsetof(Vtop___024root, ihsan_sa_pll__DOT__vco_out), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
};
extern const VlVarTableEntry Vtop___024root__VpiVarTable2[] = {
    {"clk", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_ctrl__DOT__clk), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"cp_trim0", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_ctrl__DOT__cp_trim0), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"cp_trim1", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_ctrl__DOT__cp_trim1), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"cp_trim_in", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_ctrl__DOT__cp_trim_in), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 1, {1, 0, 0, 0, 0, 0}},
    {"pll_en", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_ctrl__DOT__pll_en), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"pll_en_in", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_ctrl__DOT__pll_en_in), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"rst_n", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_ctrl__DOT__rst_n), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
};
extern const VlVarTableEntry Vtop___024root__VpiVarTable3[] = {
    {"clk_fb", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_div__DOT__clk_fb), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"clk_pre", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_div__DOT__clk_pre), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"div_cnt", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_div__DOT__div_cnt), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW), 0, 1, {2, 0, 0, 0, 0, 0}},
    {"fb_en", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_div__DOT__fb_en), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"last", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_div__DOT__last), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"n_legal", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_div__DOT__n_legal), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"n_m1", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_div__DOT__n_m1), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 1, {2, 0, 0, 0, 0, 0}},
    {"n_sel", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_div__DOT__n_sel), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 1, {2, 0, 0, 0, 0, 0}},
    {"rst_n", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_div__DOT__rst_n), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
};
extern const VlVarTableEntry Vtop___024root__VpiVarTable4[] = {
    {"clk", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_lock__DOT__clk), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"cnt_nxt", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_lock__DOT__cnt_nxt), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 1, {4, 0, 0, 0, 0, 0}},
    {"lock", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_lock__DOT__lock), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"lock_cnt", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_lock__DOT__lock_cnt), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW), 0, 1, {4, 0, 0, 0, 0, 0}},
    {"pfd_dn", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_lock__DOT__pfd_dn), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"pfd_up", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_lock__DOT__pfd_up), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"pll_en", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_lock__DOT__pll_en), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"recover", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_lock__DOT__recover), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"rst_n", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_lock__DOT__rst_n), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"wd_cnt", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_lock__DOT__wd_cnt), VLVT_UINT16, (VLVD_NODIR|VLVF_PUB_RW), 0, 1, {9, 0, 0, 0, 0, 0}},
    {"wide_q", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_lock__DOT__wide_q), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW), 0, 0, {0, 0, 0, 0, 0, 0}},
};
extern const VlVarTableEntry Vtop___024root__VpiVarTable5[] = {
    {"clk", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_pfd__DOT__clk), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"clk_fb", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_pfd__DOT__clk_fb), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"pfd_both", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_pfd__DOT__pfd_both), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"pfd_clr", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_pfd__DOT__pfd_clr), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"pfd_dly_mid", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_pfd__DOT__pfd_dly_mid), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"pfd_dn", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_pfd__DOT__pfd_dn), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"pfd_fb_q", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_pfd__DOT__pfd_fb_q), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"pfd_ref_q", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_pfd__DOT__pfd_ref_q), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"pfd_rst", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_pfd__DOT__pfd_rst), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"pfd_up", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_pfd__DOT__pfd_up), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"rst_n", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_pfd__DOT__rst_n), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
};
extern const VlVarTableEntry Vtop___024root__VpiVarTable6[] = {
    {"clk_pre", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_pre__DOT__clk_pre), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"obs_q3", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_pre__DOT__obs_q3), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"pre_c0", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_pre__DOT__pre_c0), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"pre_q0", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_pre__DOT__pre_q0), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"pre_q1", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_pre__DOT__pre_q1), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"pre_q2", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_pre__DOT__pre_q2), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"q3", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_pre__DOT__q3), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"rst_n", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_pre__DOT__rst_n), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
    {"vco_out", offsetof(Vtop___024root, ihsan_sa_pll__DOT__u_pre__DOT__vco_out), VLVT_UINT8, (VLVD_NODIR|VLVF_PUB_RW|VLVF_CONTINUOUSLY|VLVF_NET), 0, 0, {0, 0, 0, 0, 0, 0}},
};
extern const VlScopeTableEntry Vtop__Syms__VpiScopeTable[] = {
    {offsetof(Vtop__Syms, __Vscopep_TOP), "TOP", "TOP", "<null>", 0, VerilatedScope::SCOPE_OTHER},
    {offsetof(Vtop__Syms, __Vscopep_ihsan_sa_pll), "ihsan_sa_pll", "ihsan_sa_pll", "ihsan_sa_pll", -12, VerilatedScope::SCOPE_MODULE},
    {offsetof(Vtop__Syms, __Vscopep_ihsan_sa_pll__u_ctrl), "ihsan_sa_pll.u_ctrl", "u_ctrl", "pll_ctrl_regs", -12, VerilatedScope::SCOPE_MODULE},
    {offsetof(Vtop__Syms, __Vscopep_ihsan_sa_pll__u_div), "ihsan_sa_pll.u_div", "u_div", "pll_divider", -12, VerilatedScope::SCOPE_MODULE},
    {offsetof(Vtop__Syms, __Vscopep_ihsan_sa_pll__u_lock), "ihsan_sa_pll.u_lock", "u_lock", "pll_lock_det", -12, VerilatedScope::SCOPE_MODULE},
    {offsetof(Vtop__Syms, __Vscopep_ihsan_sa_pll__u_pfd), "ihsan_sa_pll.u_pfd", "u_pfd", "pll_pfd", -12, VerilatedScope::SCOPE_MODULE},
    {offsetof(Vtop__Syms, __Vscopep_ihsan_sa_pll__u_pre), "ihsan_sa_pll.u_pre", "u_pre", "pll_prescaler", -12, VerilatedScope::SCOPE_MODULE},
};
#if defined(__GNUC__)
# pragma GCC diagnostic pop
#endif
Vtop__Syms::Vtop__Syms(VerilatedContext* contextp, const char* namep, Vtop* modelp)
    : VerilatedSyms{contextp}
    // Setup internal state of the Syms class
    , __Vm_modelp{modelp}
    , __Vm_didInit{modelp->m_didInit}
    // Setup top module instance
    , TOP{this, namep}
{
    // Check resources
    Verilated::stackCheck(193);
    // Setup sub module instances
    // Configure time unit / time precision
    _vm_contextp__->timeunit(-12);
    _vm_contextp__->timeprecision(-12);
    // Setup each module's pointers to their submodules
    // Setup each module's pointer back to symbol table (for public functions)
    TOP.__Vconfigure(true);
    // Setup scopes
    VerilatedScope::scopesConstructFromTable(Vtop__Syms__VpiScopeTable, 7, this);
    // Set up scope hierarchy
    __Vhier.add(0, __Vscopep_ihsan_sa_pll);
    __Vhier.add(__Vscopep_ihsan_sa_pll, __Vscopep_ihsan_sa_pll__u_ctrl);
    __Vhier.add(__Vscopep_ihsan_sa_pll, __Vscopep_ihsan_sa_pll__u_div);
    __Vhier.add(__Vscopep_ihsan_sa_pll, __Vscopep_ihsan_sa_pll__u_lock);
    __Vhier.add(__Vscopep_ihsan_sa_pll, __Vscopep_ihsan_sa_pll__u_pfd);
    __Vhier.add(__Vscopep_ihsan_sa_pll, __Vscopep_ihsan_sa_pll__u_pre);
    // Setup export functions - final: 0
    // Setup export functions - final: 1
    // Setup public variables
    __Vscopep_TOP->varsInsertFromTable(Vtop___024root__VpiVarTable0, 15, &(TOP));
    __Vscopep_ihsan_sa_pll->varsInsertFromTable(Vtop___024root__VpiVarTable1, 22, &(TOP));
    __Vscopep_ihsan_sa_pll__u_ctrl->varsInsertFromTable(Vtop___024root__VpiVarTable2, 7, &(TOP));
    __Vscopep_ihsan_sa_pll__u_div->varsInsertFromTable(Vtop___024root__VpiVarTable3, 9, &(TOP));
    __Vscopep_ihsan_sa_pll__u_lock->varsInsertFromTable(Vtop___024root__VpiVarTable4, 11, &(TOP));
    __Vscopep_ihsan_sa_pll__u_lock->varInsert("K", const_cast<void*>(static_cast<const void*>(&(TOP.ihsan_sa_pll__DOT__u_lock__DOT__K))), true, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,4,0);
    __Vscopep_ihsan_sa_pll__u_lock->varInsert("M_LAST", const_cast<void*>(static_cast<const void*>(&(TOP.ihsan_sa_pll__DOT__u_lock__DOT__M_LAST))), true, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,9,0);
    __Vscopep_ihsan_sa_pll__u_lock->varInsert("W_LAST", const_cast<void*>(static_cast<const void*>(&(TOP.ihsan_sa_pll__DOT__u_lock__DOT__W_LAST))), true, VLVT_UINT16, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,9,0);
    __Vscopep_ihsan_sa_pll__u_pfd->varsInsertFromTable(Vtop___024root__VpiVarTable5, 11, &(TOP));
    __Vscopep_ihsan_sa_pll__u_pre->varsInsertFromTable(Vtop___024root__VpiVarTable6, 9, &(TOP));
}

Vtop__Syms::~Vtop__Syms() {
    // Tear down scope hierarchy
    __Vhier.remove(0, __Vscopep_ihsan_sa_pll);
    __Vhier.remove(__Vscopep_ihsan_sa_pll, __Vscopep_ihsan_sa_pll__u_ctrl);
    __Vhier.remove(__Vscopep_ihsan_sa_pll, __Vscopep_ihsan_sa_pll__u_div);
    __Vhier.remove(__Vscopep_ihsan_sa_pll, __Vscopep_ihsan_sa_pll__u_lock);
    __Vhier.remove(__Vscopep_ihsan_sa_pll, __Vscopep_ihsan_sa_pll__u_pfd);
    __Vhier.remove(__Vscopep_ihsan_sa_pll, __Vscopep_ihsan_sa_pll__u_pre);
    // Clear keys from hierarchy map after values have been removed
    __Vhier.clear();
    // Tear down scopes
    VL_DO_CLEAR(delete __Vscopep_TOP, __Vscopep_TOP = nullptr);
    VL_DO_CLEAR(delete __Vscopep_ihsan_sa_pll, __Vscopep_ihsan_sa_pll = nullptr);
    VL_DO_CLEAR(delete __Vscopep_ihsan_sa_pll__u_ctrl, __Vscopep_ihsan_sa_pll__u_ctrl = nullptr);
    VL_DO_CLEAR(delete __Vscopep_ihsan_sa_pll__u_div, __Vscopep_ihsan_sa_pll__u_div = nullptr);
    VL_DO_CLEAR(delete __Vscopep_ihsan_sa_pll__u_lock, __Vscopep_ihsan_sa_pll__u_lock = nullptr);
    VL_DO_CLEAR(delete __Vscopep_ihsan_sa_pll__u_pfd, __Vscopep_ihsan_sa_pll__u_pfd = nullptr);
    VL_DO_CLEAR(delete __Vscopep_ihsan_sa_pll__u_pre, __Vscopep_ihsan_sa_pll__u_pre = nullptr);
    // Tear down sub module instances
}
