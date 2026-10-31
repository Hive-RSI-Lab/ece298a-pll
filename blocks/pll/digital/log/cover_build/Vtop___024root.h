// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vtop.h for the primary calling header

#ifndef VERILATED_VTOP___024ROOT_H_
#define VERILATED_VTOP___024ROOT_H_  // guard

#include "verilated.h"
#include "verilated_cov.h"
#include "verilated_covergroup.h"


class Vtop__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vtop___024root final {
  public:

    // DESIGN SPECIFIC STATE
    // Anonymous structures to workaround compiler member-count bugs
    struct {
        VL_IN8(clk,0,0);
        VL_IN8(rst_n,0,0);
        VL_IN8(vco_div2,0,0);
        VL_IN8(n_sel,2,0);
        VL_IN8(pll_en_in,0,0);
        VL_IN8(obs_sel,0,0);
        VL_IN8(cp_trim_in,1,0);
        VL_OUT8(obs_out,0,0);
        VL_OUT8(clk_fb,0,0);
        VL_OUT8(lock,0,0);
        VL_OUT8(pfd_up,0,0);
        VL_OUT8(pfd_dn,0,0);
        VL_OUT8(pll_en,0,0);
        VL_OUT8(cp_trim0,0,0);
        VL_OUT8(cp_trim1,0,0);
        CData/*0:0*/ ihsan_sa_pll__DOT____VlemCond_0;
        CData/*0:0*/ ihsan_sa_pll__DOT__clk;
        CData/*0:0*/ ihsan_sa_pll__DOT__rst_n;
        CData/*2:0*/ ihsan_sa_pll__DOT__n_sel;
        CData/*0:0*/ ihsan_sa_pll__DOT__vco_div2;
        CData/*0:0*/ ihsan_sa_pll__DOT__pll_en_in;
        CData/*0:0*/ ihsan_sa_pll__DOT__obs_sel;
        CData/*1:0*/ ihsan_sa_pll__DOT__cp_trim_in;
        CData/*0:0*/ ihsan_sa_pll__DOT__obs_out;
        CData/*0:0*/ ihsan_sa_pll__DOT__clk_fb;
        CData/*0:0*/ ihsan_sa_pll__DOT__lock;
        CData/*0:0*/ ihsan_sa_pll__DOT__pfd_up;
        CData/*0:0*/ ihsan_sa_pll__DOT__pfd_dn;
        CData/*0:0*/ ihsan_sa_pll__DOT__pll_en;
        CData/*0:0*/ ihsan_sa_pll__DOT__cp_trim0;
        CData/*0:0*/ ihsan_sa_pll__DOT__cp_trim1;
        CData/*0:0*/ ihsan_sa_pll__DOT__clk_pre;
        CData/*0:0*/ ihsan_sa_pll__DOT__obs_q3;
        CData/*0:0*/ ihsan_sa_pll__DOT__clk_fb_int;
        CData/*0:0*/ ihsan_sa_pll__DOT__obs_int;
        CData/*0:0*/ ihsan_sa_pll__DOT__pfd_up_q;
        CData/*0:0*/ ihsan_sa_pll__DOT__pfd_dn_q;
        CData/*0:0*/ ihsan_sa_pll__DOT__recover;
        CData/*0:0*/ ihsan_sa_pll__DOT____Vtogcov__clk;
        CData/*0:0*/ ihsan_sa_pll__DOT____Vtogcov__rst_n;
        CData/*2:0*/ ihsan_sa_pll__DOT____Vtogcov__n_sel;
        CData/*0:0*/ ihsan_sa_pll__DOT____Vtogcov__vco_div2;
        CData/*0:0*/ ihsan_sa_pll__DOT____Vtogcov__pll_en_in;
        CData/*0:0*/ ihsan_sa_pll__DOT____Vtogcov__obs_sel;
        CData/*1:0*/ ihsan_sa_pll__DOT____Vtogcov__cp_trim_in;
        CData/*0:0*/ ihsan_sa_pll__DOT____Vtogcov__obs_out;
        CData/*0:0*/ ihsan_sa_pll__DOT____Vtogcov__clk_fb;
        CData/*0:0*/ ihsan_sa_pll__DOT____Vtogcov__lock;
        CData/*0:0*/ ihsan_sa_pll__DOT____Vtogcov__pfd_up;
        CData/*0:0*/ ihsan_sa_pll__DOT____Vtogcov__pfd_dn;
        CData/*0:0*/ ihsan_sa_pll__DOT____Vtogcov__pll_en;
        CData/*0:0*/ ihsan_sa_pll__DOT____Vtogcov__cp_trim0;
        CData/*0:0*/ ihsan_sa_pll__DOT____Vtogcov__cp_trim1;
        CData/*0:0*/ ihsan_sa_pll__DOT____Vtogcov__clk_pre;
        CData/*0:0*/ ihsan_sa_pll__DOT____Vtogcov__obs_q3;
        CData/*0:0*/ ihsan_sa_pll__DOT____Vtogcov__clk_fb_int;
        CData/*0:0*/ ihsan_sa_pll__DOT____Vtogcov__obs_int;
        CData/*0:0*/ ihsan_sa_pll__DOT____Vtogcov__pfd_up_q;
        CData/*0:0*/ ihsan_sa_pll__DOT____Vtogcov__pfd_dn_q;
        CData/*0:0*/ ihsan_sa_pll__DOT____Vtogcov__recover;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_ctrl__DOT__clk;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_ctrl__DOT__rst_n;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_ctrl__DOT__pll_en_in;
        CData/*1:0*/ ihsan_sa_pll__DOT__u_ctrl__DOT__cp_trim_in;
    };
    struct {
        CData/*0:0*/ ihsan_sa_pll__DOT__u_ctrl__DOT__pll_en;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_ctrl__DOT__cp_trim0;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_ctrl__DOT__cp_trim1;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_ctrl__DOT____Vtogcov__clk;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_ctrl__DOT____Vtogcov__rst_n;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_ctrl__DOT____Vtogcov__pll_en_in;
        CData/*1:0*/ ihsan_sa_pll__DOT__u_ctrl__DOT____Vtogcov__cp_trim_in;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_ctrl__DOT____Vtogcov__pll_en;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_ctrl__DOT____Vtogcov__cp_trim0;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_ctrl__DOT____Vtogcov__cp_trim1;
        CData/*4:0*/ ihsan_sa_pll__DOT__u_lock__DOT____VlemCond_1;
        CData/*4:0*/ ihsan_sa_pll__DOT__u_lock__DOT____VlemCond_0;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_lock__DOT__clk;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_lock__DOT__rst_n;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_lock__DOT__pll_en;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_lock__DOT__pfd_up;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_lock__DOT__pfd_dn;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_lock__DOT__lock;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_lock__DOT__recover;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_lock__DOT__wide_q;
        CData/*4:0*/ ihsan_sa_pll__DOT__u_lock__DOT__lock_cnt;
        CData/*4:0*/ ihsan_sa_pll__DOT__u_lock__DOT__cnt_nxt;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_lock__DOT____Vtogcov__clk;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_lock__DOT____Vtogcov__rst_n;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_lock__DOT____Vtogcov__pll_en;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_lock__DOT____Vtogcov__pfd_up;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_lock__DOT____Vtogcov__pfd_dn;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_lock__DOT____Vtogcov__lock;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_lock__DOT____Vtogcov__recover;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_lock__DOT____Vtogcov__wide_q;
        CData/*4:0*/ ihsan_sa_pll__DOT__u_lock__DOT____Vtogcov__lock_cnt;
        CData/*4:0*/ ihsan_sa_pll__DOT__u_lock__DOT____Vtogcov__cnt_nxt;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_pfd__DOT__clk;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_pfd__DOT__clk_fb;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_pfd__DOT__rst_n;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_pfd__DOT__pfd_up;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_pfd__DOT__pfd_dn;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_pfd__DOT__pfd_ref_q;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_pfd__DOT__pfd_fb_q;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_pfd__DOT__pfd_both;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_pfd__DOT__pfd_dly_mid;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_pfd__DOT__pfd_rst;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_pfd__DOT__pfd_clr;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_pfd__DOT____Vtogcov__clk;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_pfd__DOT____Vtogcov__clk_fb;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_pfd__DOT____Vtogcov__rst_n;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_pfd__DOT____Vtogcov__pfd_up;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_pfd__DOT____Vtogcov__pfd_dn;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_pfd__DOT____Vtogcov__pfd_ref_q;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_pfd__DOT____Vtogcov__pfd_fb_q;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_pfd__DOT____Vtogcov__pfd_both;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_pfd__DOT____Vtogcov__pfd_dly_mid;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_pfd__DOT____Vtogcov__pfd_rst;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_pfd__DOT____Vtogcov__pfd_clr;
        CData/*2:0*/ ihsan_sa_pll__DOT__u_div__DOT____VlemCond_0;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_div__DOT__clk_pre;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_div__DOT__rst_n;
        CData/*2:0*/ ihsan_sa_pll__DOT__u_div__DOT__n_sel;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_div__DOT__clk_fb;
        CData/*2:0*/ ihsan_sa_pll__DOT__u_div__DOT__div_cnt;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_div__DOT__fb_en;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_div__DOT__n_legal;
        CData/*2:0*/ ihsan_sa_pll__DOT__u_div__DOT__n_m1;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_div__DOT__last;
    };
    struct {
        CData/*0:0*/ ihsan_sa_pll__DOT__u_div__DOT____Vtogcov__clk_pre;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_div__DOT____Vtogcov__rst_n;
        CData/*2:0*/ ihsan_sa_pll__DOT__u_div__DOT____Vtogcov__n_sel;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_div__DOT____Vtogcov__clk_fb;
        CData/*2:0*/ ihsan_sa_pll__DOT__u_div__DOT____Vtogcov__div_cnt;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_div__DOT____Vtogcov__fb_en;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_div__DOT____Vtogcov__n_legal;
        CData/*2:0*/ ihsan_sa_pll__DOT__u_div__DOT____Vtogcov__n_m1;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_div__DOT____Vtogcov__last;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_pre__DOT__vco_div2;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_pre__DOT__rst_n;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_pre__DOT__clk_pre;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_pre__DOT__obs_q3;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_pre__DOT__pre_q0;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_pre__DOT__pre_q1;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_pre__DOT__q3;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_pre__DOT____Vtogcov__vco_div2;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_pre__DOT____Vtogcov__rst_n;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_pre__DOT____Vtogcov__clk_pre;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_pre__DOT____Vtogcov__obs_q3;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_pre__DOT____Vtogcov__pre_q0;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_pre__DOT____Vtogcov__pre_q1;
        CData/*0:0*/ ihsan_sa_pll__DOT__u_pre__DOT____Vtogcov__q3;
        CData/*0:0*/ __Vtrigprevexpr___TOP__ihsan_sa_pll__DOT__u_ctrl__DOT__clk__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__ihsan_sa_pll__DOT__u_ctrl__DOT__rst_n__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__ihsan_sa_pll__DOT__u_lock__DOT__clk__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__ihsan_sa_pll__DOT__u_lock__DOT__rst_n__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__ihsan_sa_pll__DOT__u_pfd__DOT__clk__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__ihsan_sa_pll__DOT__u_pfd__DOT__pfd_clr__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__ihsan_sa_pll__DOT__u_pfd__DOT__clk_fb__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__ihsan_sa_pll__DOT__u_div__DOT__clk_pre__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__ihsan_sa_pll__DOT__u_div__DOT__rst_n__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__ihsan_sa_pll__DOT__u_pre__DOT__rst_n__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__ihsan_sa_pll__DOT__u_pre__DOT__vco_div2__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__ihsan_sa_pll__DOT__u_pre__DOT__pre_q0__0;
        CData/*0:0*/ __Vtrigprevexpr___TOP__ihsan_sa_pll__DOT__u_pre__DOT__pre_q1__0;
        SData/*9:0*/ ihsan_sa_pll__DOT__u_lock__DOT__wd_cnt;
        SData/*9:0*/ ihsan_sa_pll__DOT__u_lock__DOT____Vtogcov__wd_cnt;
        VlUnpacked<QData/*63:0*/, 1> __VstlTriggered;
        VlUnpacked<QData/*63:0*/, 1> __VicoTriggered;
        VlUnpacked<QData/*63:0*/, 1> __VactTriggered;
        VlUnpacked<QData/*63:0*/, 1> __VnbaTriggered;
    };

