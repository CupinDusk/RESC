#include <cxxrtl/cxxrtl.h>

#if defined(CXXRTL_INCLUDE_CAPI_IMPL) || \
    defined(CXXRTL_INCLUDE_VCD_CAPI_IMPL)
#include <cxxrtl/capi/cxxrtl_capi.cc>
#endif

#if defined(CXXRTL_INCLUDE_VCD_CAPI_IMPL)
#include <cxxrtl/capi/cxxrtl_capi_vcd.cc>
#endif

using namespace cxxrtl_yosys;

namespace cxxrtl_design {

// \top: 1
// \src: controller.v:1.1-34.10
struct p_controller : public module {
	// \src: controller.v:2.57-2.61
	/*output*/ wire<1> p_busy;
	// \src: controller.v:1.69-1.73
	/*input*/ value<32> p_cfgd;
	// \src: controller.v:1.25-1.28
	/*input*/ value<1> p_clk;
	value<1> prev_p_clk;
	bool posedge_p_clk() const {
		return !prev_p_clk.slice<0>().val() && p_clk.slice<0>().val();
	}
	// \src: controller.v:1.33-1.45
	/*input*/ value<1> p_commandreset;
	// \src: controller.v:1.79-1.83
	/*input*/ value<32> p_gden;
	// \src: controller.v:1.74-1.78
	/*input*/ value<32> p_gnum;
	// \src: controller.v:3.19-3.24
	/*output*/ wire<32> p_heldd;
	// \src: controller.v:2.13-2.21
	/*output*/ wire<1> p_licensed;
	// \src: controller.v:3.35-3.40
	/*output*/ wire<32> p_phase;
	// \src: controller.v:3.25-3.34
	/*output*/ wire<32> p_previousd;
	// \src: controller.v:3.82-3.87
	/*output*/ wire<1> p_pulse;
	// \src: controller.v:3.41-3.47
	/*output*/ wire<32> p_pulses;
	// \src: controller.v:2.84-2.90
	/*output*/ wire<4> p_reason;
	// \src: controller.v:1.29-1.32
	/*input*/ value<1> p_rst;
	// \src: controller.v:2.38-2.45
	/*output*/ wire<2> p_settled;
	// \src: controller.v:1.46-1.51
	/*input*/ value<1> p_start;
	// \src: controller.v:1.52-1.56
	/*input*/ value<1> p_stop;
	// \src: controller.v:3.65-3.70
	/*output*/ wire<64> p_timer;
	// \src: controller.v:2.62-2.67
	/*output*/ wire<1> p_valid;
	// \src: controller.v:5.13-5.15
	/*outline*/ value<64> p_dg;
	// \src: controller.v:7.13-7.16
	/*outline*/ value<64> p_dg2;
	// \src: controller.v:4.13-4.15
	/*outline*/ value<64> p_gd;
	// \src: controller.v:6.13-6.16
	/*outline*/ value<64> p_gd2;
	p_controller(interior) {}
	p_controller() {
		reset();
	};

	void reset() override;

	bool eval(performer *performer = nullptr) override;

	template<class ObserverT>
	bool commit(ObserverT &observer) {
		bool changed = false;
		if (p_busy.commit(observer)) changed = true;
		prev_p_clk = p_clk;
		if (p_heldd.commit(observer)) changed = true;
		if (p_licensed.commit(observer)) changed = true;
		if (p_phase.commit(observer)) changed = true;
		if (p_previousd.commit(observer)) changed = true;
		if (p_pulse.commit(observer)) changed = true;
		if (p_pulses.commit(observer)) changed = true;
		if (p_reason.commit(observer)) changed = true;
		if (p_settled.commit(observer)) changed = true;
		if (p_timer.commit(observer)) changed = true;
		if (p_valid.commit(observer)) changed = true;
		return changed;
	}

	bool commit() override {
		observer observer;
		return commit<>(observer);
	}

	void debug_eval();
	debug_outline debug_eval_outline { std::bind(&p_controller::debug_eval, this) };

