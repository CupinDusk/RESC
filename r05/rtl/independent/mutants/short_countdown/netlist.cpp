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
// \src: reference.v:3.1-67.10
struct p_reference__job : public module {
	// \src: reference.v:7.14-7.18
	/*output*/ wire<1> p_busy;
	// \src: reference.v:5.45-5.49
	/*input*/ value<32> p_cfgd;
	// \src: reference.v:5.21-5.25
	/*input*/ value<32> p_cfgn;
	// \src: reference.v:4.14-4.17
	/*input*/ value<1> p_clk;
	value<1> prev_p_clk;
	bool posedge_p_clk() const {
		return !prev_p_clk.slice<0>().val() && p_clk.slice<0>().val();
	}
	// \src: reference.v:4.46-4.58
	/*input*/ value<1> p_commandreset;
	// \src: reference.v:7.31-7.35
	/*output*/ wire<1> p_done;
	// \src: reference.v:9.49-9.54
	/*output*/ wire<32> p_heldd;
	// \src: reference.v:12.39-12.47
	/*output*/ wire<1> p_jobpulse;
	// \src: reference.v:6.14-6.22
	/*output*/ wire<1> p_licensed;
	// \src: reference.v:9.21-9.29
	/*output*/ wire<32> p_nlatched;
	// \src: reference.v:11.21-11.26
	/*output*/ wire<32> p_phase;
	// \src: reference.v:10.21-10.30
	/*output*/ wire<32> p_previousd;
	// \src: reference.v:11.46-11.52
	/*output*/ wire<32> p_pulses;
	// \src: reference.v:8.20-8.26
	/*output*/ wire<4> p_reason;
	// \src: reference.v:10.50-10.59
	/*output*/ wire<32> p_remaining;
	// \src: reference.v:4.30-4.33
	/*input*/ value<1> p_rst;
	// \src: reference.v:6.41-6.48
	/*output*/ wire<2> p_settled;
	// \src: reference.v:4.71-4.76
	/*input*/ value<1> p_start;
	// \src: reference.v:12.21-12.26
	/*output*/ wire<64> p_timer;
	// \src: reference.v:7.48-7.53
	/*output*/ wire<1> p_valid;
	// \src: reference.v:14.15-14.17
	/*outline*/ value<40> p_dx;
	// \src: reference.v:16.8-16.15
	/*outline*/ value<1> p_guardok;
	// \src: reference.v:15.15-15.17
	/*outline*/ value<40> p_px;
	p_reference__job(interior) {}
	p_reference__job() {
		reset();
	};

	void reset() override;

	bool eval(performer *performer = nullptr) override;