    // INTERNAL VARIABLES
    Vtop__Syms* vlSymsp;
    const char* vlNamep;
    uint32_t __Vcoverage[290]{};

    // PARAMETERS
    static constexpr CData/*4:0*/ ihsan_sa_pll__DOT__u_lock__DOT__K = 0x10U;
    static constexpr SData/*9:0*/ ihsan_sa_pll__DOT__u_lock__DOT__W_LAST = 0x03ffU;
    static constexpr SData/*9:0*/ ihsan_sa_pll__DOT__u_lock__DOT__M_LAST = 0x007fU;

    // CONSTRUCTORS
    Vtop___024root(Vtop__Syms* symsp, const char* namep);
    ~Vtop___024root();
    VL_UNCOPYABLE(Vtop___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
    void __vlCoverInsert(uint32_t* countp, bool enable, bool localCounter, const char* filenamep, int lineno, int column,
        const char* hierp, const char* pagep, const char* commentp, const char* linescovp,
        const char* fsmVarp, const char* fsmFromp, const char* fsmTop, const char* fsmTagp);
    void __vlCoverToggleInsert(int begin, int end, bool ranged, uint32_t* countp, bool enable, bool localCounter, const char* filenamep, int lineno, int column,
        const char* hierp, const char* pagep, const char* commentp);
};


#endif  // guard
