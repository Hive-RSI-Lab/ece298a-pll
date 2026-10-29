// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vtop.h for the primary calling header

#include "Vtop__pch.h"

VL_ATTR_COLD void Vtop___024root___eval_static(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_static\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__Vtrigprevexpr___TOP__ihsan_sa_pll__DOT__u_ctrl__DOT__clk__0 
        = vlSelfRef.ihsan_sa_pll__DOT__u_ctrl__DOT__clk;
    vlSelfRef.__Vtrigprevexpr___TOP__ihsan_sa_pll__DOT__u_ctrl__DOT__rst_n__0 
        = vlSelfRef.ihsan_sa_pll__DOT__u_ctrl__DOT__rst_n;
    vlSelfRef.__Vtrigprevexpr___TOP__ihsan_sa_pll__DOT__u_lock__DOT__clk__0 
        = vlSelfRef.ihsan_sa_pll__DOT__u_lock__DOT__clk;
    vlSelfRef.__Vtrigprevexpr___TOP__ihsan_sa_pll__DOT__u_lock__DOT__rst_n__0 
        = vlSelfRef.ihsan_sa_pll__DOT__u_lock__DOT__rst_n;
    vlSelfRef.__Vtrigprevexpr___TOP__ihsan_sa_pll__DOT__u_pfd__DOT__clk__0 
        = vlSelfRef.ihsan_sa_pll__DOT__u_pfd__DOT__clk;
    vlSelfRef.__Vtrigprevexpr___TOP__ihsan_sa_pll__DOT__u_pfd__DOT__pfd_clr__0 
        = vlSelfRef.ihsan_sa_pll__DOT__u_pfd__DOT__pfd_clr;
    vlSelfRef.__Vtrigprevexpr___TOP__ihsan_sa_pll__DOT__u_pfd__DOT__clk_fb__0 
        = vlSelfRef.ihsan_sa_pll__DOT__u_pfd__DOT__clk_fb;
    vlSelfRef.__Vtrigprevexpr___TOP__ihsan_sa_pll__DOT__u_div__DOT__clk_pre__0 
        = vlSelfRef.ihsan_sa_pll__DOT__u_div__DOT__clk_pre;
    vlSelfRef.__Vtrigprevexpr___TOP__ihsan_sa_pll__DOT__u_div__DOT__rst_n__0 
        = vlSelfRef.ihsan_sa_pll__DOT__u_div__DOT__rst_n;
    vlSelfRef.__Vtrigprevexpr___TOP__ihsan_sa_pll__DOT__u_pre__DOT__rst_n__0 
        = vlSelfRef.ihsan_sa_pll__DOT__u_pre__DOT__rst_n;
    vlSelfRef.__Vtrigprevexpr___TOP__ihsan_sa_pll__DOT__u_pre__DOT__vco_out__0 
        = vlSelfRef.ihsan_sa_pll__DOT__u_pre__DOT__vco_out;
    vlSelfRef.__Vtrigprevexpr___TOP__ihsan_sa_pll__DOT__u_pre__DOT__pre_c0__0 
        = vlSelfRef.ihsan_sa_pll__DOT__u_pre__DOT__pre_c0;
    vlSelfRef.__Vtrigprevexpr___TOP__ihsan_sa_pll__DOT__u_pre__DOT__pre_q1__0 
        = vlSelfRef.ihsan_sa_pll__DOT__u_pre__DOT__pre_q1;
    vlSelfRef.__Vtrigprevexpr___TOP__ihsan_sa_pll__DOT__u_pre__DOT__pre_q2__0 
        = vlSelfRef.ihsan_sa_pll__DOT__u_pre__DOT__pre_q2;
}

VL_ATTR_COLD void Vtop___024root___eval_initial(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_initial\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG
VL_ATTR_COLD bool Vtop___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in);
void Vtop___024root___ico_sequent__TOP__0(Vtop___024root* vlSelf);

VL_ATTR_COLD bool Vtop___024root___eval_stl(Vtop___024root* vlSelf, CData/*0:0*/ firstIteration) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_stl\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VstlExecute;
    // Body
    vlSelfRef.__VstlTriggered[0U] = ((0xfffffffffffffffeULL 
                                      & vlSelfRef.__VstlTriggered[0U]) 
                                     | (IData)((IData)(firstIteration)));
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vtop___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
    }
#endif
    __VstlExecute = Vtop___024root___trigger_anySet__stl(vlSelfRef.__VstlTriggered);
    if (__VstlExecute) {
        {
            // Inlined CFunc: _eval_body__stl
            if ((1ULL & vlSelfRef.__VstlTriggered[0U])) {
                Vtop___024root___ico_sequent__TOP__0(vlSelf);
            }
        }
    }
    return (__VstlExecute);
}