	template<class ObserverT>
	bool commit(ObserverT &observer) {
		bool changed = false;
		if (p_busy.commit(observer)) changed = true;
		prev_p_clk = p_clk;
		if (p_done.commit(observer)) changed = true;
		if (p_heldd.commit(observer)) changed = true;
		if (p_jobpulse.commit(observer)) changed = true;
		if (p_licensed.commit(observer)) changed = true;
		if (p_nlatched.commit(observer)) changed = true;
		if (p_phase.commit(observer)) changed = true;
		if (p_previousd.commit(observer)) changed = true;
		if (p_pulses.commit(observer)) changed = true;
		if (p_reason.commit(observer)) changed = true;
		if (p_remaining.commit(observer)) changed = true;
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
	debug_outline debug_eval_outline { std::bind(&p_reference__job::debug_eval, this) };

	void debug_info(debug_items *items, debug_scopes *scopes, std::string path, metadata_map &&cell_attrs = {}) override;
}; // struct p_reference__job

void p_reference__job::reset() {
}

bool p_reference__job::eval(performer *performer) {
	bool converged = true;
	bool posedge_p_clk = this->posedge_p_clk();
	value<4> i_auto_24_wreduce_2e_cc_3a_513_3a_run_24_438;
	value<4> i_auto_24_wreduce_2e_cc_3a_513_3a_run_24_439;
	value<4> i_auto_24_wreduce_2e_cc_3a_513_3a_run_24_440;
	value<4> i_auto_24_wreduce_2e_cc_3a_513_3a_run_24_441;
	value<4> i_auto_24_wreduce_2e_cc_3a_513_3a_run_24_443;
	// \src: reference.v:44.15-44.37
	value<1> i_eq_24_reference_2e_v_3a_44_24_15__Y;
	// \src: reference.v:47.17-47.35
	value<1> i_eq_24_reference_2e_v_3a_47_24_18__Y;
	// \src: reference.v:40.22-40.77
	value<1> i_logic__or_24_reference_2e_v_3a_40_24_12__Y;
	// \src: reference.v:53.18-53.47
	value<1> i_logic__or_24_reference_2e_v_3a_53_24_23__Y;
	// \src: reference.v:54.18-54.45
	value<1> i_logic__or_24_reference_2e_v_3a_54_24_26__Y;
	// \src: reference.v:36.13-36.26
	value<1> i_ne_24_reference_2e_v_3a_36_24_9__Y;
	value<1> i_procmux_24_295__Y;
	// \src: reference.v:16.8-16.15
	value<1> p_guardok;
	// cells $logic_and$reference.v:16$7 $le$reference.v:16$3 $mul$reference.v:16$1 $mul$reference.v:16$2 $le$reference.v:17$6 $mul$reference.v:17$4 $mul$reference.v:17$5
	p_guardok = logic_and<1>(le_uu<1>(mul_uu<40>(p_cfgd, value<8>{0xc8u}), mul_uu<40>(p_previousd.curr, value<8>{0xc9u})), le_uu<1>(mul_uu<40>(p_previousd.curr, value<8>{0xc8u}), mul_uu<40>(p_cfgd, value<8>{0xc9u})));
	// \src: reference.v:47.17-47.35
	// cell $eq$reference.v:47$18
	i_eq_24_reference_2e_v_3a_47_24_18__Y = eq_uu<1>(p_remaining.curr, value<1>{0x1u});
	// cells $eq$reference.v:44$15 $sub$reference.v:44$14
	i_eq_24_reference_2e_v_3a_44_24_15__Y = eq_uu<1>(p_phase.curr, sub_uu<32>(p_heldd.curr, value<1>{0x1u}));
	// cells $logic_or$reference.v:54$26 $eq$reference.v:54$24 $eq$reference.v:54$25
	i_logic__or_24_reference_2e_v_3a_54_24_26__Y = logic_or<1>(logic_not<1>(p_nlatched.curr), logic_not<1>(p_heldd.curr));
	// \src: reference.v:62.13-62.26
	// cell $ne$reference.v:62$29
	i_ne_24_reference_2e_v_3a_36_24_9__Y = ne_uu<1>(p_cfgd, p_heldd.curr);
	// \full_case: 1
	// \src: reference.v:55.18-55.26|reference.v:55.14-60.12
	// cell $procmux$250
	i_auto_24_wreduce_2e_cc_3a_513_3a_run_24_438.slice<1,0>() = (p_guardok ? value<2>{0u} : value<2>{0x3u});
	// connection
	i_auto_24_wreduce_2e_cc_3a_513_3a_run_24_438.slice<3,2>() = value<2>{0u};
	// cells $logic_or$reference.v:40$12 $eq$reference.v:40$10 $eq$reference.v:40$11
	i_logic__or_24_reference_2e_v_3a_40_24_12__Y = logic_or<1>(eq_uu<1>(p_timer.curr, value<64>{0xffffffffu,0xffffffffu}), eq_uu<1>(p_pulses.curr, value<32>{0xffffffffu}));
	// cells $logic_or$reference.v:53$23 $ne$reference.v:53$21
	i_logic__or_24_reference_2e_v_3a_53_24_23__Y = logic_or<1>(ne_uu<1>(p_settled.curr, value<2>{0x2u}), i_ne_24_reference_2e_v_3a_36_24_9__Y);
	// \full_case: 1
	// \src: reference.v:54.18-54.45|reference.v:54.14-60.12
	// cell $procmux$253
	i_auto_24_wreduce_2e_cc_3a_513_3a_run_24_439.slice<2,0>() = (i_logic__or_24_reference_2e_v_3a_54_24_26__Y ? value<3>{0x6u} : value<1>{0u}.concat(i_auto_24_wreduce_2e_cc_3a_513_3a_run_24_438.slice<1,0>()).val());
	// connection
	i_auto_24_wreduce_2e_cc_3a_513_3a_run_24_439.slice<3>() = value<1>{0u};
	// \full_case: 1
	// \src: reference.v:53.18-53.47|reference.v:53.14-60.12
	// cell $procmux$256
	i_auto_24_wreduce_2e_cc_3a_513_3a_run_24_441.slice<2,0>() = (i_logic__or_24_reference_2e_v_3a_53_24_23__Y ? value<3>{0x2u} : i_auto_24_wreduce_2e_cc_3a_513_3a_run_24_439.slice<2,0>().val());
	// connection
	i_auto_24_wreduce_2e_cc_3a_513_3a_run_24_441.slice<3>() = value<1>{0u};
	// \full_case: 1
	// \src: reference.v:52.13-52.22|reference.v:52.9-60.12
	// cell $procmux$259
	i_auto_24_wreduce_2e_cc_3a_513_3a_run_24_440.slice<2,0>() = (p_licensed.curr ? i_auto_24_wreduce_2e_cc_3a_513_3a_run_24_441.slice<2,0>().val() : value<3>{0x1u});
	// connection
	i_auto_24_wreduce_2e_cc_3a_513_3a_run_24_440.slice<3>() = value<1>{0u};
	// cells $procmux$358 $procmux$355 $procmux$352 $procmux$349
	i_procmux_24_295__Y = (p_licensed.curr ? (i_logic__or_24_reference_2e_v_3a_53_24_23__Y ? value<1>{0u} : (i_logic__or_24_reference_2e_v_3a_54_24_26__Y ? value<1>{0u} : (p_guardok ? value<1>{0x1u} : value<1>{0u}))) : value<1>{0u});
	// \full_case: 1
	// \src: reference.v:27.13-27.17|reference.v:27.9-34.12
	// cell $procmux$277
	i_auto_24_wreduce_2e_cc_3a_513_3a_run_24_443.slice<2,0>() = (p_busy.curr ? value<3>{0x5u} : value<3>{0u});
	// connection
	i_auto_24_wreduce_2e_cc_3a_513_3a_run_24_443.slice<3>() = value<1>{0u};
	// cells $procdff$437 $procmux$51 $procmux$48 $procmux$45 $procmux$43 $procmux$40 $procmux$37 $procmux$34
	if (posedge_p_clk) {
		p_jobpulse.next = (p_rst ? value<1>{0u} : (p_commandreset ? value<1>{0u} : (p_busy.curr ? (i_ne_24_reference_2e_v_3a_36_24_9__Y ? value<1>{0u} : (p_start ? value<1>{0u} : (i_logic__or_24_reference_2e_v_3a_40_24_12__Y ? value<1>{0u} : (i_eq_24_reference_2e_v_3a_44_24_15__Y ? value<1>{0x1u} : value<1>{0u})))) : value<1>{0u})));
	}
	// cells $procdff$436 $procmux$87 $procmux$84 $procmux$78 $procmux$66 $procmux$64 $procmux$61 $procmux$58 $procmux$55 $procmux$76 $procmux$73 $procmux$70 $add$reference.v:43$13 $procmux$82
	if (posedge_p_clk) {
		p_timer.next = (p_rst ? value<64>{0u,0u} : (p_commandreset ? (p_busy.curr ? p_timer.curr : value<64>{0u,0u}) : (p_busy.curr ? (i_ne_24_reference_2e_v_3a_36_24_9__Y ? p_timer.curr : (p_start ? p_timer.curr : (i_logic__or_24_reference_2e_v_3a_40_24_12__Y ? p_timer.curr : add_uu<64>(p_timer.curr, value<1>{0x1u})))) : (p_start ? (p_licensed.curr ? (i_logic__or_24_reference_2e_v_3a_53_24_23__Y ? p_timer.curr : (i_logic__or_24_reference_2e_v_3a_54_24_26__Y ? p_timer.curr : (p_guardok ? value<64>{0u,0u} : p_timer.curr))) : p_timer.curr) : p_timer.curr))));
	}
	// cells $procdff$435 $procmux$126 $procmux$123 $procmux$117 $procmux$102 $procmux$100 $procmux$97 $procmux$94 $procmux$91 $procmux$115 $procmux$112 $procmux$109 $procmux$106 $add$reference.v:45$16 $procmux$121
	if (posedge_p_clk) {
		p_pulses.next = (p_rst ? value<32>{0u} : (p_commandreset ? (p_busy.curr ? p_pulses.curr : value<32>{0u}) : (p_busy.curr ? (i_ne_24_reference_2e_v_3a_36_24_9__Y ? p_pulses.curr : (p_start ? p_pulses.curr : (i_logic__or_24_reference_2e_v_3a_40_24_12__Y ? p_pulses.curr : (i_eq_24_reference_2e_v_3a_44_24_15__Y ? add_uu<32>(p_pulses.curr, value<1>{0x1u}) : p_pulses.curr)))) : (p_start ? (p_licensed.curr ? (i_logic__or_24_reference_2e_v_3a_53_24_23__Y ? p_pulses.curr : (i_logic__or_24_reference_2e_v_3a_54_24_26__Y ? p_pulses.curr : (p_guardok ? value<32>{0u} : p_pulses.curr))) : p_pulses.curr) : p_pulses.curr))));
	}
	// cells $procdff$434 $procmux$165 $procmux$162 $procmux$156 $procmux$141 $procmux$139 $procmux$136 $procmux$133 $procmux$130 $procmux$154 $procmux$151 $procmux$148 $procmux$145 $add$reference.v:48$19 $procmux$160
	if (posedge_p_clk) {
		p_phase.next = (p_rst ? value<32>{0u} : (p_commandreset ? (p_busy.curr ? p_phase.curr : value<32>{0u}) : (p_busy.curr ? (i_ne_24_reference_2e_v_3a_36_24_9__Y ? p_phase.curr : (p_start ? p_phase.curr : (i_logic__or_24_reference_2e_v_3a_40_24_12__Y ? p_phase.curr : (i_eq_24_reference_2e_v_3a_44_24_15__Y ? value<32>{0u} : add_uu<32>(p_phase.curr, value<1>{0x1u}))))) : (p_start ? (p_licensed.curr ? (i_logic__or_24_reference_2e_v_3a_53_24_23__Y ? p_phase.curr : (i_logic__or_24_reference_2e_v_3a_54_24_26__Y ? p_phase.curr : (p_guardok ? value<32>{0u} : p_phase.curr))) : p_phase.curr) : p_phase.curr))));
	}
	// cells $procdff$433 $procmux$204 $procmux$201 $procmux$195 $procmux$180 $procmux$178 $procmux$175 $procmux$172 $procmux$169 $sub$reference.v:58$28 $procmux$193 $procmux$190 $procmux$187 $procmux$184 $sub$reference.v:46$17 $procmux$199
	if (posedge_p_clk) {
		p_remaining.next = (p_rst ? value<32>{0u} : (p_commandreset ? (p_busy.curr ? p_remaining.curr : value<32>{0u}) : (p_busy.curr ? (i_ne_24_reference_2e_v_3a_36_24_9__Y ? p_remaining.curr : (p_start ? p_remaining.curr : (i_logic__or_24_reference_2e_v_3a_40_24_12__Y ? p_remaining.curr : (i_eq_24_reference_2e_v_3a_44_24_15__Y ? sub_uu<32>(p_remaining.curr, value<1>{0x1u}) : p_remaining.curr)))) : (p_start ? (p_licensed.curr ? (i_logic__or_24_reference_2e_v_3a_53_24_23__Y ? p_remaining.curr : (i_logic__or_24_reference_2e_v_3a_54_24_26__Y ? p_remaining.curr : (p_guardok ? sub_uu<32>(p_nlatched.curr, value<1>{0x1u}) : p_remaining.curr))) : p_remaining.curr) : p_remaining.curr))));
	}
	// cells $procdff$432 $procmux$228 $procmux$225 $procmux$222 $procmux$219 $procmux$217 $procmux$214 $procmux$211 $procmux$208
	if (posedge_p_clk) {
		p_previousd.next = (p_rst ? value<32>{0x3e8u} : (p_commandreset ? p_previousd.curr : (p_busy.curr ? p_previousd.curr : (p_start ? (p_licensed.curr ? (i_logic__or_24_reference_2e_v_3a_53_24_23__Y ? p_previousd.curr : (i_logic__or_24_reference_2e_v_3a_54_24_26__Y ? p_previousd.curr : (p_guardok ? p_heldd.curr : p_previousd.curr))) : p_previousd.curr) : p_previousd.curr))));
	}
	// cells $procdff$431 $procmux$237 $procmux$234 $procmux$232
	if (posedge_p_clk) {
		p_heldd.next = (p_rst ? value<32>{0u} : (p_commandreset ? (p_busy.curr ? p_heldd.curr : p_cfgd) : p_heldd.curr));
	}
	// cells $procdff$430 $procmux$246 $procmux$243 $procmux$241
	if (posedge_p_clk) {
		p_nlatched.next = (p_rst ? value<32>{0u} : (p_commandreset ? (p_busy.curr ? p_nlatched.curr : p_cfgn) : p_nlatched.curr));
	}
	// cells $procdff$429 $procmux$282 $procmux$279 $procmux$273 $procmux$261 $procmux$271 $procmux$268 $procmux$265
	if (posedge_p_clk) {
		p_reason.next = (p_rst ? value<4>{0u} : (p_commandreset ? value<1>{0u}.concat(i_auto_24_wreduce_2e_cc_3a_513_3a_run_24_443.slice<2,0>()).val() : (p_busy.curr ? (i_ne_24_reference_2e_v_3a_36_24_9__Y ? value<4>{0x4u} : (p_start ? value<4>{0x8u} : (i_logic__or_24_reference_2e_v_3a_40_24_12__Y ? value<4>{0x7u} : p_reason.curr))) : (p_start ? value<1>{0u}.concat(i_auto_24_wreduce_2e_cc_3a_513_3a_run_24_440.slice<2,0>()).val() : p_reason.curr))));
	}
	// cells $procdff$428 $procmux$317 $procmux$314 $procmux$309 $procmux$297 $procmux$307 $procmux$304 $procmux$301
	if (posedge_p_clk) {
		p_valid.next = (p_rst ? value<1>{0u} : (p_commandreset ? value<1>{0u} : (p_busy.curr ? (i_ne_24_reference_2e_v_3a_36_24_9__Y ? value<1>{0u} : (p_start ? value<1>{0u} : (i_logic__or_24_reference_2e_v_3a_40_24_12__Y ? value<1>{0u} : p_valid.curr))) : (p_start ? i_procmux_24_295__Y : p_valid.curr))));
	}
	// cells $procdff$427 $procmux$345 $procmux$342 $procmux$337 $procmux$320 $procmux$335 $procmux$332 $procmux$329 $procmux$326 $procmux$324
	if (posedge_p_clk) {
		p_done.next = (p_rst ? value<1>{0u} : (p_commandreset ? value<1>{0u} : (p_busy.curr ? (i_ne_24_reference_2e_v_3a_36_24_9__Y ? value<1>{0u} : (p_start ? value<1>{0u} : (i_logic__or_24_reference_2e_v_3a_40_24_12__Y ? value<1>{0u} : (i_eq_24_reference_2e_v_3a_44_24_15__Y ? (i_eq_24_reference_2e_v_3a_47_24_18__Y ? value<1>{0x1u} : p_done.curr) : p_done.curr)))) : (p_start ? value<1>{0u} : p_done.curr))));
	}
	// cells $procdff$426 $procmux$386 $procmux$383 $procmux$377 $procmux$360 $procmux$375 $procmux$372 $procmux$369 $procmux$366 $procmux$364
	if (posedge_p_clk) {
		p_busy.next = (p_rst ? value<1>{0u} : (p_commandreset ? value<1>{0u} : (p_busy.curr ? (i_ne_24_reference_2e_v_3a_36_24_9__Y ? value<1>{0u} : (p_start ? value<1>{0u} : (i_logic__or_24_reference_2e_v_3a_40_24_12__Y ? value<1>{0u} : (i_eq_24_reference_2e_v_3a_44_24_15__Y ? (i_eq_24_reference_2e_v_3a_47_24_18__Y ? value<1>{0u} : value<1>{0x1u}) : value<1>{0x1u})))) : (p_start ? i_procmux_24_295__Y : value<1>{0u}))));
	}
	// cells $procdff$425 $procmux$407 $procmux$404 $procmux$399 $procmux$396 $procmux$393 $procmux$391 $procmux$388 $add$reference.v:63$31 $lt$reference.v:63$30
	if (posedge_p_clk) {
		p_settled.next = (p_rst ? value<2>{0u} : (p_commandreset ? value<2>{0u} : (p_busy.curr ? p_settled.curr : (p_start ? p_settled.curr : (p_licensed.curr ? (i_ne_24_reference_2e_v_3a_36_24_9__Y ? value<2>{0u} : (lt_uu<1>(p_settled.curr, value<2>{0x2u}) ? add_uu<2>(p_settled.curr, value<1>{0x1u}) : p_settled.curr)) : p_settled.curr)))));
	}
	// cells $procdff$424 $procmux$422 $procmux$419 $procmux$413 $procmux$410 $procmux$417
	if (posedge_p_clk) {
		p_licensed.next = (p_rst ? value<1>{0u} : (p_commandreset ? (p_busy.curr ? value<1>{0u} : value<1>{0x1u}) : (p_busy.curr ? p_licensed.curr : (p_start ? value<1>{0u} : p_licensed.curr))));
	}
	return converged;
}

void p_reference__job::debug_eval() {
	// cells $logic_and$reference.v:16$7 $le$reference.v:16$3 $mul$reference.v:16$1 $mul$reference.v:16$2 $le$reference.v:17$6 $mul$reference.v:17$4 $mul$reference.v:17$5
	p_guardok = logic_and<1>(le_uu<1>(mul_uu<40>(p_cfgd, value<8>{0xc8u}), mul_uu<40>(p_previousd.curr, value<8>{0xc9u})), le_uu<1>(mul_uu<40>(p_previousd.curr, value<8>{0xc8u}), mul_uu<40>(p_cfgd, value<8>{0xc9u})));
	// connection
	p_dx = value<8>{0u}.concat(p_cfgd).val();
	// connection
	p_px = value<8>{0u}.concat(p_previousd.curr).val();
}

CXXRTL_EXTREMELY_COLD
void p_reference__job::debug_info(debug_items *items, debug_scopes *scopes, std::string path, metadata_map &&cell_attrs) {
	assert(path.empty() || path[path.size() - 1] == ' ');
	if (scopes) {
		scopes->add(path.empty() ? path : path.substr(0, path.size() - 1), "reference_job", metadata_map({
			{ "top", UINT64_C(1) },
			{ "src", "reference.v:3.1-67.10" },
		}), std::move(cell_attrs));
	}
	if (items) {
		items->add(path, "busy", "src\000sreference.v:7.14-7.18\000", p_busy, 0, debug_item::OUTPUT|debug_item::DRIVEN_SYNC);
		items->add(path, "cfgd", "src\000sreference.v:5.45-5.49\000", p_cfgd, 0, debug_item::INPUT|debug_item::UNDRIVEN);
		items->add(path, "cfgn", "src\000sreference.v:5.21-5.25\000", p_cfgn, 0, debug_item::INPUT|debug_item::UNDRIVEN);
		items->add(path, "clk", "src\000sreference.v:4.14-4.17\000", p_clk, 0, debug_item::INPUT|debug_item::UNDRIVEN);
		items->add(path, "commandreset", "src\000sreference.v:4.46-4.58\000", p_commandreset, 0, debug_item::INPUT|debug_item::UNDRIVEN);
		items->add(path, "done", "src\000sreference.v:7.31-7.35\000", p_done, 0, debug_item::OUTPUT|debug_item::DRIVEN_SYNC);
		items->add(path, "dx", "src\000sreference.v:14.15-14.17\000", debug_eval_outline, p_dx);
		items->add(path, "guardok", "src\000sreference.v:16.8-16.15\000", debug_eval_outline, p_guardok);
		items->add(path, "heldd", "src\000sreference.v:9.49-9.54\000", p_heldd, 0, debug_item::OUTPUT|debug_item::DRIVEN_SYNC);
		items->add(path, "jobpulse", "src\000sreference.v:12.39-12.47\000", p_jobpulse, 0, debug_item::OUTPUT|debug_item::DRIVEN_SYNC);
		items->add(path, "licensed", "src\000sreference.v:6.14-6.22\000", p_licensed, 0, debug_item::OUTPUT|debug_item::DRIVEN_SYNC);
		items->add(path, "nlatched", "src\000sreference.v:9.21-9.29\000", p_nlatched, 0, debug_item::OUTPUT|debug_item::DRIVEN_SYNC);
		items->add(path, "phase", "src\000sreference.v:11.21-11.26\000", p_phase, 0, debug_item::OUTPUT|debug_item::DRIVEN_SYNC);
		items->add(path, "previousd", "src\000sreference.v:10.21-10.30\000", p_previousd, 0, debug_item::OUTPUT|debug_item::DRIVEN_SYNC);
		items->add(path, "pulses", "src\000sreference.v:11.46-11.52\000", p_pulses, 0, debug_item::OUTPUT|debug_item::DRIVEN_SYNC);
		items->add(path, "px", "src\000sreference.v:15.15-15.17\000", debug_eval_outline, p_px);
		items->add(path, "reason", "src\000sreference.v:8.20-8.26\000", p_reason, 0, debug_item::OUTPUT|debug_item::DRIVEN_SYNC);
		items->add(path, "remaining", "src\000sreference.v:10.50-10.59\000", p_remaining, 0, debug_item::OUTPUT|debug_item::DRIVEN_SYNC);
		items->add(path, "rst", "src\000sreference.v:4.30-4.33\000", p_rst, 0, debug_item::INPUT|debug_item::UNDRIVEN);
		items->add(path, "settled", "src\000sreference.v:6.41-6.48\000", p_settled, 0, debug_item::OUTPUT|debug_item::DRIVEN_SYNC);
		items->add(path, "start", "src\000sreference.v:4.71-4.76\000", p_start, 0, debug_item::INPUT|debug_item::UNDRIVEN);
		items->add(path, "timer", "src\000sreference.v:12.21-12.26\000", p_timer, 0, debug_item::OUTPUT|debug_item::DRIVEN_SYNC);
		items->add(path, "valid", "src\000sreference.v:7.48-7.53\000", p_valid, 0, debug_item::OUTPUT|debug_item::DRIVEN_SYNC);
	}
}

} // namespace cxxrtl_design

extern "C"
cxxrtl_toplevel cxxrtl_design_create() {
	return new _cxxrtl_toplevel { std::unique_ptr<cxxrtl_design::p_reference__job>(new cxxrtl_design::p_reference__job) };
}