	void debug_info(debug_items *items, debug_scopes *scopes, std::string path, metadata_map &&cell_attrs = {}) override;
}; // struct p_controller

void p_controller::reset() {
}

bool p_controller::eval(performer *performer) {
	bool converged = true;
	bool posedge_p_clk = this->posedge_p_clk();
	value<4> i_auto_24_wreduce_2e_cc_3a_513_3a_run_24_467;
	value<4> i_auto_24_wreduce_2e_cc_3a_513_3a_run_24_468;
	value<4> i_auto_24_wreduce_2e_cc_3a_513_3a_run_24_469;
	// \src: controller.v:29.34-29.48
	value<1> i_eq_24_controller_2e_v_3a_29_24_44__Y;
	// \src: controller.v:16.8-16.66
	value<1> i_logic__or_24_controller_2e_v_3a_16_24_28__Y;
	// \src: controller.v:17.13-17.27
	value<1> i_logic__or_24_controller_2e_v_3a_17_24_31__Y;
	// \src: controller.v:28.12-28.61
	value<1> i_logic__or_24_controller_2e_v_3a_28_24_41__Y;
	// \src: controller.v:23.12-23.21
	value<1> i_lt_24_controller_2e_v_3a_23_24_37__Y;
	// \src: controller.v:21.12-21.21
	value<1> i_ne_24_controller_2e_v_3a_21_24_34__Y;
	// \src: controller.v:26.7-26.18
	value<1> i_ne_24_controller_2e_v_3a_26_24_38__Y;
	value<1> i_procmux_24_340__Y;
	// cells $eq$controller.v:29$44 $sub$controller.v:29$43
	i_eq_24_controller_2e_v_3a_29_24_44__Y = eq_uu<1>(p_phase.curr, sub_uu<32>(p_heldd.curr, value<1>{0x1u}));
	// cells $logic_or$controller.v:28$41 $eq$controller.v:28$39 $eq$controller.v:28$40
	i_logic__or_24_controller_2e_v_3a_28_24_41__Y = logic_or<1>(eq_uu<1>(p_timer.curr, value<64>{0xffffffffu,0xffffffffu}), eq_uu<1>(p_pulses.curr, value<32>{0xffffffffu}));
	// \src: controller.v:31.48-31.57
	// cell $lt$controller.v:31$48
	i_lt_24_controller_2e_v_3a_23_24_37__Y = lt_uu<1>(p_settled.curr, value<2>{0x2u});
	// \src: controller.v:31.7-31.18
	// cell $ne$controller.v:31$47
	i_ne_24_controller_2e_v_3a_26_24_38__Y = ne_uu<1>(p_cfgd, p_heldd.curr);
	// \src: controller.v:21.12-21.21
	// cell $ne$controller.v:21$34
	i_ne_24_controller_2e_v_3a_21_24_34__Y = reduce_bool<1>(p_reason.curr);
	// cells $logic_or$controller.v:17$31 $lt$controller.v:17$29 $mul$controller.v:4$10 $mul$controller.v:5$11 $lt$controller.v:17$30 $mul$controller.v:6$12 $mul$controller.v:7$13
	i_logic__or_24_controller_2e_v_3a_17_24_31__Y = logic_or<1>(lt_uu<1>(mul_uu<64>(p_gnum, p_previousd.curr), mul_uu<64>(p_gden, p_cfgd)), lt_uu<1>(mul_uu<64>(p_gnum, p_cfgd), mul_uu<64>(p_gden, p_previousd.curr)));
	// \src: controller.v:17.13-17.27|controller.v:17.10-17.36
	// cell $procmux$304
	i_auto_24_wreduce_2e_cc_3a_513_3a_run_24_467.slice<1,0>() = (i_logic__or_24_controller_2e_v_3a_17_24_31__Y ? value<2>{0x3u} : value<2>{0u});
	// cells $logic_or$controller.v:16$28 $logic_or$controller.v:16$26 $logic_or$controller.v:16$24 $logic_or$controller.v:16$22 $logic_or$controller.v:16$20 $eq$controller.v:16$18 $gt$controller.v:16$19 $eq$controller.v:16$21 $gt$controller.v:16$23 $eq$controller.v:16$25 $gt$controller.v:16$27
	i_logic__or_24_controller_2e_v_3a_16_24_28__Y = logic_or<1>(logic_or<1>(logic_or<1>(logic_or<1>(logic_or<1>(logic_not<1>(p_cfgd), gt_uu<1>(p_cfgd, value<11>{0x7d0u})), logic_not<1>(p_gnum)), gt_uu<1>(p_gnum, value<10>{0x3e8u})), logic_not<1>(p_gden)), gt_uu<1>(p_gden, value<10>{0x3e8u}));
	// connection
	i_auto_24_wreduce_2e_cc_3a_513_3a_run_24_467.slice<3,2>() = value<2>{0u};
	// \full_case: 1
	// \src: controller.v:16.8-16.66|controller.v:16.5-17.36
	// cell $procmux$307
	i_auto_24_wreduce_2e_cc_3a_513_3a_run_24_468.slice<2,0>() = (i_logic__or_24_controller_2e_v_3a_16_24_28__Y ? value<3>{0x6u} : value<1>{0u}.concat(i_auto_24_wreduce_2e_cc_3a_513_3a_run_24_467.slice<1,0>()).val());
	// connection
	i_auto_24_wreduce_2e_cc_3a_513_3a_run_24_468.slice<3>() = value<1>{0u};
	// cells $procmux$378 $procmux$375 $procmux$372 $procmux$369
	i_procmux_24_340__Y = (p_busy.curr ? value<1>{0u} : (i_ne_24_controller_2e_v_3a_21_24_34__Y ? value<1>{0u} : (p_licensed.curr ? (i_lt_24_controller_2e_v_3a_23_24_37__Y ? value<1>{0u} : value<1>{0x1u}) : value<1>{0u})));
	// \full_case: 1
	// \src: controller.v:13.7-13.11|controller.v:13.4-18.7
	// cell $procmux$310
	i_auto_24_wreduce_2e_cc_3a_513_3a_run_24_469.slice<2,0>() = (p_busy.curr ? value<3>{0x5u} : i_auto_24_wreduce_2e_cc_3a_513_3a_run_24_468.slice<2,0>().val());
	// connection
	i_auto_24_wreduce_2e_cc_3a_513_3a_run_24_469.slice<3>() = value<1>{0u};
	// cells $procdff$465 $procmux$130 $procmux$127 $procmux$119 $procmux$108 $procmux$106 $procmux$103 $procmux$100 $procmux$97
	if (posedge_p_clk) {
		p_pulse.next = (p_rst ? value<1>{0u} : (p_commandreset ? value<1>{0u} : (p_start ? value<1>{0u} : (p_busy.curr ? (i_ne_24_controller_2e_v_3a_26_24_38__Y ? value<1>{0u} : (p_stop ? value<1>{0u} : (i_logic__or_24_controller_2e_v_3a_28_24_41__Y ? value<1>{0u} : (i_eq_24_controller_2e_v_3a_29_24_44__Y ? value<1>{0x1u} : value<1>{0u})))) : value<1>{0u}))));
	}
	// cells $procdff$464 $procmux$166 $procmux$163 $procmux$157 $procmux$142 $procmux$140 $procmux$137 $procmux$134 $add$controller.v:29$42 $procmux$155 $procmux$152 $procmux$149 $procmux$146 $procmux$161
	if (posedge_p_clk) {
		p_timer.next = (p_rst ? value<64>{0u,0u} : (p_commandreset ? (p_busy.curr ? p_timer.curr : value<64>{0u,0u}) : (p_start ? (p_busy.curr ? p_timer.curr : (i_ne_24_controller_2e_v_3a_21_24_34__Y ? p_timer.curr : (p_licensed.curr ? (i_lt_24_controller_2e_v_3a_23_24_37__Y ? p_timer.curr : value<64>{0u,0u}) : p_timer.curr))) : (p_busy.curr ? (i_ne_24_controller_2e_v_3a_26_24_38__Y ? p_timer.curr : (p_stop ? p_timer.curr : (i_logic__or_24_controller_2e_v_3a_28_24_41__Y ? p_timer.curr : add_uu<64>(p_timer.curr, value<1>{0x1u})))) : p_timer.curr))));
	}
	// cells $procdff$463 $procmux$205 $procmux$202 $procmux$196 $procmux$181 $procmux$179 $procmux$176 $procmux$173 $procmux$170 $add$controller.v:29$45 $procmux$194 $procmux$191 $procmux$188 $procmux$185 $procmux$200
	if (posedge_p_clk) {
		p_pulses.next = (p_rst ? value<32>{0u} : (p_commandreset ? (p_busy.curr ? p_pulses.curr : value<32>{0u}) : (p_start ? (p_busy.curr ? p_pulses.curr : (i_ne_24_controller_2e_v_3a_21_24_34__Y ? p_pulses.curr : (p_licensed.curr ? (i_lt_24_controller_2e_v_3a_23_24_37__Y ? p_pulses.curr : value<32>{0u}) : p_pulses.curr))) : (p_busy.curr ? (i_ne_24_controller_2e_v_3a_26_24_38__Y ? p_pulses.curr : (p_stop ? p_pulses.curr : (i_logic__or_24_controller_2e_v_3a_28_24_41__Y ? p_pulses.curr : (i_eq_24_controller_2e_v_3a_29_24_44__Y ? add_uu<32>(p_pulses.curr, value<1>{0x1u}) : p_pulses.curr)))) : p_pulses.curr))));
	}
	// cells $procdff$462 $procmux$244 $procmux$241 $procmux$235 $procmux$220 $procmux$218 $procmux$215 $procmux$212 $procmux$209 $add$controller.v:29$46 $procmux$233 $procmux$230 $procmux$227 $procmux$224 $procmux$239
	if (posedge_p_clk) {
		p_phase.next = (p_rst ? value<32>{0u} : (p_commandreset ? (p_busy.curr ? p_phase.curr : value<32>{0u}) : (p_start ? (p_busy.curr ? p_phase.curr : (i_ne_24_controller_2e_v_3a_21_24_34__Y ? p_phase.curr : (p_licensed.curr ? (i_lt_24_controller_2e_v_3a_23_24_37__Y ? p_phase.curr : value<32>{0u}) : p_phase.curr))) : (p_busy.curr ? (i_ne_24_controller_2e_v_3a_26_24_38__Y ? p_phase.curr : (p_stop ? p_phase.curr : (i_logic__or_24_controller_2e_v_3a_28_24_41__Y ? p_phase.curr : (i_eq_24_controller_2e_v_3a_29_24_44__Y ? value<32>{0u} : add_uu<32>(p_phase.curr, value<1>{0x1u}))))) : p_phase.curr))));
	}
	// cells $procdff$461 $procmux$265 $procmux$262 $procmux$259 $procmux$257 $procmux$254 $procmux$251 $procmux$248
	if (posedge_p_clk) {
		p_previousd.next = (p_rst ? value<32>{0x3e8u} : (p_commandreset ? p_previousd.curr : (p_start ? (p_busy.curr ? p_previousd.curr : (i_ne_24_controller_2e_v_3a_21_24_34__Y ? p_previousd.curr : (p_licensed.curr ? (i_lt_24_controller_2e_v_3a_23_24_37__Y ? p_previousd.curr : p_heldd.curr) : p_previousd.curr))) : p_previousd.curr)));
	}
	// cells $procdff$460 $procmux$274 $procmux$271 $procmux$269
	if (posedge_p_clk) {
		p_heldd.next = (p_rst ? value<32>{0u} : (p_commandreset ? (p_busy.curr ? p_heldd.curr : p_cfgd) : p_heldd.curr));
	}
	// cells $procdff$459 $procmux$315 $procmux$312 $procmux$301 $procmux$286 $procmux$284 $procmux$281 $procmux$278 $procmux$299 $procmux$296 $procmux$293 $procmux$290
	if (posedge_p_clk) {
		p_reason.next = (p_rst ? value<4>{0u} : (p_commandreset ? value<1>{0u}.concat(i_auto_24_wreduce_2e_cc_3a_513_3a_run_24_469.slice<2,0>()).val() : (p_start ? (p_busy.curr ? value<4>{0x8u} : (i_ne_24_controller_2e_v_3a_21_24_34__Y ? p_reason.curr : (p_licensed.curr ? (i_lt_24_controller_2e_v_3a_23_24_37__Y ? value<4>{0x2u} : p_reason.curr) : value<4>{0x1u}))) : (p_busy.curr ? (i_ne_24_controller_2e_v_3a_26_24_38__Y ? value<4>{0x4u} : (p_stop ? p_reason.curr : (i_logic__or_24_controller_2e_v_3a_28_24_41__Y ? value<4>{0x7u} : p_reason.curr))) : p_reason.curr))));
	}
	// cells $procdff$458 $procmux$353 $procmux$350 $procmux$342 $procmux$327 $procmux$325 $procmux$322 $procmux$319
	if (posedge_p_clk) {
		p_valid.next = (p_rst ? value<1>{0u} : (p_commandreset ? value<1>{0u} : (p_start ? i_procmux_24_340__Y : (p_busy.curr ? (i_ne_24_controller_2e_v_3a_26_24_38__Y ? value<1>{0u} : (p_stop ? p_valid.curr : (i_logic__or_24_controller_2e_v_3a_28_24_41__Y ? value<1>{0u} : p_valid.curr))) : p_valid.curr))));
	}
	// cells $procdff$457 $procmux$394 $procmux$391 $procmux$380 $procmux$365 $procmux$363 $procmux$360 $procmux$357
	if (posedge_p_clk) {
		p_busy.next = (p_rst ? value<1>{0u} : (p_commandreset ? value<1>{0u} : (p_start ? i_procmux_24_340__Y : (p_busy.curr ? (i_ne_24_controller_2e_v_3a_26_24_38__Y ? value<1>{0u} : (p_stop ? value<1>{0u} : (i_logic__or_24_controller_2e_v_3a_28_24_41__Y ? value<1>{0u} : value<1>{0x1u}))) : value<1>{0u}))));
	}
	// cells $procdff$456 $procmux$416 $procmux$413 $procmux$407 $procmux$404 $procmux$401 $procmux$399 $procmux$396 $add$controller.v:31$49 $procmux$411
	if (posedge_p_clk) {
		p_settled.next = (p_rst ? value<2>{0u} : (p_commandreset ? (p_busy.curr ? p_settled.curr : value<2>{0u}) : (p_start ? p_settled.curr : (p_busy.curr ? p_settled.curr : (p_licensed.curr ? (i_ne_24_controller_2e_v_3a_26_24_38__Y ? value<2>{0u} : (i_lt_24_controller_2e_v_3a_23_24_37__Y ? add_uu<2>(p_settled.curr, value<1>{0x1u}) : p_settled.curr)) : p_settled.curr)))));
	}
	// cells $procdff$455 $procmux$453 $procmux$450 $procmux$439 $procmux$428 $procmux$426 $procmux$423 $procmux$420 $procmux$448 $procmux$445 $procmux$442
	if (posedge_p_clk) {
		p_licensed.next = (p_rst ? value<1>{0u} : (p_commandreset ? (p_busy.curr ? value<1>{0u} : (i_logic__or_24_controller_2e_v_3a_16_24_28__Y ? value<1>{0u} : (i_logic__or_24_controller_2e_v_3a_17_24_31__Y ? value<1>{0u} : value<1>{0x1u}))) : (p_start ? value<1>{0u} : (p_busy.curr ? (i_ne_24_controller_2e_v_3a_26_24_38__Y ? value<1>{0u} : (p_stop ? p_licensed.curr : (i_logic__or_24_controller_2e_v_3a_28_24_41__Y ? value<1>{0u} : p_licensed.curr))) : p_licensed.curr))));
	}
	return converged;
}

void p_controller::debug_eval() {
	// \src: controller.v:7.17-7.47
	// cell $mul$controller.v:7$13
	p_dg2 = mul_uu<64>(p_gden, p_previousd.curr);
	// \src: controller.v:6.17-6.42
	// cell $mul$controller.v:6$12
	p_gd2 = mul_uu<64>(p_gnum, p_cfgd);
	// \src: controller.v:5.16-5.41
	// cell $mul$controller.v:5$11
	p_dg = mul_uu<64>(p_gden, p_cfgd);
	// \src: controller.v:4.16-4.46
	// cell $mul$controller.v:4$10
	p_gd = mul_uu<64>(p_gnum, p_previousd.curr);
}

CXXRTL_EXTREMELY_COLD
void p_controller::debug_info(debug_items *items, debug_scopes *scopes, std::string path, metadata_map &&cell_attrs) {
	assert(path.empty() || path[path.size() - 1] == ' ');
	if (scopes) {
		scopes->add(path.empty() ? path : path.substr(0, path.size() - 1), "controller", metadata_map({
			{ "top", UINT64_C(1) },
			{ "src", "controller.v:1.1-34.10" },
		}), std::move(cell_attrs));
	}
	if (items) {
		items->add(path, "busy", "src\000scontroller.v:2.57-2.61\000", p_busy, 0, debug_item::OUTPUT|debug_item::DRIVEN_SYNC);
		items->add(path, "cfgd", "src\000scontroller.v:1.69-1.73\000", p_cfgd, 0, debug_item::INPUT|debug_item::UNDRIVEN);
		items->add(path, "clk", "src\000scontroller.v:1.25-1.28\000", p_clk, 0, debug_item::INPUT|debug_item::UNDRIVEN);
		items->add(path, "commandreset", "src\000scontroller.v:1.33-1.45\000", p_commandreset, 0, debug_item::INPUT|debug_item::UNDRIVEN);
		items->add(path, "dg", "src\000scontroller.v:5.13-5.15\000", debug_eval_outline, p_dg);
		items->add(path, "dg2", "src\000scontroller.v:7.13-7.16\000", debug_eval_outline, p_dg2);
		items->add(path, "gd", "src\000scontroller.v:4.13-4.15\000", debug_eval_outline, p_gd);
		items->add(path, "gd2", "src\000scontroller.v:6.13-6.16\000", debug_eval_outline, p_gd2);
		items->add(path, "gden", "src\000scontroller.v:1.79-1.83\000", p_gden, 0, debug_item::INPUT|debug_item::UNDRIVEN);
		items->add(path, "gnum", "src\000scontroller.v:1.74-1.78\000", p_gnum, 0, debug_item::INPUT|debug_item::UNDRIVEN);
		items->add(path, "heldd", "src\000scontroller.v:3.19-3.24\000", p_heldd, 0, debug_item::OUTPUT|debug_item::DRIVEN_SYNC);
		items->add(path, "licensed", "src\000scontroller.v:2.13-2.21\000", p_licensed, 0, debug_item::OUTPUT|debug_item::DRIVEN_SYNC);
		items->add(path, "phase", "src\000scontroller.v:3.35-3.40\000", p_phase, 0, debug_item::OUTPUT|debug_item::DRIVEN_SYNC);
		items->add(path, "previousd", "src\000scontroller.v:3.25-3.34\000", p_previousd, 0, debug_item::OUTPUT|debug_item::DRIVEN_SYNC);
		items->add(path, "pulse", "src\000scontroller.v:3.82-3.87\000", p_pulse, 0, debug_item::OUTPUT|debug_item::DRIVEN_SYNC);
		items->add(path, "pulses", "src\000scontroller.v:3.41-3.47\000", p_pulses, 0, debug_item::OUTPUT|debug_item::DRIVEN_SYNC);
		items->add(path, "reason", "src\000scontroller.v:2.84-2.90\000", p_reason, 0, debug_item::OUTPUT|debug_item::DRIVEN_SYNC);
		items->add(path, "rst", "src\000scontroller.v:1.29-1.32\000", p_rst, 0, debug_item::INPUT|debug_item::UNDRIVEN);
		items->add(path, "settled", "src\000scontroller.v:2.38-2.45\000", p_settled, 0, debug_item::OUTPUT|debug_item::DRIVEN_SYNC);
		items->add(path, "start", "src\000scontroller.v:1.46-1.51\000", p_start, 0, debug_item::INPUT|debug_item::UNDRIVEN);
		items->add(path, "stop", "src\000scontroller.v:1.52-1.56\000", p_stop, 0, debug_item::INPUT|debug_item::UNDRIVEN);
		items->add(path, "timer", "src\000scontroller.v:3.65-3.70\000", p_timer, 0, debug_item::OUTPUT|debug_item::DRIVEN_SYNC);
		items->add(path, "valid", "src\000scontroller.v:2.62-2.67\000", p_valid, 0, debug_item::OUTPUT|debug_item::DRIVEN_SYNC);
	}
}

} // namespace cxxrtl_design

extern "C"
cxxrtl_toplevel cxxrtl_design_create() {
	return new _cxxrtl_toplevel { std::unique_ptr<cxxrtl_design::p_controller>(new cxxrtl_design::p_controller) };
}