VL_ATTR_COLD void Vtop___024root___eval_dump_triggers__stl(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_dump_triggers__stl\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
#ifdef VL_DEBUG
    Vtop___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
#endif
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__ico(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG

VL_ATTR_COLD void Vtop___024root___eval_dump_triggers__ico(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_dump_triggers__ico\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
#ifdef VL_DEBUG
    Vtop___024root___dump_triggers__ico(vlSelfRef.__VicoTriggered, "ico"s);
#endif
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG

VL_ATTR_COLD void Vtop___024root___eval_dump_triggers__act(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_dump_triggers__act\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
#ifdef VL_DEBUG
    Vtop___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
#endif
}

VL_ATTR_COLD void Vtop___024root___eval_dump_triggers__nba(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_dump_triggers__nba\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
#ifdef VL_DEBUG
    Vtop___024root___dump_triggers__act(vlSelfRef.__VnbaTriggered, "nba"s);
#endif
}

VL_ATTR_COLD void Vtop___024root___eval_dump_triggers__obs(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_dump_triggers__obs\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

VL_ATTR_COLD void Vtop___024root___eval_dump_triggers__react(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_dump_triggers__react\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

VL_ATTR_COLD void Vtop___024root___eval_final(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_final\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___dump_triggers__stl\n"); );
    // Body
    if ((1U & (~ (IData)(Vtop___024root___trigger_anySet__stl(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: Internal 'stl' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD bool Vtop___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___trigger_anySet__stl\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        if (in[n]) {
            return (1U);
        }
        n = ((IData)(1U) + n);
    } while ((1U > n));
    return (0U);
}

bool Vtop___024root___trigger_anySet__ico(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__ico(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___dump_triggers__ico\n"); );
    // Body
    if ((1U & (~ (IData)(Vtop___024root___trigger_anySet__ico(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: Internal 'ico' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

bool Vtop___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___dump_triggers__act\n"); );
    // Body
    if ((1U & (~ (IData)(Vtop___024root___trigger_anySet__act(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: @(posedge ihsan_sa_pll.u_ctrl.clk)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 1U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 1 is active: @(negedge ihsan_sa_pll.u_ctrl.rst_n)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 2U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 2 is active: @(negedge ihsan_sa_pll.u_lock.clk)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 3U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 3 is active: @(negedge ihsan_sa_pll.u_lock.rst_n)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 4U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 4 is active: @(posedge ihsan_sa_pll.u_lock.clk)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 5U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 5 is active: @(posedge ihsan_sa_pll.u_pfd.clk)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 6U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 6 is active: @(posedge ihsan_sa_pll.u_pfd.pfd_clr)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 7U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 7 is active: @(posedge ihsan_sa_pll.u_pfd.clk_fb)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 8U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 8 is active: @(posedge ihsan_sa_pll.u_div.clk_pre)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 9U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 9 is active: @(negedge ihsan_sa_pll.u_div.rst_n)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000aU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 10 is active: @(negedge ihsan_sa_pll.u_div.clk_pre)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000bU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 11 is active: @(negedge ihsan_sa_pll.u_pre.rst_n)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000cU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 12 is active: @(posedge ihsan_sa_pll.u_pre.vco_out)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000dU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 13 is active: @(posedge ihsan_sa_pll.u_pre.pre_c0)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000eU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 14 is active: @(posedge ihsan_sa_pll.u_pre.pre_q1)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 0x0000000fU)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 15 is active: @(posedge ihsan_sa_pll.u_pre.pre_q2)\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void Vtop___024root___ctor_var_reset(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___ctor_var_reset\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->vlNamep);
    vlSelf->clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16707436170211756652ull);
    vlSelf->rst_n = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1638864771569018232ull);
    vlSelf->n_sel = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 13861315636995106344ull);
    vlSelf->vco_out = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14030952074684920407ull);
    vlSelf->pll_en_in = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9198092914150464314ull);
    vlSelf->obs_sel = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17736905269052188940ull);
    vlSelf->cp_trim_in = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 8579801363876981793ull);
    vlSelf->obs_out = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6139016576332575188ull);
    vlSelf->clk_fb = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8118658279804137748ull);
    vlSelf->lock = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5580153086071103576ull);
    vlSelf->pfd_up = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10488131373785415327ull);
    vlSelf->pfd_dn = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17338478355874751429ull);
    vlSelf->pll_en = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1472359947486714354ull);
    vlSelf->cp_trim0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6599077995806622669ull);
    vlSelf->cp_trim1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12321575865466420355ull);
    vlSelf->ihsan_sa_pll__DOT__clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13650864205234946267ull);
    vlSelf->ihsan_sa_pll__DOT__rst_n = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9532562969552328807ull);
    vlSelf->ihsan_sa_pll__DOT__n_sel = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 14877348486096985535ull);
    vlSelf->ihsan_sa_pll__DOT__vco_out = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7693279463502932487ull);
    vlSelf->ihsan_sa_pll__DOT__pll_en_in = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12007047101773805953ull);
    vlSelf->ihsan_sa_pll__DOT__obs_sel = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9632110388556293288ull);
    vlSelf->ihsan_sa_pll__DOT__cp_trim_in = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 808010375139981618ull);
    vlSelf->ihsan_sa_pll__DOT__obs_out = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7983509076043332117ull);
    vlSelf->ihsan_sa_pll__DOT__clk_fb = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6581891111924884297ull);
    vlSelf->ihsan_sa_pll__DOT__lock = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12908466780711471747ull);
    vlSelf->ihsan_sa_pll__DOT__pfd_up = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14913232829163510702ull);
    vlSelf->ihsan_sa_pll__DOT__pfd_dn = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16493560740993977196ull);
    vlSelf->ihsan_sa_pll__DOT__pll_en = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12667824848526646164ull);
    vlSelf->ihsan_sa_pll__DOT__cp_trim0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 150551867398346610ull);
    vlSelf->ihsan_sa_pll__DOT__cp_trim1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16018672605139749872ull);
    vlSelf->ihsan_sa_pll__DOT__clk_pre = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5605143549271000994ull);
    vlSelf->ihsan_sa_pll__DOT__obs_q3 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4667687931554656986ull);
    vlSelf->ihsan_sa_pll__DOT__clk_fb_int = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5823104482960443354ull);
    vlSelf->ihsan_sa_pll__DOT__obs_int = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 557804297246370489ull);
    vlSelf->ihsan_sa_pll__DOT__pfd_up_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14896427600577522906ull);
    vlSelf->ihsan_sa_pll__DOT__pfd_dn_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7815725853911695152ull);
    vlSelf->ihsan_sa_pll__DOT__recover = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1455938682897516576ull);
    vlSelf->ihsan_sa_pll__DOT____Vtogcov__clk = 0;
    vlSelf->ihsan_sa_pll__DOT____Vtogcov__rst_n = 0;
    vlSelf->ihsan_sa_pll__DOT____Vtogcov__n_sel = 0;
    vlSelf->ihsan_sa_pll__DOT____Vtogcov__vco_out = 0;
    vlSelf->ihsan_sa_pll__DOT____Vtogcov__pll_en_in = 0;
    vlSelf->ihsan_sa_pll__DOT____Vtogcov__obs_sel = 0;
    vlSelf->ihsan_sa_pll__DOT____Vtogcov__cp_trim_in = 0;
    vlSelf->ihsan_sa_pll__DOT____Vtogcov__obs_out = 0;
    vlSelf->ihsan_sa_pll__DOT____Vtogcov__clk_fb = 0;
    vlSelf->ihsan_sa_pll__DOT____Vtogcov__lock = 0;
    vlSelf->ihsan_sa_pll__DOT____Vtogcov__pfd_up = 0;
    vlSelf->ihsan_sa_pll__DOT____Vtogcov__pfd_dn = 0;
    vlSelf->ihsan_sa_pll__DOT____Vtogcov__pll_en = 0;
    vlSelf->ihsan_sa_pll__DOT____Vtogcov__cp_trim0 = 0;
    vlSelf->ihsan_sa_pll__DOT____Vtogcov__cp_trim1 = 0;
    vlSelf->ihsan_sa_pll__DOT____Vtogcov__clk_pre = 0;
    vlSelf->ihsan_sa_pll__DOT____Vtogcov__obs_q3 = 0;
    vlSelf->ihsan_sa_pll__DOT____Vtogcov__clk_fb_int = 0;
    vlSelf->ihsan_sa_pll__DOT____Vtogcov__obs_int = 0;
    vlSelf->ihsan_sa_pll__DOT____Vtogcov__pfd_up_q = 0;
    vlSelf->ihsan_sa_pll__DOT____Vtogcov__pfd_dn_q = 0;
    vlSelf->ihsan_sa_pll__DOT____Vtogcov__recover = 0;
    vlSelf->ihsan_sa_pll__DOT__u_ctrl__DOT__clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17438608198327369272ull);
    vlSelf->ihsan_sa_pll__DOT__u_ctrl__DOT__rst_n = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9184937104430984674ull);
    vlSelf->ihsan_sa_pll__DOT__u_ctrl__DOT__pll_en_in = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 15091098696178548979ull);
    vlSelf->ihsan_sa_pll__DOT__u_ctrl__DOT__cp_trim_in = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 2731579224415563926ull);
    vlSelf->ihsan_sa_pll__DOT__u_ctrl__DOT__pll_en = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13206945554494866103ull);
    vlSelf->ihsan_sa_pll__DOT__u_ctrl__DOT__cp_trim0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11098499781094081461ull);
    vlSelf->ihsan_sa_pll__DOT__u_ctrl__DOT__cp_trim1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4638202044065460865ull);
    vlSelf->ihsan_sa_pll__DOT__u_ctrl__DOT____Vtogcov__clk = 0;
    vlSelf->ihsan_sa_pll__DOT__u_ctrl__DOT____Vtogcov__rst_n = 0;
    vlSelf->ihsan_sa_pll__DOT__u_ctrl__DOT____Vtogcov__pll_en_in = 0;
    vlSelf->ihsan_sa_pll__DOT__u_ctrl__DOT____Vtogcov__cp_trim_in = 0;
    vlSelf->ihsan_sa_pll__DOT__u_ctrl__DOT____Vtogcov__pll_en = 0;
    vlSelf->ihsan_sa_pll__DOT__u_ctrl__DOT____Vtogcov__cp_trim0 = 0;
    vlSelf->ihsan_sa_pll__DOT__u_ctrl__DOT____Vtogcov__cp_trim1 = 0;
    vlSelf->ihsan_sa_pll__DOT__u_lock__DOT__clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14450984280647763747ull);
    vlSelf->ihsan_sa_pll__DOT__u_lock__DOT__rst_n = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18053398535558504243ull);
    vlSelf->ihsan_sa_pll__DOT__u_lock__DOT__pll_en = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16551110794397571238ull);
    vlSelf->ihsan_sa_pll__DOT__u_lock__DOT__pfd_up = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4613914908260620911ull);
    vlSelf->ihsan_sa_pll__DOT__u_lock__DOT__pfd_dn = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5609380006354632279ull);
    vlSelf->ihsan_sa_pll__DOT__u_lock__DOT__lock = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6365038384631608368ull);
    vlSelf->ihsan_sa_pll__DOT__u_lock__DOT__recover = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4591988536993291907ull);
    vlSelf->ihsan_sa_pll__DOT__u_lock__DOT__wide_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13508837227596510024ull);
    vlSelf->ihsan_sa_pll__DOT__u_lock__DOT__lock_cnt = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 8345636112372214708ull);
    vlSelf->ihsan_sa_pll__DOT__u_lock__DOT__wd_cnt = VL_SCOPED_RAND_RESET_I(10, __VscopeHash, 15024791705243602023ull);
    vlSelf->ihsan_sa_pll__DOT__u_lock__DOT__cnt_nxt = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 9882110918868192671ull);
    vlSelf->ihsan_sa_pll__DOT__u_lock__DOT____Vtogcov__clk = 0;
    vlSelf->ihsan_sa_pll__DOT__u_lock__DOT____Vtogcov__rst_n = 0;
    vlSelf->ihsan_sa_pll__DOT__u_lock__DOT____Vtogcov__pll_en = 0;
    vlSelf->ihsan_sa_pll__DOT__u_lock__DOT____Vtogcov__pfd_up = 0;
    vlSelf->ihsan_sa_pll__DOT__u_lock__DOT____Vtogcov__pfd_dn = 0;
    vlSelf->ihsan_sa_pll__DOT__u_lock__DOT____Vtogcov__lock = 0;
    vlSelf->ihsan_sa_pll__DOT__u_lock__DOT____Vtogcov__recover = 0;
    vlSelf->ihsan_sa_pll__DOT__u_lock__DOT____Vtogcov__wide_q = 0;
    vlSelf->ihsan_sa_pll__DOT__u_lock__DOT____Vtogcov__lock_cnt = 0;
    vlSelf->ihsan_sa_pll__DOT__u_lock__DOT____Vtogcov__wd_cnt = 0;
    vlSelf->ihsan_sa_pll__DOT__u_lock__DOT____Vtogcov__cnt_nxt = 0;
    vlSelf->ihsan_sa_pll__DOT__u_pfd__DOT__clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12869428412612086240ull);
    vlSelf->ihsan_sa_pll__DOT__u_pfd__DOT__clk_fb = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 212291814539594148ull);
    vlSelf->ihsan_sa_pll__DOT__u_pfd__DOT__rst_n = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10971571614634599196ull);
    vlSelf->ihsan_sa_pll__DOT__u_pfd__DOT__pfd_up = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3581852380235626026ull);
    vlSelf->ihsan_sa_pll__DOT__u_pfd__DOT__pfd_dn = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12385635862550913165ull);
    vlSelf->ihsan_sa_pll__DOT__u_pfd__DOT__pfd_ref_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6564904429037023430ull);
    vlSelf->ihsan_sa_pll__DOT__u_pfd__DOT__pfd_fb_q = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6157439009338149830ull);
    vlSelf->ihsan_sa_pll__DOT__u_pfd__DOT__pfd_both = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16721535802808491519ull);
    vlSelf->ihsan_sa_pll__DOT__u_pfd__DOT__pfd_dly_mid = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1809123131522655225ull);
    vlSelf->ihsan_sa_pll__DOT__u_pfd__DOT__pfd_rst = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9738779353498485763ull);
    vlSelf->ihsan_sa_pll__DOT__u_pfd__DOT__pfd_clr = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7969161325676284567ull);
    vlSelf->ihsan_sa_pll__DOT__u_pfd__DOT____Vtogcov__clk = 0;
    vlSelf->ihsan_sa_pll__DOT__u_pfd__DOT____Vtogcov__clk_fb = 0;
    vlSelf->ihsan_sa_pll__DOT__u_pfd__DOT____Vtogcov__rst_n = 0;
    vlSelf->ihsan_sa_pll__DOT__u_pfd__DOT____Vtogcov__pfd_up = 0;
    vlSelf->ihsan_sa_pll__DOT__u_pfd__DOT____Vtogcov__pfd_dn = 0;
    vlSelf->ihsan_sa_pll__DOT__u_pfd__DOT____Vtogcov__pfd_ref_q = 0;
    vlSelf->ihsan_sa_pll__DOT__u_pfd__DOT____Vtogcov__pfd_fb_q = 0;
    vlSelf->ihsan_sa_pll__DOT__u_pfd__DOT____Vtogcov__pfd_both = 0;
    vlSelf->ihsan_sa_pll__DOT__u_pfd__DOT____Vtogcov__pfd_dly_mid = 0;
    vlSelf->ihsan_sa_pll__DOT__u_pfd__DOT____Vtogcov__pfd_rst = 0;
    vlSelf->ihsan_sa_pll__DOT__u_pfd__DOT____Vtogcov__pfd_clr = 0;
    vlSelf->ihsan_sa_pll__DOT__u_div__DOT__clk_pre = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8604474923806549523ull);
    vlSelf->ihsan_sa_pll__DOT__u_div__DOT__rst_n = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7113323322595467033ull);
    vlSelf->ihsan_sa_pll__DOT__u_div__DOT__n_sel = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 2849317606758651675ull);
    vlSelf->ihsan_sa_pll__DOT__u_div__DOT__clk_fb = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18013144078579582407ull);
    vlSelf->ihsan_sa_pll__DOT__u_div__DOT__div_cnt = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 11714513203152207463ull);
    vlSelf->ihsan_sa_pll__DOT__u_div__DOT__fb_en = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12203259885645185179ull);
    vlSelf->ihsan_sa_pll__DOT__u_div__DOT__n_legal = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4725816383631429200ull);
    vlSelf->ihsan_sa_pll__DOT__u_div__DOT__n_m1 = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 6693071574392786698ull);
    vlSelf->ihsan_sa_pll__DOT__u_div__DOT__last = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10553576410929552310ull);
    vlSelf->ihsan_sa_pll__DOT__u_div__DOT____Vtogcov__clk_pre = 0;
    vlSelf->ihsan_sa_pll__DOT__u_div__DOT____Vtogcov__rst_n = 0;
    vlSelf->ihsan_sa_pll__DOT__u_div__DOT____Vtogcov__n_sel = 0;
    vlSelf->ihsan_sa_pll__DOT__u_div__DOT____Vtogcov__clk_fb = 0;
    vlSelf->ihsan_sa_pll__DOT__u_div__DOT____Vtogcov__div_cnt = 0;
    vlSelf->ihsan_sa_pll__DOT__u_div__DOT____Vtogcov__fb_en = 0;
    vlSelf->ihsan_sa_pll__DOT__u_div__DOT____Vtogcov__n_legal = 0;
    vlSelf->ihsan_sa_pll__DOT__u_div__DOT____Vtogcov__n_m1 = 0;
    vlSelf->ihsan_sa_pll__DOT__u_div__DOT____Vtogcov__last = 0;
    vlSelf->ihsan_sa_pll__DOT__u_pre__DOT__vco_out = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6103691815910805590ull);
    vlSelf->ihsan_sa_pll__DOT__u_pre__DOT__rst_n = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17690435385132358202ull);
    vlSelf->ihsan_sa_pll__DOT__u_pre__DOT__clk_pre = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2397658262469019239ull);
    vlSelf->ihsan_sa_pll__DOT__u_pre__DOT__obs_q3 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10126738546993501792ull);
    vlSelf->ihsan_sa_pll__DOT__u_pre__DOT__pre_q1 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12948706277378452837ull);
    vlSelf->ihsan_sa_pll__DOT__u_pre__DOT__pre_q2 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 4565821189847337382ull);
    vlSelf->ihsan_sa_pll__DOT__u_pre__DOT__q3 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6280954010023406433ull);
    vlSelf->ihsan_sa_pll__DOT__u_pre__DOT__pre_q0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2377274436156329922ull);
    vlSelf->ihsan_sa_pll__DOT__u_pre__DOT__pre_c0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1504759165016364958ull);
    vlSelf->ihsan_sa_pll__DOT__u_pre__DOT____Vtogcov__vco_out = 0;
    vlSelf->ihsan_sa_pll__DOT__u_pre__DOT____Vtogcov__rst_n = 0;
    vlSelf->ihsan_sa_pll__DOT__u_pre__DOT____Vtogcov__clk_pre = 0;
    vlSelf->ihsan_sa_pll__DOT__u_pre__DOT____Vtogcov__obs_q3 = 0;
    vlSelf->ihsan_sa_pll__DOT__u_pre__DOT____Vtogcov__pre_q1 = 0;
    vlSelf->ihsan_sa_pll__DOT__u_pre__DOT____Vtogcov__pre_q2 = 0;
    vlSelf->ihsan_sa_pll__DOT__u_pre__DOT____Vtogcov__q3 = 0;
    vlSelf->ihsan_sa_pll__DOT__u_pre__DOT____Vtogcov__pre_q0 = 0;
    vlSelf->ihsan_sa_pll__DOT__u_pre__DOT____Vtogcov__pre_c0 = 0;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VstlTriggered[__Vi0] = 0;
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VicoTriggered[__Vi0] = 0;
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VactTriggered[__Vi0] = 0;
    }
    vlSelf->__Vtrigprevexpr___TOP__ihsan_sa_pll__DOT__u_ctrl__DOT__clk__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__ihsan_sa_pll__DOT__u_ctrl__DOT__rst_n__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__ihsan_sa_pll__DOT__u_lock__DOT__clk__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__ihsan_sa_pll__DOT__u_lock__DOT__rst_n__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__ihsan_sa_pll__DOT__u_pfd__DOT__clk__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__ihsan_sa_pll__DOT__u_pfd__DOT__pfd_clr__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__ihsan_sa_pll__DOT__u_pfd__DOT__clk_fb__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__ihsan_sa_pll__DOT__u_div__DOT__clk_pre__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__ihsan_sa_pll__DOT__u_div__DOT__rst_n__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__ihsan_sa_pll__DOT__u_pre__DOT__rst_n__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__ihsan_sa_pll__DOT__u_pre__DOT__vco_out__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__ihsan_sa_pll__DOT__u_pre__DOT__pre_c0__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__ihsan_sa_pll__DOT__u_pre__DOT__pre_q1__0 = 0;
    vlSelf->__Vtrigprevexpr___TOP__ihsan_sa_pll__DOT__u_pre__DOT__pre_q2__0 = 0;
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VnbaTriggered[__Vi0] = 0;
    }
}

VL_ATTR_COLD void Vtop___024root___configure_coverage(Vtop___024root* vlSelf, bool first) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___configure_coverage\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    (void)first;  // Prevent unused variable warning
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 0, first, true, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 13, 23, ".ihsan_sa_pll", "v_toggle/ihsan_sa_pll", "clk");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 2, first, true, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 14, 23, ".ihsan_sa_pll", "v_toggle/ihsan_sa_pll", "rst_n");
    vlSelf->__vlCoverToggleInsert(0, 2, 1, vlSelf->__Vcoverage + 4, first, true, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 15, 23, ".ihsan_sa_pll", "v_toggle/ihsan_sa_pll", "n_sel");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 10, first, true, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 16, 23, ".ihsan_sa_pll", "v_toggle/ihsan_sa_pll", "vco_out");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 12, first, true, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 17, 23, ".ihsan_sa_pll", "v_toggle/ihsan_sa_pll", "pll_en_in");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 14, first, true, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 18, 23, ".ihsan_sa_pll", "v_toggle/ihsan_sa_pll", "obs_sel");
    vlSelf->__vlCoverToggleInsert(0, 1, 1, vlSelf->__Vcoverage + 16, first, true, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 19, 23, ".ihsan_sa_pll", "v_toggle/ihsan_sa_pll", "cp_trim_in");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 20, first, true, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 20, 23, ".ihsan_sa_pll", "v_toggle/ihsan_sa_pll", "obs_out");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 22, first, true, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 21, 23, ".ihsan_sa_pll", "v_toggle/ihsan_sa_pll", "clk_fb");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 24, first, true, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 22, 23, ".ihsan_sa_pll", "v_toggle/ihsan_sa_pll", "lock");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 26, first, true, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 23, 23, ".ihsan_sa_pll", "v_toggle/ihsan_sa_pll", "pfd_up");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 28, first, true, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 24, 23, ".ihsan_sa_pll", "v_toggle/ihsan_sa_pll", "pfd_dn");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 30, first, true, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 25, 23, ".ihsan_sa_pll", "v_toggle/ihsan_sa_pll", "pll_en");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 32, first, true, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 26, 23, ".ihsan_sa_pll", "v_toggle/ihsan_sa_pll", "cp_trim0");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 34, first, true, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 27, 23, ".ihsan_sa_pll", "v_toggle/ihsan_sa_pll", "cp_trim1");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 36, first, true, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 33, 8, ".ihsan_sa_pll", "v_toggle/ihsan_sa_pll", "clk_pre");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 38, first, true, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 34, 8, ".ihsan_sa_pll", "v_toggle/ihsan_sa_pll", "obs_q3");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 40, first, true, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 35, 8, ".ihsan_sa_pll", "v_toggle/ihsan_sa_pll", "clk_fb_int");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 42, first, true, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 36, 8, ".ihsan_sa_pll", "v_toggle/ihsan_sa_pll", "obs_int");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 44, first, true, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 37, 8, ".ihsan_sa_pll", "v_toggle/ihsan_sa_pll", "pfd_up_q");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 46, first, true, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 38, 8, ".ihsan_sa_pll", "v_toggle/ihsan_sa_pll", "pfd_dn_q");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 48, first, true, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 39, 8, ".ihsan_sa_pll", "v_toggle/ihsan_sa_pll", "recover");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 50, first, true, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 52, 28, ".ihsan_sa_pll", "v_expr/ihsan_sa_pll", "(pfd_up_q==1 && recover==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 50, first, false, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 52, 28, ".ihsan_sa_pll", "v_expr/ihsan_sa_pll", "(pfd_up_q==1 && recover==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 51, first, true, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 52, 28, ".ihsan_sa_pll", "v_expr/ihsan_sa_pll", "(recover==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 51, first, false, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 52, 28, ".ihsan_sa_pll", "v_expr/ihsan_sa_pll", "(recover==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 52, first, true, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 52, 28, ".ihsan_sa_pll", "v_expr/ihsan_sa_pll", "(pfd_up_q==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 52, first, false, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 52, 28, ".ihsan_sa_pll", "v_expr/ihsan_sa_pll", "(pfd_up_q==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 53, first, true, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 53, 28, ".ihsan_sa_pll", "v_expr/ihsan_sa_pll", "(recover==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 53, first, false, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 53, 28, ".ihsan_sa_pll", "v_expr/ihsan_sa_pll", "(recover==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 54, first, true, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 53, 28, ".ihsan_sa_pll", "v_expr/ihsan_sa_pll", "(pfd_dn_q==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 54, first, false, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 53, 28, ".ihsan_sa_pll", "v_expr/ihsan_sa_pll", "(pfd_dn_q==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 55, first, true, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 53, 28, ".ihsan_sa_pll", "v_expr/ihsan_sa_pll", "(pfd_dn_q==0 && recover==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 55, first, false, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 53, 28, ".ihsan_sa_pll", "v_expr/ihsan_sa_pll", "(pfd_dn_q==0 && recover==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 56, first, true, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 65, 20, ".ihsan_sa_pll", "v_expr/ihsan_sa_pll", "(obs_sel==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 56, first, false, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 65, 20, ".ihsan_sa_pll", "v_expr/ihsan_sa_pll", "(obs_sel==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 57, first, true, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 65, 20, ".ihsan_sa_pll", "v_expr/ihsan_sa_pll", "(obs_sel==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 57, first, false, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 65, 20, ".ihsan_sa_pll", "v_expr/ihsan_sa_pll", "(obs_sel==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 58, first, true, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 65, 30, ".ihsan_sa_pll", "v_branch/ihsan_sa_pll", "cond_then", "65", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 58, first, false, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 65, 30, ".ihsan_sa_pll", "v_branch/ihsan_sa_pll", "cond_then", "65", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 59, first, true, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 65, 31, ".ihsan_sa_pll", "v_branch/ihsan_sa_pll", "cond_else", "65", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 59, first, false, "/work/blocks/pll/digital/rtl/ihsan_sa_pll.v", 65, 31, ".ihsan_sa_pll", "v_branch/ihsan_sa_pll", "cond_else", "65", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 60, first, true, "/work/blocks/pll/digital/rtl/pll_ctrl_regs.v", 4, 23, ".ihsan_sa_pll.u_ctrl", "v_toggle/pll_ctrl_regs", "clk");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 62, first, true, "/work/blocks/pll/digital/rtl/pll_ctrl_regs.v", 5, 23, ".ihsan_sa_pll.u_ctrl", "v_toggle/pll_ctrl_regs", "rst_n");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 64, first, true, "/work/blocks/pll/digital/rtl/pll_ctrl_regs.v", 6, 23, ".ihsan_sa_pll.u_ctrl", "v_toggle/pll_ctrl_regs", "pll_en_in");
    vlSelf->__vlCoverToggleInsert(0, 1, 1, vlSelf->__Vcoverage + 66, first, true, "/work/blocks/pll/digital/rtl/pll_ctrl_regs.v", 7, 23, ".ihsan_sa_pll.u_ctrl", "v_toggle/pll_ctrl_regs", "cp_trim_in");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 70, first, true, "/work/blocks/pll/digital/rtl/pll_ctrl_regs.v", 8, 23, ".ihsan_sa_pll.u_ctrl", "v_toggle/pll_ctrl_regs", "pll_en");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 72, first, true, "/work/blocks/pll/digital/rtl/pll_ctrl_regs.v", 9, 23, ".ihsan_sa_pll.u_ctrl", "v_toggle/pll_ctrl_regs", "cp_trim0");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 74, first, true, "/work/blocks/pll/digital/rtl/pll_ctrl_regs.v", 10, 23, ".ihsan_sa_pll.u_ctrl", "v_toggle/pll_ctrl_regs", "cp_trim1");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 76, first, true, "/work/blocks/pll/digital/rtl/pll_ctrl_regs.v", 13, 5, ".ihsan_sa_pll.u_ctrl", "v_branch/pll_ctrl_regs", "if", "13-16", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 76, first, false, "/work/blocks/pll/digital/rtl/pll_ctrl_regs.v", 13, 5, ".ihsan_sa_pll.u_ctrl", "v_branch/pll_ctrl_regs", "if", "13-16", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 77, first, true, "/work/blocks/pll/digital/rtl/pll_ctrl_regs.v", 13, 6, ".ihsan_sa_pll.u_ctrl", "v_branch/pll_ctrl_regs", "else", "17-20", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 77, first, false, "/work/blocks/pll/digital/rtl/pll_ctrl_regs.v", 13, 6, ".ihsan_sa_pll.u_ctrl", "v_branch/pll_ctrl_regs", "else", "17-20", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 78, first, true, "/work/blocks/pll/digital/rtl/pll_ctrl_regs.v", 13, 9, ".ihsan_sa_pll.u_ctrl", "v_expr/pll_ctrl_regs", "(rst_n==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 78, first, false, "/work/blocks/pll/digital/rtl/pll_ctrl_regs.v", 13, 9, ".ihsan_sa_pll.u_ctrl", "v_expr/pll_ctrl_regs", "(rst_n==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 79, first, true, "/work/blocks/pll/digital/rtl/pll_ctrl_regs.v", 13, 9, ".ihsan_sa_pll.u_ctrl", "v_expr/pll_ctrl_regs", "(rst_n==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 79, first, false, "/work/blocks/pll/digital/rtl/pll_ctrl_regs.v", 13, 9, ".ihsan_sa_pll.u_ctrl", "v_expr/pll_ctrl_regs", "(rst_n==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 80, first, true, "/work/blocks/pll/digital/rtl/pll_ctrl_regs.v", 12, 3, ".ihsan_sa_pll.u_ctrl", "v_line/pll_ctrl_regs", "block", "12", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 80, first, false, "/work/blocks/pll/digital/rtl/pll_ctrl_regs.v", 12, 3, ".ihsan_sa_pll.u_ctrl", "v_line/pll_ctrl_regs", "block", "12", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 81, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 19, 17, ".ihsan_sa_pll.u_lock", "v_toggle/pll_lock_det", "clk");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 83, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 20, 17, ".ihsan_sa_pll.u_lock", "v_toggle/pll_lock_det", "rst_n");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 85, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 21, 17, ".ihsan_sa_pll.u_lock", "v_toggle/pll_lock_det", "pll_en");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 87, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 22, 17, ".ihsan_sa_pll.u_lock", "v_toggle/pll_lock_det", "pfd_up");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 89, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 23, 17, ".ihsan_sa_pll.u_lock", "v_toggle/pll_lock_det", "pfd_dn");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 91, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 24, 17, ".ihsan_sa_pll.u_lock", "v_toggle/pll_lock_det", "lock");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 93, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 25, 17, ".ihsan_sa_pll.u_lock", "v_toggle/pll_lock_det", "recover");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 95, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 31, 13, ".ihsan_sa_pll.u_lock", "v_toggle/pll_lock_det", "wide_q");
    vlSelf->__vlCoverToggleInsert(0, 4, 1, vlSelf->__Vcoverage + 97, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 32, 13, ".ihsan_sa_pll.u_lock", "v_toggle/pll_lock_det", "lock_cnt");
    vlSelf->__vlCoverToggleInsert(0, 9, 1, vlSelf->__Vcoverage + 107, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 33, 13, ".ihsan_sa_pll.u_lock", "v_toggle/pll_lock_det", "wd_cnt");
    vlSelf->__vlCoverToggleInsert(0, 4, 1, vlSelf->__Vcoverage + 127, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 34, 14, ".ihsan_sa_pll.u_lock", "v_toggle/pll_lock_det", "cnt_nxt");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 137, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 34, 24, ".ihsan_sa_pll.u_lock", "v_expr/pll_lock_det", "(wide_q==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 137, first, false, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 34, 24, ".ihsan_sa_pll.u_lock", "v_expr/pll_lock_det", "(wide_q==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 138, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 34, 24, ".ihsan_sa_pll.u_lock", "v_expr/pll_lock_det", "(wide_q==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 138, first, false, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 34, 24, ".ihsan_sa_pll.u_lock", "v_expr/pll_lock_det", "(wide_q==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 139, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 34, 42, ".ihsan_sa_pll.u_lock", "v_branch/pll_lock_det", "cond_then", "34", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 139, first, false, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 34, 42, ".ihsan_sa_pll.u_lock", "v_branch/pll_lock_det", "cond_then", "34", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 140, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 35, 42, ".ihsan_sa_pll.u_lock", "v_branch/pll_lock_det", "cond_then", "35", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 140, first, false, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 35, 42, ".ihsan_sa_pll.u_lock", "v_branch/pll_lock_det", "cond_then", "35", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 141, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 35, 43, ".ihsan_sa_pll.u_lock", "v_branch/pll_lock_det", "cond_else", "35", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 141, first, false, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 35, 43, ".ihsan_sa_pll.u_lock", "v_branch/pll_lock_det", "cond_else", "35", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 142, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 34, 43, ".ihsan_sa_pll.u_lock", "v_branch/pll_lock_det", "cond_else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 142, first, false, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 34, 43, ".ihsan_sa_pll.u_lock", "v_branch/pll_lock_det", "cond_else", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 143, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 39, 34, ".ihsan_sa_pll.u_lock", "v_expr/pll_lock_det", "(pfd_dn==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 143, first, false, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 39, 34, ".ihsan_sa_pll.u_lock", "v_expr/pll_lock_det", "(pfd_dn==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 144, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 39, 34, ".ihsan_sa_pll.u_lock", "v_expr/pll_lock_det", "(pfd_up==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 144, first, false, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 39, 34, ".ihsan_sa_pll.u_lock", "v_expr/pll_lock_det", "(pfd_up==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 145, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 39, 34, ".ihsan_sa_pll.u_lock", "v_expr/pll_lock_det", "(pfd_up==0 && pfd_dn==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 145, first, false, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 39, 34, ".ihsan_sa_pll.u_lock", "v_expr/pll_lock_det", "(pfd_up==0 && pfd_dn==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 146, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 38, 5, ".ihsan_sa_pll.u_lock", "v_branch/pll_lock_det", "if", "38", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 146, first, false, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 38, 5, ".ihsan_sa_pll.u_lock", "v_branch/pll_lock_det", "if", "38", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 147, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 38, 6, ".ihsan_sa_pll.u_lock", "v_branch/pll_lock_det", "else", "39", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 147, first, false, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 38, 6, ".ihsan_sa_pll.u_lock", "v_branch/pll_lock_det", "else", "39", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 148, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 38, 9, ".ihsan_sa_pll.u_lock", "v_expr/pll_lock_det", "(rst_n==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 148, first, false, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 38, 9, ".ihsan_sa_pll.u_lock", "v_expr/pll_lock_det", "(rst_n==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 149, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 38, 9, ".ihsan_sa_pll.u_lock", "v_expr/pll_lock_det", "(rst_n==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 149, first, false, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 38, 9, ".ihsan_sa_pll.u_lock", "v_expr/pll_lock_det", "(rst_n==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 150, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 37, 3, ".ihsan_sa_pll.u_lock", "v_line/pll_lock_det", "block", "37", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 150, first, false, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 37, 3, ".ihsan_sa_pll.u_lock", "v_line/pll_lock_det", "block", "37", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 151, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 42, 5, ".ihsan_sa_pll.u_lock", "v_branch/pll_lock_det", "if", "42-44", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 151, first, false, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 42, 5, ".ihsan_sa_pll.u_lock", "v_branch/pll_lock_det", "if", "42-44", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 152, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 42, 6, ".ihsan_sa_pll.u_lock", "v_branch/pll_lock_det", "else", "45-47", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 152, first, false, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 42, 6, ".ihsan_sa_pll.u_lock", "v_branch/pll_lock_det", "else", "45-47", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 153, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 42, 9, ".ihsan_sa_pll.u_lock", "v_expr/pll_lock_det", "(rst_n==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 153, first, false, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 42, 9, ".ihsan_sa_pll.u_lock", "v_expr/pll_lock_det", "(rst_n==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 154, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 42, 9, ".ihsan_sa_pll.u_lock", "v_expr/pll_lock_det", "(rst_n==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 154, first, false, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 42, 9, ".ihsan_sa_pll.u_lock", "v_expr/pll_lock_det", "(rst_n==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 155, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 41, 3, ".ihsan_sa_pll.u_lock", "v_line/pll_lock_det", "block", "41", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 155, first, false, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 41, 3, ".ihsan_sa_pll.u_lock", "v_line/pll_lock_det", "block", "41", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 156, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 59, 18, ".ihsan_sa_pll.u_lock", "v_expr/pll_lock_det", "(recover==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 156, first, false, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 59, 18, ".ihsan_sa_pll.u_lock", "v_expr/pll_lock_det", "(recover==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 157, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 59, 18, ".ihsan_sa_pll.u_lock", "v_expr/pll_lock_det", "(recover==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 157, first, false, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 59, 18, ".ihsan_sa_pll.u_lock", "v_expr/pll_lock_det", "(recover==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 158, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 57, 14, ".ihsan_sa_pll.u_lock", "v_line/pll_lock_det", "if", "57-59", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 158, first, false, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 57, 14, ".ihsan_sa_pll.u_lock", "v_line/pll_lock_det", "if", "57-59", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 159, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 57, 15, ".ihsan_sa_pll.u_lock", "v_line/pll_lock_det", "else", "60-61", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 159, first, false, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 57, 15, ".ihsan_sa_pll.u_lock", "v_line/pll_lock_det", "else", "60-61", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 160, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 57, 29, ".ihsan_sa_pll.u_lock", "v_expr/pll_lock_det", "(recover==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 160, first, false, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 57, 29, ".ihsan_sa_pll.u_lock", "v_expr/pll_lock_det", "(recover==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 161, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 57, 29, ".ihsan_sa_pll.u_lock", "v_expr/pll_lock_det", "(recover==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 161, first, false, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 57, 29, ".ihsan_sa_pll.u_lock", "v_expr/pll_lock_det", "(recover==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 162, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 54, 14, ".ihsan_sa_pll.u_lock", "v_line/pll_lock_det", "elsif", "54-56", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 162, first, false, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 54, 14, ".ihsan_sa_pll.u_lock", "v_line/pll_lock_det", "elsif", "54-56", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 163, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 54, 26, ".ihsan_sa_pll.u_lock", "v_expr/pll_lock_det", "(lock==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 163, first, false, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 54, 26, ".ihsan_sa_pll.u_lock", "v_expr/pll_lock_det", "(lock==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 164, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 54, 26, ".ihsan_sa_pll.u_lock", "v_expr/pll_lock_det", "(pll_en==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 164, first, false, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 54, 26, ".ihsan_sa_pll.u_lock", "v_expr/pll_lock_det", "(pll_en==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 165, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 54, 26, ".ihsan_sa_pll.u_lock", "v_expr/pll_lock_det", "(pll_en==1 && lock==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 165, first, false, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 54, 26, ".ihsan_sa_pll.u_lock", "v_expr/pll_lock_det", "(pll_en==1 && lock==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 166, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 51, 5, ".ihsan_sa_pll.u_lock", "v_line/pll_lock_det", "elsif", "51-53", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 166, first, false, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 51, 5, ".ihsan_sa_pll.u_lock", "v_line/pll_lock_det", "elsif", "51-53", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 167, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 51, 9, ".ihsan_sa_pll.u_lock", "v_expr/pll_lock_det", "(rst_n==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 167, first, false, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 51, 9, ".ihsan_sa_pll.u_lock", "v_expr/pll_lock_det", "(rst_n==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 168, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 51, 9, ".ihsan_sa_pll.u_lock", "v_expr/pll_lock_det", "(rst_n==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 168, first, false, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 51, 9, ".ihsan_sa_pll.u_lock", "v_expr/pll_lock_det", "(rst_n==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 169, first, true, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 50, 3, ".ihsan_sa_pll.u_lock", "v_line/pll_lock_det", "block", "50", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 169, first, false, "/work/blocks/pll/digital/rtl/pll_lock_det.v", 50, 3, ".ihsan_sa_pll.u_lock", "v_line/pll_lock_det", "block", "50", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 170, first, true, "/work/blocks/pll/digital/rtl/pll_pfd.v", 9, 17, ".ihsan_sa_pll.u_pfd", "v_toggle/pll_pfd", "clk");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 172, first, true, "/work/blocks/pll/digital/rtl/pll_pfd.v", 10, 17, ".ihsan_sa_pll.u_pfd", "v_toggle/pll_pfd", "clk_fb");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 174, first, true, "/work/blocks/pll/digital/rtl/pll_pfd.v", 11, 17, ".ihsan_sa_pll.u_pfd", "v_toggle/pll_pfd", "rst_n");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 176, first, true, "/work/blocks/pll/digital/rtl/pll_pfd.v", 12, 17, ".ihsan_sa_pll.u_pfd", "v_toggle/pll_pfd", "pfd_up");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 178, first, true, "/work/blocks/pll/digital/rtl/pll_pfd.v", 13, 17, ".ihsan_sa_pll.u_pfd", "v_toggle/pll_pfd", "pfd_dn");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 180, first, true, "/work/blocks/pll/digital/rtl/pll_pfd.v", 15, 8, ".ihsan_sa_pll.u_pfd", "v_toggle/pll_pfd", "pfd_ref_q");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 182, first, true, "/work/blocks/pll/digital/rtl/pll_pfd.v", 15, 19, ".ihsan_sa_pll.u_pfd", "v_toggle/pll_pfd", "pfd_fb_q");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 184, first, true, "/work/blocks/pll/digital/rtl/pll_pfd.v", 16, 8, ".ihsan_sa_pll.u_pfd", "v_toggle/pll_pfd", "pfd_both");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 186, first, true, "/work/blocks/pll/digital/rtl/pll_pfd.v", 16, 29, ".ihsan_sa_pll.u_pfd", "v_expr/pll_pfd", "(pfd_ref_q==1 && pfd_fb_q==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 186, first, false, "/work/blocks/pll/digital/rtl/pll_pfd.v", 16, 29, ".ihsan_sa_pll.u_pfd", "v_expr/pll_pfd", "(pfd_ref_q==1 && pfd_fb_q==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 187, first, true, "/work/blocks/pll/digital/rtl/pll_pfd.v", 16, 29, ".ihsan_sa_pll.u_pfd", "v_expr/pll_pfd", "(pfd_fb_q==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 187, first, false, "/work/blocks/pll/digital/rtl/pll_pfd.v", 16, 29, ".ihsan_sa_pll.u_pfd", "v_expr/pll_pfd", "(pfd_fb_q==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 188, first, true, "/work/blocks/pll/digital/rtl/pll_pfd.v", 16, 29, ".ihsan_sa_pll.u_pfd", "v_expr/pll_pfd", "(pfd_ref_q==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 188, first, false, "/work/blocks/pll/digital/rtl/pll_pfd.v", 16, 29, ".ihsan_sa_pll.u_pfd", "v_expr/pll_pfd", "(pfd_ref_q==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 189, first, true, "/work/blocks/pll/digital/rtl/pll_pfd.v", 17, 19, ".ihsan_sa_pll.u_pfd", "v_toggle/pll_pfd", "pfd_dly_mid");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 191, first, true, "/work/blocks/pll/digital/rtl/pll_pfd.v", 18, 19, ".ihsan_sa_pll.u_pfd", "v_toggle/pll_pfd", "pfd_rst");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 193, first, true, "/work/blocks/pll/digital/rtl/pll_pfd.v", 19, 8, ".ihsan_sa_pll.u_pfd", "v_toggle/pll_pfd", "pfd_clr");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 195, first, true, "/work/blocks/pll/digital/rtl/pll_pfd.v", 19, 25, ".ihsan_sa_pll.u_pfd", "v_expr/pll_pfd", "(pfd_rst==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 195, first, false, "/work/blocks/pll/digital/rtl/pll_pfd.v", 19, 25, ".ihsan_sa_pll.u_pfd", "v_expr/pll_pfd", "(pfd_rst==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 196, first, true, "/work/blocks/pll/digital/rtl/pll_pfd.v", 19, 25, ".ihsan_sa_pll.u_pfd", "v_expr/pll_pfd", "(rst_n==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 196, first, false, "/work/blocks/pll/digital/rtl/pll_pfd.v", 19, 25, ".ihsan_sa_pll.u_pfd", "v_expr/pll_pfd", "(rst_n==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 197, first, true, "/work/blocks/pll/digital/rtl/pll_pfd.v", 19, 25, ".ihsan_sa_pll.u_pfd", "v_expr/pll_pfd", "(rst_n==1 && pfd_rst==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 197, first, false, "/work/blocks/pll/digital/rtl/pll_pfd.v", 19, 25, ".ihsan_sa_pll.u_pfd", "v_expr/pll_pfd", "(rst_n==1 && pfd_rst==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 198, first, true, "/work/blocks/pll/digital/rtl/pll_pfd.v", 30, 5, ".ihsan_sa_pll.u_pfd", "v_branch/pll_pfd", "if", "30", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 198, first, false, "/work/blocks/pll/digital/rtl/pll_pfd.v", 30, 5, ".ihsan_sa_pll.u_pfd", "v_branch/pll_pfd", "if", "30", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 199, first, true, "/work/blocks/pll/digital/rtl/pll_pfd.v", 30, 6, ".ihsan_sa_pll.u_pfd", "v_branch/pll_pfd", "else", "31", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 199, first, false, "/work/blocks/pll/digital/rtl/pll_pfd.v", 30, 6, ".ihsan_sa_pll.u_pfd", "v_branch/pll_pfd", "else", "31", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 200, first, true, "/work/blocks/pll/digital/rtl/pll_pfd.v", 29, 3, ".ihsan_sa_pll.u_pfd", "v_line/pll_pfd", "block", "29", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 200, first, false, "/work/blocks/pll/digital/rtl/pll_pfd.v", 29, 3, ".ihsan_sa_pll.u_pfd", "v_line/pll_pfd", "block", "29", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 201, first, true, "/work/blocks/pll/digital/rtl/pll_pfd.v", 34, 5, ".ihsan_sa_pll.u_pfd", "v_branch/pll_pfd", "if", "34", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 201, first, false, "/work/blocks/pll/digital/rtl/pll_pfd.v", 34, 5, ".ihsan_sa_pll.u_pfd", "v_branch/pll_pfd", "if", "34", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 202, first, true, "/work/blocks/pll/digital/rtl/pll_pfd.v", 34, 6, ".ihsan_sa_pll.u_pfd", "v_branch/pll_pfd", "else", "35", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 202, first, false, "/work/blocks/pll/digital/rtl/pll_pfd.v", 34, 6, ".ihsan_sa_pll.u_pfd", "v_branch/pll_pfd", "else", "35", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 203, first, true, "/work/blocks/pll/digital/rtl/pll_pfd.v", 33, 3, ".ihsan_sa_pll.u_pfd", "v_line/pll_pfd", "block", "33", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 203, first, false, "/work/blocks/pll/digital/rtl/pll_pfd.v", 33, 3, ".ihsan_sa_pll.u_pfd", "v_line/pll_pfd", "block", "33", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 204, first, true, "/work/blocks/pll/digital/rtl/pll_divider.v", 8, 23, ".ihsan_sa_pll.u_div", "v_toggle/pll_divider", "clk_pre");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 206, first, true, "/work/blocks/pll/digital/rtl/pll_divider.v", 9, 23, ".ihsan_sa_pll.u_div", "v_toggle/pll_divider", "rst_n");
    vlSelf->__vlCoverToggleInsert(0, 2, 1, vlSelf->__Vcoverage + 208, first, true, "/work/blocks/pll/digital/rtl/pll_divider.v", 10, 23, ".ihsan_sa_pll.u_div", "v_toggle/pll_divider", "n_sel");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 214, first, true, "/work/blocks/pll/digital/rtl/pll_divider.v", 11, 23, ".ihsan_sa_pll.u_div", "v_toggle/pll_divider", "clk_fb");
    vlSelf->__vlCoverToggleInsert(0, 2, 1, vlSelf->__Vcoverage + 216, first, true, "/work/blocks/pll/digital/rtl/pll_divider.v", 13, 13, ".ihsan_sa_pll.u_div", "v_toggle/pll_divider", "div_cnt");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 222, first, true, "/work/blocks/pll/digital/rtl/pll_divider.v", 14, 13, ".ihsan_sa_pll.u_div", "v_toggle/pll_divider", "fb_en");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 224, first, true, "/work/blocks/pll/digital/rtl/pll_divider.v", 17, 14, ".ihsan_sa_pll.u_div", "v_toggle/pll_divider", "n_legal");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 226, first, true, "/work/blocks/pll/digital/rtl/pll_divider.v", 17, 40, ".ihsan_sa_pll.u_div", "v_expr/pll_divider", "((n_sel >= 3'h1)==1 && (n_sel <= 3'h5)==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 226, first, false, "/work/blocks/pll/digital/rtl/pll_divider.v", 17, 40, ".ihsan_sa_pll.u_div", "v_expr/pll_divider", "((n_sel >= 3'h1)==1 && (n_sel <= 3'h5)==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 227, first, true, "/work/blocks/pll/digital/rtl/pll_divider.v", 17, 40, ".ihsan_sa_pll.u_div", "v_expr/pll_divider", "((n_sel <= 3'h5)==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 227, first, false, "/work/blocks/pll/digital/rtl/pll_divider.v", 17, 40, ".ihsan_sa_pll.u_div", "v_expr/pll_divider", "((n_sel <= 3'h5)==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 228, first, true, "/work/blocks/pll/digital/rtl/pll_divider.v", 17, 40, ".ihsan_sa_pll.u_div", "v_expr/pll_divider", "((n_sel >= 3'h1)==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 228, first, false, "/work/blocks/pll/digital/rtl/pll_divider.v", 17, 40, ".ihsan_sa_pll.u_div", "v_expr/pll_divider", "((n_sel >= 3'h1)==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 2, 1, vlSelf->__Vcoverage + 229, first, true, "/work/blocks/pll/digital/rtl/pll_divider.v", 18, 14, ".ihsan_sa_pll.u_div", "v_toggle/pll_divider", "n_m1");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 235, first, true, "/work/blocks/pll/digital/rtl/pll_divider.v", 18, 24, ".ihsan_sa_pll.u_div", "v_expr/pll_divider", "(n_legal==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 235, first, false, "/work/blocks/pll/digital/rtl/pll_divider.v", 18, 24, ".ihsan_sa_pll.u_div", "v_expr/pll_divider", "(n_legal==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 236, first, true, "/work/blocks/pll/digital/rtl/pll_divider.v", 18, 24, ".ihsan_sa_pll.u_div", "v_expr/pll_divider", "(n_legal==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 236, first, false, "/work/blocks/pll/digital/rtl/pll_divider.v", 18, 24, ".ihsan_sa_pll.u_div", "v_expr/pll_divider", "(n_legal==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 237, first, true, "/work/blocks/pll/digital/rtl/pll_divider.v", 18, 41, ".ihsan_sa_pll.u_div", "v_branch/pll_divider", "cond_then", "18", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 237, first, false, "/work/blocks/pll/digital/rtl/pll_divider.v", 18, 41, ".ihsan_sa_pll.u_div", "v_branch/pll_divider", "cond_then", "18", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 238, first, true, "/work/blocks/pll/digital/rtl/pll_divider.v", 18, 42, ".ihsan_sa_pll.u_div", "v_branch/pll_divider", "cond_else", "18", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 238, first, false, "/work/blocks/pll/digital/rtl/pll_divider.v", 18, 42, ".ihsan_sa_pll.u_div", "v_branch/pll_divider", "cond_else", "18", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 239, first, true, "/work/blocks/pll/digital/rtl/pll_divider.v", 20, 14, ".ihsan_sa_pll.u_div", "v_toggle/pll_divider", "last");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 241, first, true, "/work/blocks/pll/digital/rtl/pll_divider.v", 24, 10, ".ihsan_sa_pll.u_div", "v_line/pll_divider", "if", "24", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 241, first, false, "/work/blocks/pll/digital/rtl/pll_divider.v", 24, 10, ".ihsan_sa_pll.u_div", "v_line/pll_divider", "if", "24", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 242, first, true, "/work/blocks/pll/digital/rtl/pll_divider.v", 24, 11, ".ihsan_sa_pll.u_div", "v_line/pll_divider", "else", "25", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 242, first, false, "/work/blocks/pll/digital/rtl/pll_divider.v", 24, 11, ".ihsan_sa_pll.u_div", "v_line/pll_divider", "else", "25", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 243, first, true, "/work/blocks/pll/digital/rtl/pll_divider.v", 23, 5, ".ihsan_sa_pll.u_div", "v_line/pll_divider", "elsif", "23", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 243, first, false, "/work/blocks/pll/digital/rtl/pll_divider.v", 23, 5, ".ihsan_sa_pll.u_div", "v_line/pll_divider", "elsif", "23", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 244, first, true, "/work/blocks/pll/digital/rtl/pll_divider.v", 23, 9, ".ihsan_sa_pll.u_div", "v_expr/pll_divider", "(rst_n==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 244, first, false, "/work/blocks/pll/digital/rtl/pll_divider.v", 23, 9, ".ihsan_sa_pll.u_div", "v_expr/pll_divider", "(rst_n==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 245, first, true, "/work/blocks/pll/digital/rtl/pll_divider.v", 23, 9, ".ihsan_sa_pll.u_div", "v_expr/pll_divider", "(rst_n==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 245, first, false, "/work/blocks/pll/digital/rtl/pll_divider.v", 23, 9, ".ihsan_sa_pll.u_div", "v_expr/pll_divider", "(rst_n==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 246, first, true, "/work/blocks/pll/digital/rtl/pll_divider.v", 22, 3, ".ihsan_sa_pll.u_div", "v_line/pll_divider", "block", "22", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 246, first, false, "/work/blocks/pll/digital/rtl/pll_divider.v", 22, 3, ".ihsan_sa_pll.u_div", "v_line/pll_divider", "block", "22", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 247, first, true, "/work/blocks/pll/digital/rtl/pll_divider.v", 28, 5, ".ihsan_sa_pll.u_div", "v_branch/pll_divider", "if", "28", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 247, first, false, "/work/blocks/pll/digital/rtl/pll_divider.v", 28, 5, ".ihsan_sa_pll.u_div", "v_branch/pll_divider", "if", "28", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 248, first, true, "/work/blocks/pll/digital/rtl/pll_divider.v", 28, 6, ".ihsan_sa_pll.u_div", "v_branch/pll_divider", "else", "29", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 248, first, false, "/work/blocks/pll/digital/rtl/pll_divider.v", 28, 6, ".ihsan_sa_pll.u_div", "v_branch/pll_divider", "else", "29", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 249, first, true, "/work/blocks/pll/digital/rtl/pll_divider.v", 28, 9, ".ihsan_sa_pll.u_div", "v_expr/pll_divider", "(rst_n==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 249, first, false, "/work/blocks/pll/digital/rtl/pll_divider.v", 28, 9, ".ihsan_sa_pll.u_div", "v_expr/pll_divider", "(rst_n==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 250, first, true, "/work/blocks/pll/digital/rtl/pll_divider.v", 28, 9, ".ihsan_sa_pll.u_div", "v_expr/pll_divider", "(rst_n==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 250, first, false, "/work/blocks/pll/digital/rtl/pll_divider.v", 28, 9, ".ihsan_sa_pll.u_div", "v_expr/pll_divider", "(rst_n==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 251, first, true, "/work/blocks/pll/digital/rtl/pll_divider.v", 27, 3, ".ihsan_sa_pll.u_div", "v_line/pll_divider", "block", "27", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 251, first, false, "/work/blocks/pll/digital/rtl/pll_divider.v", 27, 3, ".ihsan_sa_pll.u_div", "v_line/pll_divider", "block", "27", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 252, first, true, "/work/blocks/pll/digital/rtl/pll_divider.v", 31, 27, ".ihsan_sa_pll.u_div", "v_expr/pll_divider", "(clk_pre==1 && fb_en==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 252, first, false, "/work/blocks/pll/digital/rtl/pll_divider.v", 31, 27, ".ihsan_sa_pll.u_div", "v_expr/pll_divider", "(clk_pre==1 && fb_en==1) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 253, first, true, "/work/blocks/pll/digital/rtl/pll_divider.v", 31, 27, ".ihsan_sa_pll.u_div", "v_expr/pll_divider", "(fb_en==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 253, first, false, "/work/blocks/pll/digital/rtl/pll_divider.v", 31, 27, ".ihsan_sa_pll.u_div", "v_expr/pll_divider", "(fb_en==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 254, first, true, "/work/blocks/pll/digital/rtl/pll_divider.v", 31, 27, ".ihsan_sa_pll.u_div", "v_expr/pll_divider", "(clk_pre==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 254, first, false, "/work/blocks/pll/digital/rtl/pll_divider.v", 31, 27, ".ihsan_sa_pll.u_div", "v_expr/pll_divider", "(clk_pre==0) => 0", "", "", "", "", "");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 255, first, true, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 15, 17, ".ihsan_sa_pll.u_pre", "v_toggle/pll_prescaler", "vco_out");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 257, first, true, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 16, 17, ".ihsan_sa_pll.u_pre", "v_toggle/pll_prescaler", "rst_n");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 259, first, true, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 17, 17, ".ihsan_sa_pll.u_pre", "v_toggle/pll_prescaler", "clk_pre");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 261, first, true, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 18, 17, ".ihsan_sa_pll.u_pre", "v_toggle/pll_prescaler", "obs_q3");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 263, first, true, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 20, 7, ".ihsan_sa_pll.u_pre", "v_toggle/pll_prescaler", "pre_q1");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 265, first, true, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 20, 15, ".ihsan_sa_pll.u_pre", "v_toggle/pll_prescaler", "pre_q2");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 267, first, true, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 20, 23, ".ihsan_sa_pll.u_pre", "v_toggle/pll_prescaler", "q3");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 269, first, true, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 37, 7, ".ihsan_sa_pll.u_pre", "v_toggle/pll_prescaler", "pre_q0");
    vlSelf->__vlCoverToggleInsert(0, 0, 0, vlSelf->__Vcoverage + 271, first, true, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 38, 8, ".ihsan_sa_pll.u_pre", "v_toggle/pll_prescaler", "pre_c0");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 273, first, true, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 41, 27, ".ihsan_sa_pll.u_pre", "v_expr/pll_prescaler", "(pre_q0==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 273, first, false, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 41, 27, ".ihsan_sa_pll.u_pre", "v_expr/pll_prescaler", "(pre_q0==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 274, first, true, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 41, 27, ".ihsan_sa_pll.u_pre", "v_expr/pll_prescaler", "(pre_q0==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 274, first, false, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 41, 27, ".ihsan_sa_pll.u_pre", "v_expr/pll_prescaler", "(pre_q0==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 275, first, true, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 40, 5, ".ihsan_sa_pll.u_pre", "v_branch/pll_prescaler", "if", "40", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 275, first, false, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 40, 5, ".ihsan_sa_pll.u_pre", "v_branch/pll_prescaler", "if", "40", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 276, first, true, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 40, 6, ".ihsan_sa_pll.u_pre", "v_branch/pll_prescaler", "else", "41", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 276, first, false, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 40, 6, ".ihsan_sa_pll.u_pre", "v_branch/pll_prescaler", "else", "41", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 277, first, true, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 40, 9, ".ihsan_sa_pll.u_pre", "v_expr/pll_prescaler", "(rst_n==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 277, first, false, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 40, 9, ".ihsan_sa_pll.u_pre", "v_expr/pll_prescaler", "(rst_n==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 278, first, true, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 40, 9, ".ihsan_sa_pll.u_pre", "v_expr/pll_prescaler", "(rst_n==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 278, first, false, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 40, 9, ".ihsan_sa_pll.u_pre", "v_expr/pll_prescaler", "(rst_n==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 279, first, true, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 39, 3, ".ihsan_sa_pll.u_pre", "v_line/pll_prescaler", "block", "39", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 279, first, false, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 39, 3, ".ihsan_sa_pll.u_pre", "v_line/pll_prescaler", "block", "39", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 280, first, true, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 46, 27, ".ihsan_sa_pll.u_pre", "v_expr/pll_prescaler", "(pre_q1==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 280, first, false, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 46, 27, ".ihsan_sa_pll.u_pre", "v_expr/pll_prescaler", "(pre_q1==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 281, first, true, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 46, 27, ".ihsan_sa_pll.u_pre", "v_expr/pll_prescaler", "(pre_q1==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 281, first, false, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 46, 27, ".ihsan_sa_pll.u_pre", "v_expr/pll_prescaler", "(pre_q1==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 282, first, true, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 45, 5, ".ihsan_sa_pll.u_pre", "v_branch/pll_prescaler", "if", "45", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 282, first, false, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 45, 5, ".ihsan_sa_pll.u_pre", "v_branch/pll_prescaler", "if", "45", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 283, first, true, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 45, 6, ".ihsan_sa_pll.u_pre", "v_branch/pll_prescaler", "else", "46", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 283, first, false, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 45, 6, ".ihsan_sa_pll.u_pre", "v_branch/pll_prescaler", "else", "46", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 284, first, true, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 45, 9, ".ihsan_sa_pll.u_pre", "v_expr/pll_prescaler", "(rst_n==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 284, first, false, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 45, 9, ".ihsan_sa_pll.u_pre", "v_expr/pll_prescaler", "(rst_n==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 285, first, true, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 45, 9, ".ihsan_sa_pll.u_pre", "v_expr/pll_prescaler", "(rst_n==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 285, first, false, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 45, 9, ".ihsan_sa_pll.u_pre", "v_expr/pll_prescaler", "(rst_n==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 286, first, true, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 44, 3, ".ihsan_sa_pll.u_pre", "v_line/pll_prescaler", "block", "44", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 286, first, false, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 44, 3, ".ihsan_sa_pll.u_pre", "v_line/pll_prescaler", "block", "44", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 287, first, true, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 50, 27, ".ihsan_sa_pll.u_pre", "v_expr/pll_prescaler", "(pre_q2==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 287, first, false, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 50, 27, ".ihsan_sa_pll.u_pre", "v_expr/pll_prescaler", "(pre_q2==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 288, first, true, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 50, 27, ".ihsan_sa_pll.u_pre", "v_expr/pll_prescaler", "(pre_q2==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 288, first, false, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 50, 27, ".ihsan_sa_pll.u_pre", "v_expr/pll_prescaler", "(pre_q2==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 289, first, true, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 49, 5, ".ihsan_sa_pll.u_pre", "v_branch/pll_prescaler", "if", "49", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 289, first, false, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 49, 5, ".ihsan_sa_pll.u_pre", "v_branch/pll_prescaler", "if", "49", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 290, first, true, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 49, 6, ".ihsan_sa_pll.u_pre", "v_branch/pll_prescaler", "else", "50", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 290, first, false, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 49, 6, ".ihsan_sa_pll.u_pre", "v_branch/pll_prescaler", "else", "50", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 291, first, true, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 49, 9, ".ihsan_sa_pll.u_pre", "v_expr/pll_prescaler", "(rst_n==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 291, first, false, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 49, 9, ".ihsan_sa_pll.u_pre", "v_expr/pll_prescaler", "(rst_n==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 292, first, true, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 49, 9, ".ihsan_sa_pll.u_pre", "v_expr/pll_prescaler", "(rst_n==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 292, first, false, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 49, 9, ".ihsan_sa_pll.u_pre", "v_expr/pll_prescaler", "(rst_n==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 293, first, true, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 48, 3, ".ihsan_sa_pll.u_pre", "v_line/pll_prescaler", "block", "48", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 293, first, false, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 48, 3, ".ihsan_sa_pll.u_pre", "v_line/pll_prescaler", "block", "48", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 294, first, true, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 54, 23, ".ihsan_sa_pll.u_pre", "v_expr/pll_prescaler", "(q3==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 294, first, false, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 54, 23, ".ihsan_sa_pll.u_pre", "v_expr/pll_prescaler", "(q3==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 295, first, true, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 54, 23, ".ihsan_sa_pll.u_pre", "v_expr/pll_prescaler", "(q3==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 295, first, false, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 54, 23, ".ihsan_sa_pll.u_pre", "v_expr/pll_prescaler", "(q3==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 296, first, true, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 53, 5, ".ihsan_sa_pll.u_pre", "v_branch/pll_prescaler", "if", "53", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 296, first, false, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 53, 5, ".ihsan_sa_pll.u_pre", "v_branch/pll_prescaler", "if", "53", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 297, first, true, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 53, 6, ".ihsan_sa_pll.u_pre", "v_branch/pll_prescaler", "else", "54", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 297, first, false, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 53, 6, ".ihsan_sa_pll.u_pre", "v_branch/pll_prescaler", "else", "54", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 298, first, true, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 53, 9, ".ihsan_sa_pll.u_pre", "v_expr/pll_prescaler", "(rst_n==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 298, first, false, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 53, 9, ".ihsan_sa_pll.u_pre", "v_expr/pll_prescaler", "(rst_n==0) => 1", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 299, first, true, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 53, 9, ".ihsan_sa_pll.u_pre", "v_expr/pll_prescaler", "(rst_n==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 299, first, false, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 53, 9, ".ihsan_sa_pll.u_pre", "v_expr/pll_prescaler", "(rst_n==1) => 0", "", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSelf->__Vcoverage + 300, first, true, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 52, 3, ".ihsan_sa_pll.u_pre", "v_line/pll_prescaler", "block", "52", "", "", "", "");
    vlSelf->__vlCoverInsert(vlSymsp->__Vcoverage + 300, first, false, "/work/blocks/pll/digital/rtl/pll_prescaler.v", 52, 3, ".ihsan_sa_pll.u_pre", "v_line/pll_prescaler", "block", "52", "", "", "", "");
}
