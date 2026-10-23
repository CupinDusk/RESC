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
// \src: core_wrapper.v:1.1-13.10
struct p_core__wrapper : public module {
	// \hdlname: cpu trap
	// \src: upstream/picorv32.v:91.13-91.17
	wire<1> p_cpu_2e_trap;
	// \hdlname: cpu trace_valid
	// \src: upstream/picorv32.v:158.20-158.31
	wire<1> p_cpu_2e_trace__valid;
	// \hdlname: cpu trace_data
	// \src: upstream/picorv32.v:159.20-159.30
	wire<36> p_cpu_2e_trace__data;
	// \hdlname: cpu reg_sh
	// \src: upstream/picorv32.v:177.12-177.18
	wire<5> p_cpu_2e_reg__sh;
	// \hdlname: cpu reg_pc
	// \src: upstream/picorv32.v:176.13-176.19
	wire<32> p_cpu_2e_reg__pc;
	// \hdlname: cpu reg_out
	// \src: upstream/picorv32.v:176.52-176.59
	wire<32> p_cpu_2e_reg__out;
	// \hdlname: cpu reg_op2
	// \src: upstream/picorv32.v:176.43-176.50
	wire<32> p_cpu_2e_reg__op2;
	// \hdlname: cpu reg_op1
	// \src: upstream/picorv32.v:176.34-176.41
	wire<32> p_cpu_2e_reg__op1;
	// \hdlname: cpu reg_next_pc
	// \src: upstream/picorv32.v:176.21-176.32
	wire<32> p_cpu_2e_reg__next__pc;
	// \hdlname: cpu pcpi_valid
	// \src: upstream/picorv32.v:110.20-110.30
	wire<1> p_cpu_2e_pcpi__valid;
	// \hdlname: cpu pcpi_insn
	// \src: upstream/picorv32.v:111.20-111.29
	wire<32> p_cpu_2e_pcpi__insn;
	// \hdlname: cpu mem_wstrb
	// \src: upstream/picorv32.v:99.20-99.29
	wire<4> p_cpu_2e_mem__wstrb;
	// \hdlname: cpu mem_wordsize
	// \src: upstream/picorv32.v:352.12-352.24
	wire<2> p_cpu_2e_mem__wordsize;
	// \hdlname: cpu mem_wdata
	// \src: upstream/picorv32.v:98.20-98.29
	wire<32> p_cpu_2e_mem__wdata;
	// \hdlname: cpu mem_valid
	// \src: upstream/picorv32.v:93.20-93.29
	wire<1> p_cpu_2e_mem__valid;
	// \hdlname: cpu mem_state
	// \src: upstream/picorv32.v:351.12-351.21
	wire<2> p_cpu_2e_mem__state;
	// \hdlname: cpu mem_rdata_q
	// \src: upstream/picorv32.v:354.13-354.24
	wire<32> p_cpu_2e_mem__rdata__q;
	// \hdlname: cpu mem_instr
	// \src: upstream/picorv32.v:94.20-94.29
	wire<1> p_cpu_2e_mem__instr;
	// \hdlname: cpu mem_do_wdata
	// \src: upstream/picorv32.v:358.6-358.18
	wire<1> p_cpu_2e_mem__do__wdata;
	// \hdlname: cpu mem_do_rinst
	// \src: upstream/picorv32.v:356.6-356.18
	wire<1> p_cpu_2e_mem__do__rinst;
	// \hdlname: cpu mem_do_rdata
	// \src: upstream/picorv32.v:357.6-357.18
	wire<1> p_cpu_2e_mem__do__rdata;
	// \hdlname: cpu mem_do_prefetch
	// \src: upstream/picorv32.v:355.6-355.21
	wire<1> p_cpu_2e_mem__do__prefetch;
	// \hdlname: cpu mem_addr
	// \src: upstream/picorv32.v:97.20-97.28
	wire<32> p_cpu_2e_mem__addr;
	// \hdlname: cpu latched_trace
	// \src: upstream/picorv32.v:1206.6-1206.19
	wire<1> p_cpu_2e_latched__trace;
	// \hdlname: cpu latched_store
	// \src: upstream/picorv32.v:1202.6-1202.19
	wire<1> p_cpu_2e_latched__store;
	// \hdlname: cpu latched_stalu
	// \src: upstream/picorv32.v:1203.6-1203.19
	wire<1> p_cpu_2e_latched__stalu;
	// \hdlname: cpu latched_rd
	// \src: upstream/picorv32.v:1210.26-1210.36
	wire<5> p_cpu_2e_latched__rd;
	// \hdlname: cpu latched_is_lu
	// \src: upstream/picorv32.v:1207.6-1207.19
	wire<1> p_cpu_2e_latched__is__lu;
	// \hdlname: cpu latched_is_lh
	// \src: upstream/picorv32.v:1208.6-1208.19
	wire<1> p_cpu_2e_latched__is__lh;
	// \hdlname: cpu latched_is_lb
	// \src: upstream/picorv32.v:1209.6-1209.19
	wire<1> p_cpu_2e_latched__is__lb;
	// \hdlname: cpu latched_compr
	// \src: upstream/picorv32.v:1205.6-1205.19
	wire<1> p_cpu_2e_latched__compr;
	// \hdlname: cpu latched_branch
	// \src: upstream/picorv32.v:1204.6-1204.20
	wire<1> p_cpu_2e_latched__branch;
	// \hdlname: cpu is_sltiu_bltu_sltu
	// \src: upstream/picorv32.v:672.6-672.24
	wire<1> p_cpu_2e_is__sltiu__bltu__sltu;
	// \hdlname: cpu is_slti_blt_slt
	// \src: upstream/picorv32.v:671.6-671.21
	wire<1> p_cpu_2e_is__slti__blt__slt;
	// \hdlname: cpu is_slli_srli_srai
	// \src: upstream/picorv32.v:666.6-666.23
	wire<1> p_cpu_2e_is__slli__srli__srai;
	// \hdlname: cpu is_sll_srl_sra
	// \src: upstream/picorv32.v:669.6-669.20
	wire<1> p_cpu_2e_is__sll__srl__sra;
	// \hdlname: cpu is_sb_sh_sw
	// \src: upstream/picorv32.v:668.6-668.17
	wire<1> p_cpu_2e_is__sb__sh__sw;
	// \hdlname: cpu is_lui_auipc_jal_jalr_addi_add_sub
	// \src: upstream/picorv32.v:670.6-670.40
	wire<1> p_cpu_2e_is__lui__auipc__jal__jalr__addi__add__sub;
	// \hdlname: cpu is_lui_auipc_jal
	// \src: upstream/picorv32.v:664.6-664.22
	wire<1> p_cpu_2e_is__lui__auipc__jal;
	// \hdlname: cpu is_lbu_lhu_lw
	// \src: upstream/picorv32.v:674.6-674.19
	wire<1> p_cpu_2e_is__lbu__lhu__lw;
	// \hdlname: cpu is_lb_lh_lw_lbu_lhu
	// \src: upstream/picorv32.v:665.6-665.25
	wire<1> p_cpu_2e_is__lb__lh__lw__lbu__lhu;
	// \hdlname: cpu is_jalr_addi_slti_sltiu_xori_ori_andi
	// \src: upstream/picorv32.v:667.6-667.43
	wire<1> p_cpu_2e_is__jalr__addi__slti__sltiu__xori__ori__andi;
	// \hdlname: cpu is_compare
	// \src: upstream/picorv32.v:677.6-677.16
	wire<1> p_cpu_2e_is__compare;
	// \hdlname: cpu is_beq_bne_blt_bge_bltu_bgeu
	// \src: upstream/picorv32.v:673.6-673.34
	wire<1> p_cpu_2e_is__beq__bne__blt__bge__bltu__bgeu;
	// \hdlname: cpu is_alu_reg_reg
	// \src: upstream/picorv32.v:676.6-676.20
	wire<1> p_cpu_2e_is__alu__reg__reg;
	// \hdlname: cpu is_alu_reg_imm
	// \src: upstream/picorv32.v:675.6-675.20
	wire<1> p_cpu_2e_is__alu__reg__imm;
	// \hdlname: cpu irq_active
	// \src: upstream/picorv32.v:197.6-197.16
	wire<1> p_cpu_2e_irq__active;
	// \hdlname: cpu instr_xori
	// \src: upstream/picorv32.v:649.43-649.53
	wire<1> p_cpu_2e_instr__xori;
	// \hdlname: cpu instr_xor
	// \src: upstream/picorv32.v:650.62-650.71
	wire<1> p_cpu_2e_instr__xor;
	// \hdlname: cpu instr_waitirq
	// \src: upstream/picorv32.v:652.59-652.72
	wire<1> p_cpu_2e_instr__waitirq;
	// \hdlname: cpu instr_timer
	// \src: upstream/picorv32.v:652.74-652.85
	wire<1> p_cpu_2e_instr__timer;
	// \hdlname: cpu instr_sw
	// \src: upstream/picorv32.v:648.78-648.86
	wire<1> p_cpu_2e_instr__sw;
	// \hdlname: cpu instr_sub
	// \src: upstream/picorv32.v:650.17-650.26
	wire<1> p_cpu_2e_instr__sub;
	// \hdlname: cpu instr_srli
	// \src: upstream/picorv32.v:649.90-649.100
	wire<1> p_cpu_2e_instr__srli;
	// \hdlname: cpu instr_srl
	// \src: upstream/picorv32.v:650.73-650.82
	wire<1> p_cpu_2e_instr__srl;
	// \hdlname: cpu instr_srai
	// \src: upstream/picorv32.v:649.102-649.112
	wire<1> p_cpu_2e_instr__srai;
	// \hdlname: cpu instr_sra
	// \src: upstream/picorv32.v:650.84-650.93
	wire<1> p_cpu_2e_instr__sra;
	// \hdlname: cpu instr_sltu
	// \src: upstream/picorv32.v:650.50-650.60
	wire<1> p_cpu_2e_instr__sltu;
	// \hdlname: cpu instr_sltiu
	// \src: upstream/picorv32.v:649.30-649.41
	wire<1> p_cpu_2e_instr__sltiu;
	// \hdlname: cpu instr_slti
	// \src: upstream/picorv32.v:649.18-649.28
	wire<1> p_cpu_2e_instr__slti;
	// \hdlname: cpu instr_slt
	// \src: upstream/picorv32.v:650.39-650.48
	wire<1> p_cpu_2e_instr__slt;
	// \hdlname: cpu instr_slli
	// \src: upstream/picorv32.v:649.78-649.88
	wire<1> p_cpu_2e_instr__slli;
	// \hdlname: cpu instr_sll
	// \src: upstream/picorv32.v:650.28-650.37
	wire<1> p_cpu_2e_instr__sll;
	// \hdlname: cpu instr_sh
	// \src: upstream/picorv32.v:648.68-648.76
	wire<1> p_cpu_2e_instr__sh;
	// \hdlname: cpu instr_setq
	// \src: upstream/picorv32.v:652.18-652.28
	wire<1> p_cpu_2e_instr__setq;
	// \hdlname: cpu instr_sb
	// \src: upstream/picorv32.v:648.58-648.66
	wire<1> p_cpu_2e_instr__sb;
	// \hdlname: cpu instr_retirq
	// \src: upstream/picorv32.v:652.30-652.42
	wire<1> p_cpu_2e_instr__retirq;
	// \hdlname: cpu instr_rdinstrh
	// \src: upstream/picorv32.v:651.52-651.66
	wire<1> p_cpu_2e_instr__rdinstrh;
	// \hdlname: cpu instr_rdinstr
	// \src: upstream/picorv32.v:651.37-651.50
	wire<1> p_cpu_2e_instr__rdinstr;
	// \hdlname: cpu instr_rdcycleh
	// \src: upstream/picorv32.v:651.21-651.35
	wire<1> p_cpu_2e_instr__rdcycleh;
	// \hdlname: cpu instr_rdcycle
	// \src: upstream/picorv32.v:651.6-651.19
	wire<1> p_cpu_2e_instr__rdcycle;
	// \hdlname: cpu instr_ori
	// \src: upstream/picorv32.v:649.55-649.64
	wire<1> p_cpu_2e_instr__ori;
	// \hdlname: cpu instr_or
	// \src: upstream/picorv32.v:650.95-650.103
	wire<1> p_cpu_2e_instr__or;
	// \hdlname: cpu instr_maskirq
	// \src: upstream/picorv32.v:652.44-652.57
	wire<1> p_cpu_2e_instr__maskirq;
	// \hdlname: cpu instr_lw
	// \src: upstream/picorv32.v:648.26-648.34
	wire<1> p_cpu_2e_instr__lw;
	// \hdlname: cpu instr_lui
	// \src: upstream/picorv32.v:646.6-646.15
	wire<1> p_cpu_2e_instr__lui;
	// \hdlname: cpu instr_lhu
	// \src: upstream/picorv32.v:648.47-648.56
	wire<1> p_cpu_2e_instr__lhu;
	// \hdlname: cpu instr_lh
	// \src: upstream/picorv32.v:648.16-648.24
	wire<1> p_cpu_2e_instr__lh;
	// \hdlname: cpu instr_lbu
	// \src: upstream/picorv32.v:648.36-648.45
	wire<1> p_cpu_2e_instr__lbu;
	// \hdlname: cpu instr_lb
	// \src: upstream/picorv32.v:648.6-648.14
	wire<1> p_cpu_2e_instr__lb;
	// \hdlname: cpu instr_jalr
	// \src: upstream/picorv32.v:646.41-646.51
	wire<1> p_cpu_2e_instr__jalr;
	// \hdlname: cpu instr_jal
	// \src: upstream/picorv32.v:646.30-646.39
	wire<1> p_cpu_2e_instr__jal;
	// \hdlname: cpu instr_getq
	// \src: upstream/picorv32.v:652.6-652.16
	wire<1> p_cpu_2e_instr__getq;
	// \hdlname: cpu instr_fence
	// \src: upstream/picorv32.v:651.88-651.99
	wire<1> p_cpu_2e_instr__fence;
	// \hdlname: cpu instr_bne
	// \src: upstream/picorv32.v:647.17-647.26
	wire<1> p_cpu_2e_instr__bne;
	// \hdlname: cpu instr_bltu
	// \src: upstream/picorv32.v:647.50-647.60
	wire<1> p_cpu_2e_instr__bltu;
	// \hdlname: cpu instr_blt
	// \src: upstream/picorv32.v:647.28-647.37
	wire<1> p_cpu_2e_instr__blt;
	// \hdlname: cpu instr_bgeu
	// \src: upstream/picorv32.v:647.62-647.72
	wire<1> p_cpu_2e_instr__bgeu;
	// \hdlname: cpu instr_bge
	// \src: upstream/picorv32.v:647.39-647.48
	wire<1> p_cpu_2e_instr__bge;
	// \hdlname: cpu instr_beq
	// \src: upstream/picorv32.v:647.6-647.15
	wire<1> p_cpu_2e_instr__beq;
	// \hdlname: cpu instr_auipc
	// \src: upstream/picorv32.v:646.17-646.28
	wire<1> p_cpu_2e_instr__auipc;
	// \hdlname: cpu instr_andi
	// \src: upstream/picorv32.v:649.66-649.76
	wire<1> p_cpu_2e_instr__andi;
	// \hdlname: cpu instr_and
	// \src: upstream/picorv32.v:650.105-650.114
	wire<1> p_cpu_2e_instr__and;
	// \hdlname: cpu instr_addi
	// \src: upstream/picorv32.v:649.6-649.16
	wire<1> p_cpu_2e_instr__addi;
	// \hdlname: cpu instr_add
	// \src: upstream/picorv32.v:650.6-650.15
	wire<1> p_cpu_2e_instr__add;
	// \hdlname: cpu eoi
	// \src: upstream/picorv32.v:121.20-121.23
	wire<32> p_cpu_2e_eoi;
	// \hdlname: cpu do_waitirq
	// \src: upstream/picorv32.v:1219.6-1219.16
	wire<1> p_cpu_2e_do__waitirq;
	// \hdlname: cpu decoder_trigger
	// \src: upstream/picorv32.v:658.6-658.21
	wire<1> p_cpu_2e_decoder__trigger;
	// \hdlname: cpu decoder_pseudo_trigger
	// \src: upstream/picorv32.v:660.6-660.28
	wire<1> p_cpu_2e_decoder__pseudo__trigger;
	// \hdlname: cpu decoded_rs2
	// \src: upstream/picorv32.v:656.12-656.23
	wire<5> p_cpu_2e_decoded__rs2;
	// \hdlname: cpu decoded_rs1
	// \src: upstream/picorv32.v:655.38-655.49
	wire<5> p_cpu_2e_decoded__rs1;
	// \hdlname: cpu decoded_rd
	// \src: upstream/picorv32.v:655.26-655.36
	wire<5> p_cpu_2e_decoded__rd;
	// \hdlname: cpu decoded_imm_j
	// \src: upstream/picorv32.v:657.26-657.39
	wire<32> p_cpu_2e_decoded__imm__j;
	// \hdlname: cpu decoded_imm
	// \src: upstream/picorv32.v:657.13-657.24
	wire<32> p_cpu_2e_decoded__imm;
	// \hdlname: cpu cpu_state
	// \src: upstream/picorv32.v:1181.12-1181.21
	wire<8> p_cpu_2e_cpu__state;
	// \hdlname: cpu compressed_instr
	// \src: upstream/picorv32.v:662.6-662.22
	wire<1> p_cpu_2e_compressed__instr;
	// \hdlname: cpu alu_out_q
	// \src: upstream/picorv32.v:1221.22-1221.31
	wire<32> p_cpu_2e_alu__out__q;
	// \src: upstream/picorv32.v:1337.2-1346.5
	wire<32> i_flatten_5c_cpu_2e__24_0_24_memwr_24__5c_cpuregs_24_upstream_2f_picorv32_2e_v_3a_1344_24_902__EN_5b_31_3a_0_5d__24_1372;
	// \src: core_wrapper.v:1.27-1.30
	/*input*/ value<1> p_clk;
	value<1> prev_p_clk;
	bool posedge_p_clk() const {
		return !prev_p_clk.slice<0>().val() && p_clk.slice<0>().val();
	}
	// \src: core_wrapper.v:2.48-2.56
	/*output*/ value<32> p_mem__addr;
	// \src: core_wrapper.v:2.24-2.33
	/*output*/ value<1> p_mem__instr;
	// \src: core_wrapper.v:1.61-1.70
	/*input*/ value<32> p_mem__rdata;
	// \src: core_wrapper.v:1.38-1.47
	/*input*/ value<1> p_mem__ready;
	// \src: core_wrapper.v:2.14-2.23
	/*output*/ value<1> p_mem__valid;
	// \src: core_wrapper.v:2.57-2.66
	/*output*/ value<32> p_mem__wdata;
	// \src: core_wrapper.v:2.80-2.89
	/*output*/ value<4> p_mem__wstrb;
	// \src: core_wrapper.v:1.31-1.37
	/*input*/ value<1> p_resetn;
	// \src: core_wrapper.v:3.35-3.45
	/*output*/ value<36> p_trace__data;
	// \src: core_wrapper.v:3.9-3.20
	/*output*/ value<1> p_trace__valid;
	// \src: core_wrapper.v:2.9-2.13
	/*output*/ value<1> p_trap;
	// \hdlname: cpu next_pc
	// \src: upstream/picorv32.v:194.14-194.21
	/*outline*/ value<32> p_cpu_2e_next__pc;
	// \hdlname: cpu mem_xfer
	// \src: upstream/picorv32.v:360.7-360.15
	/*outline*/ value<1> p_cpu_2e_mem__xfer;
	// \hdlname: cpu mem_rdata_word
	// \src: upstream/picorv32.v:353.13-353.27
	/*outline*/ value<32> p_cpu_2e_mem__rdata__word;
	// \hdlname: cpu mem_rdata_latched
	// \src: upstream/picorv32.v:370.14-370.31
	/*outline*/ value<32> p_cpu_2e_mem__rdata__latched;
	// \hdlname: cpu mem_la_wstrb
	// \src: upstream/picorv32.v:107.20-107.32
	/*outline*/ value<4> p_cpu_2e_mem__la__wstrb;
	// \hdlname: cpu mem_la_write
	// \src: upstream/picorv32.v:104.20-104.32
	/*outline*/ value<1> p_cpu_2e_mem__la__write;
	// \hdlname: cpu mem_la_wdata
	// \src: upstream/picorv32.v:106.20-106.32
	/*outline*/ value<32> p_cpu_2e_mem__la__wdata;
	// \hdlname: cpu mem_la_read
	// \src: upstream/picorv32.v:103.20-103.31
	/*outline*/ value<1> p_cpu_2e_mem__la__read;
	// \hdlname: cpu mem_la_addr
	// \src: upstream/picorv32.v:105.20-105.31
	/*outline*/ value<32> p_cpu_2e_mem__la__addr;
	// \hdlname: cpu mem_done
	// \src: upstream/picorv32.v:376.7-376.15
	/*outline*/ value<1> p_cpu_2e_mem__done;
	// \hdlname: cpu instr_trap
	// \src: upstream/picorv32.v:653.7-653.17
	/*outline*/ value<1> p_cpu_2e_instr__trap;
	// \hdlname: cpu cpuregs_write
	// \src: upstream/picorv32.v:1303.6-1303.19
	/*outline*/ value<1> p_cpu_2e_cpuregs__write;
	// \hdlname: cpu cpuregs_wrdata
	// \src: upstream/picorv32.v:1304.13-1304.27
	/*outline*/ value<32> p_cpu_2e_cpuregs__wrdata;
	// \hdlname: cpu cpuregs_rs2
	// \src: upstream/picorv32.v:1306.13-1306.24
	/*outline*/ value<32> p_cpu_2e_cpuregs__rs2;
	// \hdlname: cpu cpuregs_rs1
	// \src: upstream/picorv32.v:1305.13-1305.24
	/*outline*/ value<32> p_cpu_2e_cpuregs__rs1;
	// \hdlname: cpu alu_out_0
	// \src: upstream/picorv32.v:1222.6-1222.15
	/*outline*/ value<1> p_cpu_2e_alu__out__0;
	// \hdlname: cpu alu_out
	// \src: upstream/picorv32.v:1221.13-1221.20
	/*outline*/ value<32> p_cpu_2e_alu__out;
	// \hdlname: cpu alu_ltu
	// \src: upstream/picorv32.v:1227.14-1227.21
	/*outline*/ value<1> p_cpu_2e_alu__ltu;
	// \hdlname: cpu alu_lts
	// \src: upstream/picorv32.v:1227.23-1227.30
	/*outline*/ value<1> p_cpu_2e_alu__lts;
	// \hdlname: cpu alu_eq
	// \src: upstream/picorv32.v:1227.6-1227.12
	/*outline*/ value<1> p_cpu_2e_alu__eq;
	// \hdlname: cpu alu_add_sub
	// \src: upstream/picorv32.v:1225.13-1225.24
	/*outline*/ value<32> p_cpu_2e_alu__add__sub;
	// \hdlname: cpu cpuregs
	// \src: upstream/picorv32.v:203.13-203.20
	memory<32> memory_p_cpu_2e_cpuregs { 32u };

	p_core__wrapper(interior) {}
	p_core__wrapper() {
		reset();
	};

	void reset() override;

	bool eval(performer *performer = nullptr) override;

	template<class ObserverT>
	bool commit(ObserverT &observer) {
		bool changed = false;
		if (p_cpu_2e_trap.commit(observer)) changed = true;
		if (p_cpu_2e_trace__valid.commit(observer)) changed = true;
		if (p_cpu_2e_trace__data.commit(observer)) changed = true;
		if (p_cpu_2e_reg__sh.commit(observer)) changed = true;
		if (p_cpu_2e_reg__pc.commit(observer)) changed = true;
		if (p_cpu_2e_reg__out.commit(observer)) changed = true;
		if (p_cpu_2e_reg__op2.commit(observer)) changed = true;
		if (p_cpu_2e_reg__op1.commit(observer)) changed = true;
		if (p_cpu_2e_reg__next__pc.commit(observer)) changed = true;
		if (p_cpu_2e_pcpi__valid.commit(observer)) changed = true;
		if (p_cpu_2e_pcpi__insn.commit(observer)) changed = true;
		if (p_cpu_2e_mem__wstrb.commit(observer)) changed = true;
		if (p_cpu_2e_mem__wordsize.commit(observer)) changed = true;
		if (p_cpu_2e_mem__wdata.commit(observer)) changed = true;
		if (p_cpu_2e_mem__valid.commit(observer)) changed = true;
		if (p_cpu_2e_mem__state.commit(observer)) changed = true;
		if (p_cpu_2e_mem__rdata__q.commit(observer)) changed = true;
		if (p_cpu_2e_mem__instr.commit(observer)) changed = true;
		if (p_cpu_2e_mem__do__wdata.commit(observer)) changed = true;
		if (p_cpu_2e_mem__do__rinst.commit(observer)) changed = true;
		if (p_cpu_2e_mem__do__rdata.commit(observer)) changed = true;
		if (p_cpu_2e_mem__do__prefetch.commit(observer)) changed = true;
		if (p_cpu_2e_mem__addr.commit(observer)) changed = true;
		if (p_cpu_2e_latched__trace.commit(observer)) changed = true;
		if (p_cpu_2e_latched__store.commit(observer)) changed = true;
		if (p_cpu_2e_latched__stalu.commit(observer)) changed = true;
		if (p_cpu_2e_latched__rd.commit(observer)) changed = true;
		if (p_cpu_2e_latched__is__lu.commit(observer)) changed = true;
		if (p_cpu_2e_latched__is__lh.commit(observer)) changed = true;
		if (p_cpu_2e_latched__is__lb.commit(observer)) changed = true;
		if (p_cpu_2e_latched__compr.commit(observer)) changed = true;
		if (p_cpu_2e_latched__branch.commit(observer)) changed = true;
		if (p_cpu_2e_is__sltiu__bltu__sltu.commit(observer)) changed = true;
		if (p_cpu_2e_is__slti__blt__slt.commit(observer)) changed = true;
		if (p_cpu_2e_is__slli__srli__srai.commit(observer)) changed = true;
		if (p_cpu_2e_is__sll__srl__sra.commit(observer)) changed = true;
		if (p_cpu_2e_is__sb__sh__sw.commit(observer)) changed = true;
		if (p_cpu_2e_is__lui__auipc__jal__jalr__addi__add__sub.commit(observer)) changed = true;
		if (p_cpu_2e_is__lui__auipc__jal.commit(observer)) changed = true;
		if (p_cpu_2e_is__lbu__lhu__lw.commit(observer)) changed = true;
		if (p_cpu_2e_is__lb__lh__lw__lbu__lhu.commit(observer)) changed = true;
		if (p_cpu_2e_is__jalr__addi__slti__sltiu__xori__ori__andi.commit(observer)) changed = true;
		if (p_cpu_2e_is__compare.commit(observer)) changed = true;
		if (p_cpu_2e_is__beq__bne__blt__bge__bltu__bgeu.commit(observer)) changed = true;
		if (p_cpu_2e_is__alu__reg__reg.commit(observer)) changed = true;
		if (p_cpu_2e_is__alu__reg__imm.commit(observer)) changed = true;
		if (p_cpu_2e_irq__active.commit(observer)) changed = true;
		if (p_cpu_2e_instr__xori.commit(observer)) changed = true;
		if (p_cpu_2e_instr__xor.commit(observer)) changed = true;
		if (p_cpu_2e_instr__waitirq.commit(observer)) changed = true;
		if (p_cpu_2e_instr__timer.commit(observer)) changed = true;
		if (p_cpu_2e_instr__sw.commit(observer)) changed = true;
		if (p_cpu_2e_instr__sub.commit(observer)) changed = true;
		if (p_cpu_2e_instr__srli.commit(observer)) changed = true;
		if (p_cpu_2e_instr__srl.commit(observer)) changed = true;
		if (p_cpu_2e_instr__srai.commit(observer)) changed = true;
		if (p_cpu_2e_instr__sra.commit(observer)) changed = true;
		if (p_cpu_2e_instr__sltu.commit(observer)) changed = true;
		if (p_cpu_2e_instr__sltiu.commit(observer)) changed = true;
		if (p_cpu_2e_instr__slti.commit(observer)) changed = true;
		if (p_cpu_2e_instr__slt.commit(observer)) changed = true;
		if (p_cpu_2e_instr__slli.commit(observer)) changed = true;
		if (p_cpu_2e_instr__sll.commit(observer)) changed = true;
		if (p_cpu_2e_instr__sh.commit(observer)) changed = true;
		if (p_cpu_2e_instr__setq.commit(observer)) changed = true;
		if (p_cpu_2e_instr__sb.commit(observer)) changed = true;
		if (p_cpu_2e_instr__retirq.commit(observer)) changed = true;
		if (p_cpu_2e_instr__rdinstrh.commit(observer)) changed = true;
		if (p_cpu_2e_instr__rdinstr.commit(observer)) changed = true;
		if (p_cpu_2e_instr__rdcycleh.commit(observer)) changed = true;
		if (p_cpu_2e_instr__rdcycle.commit(observer)) changed = true;
		if (p_cpu_2e_instr__ori.commit(observer)) changed = true;
		if (p_cpu_2e_instr__or.commit(observer)) changed = true;
		if (p_cpu_2e_instr__maskirq.commit(observer)) changed = true;
		if (p_cpu_2e_instr__lw.commit(observer)) changed = true;
		if (p_cpu_2e_instr__lui.commit(observer)) changed = true;
		if (p_cpu_2e_instr__lhu.commit(observer)) changed = true;
		if (p_cpu_2e_instr__lh.commit(observer)) changed = true;
		if (p_cpu_2e_instr__lbu.commit(observer)) changed = true;
		if (p_cpu_2e_instr__lb.commit(observer)) changed = true;
		if (p_cpu_2e_instr__jalr.commit(observer)) changed = true;
		if (p_cpu_2e_instr__jal.commit(observer)) changed = true;
		if (p_cpu_2e_instr__getq.commit(observer)) changed = true;
		if (p_cpu_2e_instr__fence.commit(observer)) changed = true;
		if (p_cpu_2e_instr__bne.commit(observer)) changed = true;
		if (p_cpu_2e_instr__bltu.commit(observer)) changed = true;
		if (p_cpu_2e_instr__blt.commit(observer)) changed = true;
		if (p_cpu_2e_instr__bgeu.commit(observer)) changed = true;
		if (p_cpu_2e_instr__bge.commit(observer)) changed = true;
		if (p_cpu_2e_instr__beq.commit(observer)) changed = true;
		if (p_cpu_2e_instr__auipc.commit(observer)) changed = true;
		if (p_cpu_2e_instr__andi.commit(observer)) changed = true;
		if (p_cpu_2e_instr__and.commit(observer)) changed = true;
		if (p_cpu_2e_instr__addi.commit(observer)) changed = true;
		if (p_cpu_2e_instr__add.commit(observer)) changed = true;
		if (p_cpu_2e_eoi.commit(observer)) changed = true;
		if (p_cpu_2e_do__waitirq.commit(observer)) changed = true;
		if (p_cpu_2e_decoder__trigger.commit(observer)) changed = true;
		if (p_cpu_2e_decoder__pseudo__trigger.commit(observer)) changed = true;
		if (p_cpu_2e_decoded__rs2.commit(observer)) changed = true;
		if (p_cpu_2e_decoded__rs1.commit(observer)) changed = true;
		if (p_cpu_2e_decoded__rd.commit(observer)) changed = true;
		if (p_cpu_2e_decoded__imm__j.commit(observer)) changed = true;
		if (p_cpu_2e_decoded__imm.commit(observer)) changed = true;
		if (p_cpu_2e_cpu__state.commit(observer)) changed = true;
		if (p_cpu_2e_compressed__instr.commit(observer)) changed = true;
		if (p_cpu_2e_alu__out__q.commit(observer)) changed = true;
		if (i_flatten_5c_cpu_2e__24_0_24_memwr_24__5c_cpuregs_24_upstream_2f_picorv32_2e_v_3a_1344_24_902__EN_5b_31_3a_0_5d__24_1372.commit(observer)) changed = true;
		prev_p_clk = p_clk;
		if (memory_p_cpu_2e_cpuregs.commit(observer)) changed = true;
		return changed;
	}

	bool commit() override {
		observer observer;
		return commit<>(observer);
	}

	void debug_eval();
	debug_outline debug_eval_outline { std::bind(&p_core__wrapper::debug_eval, this) };

	void debug_info(debug_items *items, debug_scopes *scopes, std::string path, metadata_map &&cell_attrs = {}) override;
}; // struct p_core__wrapper

void p_core__wrapper::reset() {
	static const value<32> mem_init_1[32] {
		value<32>{0x00000000u}, value<32>{0x00000000u}, value<32>{0x00000000u}, value<32>{0x00000000u},
		value<32>{0x00000000u}, value<32>{0x00000000u}, value<32>{0x00000000u}, value<32>{0x00000000u},
		value<32>{0x00000000u}, value<32>{0x00000000u}, value<32>{0x00000000u}, value<32>{0x00000000u},
		value<32>{0x00000000u}, value<32>{0x00000000u}, value<32>{0x00000000u}, value<32>{0x00000000u},
		value<32>{0x00000000u}, value<32>{0x00000000u}, value<32>{0x00000000u}, value<32>{0x00000000u},
		value<32>{0x00000000u}, value<32>{0x00000000u}, value<32>{0x00000000u}, value<32>{0x00000000u},
		value<32>{0x00000000u}, value<32>{0x00000000u}, value<32>{0x00000000u}, value<32>{0x00000000u},
		value<32>{0x00000000u}, value<32>{0x00000000u}, value<32>{0x00000000u}, value<32>{0x00000000u},
	};
	std::copy(std::begin(mem_init_1), std::end(mem_init_1), &memory_p_cpu_2e_cpuregs.data[0]);
}

bool p_core__wrapper::eval(performer *performer) {
	bool converged = false;
	bool posedge_p_clk = this->posedge_p_clk();
	// \hdlname: cpu resetn
	// \src: upstream/picorv32.v:90.13-90.19
	value<1> p_cpu_2e_resetn;
	// \hdlname: cpu mem_xfer
	// \src: upstream/picorv32.v:360.7-360.15
	value<1> p_cpu_2e_mem__xfer;
	// \hdlname: cpu mem_ready
	// \src: upstream/picorv32.v:95.20-95.29
	value<1> p_cpu_2e_mem__ready;
	// \hdlname: cpu mem_rdata_word
	// \src: upstream/picorv32.v:353.13-353.27
	value<32> p_cpu_2e_mem__rdata__word;
	// \hdlname: cpu mem_rdata_latched
	// \src: upstream/picorv32.v:370.14-370.31
	value<32> p_cpu_2e_mem__rdata__latched;
	// \hdlname: cpu mem_rdata
	// \src: upstream/picorv32.v:100.20-100.29
	value<32> p_cpu_2e_mem__rdata;
	// \hdlname: cpu mem_la_write
	// \src: upstream/picorv32.v:104.20-104.32
	value<1> p_cpu_2e_mem__la__write;
	// \hdlname: cpu mem_done
	// \src: upstream/picorv32.v:376.7-376.15
	value<1> p_cpu_2e_mem__done;
	// \hdlname: cpu instr_trap
	// \src: upstream/picorv32.v:653.7-653.17
	value<1> p_cpu_2e_instr__trap;
	// \hdlname: cpu cpuregs_rs2
	// \src: upstream/picorv32.v:1306.13-1306.24
	value<32> p_cpu_2e_cpuregs__rs2;
	// \hdlname: cpu clk
	// \src: upstream/picorv32.v:90.8-90.11
	value<1> p_cpu_2e_clk;
	// \hdlname: cpu alu_out_0
	// \src: upstream/picorv32.v:1222.6-1222.15
	value<1> p_cpu_2e_alu__out__0;
	// \hdlname: cpu alu_ltu
	// \src: upstream/picorv32.v:1227.14-1227.21
	value<1> p_cpu_2e_alu__ltu;
	// \hdlname: cpu alu_lts
	// \src: upstream/picorv32.v:1227.23-1227.30
	value<1> p_cpu_2e_alu__lts;
	// \hdlname: cpu alu_eq
	// \src: upstream/picorv32.v:1227.6-1227.12
	value<1> p_cpu_2e_alu__eq;
	// \src: upstream/picorv32.v:1321.23-1321.58
	value<32> i_flatten_5c_cpu_2e__24_ternary_24_upstream_2f_picorv32_2e_v_3a_1321_24_1363__Y;
	// \src: upstream/picorv32.v:1095.43-1099.5
	value<1> i_flatten_5c_cpu_2e__24_reduce__or_24_upstream_2f_picorv32_2e_v_3a_1095_24_1291__Y;
	value<1> i_flatten_5c_cpu_2e__24_procmux_24_4372__CMP;
	value<4> i_flatten_5c_cpu_2e__24_procmux_24_4093__Y;
	value<1> i_flatten_5c_cpu_2e__24_procmux_24_4082__CMP;
	value<1> i_flatten_5c_cpu_2e__24_procmux_24_4076__CMP;
	value<1> i_flatten_5c_cpu_2e__24_procmux_24_2819__Y;
	value<8> i_flatten_5c_cpu_2e__24_procmux_24_2666__Y;
	value<1> i_flatten_5c_cpu_2e__24_procmux_24_2500__Y;
	value<1> i_flatten_5c_cpu_2e__24_procmux_24_2052__CMP;
	value<1> i_flatten_5c_cpu_2e__24_procmux_24_2047__CMP;
	value<1> i_flatten_5c_cpu_2e__24_procmux_24_1786__CMP;
	value<1> i_flatten_5c_cpu_2e__24_procmux_24_1759__CMP;
	value<1> i_flatten_5c_cpu_2e__24_procmux_24_1748__CMP;
	value<1> i_flatten_5c_cpu_2e__24_procmux_24_1747__CMP;
	value<1> i_flatten_5c_cpu_2e__24_procmux_24_1737__CMP;
	// \src: upstream/picorv32.v:1867.22-1867.106
	value<36> i_flatten_5c_cpu_2e__24_or_24_upstream_2f_picorv32_2e_v_3a_1867_24_1520__Y;
	// \src: upstream/picorv32.v:1867.22-1867.63
	value<36> i_flatten_5c_cpu_2e__24_or_24_upstream_2f_picorv32_2e_v_3a_1867_24_1517__Y;
	// \src: upstream/picorv32.v:1521.21-1521.64
	value<36> i_flatten_5c_cpu_2e__24_or_24_upstream_2f_picorv32_2e_v_3a_1521_24_1415__Y;
	// \src: upstream/picorv32.v:1353.32-1353.39
	value<32> i_flatten_5c_cpu_2e__24_memrd_24__5c_cpuregs_24_upstream_2f_picorv32_2e_v_3a_1353_24_1382__DATA;
	// \src: upstream/picorv32.v:1352.32-1352.39
	value<32> i_flatten_5c_cpu_2e__24_memrd_24__5c_cpuregs_24_upstream_2f_picorv32_2e_v_3a_1352_24_1379__DATA;
	// \src: upstream/picorv32.v:574.8-574.35
	value<1> i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_574_24_1029__Y;
	// \src: upstream/picorv32.v:566.7-566.22
	value<1> i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_566_24_1025__Y;
	// \src: upstream/picorv32.v:380.86-380.133
	value<1> i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_380_24_954__Y;
	// \src: upstream/picorv32.v:380.86-380.117
	value<1> i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_380_24_953__Y;
	// \src: upstream/picorv32.v:376.57-376.85
	value<1> i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_376_24_934__Y;
	// \src: upstream/picorv32.v:1949.7-1949.26
	value<1> i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_1949_24_1568__Y;
	// \src: upstream/picorv32.v:1857.9-1857.37
	value<1> i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_1857_24_1513__Y;
	// \src: upstream/picorv32.v:1839.7-1839.30
	value<1> i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_1839_24_1500__Y;
	// \src: upstream/picorv32.v:1838.7-1838.30
	value<1> i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_1838_24_1498__Y;
	// \src: upstream/picorv32.v:1245.23-1245.46
	value<1> i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_1245_24_1578__Y;
	// \src: upstream/picorv32.v:1949.7-1949.14
	value<1> i_flatten_5c_cpu_2e__24_logic__not_24_upstream_2f_picorv32_2e_v_3a_1949_24_1567__Y;
	// \src: upstream/picorv32.v:1857.9-1857.25
	value<1> i_flatten_5c_cpu_2e__24_logic__not_24_upstream_2f_picorv32_2e_v_3a_1857_24_1512__Y;
	// \src: upstream/picorv32.v:380.35-380.81
	value<1> i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_380_24_952__Y;
	// \src: upstream/picorv32.v:1872.10-1872.38
	value<1> i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1872_24_1523__Y;
	// \src: upstream/picorv32.v:1696.6-1696.40
	value<1> i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1696_24_1467__Y;
	// \src: upstream/picorv32.v:1446.22-1446.46
	value<1> i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1446_24_1397__Y;
	// \src: upstream/picorv32.v:1338.7-1338.44
	value<1> i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1338_24_1374__Y;
	// \src: upstream/picorv32.v:1320.5-1320.37
	value<1> i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1320_24_1362__Y;
	// \src: upstream/picorv32.v:1074.19-1074.65
	value<1> i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1074_24_1211__Y;
	// \src: upstream/picorv32.v:1068.19-1068.65
	value<1> i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1068_24_1187__Y;
	// \src: upstream/picorv32.v:1065.19-1065.65
	value<1> i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1065_24_1179__Y;
	// \src: upstream/picorv32.v:1037.7-1037.49
	value<1> i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y;
	// \src: upstream/picorv32.v:1835.37-1835.48
	value<1> i_flatten_5c_cpu_2e__24_ge_24_upstream_2f_picorv32_2e_v_3a_1835_24_1496__Y;
	// \src: upstream/picorv32.v:1930.8-1930.25
	value<1> i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1930_24_1548__Y;
	// \src: upstream/picorv32.v:1923.8-1923.25
	value<1> i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1923_24_1541__Y;
	// \src: upstream/picorv32.v:1831.9-1831.20
	value<1> i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1831_24_1495__Y;
	// \src: upstream/picorv32.v:1313.7-1313.35
	value<1> i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1313_24_1358__Y;
	// \src: upstream/picorv32.v:1066.69-1066.101
	value<1> i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1066_24_1184__Y;
	// \src: upstream/picorv32.v:1064.69-1064.101
	value<1> i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1064_24_1176__Y;
	// \src: upstream/picorv32.v:1059.37-1059.65
	value<1> i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1059_24_1166__Y;
	// \src: upstream/picorv32.v:1049.42-1049.70
	value<1> i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1049_24_1150__Y;
	// \src: upstream/picorv32.v:1045.51-1045.79
	value<1> i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1045_24_1144__Y;
	// \src: upstream/picorv32.v:1044.51-1044.79
	value<1> i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1044_24_1142__Y;
	// \src: upstream/picorv32.v:1043.51-1043.79
	value<1> i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1043_24_1140__Y;
	// \src: upstream/picorv32.v:1042.51-1042.79
	value<1> i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1042_24_1138__Y;
	// \src: upstream/picorv32.v:1041.51-1041.79
	value<1> i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1041_24_1136__Y;
	// \src: upstream/picorv32.v:1040.51-1040.79
	value<1> i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1040_24_1134__Y;
	// \src: upstream/picorv32.v:1317.33-1317.54
	value<32> i_flatten_5c_cpu_2e__24_auto_24_wreduce_2e_cc_3a_513_3a_run_24_4603;
	// \src: upstream/picorv32.v:1560.35-1560.59
	value<32> i_flatten_5c_cpu_2e__24_auto_24_wreduce_2e_cc_3a_513_3a_run_24_4602;
	value<8> i_flatten_5c_cpu_2e__24_auto_24_wreduce_2e_cc_3a_513_3a_run_24_4601;
	// \src: upstream/picorv32.v:1842.16-1842.26
	value<32> i_flatten_5c_cpu_2e__24_auto_24_wreduce_2e_cc_3a_513_3a_run_24_4600;
	// \src: upstream/picorv32.v:1850.16-1850.26
	value<32> i_flatten_5c_cpu_2e__24_auto_24_wreduce_2e_cc_3a_513_3a_run_24_4599;
	value<1> i_flatten_5c_cpu_2e__24_auto_24_opt__reduce_2e_cc_3a_137_3a_opt__pmux_24_4591;
	value<1> i_flatten_5c_cpu_2e__24_auto_24_opt__reduce_2e_cc_3a_137_3a_opt__pmux_24_4569;
	// \src: upstream/picorv32.v:1500.36-1500.78
	value<32> i_flatten_5c_cpu_2e__24_and_24_upstream_2f_picorv32_2e_v_3a_1500_24_1403__Y;
	value<32> i_flatten_5c_cpu_2e__24_add_24_upstream_2f_picorv32_2e_v_3a_1867_24_1518__Y;
	// \src: upstream/picorv32.v:1402.2-1975.5
	value<1> i_flatten_5c_cpu_2e__24_3_5c_set__mem__do__wdata_5b_0_3a_0_5d_;
	// \src: upstream/picorv32.v:1402.2-1975.5
	value<1> i_flatten_5c_cpu_2e__24_3_5c_set__mem__do__rdata_5b_0_3a_0_5d_;
	// \src: upstream/picorv32.v:1402.2-1975.5
	value<32> i_flatten_5c_cpu_2e__24_3_5c_current__pc_5b_31_3a_0_5d_;
	// \src: upstream/picorv32.v:430.2-544.5
	value<32> i_flatten_5c_cpu_2e__24_0_5c_mem__rdata__q_5b_31_3a_0_5d_;
	// \src: upstream/picorv32.v:858.2-1167.5
	value<5> i_flatten_5c_cpu_2e__24_0_5c_decoded__rs1_5b_4_3a_0_5d_;
	// \src: upstream/picorv32.v:858.2-1167.5
	value<32> i_flatten_5c_cpu_2e__24_0_5c_decoded__imm__j_5b_31_3a_0_5d_;
	// \full_case: 1
	// \parallel_case: 1
	// \src: upstream/picorv32.v:1489.7-1489.7|upstream/picorv32.v:1486.3-1913.10
	// cell $flatten\cpu.$procmux$3168_CMP0
	i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1313_24_1358__Y = eq_uu<1>(p_cpu_2e_cpu__state.curr, value<7>{0x40u});
	// connection
	p_cpu_2e_resetn = p_resetn;
	// cells $flatten\cpu.$logic_and$upstream/picorv32.v:1320$1362 $flatten\cpu.$logic_not$upstream/picorv32.v:1320$1361
	i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1320_24_1362__Y = logic_and<1>(p_cpu_2e_latched__store.curr, logic_not<1>(p_cpu_2e_latched__branch.curr));
	// cells $flatten\cpu.$logic_and$upstream/picorv32.v:1338$1374 $flatten\cpu.$logic_and$upstream/picorv32.v:1338$1373 $flatten\cpu.$procmux$3224 $flatten\cpu.$procmux$3204 $flatten\cpu.$auto$opt_reduce.cc:131:opt_pmux$4582
	i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1338_24_1374__Y = logic_and<1>(logic_and<1>(p_cpu_2e_resetn, (i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1313_24_1358__Y ? (reduce_or<1>(i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1320_24_1362__Y.concat(p_cpu_2e_latched__branch.curr).val()) ? value<1>{0x1u} : value<1>{0u}) : value<1>{0u})), p_cpu_2e_latched__rd.curr);
	// \full_case: 1
	// \src: upstream/picorv32.v:1338.7-1338.44|upstream/picorv32.v:1338.3-1344.42
	// cell $flatten\cpu.$procmux$3194
	i_flatten_5c_cpu_2e__24_0_24_memwr_24__5c_cpuregs_24_upstream_2f_picorv32_2e_v_3a_1344_24_902__EN_5b_31_3a_0_5d__24_1372.next.slice<0>() = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1338_24_1374__Y ? value<1>{0x1u} : value<1>{0u});
	// connection
	i_flatten_5c_cpu_2e__24_0_24_memwr_24__5c_cpuregs_24_upstream_2f_picorv32_2e_v_3a_1344_24_902__EN_5b_31_3a_0_5d__24_1372.next.slice<31,1>() = i_flatten_5c_cpu_2e__24_0_24_memwr_24__5c_cpuregs_24_upstream_2f_picorv32_2e_v_3a_1344_24_902__EN_5b_31_3a_0_5d__24_1372.curr.slice<0>().val().repeat<31>().val();
	// connection
	p_cpu_2e_mem__ready = p_mem__ready;
	// \src: upstream/picorv32.v:373.21-373.43
	// cell $flatten\cpu.$logic_and$upstream/picorv32.v:373$928
	p_cpu_2e_mem__xfer = logic_and<1>(p_cpu_2e_mem__valid.curr, p_cpu_2e_mem__ready);
	// \src: upstream/picorv32.v:617.21-617.49
	// cell $flatten\cpu.$logic_or$upstream/picorv32.v:617$1042
	i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_376_24_934__Y = logic_or<1>(p_cpu_2e_mem__do__rinst.curr, p_cpu_2e_mem__do__rdata.curr);
	// \src: upstream/picorv32.v:1523.53-1523.88
	// cell $flatten\cpu.$ternary$upstream/picorv32.v:1523$1420
	i_flatten_5c_cpu_2e__24_and_24_upstream_2f_picorv32_2e_v_3a_1500_24_1403__Y.slice<31,1>().concat(i_flatten_5c_cpu_2e__24_ternary_24_upstream_2f_picorv32_2e_v_3a_1321_24_1363__Y.slice<0>()) = (p_cpu_2e_latched__stalu.curr ? p_cpu_2e_alu__out__q.curr : p_cpu_2e_reg__out.curr);
	// connection
	i_flatten_5c_cpu_2e__24_and_24_upstream_2f_picorv32_2e_v_3a_1500_24_1403__Y.slice<0>() = value<1>{0u};
	// cells $flatten\cpu.$logic_and$upstream/picorv32.v:376$940 $flatten\cpu.$logic_or$upstream/picorv32.v:376$939 $flatten\cpu.$logic_and$upstream/picorv32.v:376$936 $flatten\cpu.$logic_and$upstream/picorv32.v:376$933 $flatten\cpu.$reduce_or$upstream/picorv32.v:376$932 $flatten\cpu.$logic_or$upstream/picorv32.v:376$935 $flatten\cpu.$logic_and$upstream/picorv32.v:376$938 $flatten\cpu.$reduce_and$upstream/picorv32.v:376$937
	p_cpu_2e_mem__done = logic_and<1>(p_cpu_2e_resetn, logic_or<1>(logic_and<1>(logic_and<1>(p_cpu_2e_mem__xfer, reduce_or<1>(p_cpu_2e_mem__state.curr)), logic_or<1>(i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_376_24_934__Y, p_cpu_2e_mem__do__wdata.curr)), logic_and<1>(reduce_and<1>(p_cpu_2e_mem__state.curr), p_cpu_2e_mem__do__rinst.curr)));
	// \src: upstream/picorv32.v:1900.10-1900.26
	// cell $flatten\cpu.$logic_not$upstream/picorv32.v:1900$1536
	i_flatten_5c_cpu_2e__24_logic__not_24_upstream_2f_picorv32_2e_v_3a_1857_24_1512__Y = logic_not<1>(p_cpu_2e_mem__do__prefetch.curr);
	// \src: upstream/picorv32.v:679.54-685.84
	// cell $flatten\cpu.$logic_not$upstream/picorv32.v:679$1044
	p_cpu_2e_instr__trap = logic_not<1>(p_cpu_2e_instr__lui.curr.concat(p_cpu_2e_instr__auipc.curr).concat(p_cpu_2e_instr__jal.curr).concat(p_cpu_2e_instr__jalr.curr).concat(p_cpu_2e_instr__beq.curr).concat(p_cpu_2e_instr__bne.curr).concat(p_cpu_2e_instr__blt.curr).concat(p_cpu_2e_instr__bge.curr).concat(p_cpu_2e_instr__bltu.curr).concat(p_cpu_2e_instr__bgeu.curr).concat(p_cpu_2e_instr__lb.curr).concat(p_cpu_2e_instr__lh.curr).concat(p_cpu_2e_instr__lw.curr).concat(p_cpu_2e_instr__lbu.curr).concat(p_cpu_2e_instr__lhu.curr).concat(p_cpu_2e_instr__sb.curr).concat(p_cpu_2e_instr__sh.curr).concat(p_cpu_2e_instr__sw.curr).concat(p_cpu_2e_instr__addi.curr).concat(p_cpu_2e_instr__slti.curr).concat(p_cpu_2e_instr__sltiu.curr).concat(p_cpu_2e_instr__xori.curr).concat(p_cpu_2e_instr__ori.curr).concat(p_cpu_2e_instr__andi.curr).concat(p_cpu_2e_instr__slli.curr).concat(p_cpu_2e_instr__srli.curr).concat(p_cpu_2e_instr__srai.curr).concat(p_cpu_2e_instr__add.curr).concat(p_cpu_2e_instr__sub.curr).concat(p_cpu_2e_instr__sll.curr).concat(p_cpu_2e_instr__slt.curr).concat(p_cpu_2e_instr__sltu.curr).concat(p_cpu_2e_instr__xor.curr).concat(p_cpu_2e_instr__srl.curr).concat(p_cpu_2e_instr__sra.curr).concat(p_cpu_2e_instr__or.curr).concat(p_cpu_2e_instr__and.curr).concat(p_cpu_2e_instr__rdcycle.curr).concat(p_cpu_2e_instr__rdcycleh.curr).concat(p_cpu_2e_instr__rdinstr.curr).concat(p_cpu_2e_instr__rdinstrh.curr).concat(p_cpu_2e_instr__fence.curr).concat(p_cpu_2e_instr__getq.curr).concat(p_cpu_2e_instr__setq.curr).concat(p_cpu_2e_instr__retirq.curr).concat(p_cpu_2e_instr__maskirq.curr).concat(p_cpu_2e_instr__waitirq.curr).concat(p_cpu_2e_instr__timer.curr).val());
	// \src: upstream/picorv32.v:1900.10-1900.38
	// cell $flatten\cpu.$logic_and$upstream/picorv32.v:1900$1537
	i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1872_24_1523__Y = logic_and<1>(i_flatten_5c_cpu_2e__24_logic__not_24_upstream_2f_picorv32_2e_v_3a_1857_24_1512__Y, p_cpu_2e_mem__done);
	// \src: upstream/picorv32.v:585.20-585.51
	// cell $flatten\cpu.$logic_or$upstream/picorv32.v:585$1034
	i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_380_24_953__Y = logic_or<1>(p_cpu_2e_mem__do__prefetch.curr, p_cpu_2e_mem__do__rinst.curr);
	// connection
	p_cpu_2e_mem__rdata = p_mem__rdata;
	// \src: upstream/picorv32.v:1241.13-1241.31
	// cell $flatten\cpu.$eq$upstream/picorv32.v:1241$1574
	p_cpu_2e_alu__eq = eq_uu<1>(p_cpu_2e_reg__op1.curr, p_cpu_2e_reg__op2.curr);
	// \src: upstream/picorv32.v:1242.14-1242.49
	// cell $flatten\cpu.$lt$upstream/picorv32.v:1242$1575
	p_cpu_2e_alu__lts = lt_ss<1>(p_cpu_2e_reg__op1.curr, p_cpu_2e_reg__op2.curr);
	// \src: upstream/picorv32.v:1243.14-1243.31
	// cell $flatten\cpu.$lt$upstream/picorv32.v:1243$1576
	p_cpu_2e_alu__ltu = lt_uu<1>(p_cpu_2e_reg__op1.curr, p_cpu_2e_reg__op2.curr);
	// \full_case: 1
	// \parallel_case: 1
	// \src: upstream/picorv32.v:1852.7-1852.7|upstream/picorv32.v:1486.3-1913.10
	// cell $flatten\cpu.$procmux$2174_CMP0
	i_flatten_5c_cpu_2e__24_procmux_24_1759__CMP = eq_uu<1>(p_cpu_2e_cpu__state.curr, value<2>{0x2u});
	// \full_case: 1
	// \parallel_case: 1
	// \src: upstream/picorv32.v:1878.7-1878.7|upstream/picorv32.v:1486.3-1913.10
	// cell $flatten\cpu.$procmux$2410_CMP0
	i_flatten_5c_cpu_2e__24_procmux_24_1737__CMP = eq_uu<1>(p_cpu_2e_cpu__state.curr, value<1>{0x1u});
	// \src: upstream/picorv32.v:1882.9-1882.37
	// cell $flatten\cpu.$logic_or$upstream/picorv32.v:1882$1525
	i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_1857_24_1513__Y = logic_or<1>(i_flatten_5c_cpu_2e__24_logic__not_24_upstream_2f_picorv32_2e_v_3a_1857_24_1512__Y, p_cpu_2e_mem__done);
	// \src: upstream/picorv32.v:1831.9-1831.20
	// cell $flatten\cpu.$eq$upstream/picorv32.v:1831$1495
	i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1831_24_1495__Y = logic_not<1>(p_cpu_2e_reg__sh.curr);
	// cell $flatten\cpu.$auto$opt_reduce.cc:131:opt_pmux$4568
	i_flatten_5c_cpu_2e__24_auto_24_opt__reduce_2e_cc_3a_137_3a_opt__pmux_24_4569 = reduce_or<1>(p_cpu_2e_is__jalr__addi__slti__sltiu__xori__ori__andi.curr.concat(p_cpu_2e_is__lui__auipc__jal.curr).val());
	// cells $flatten\cpu.$logic_and$upstream/picorv32.v:1696$1467 $flatten\cpu.$logic_not$upstream/picorv32.v:1696$1466
	i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1696_24_1467__Y = logic_and<1>(p_cpu_2e_is__lb__lh__lw__lbu__lhu.curr, logic_not<1>(p_cpu_2e_instr__trap));
	// \full_case: 1
	// \parallel_case: 1
	// \src: upstream/picorv32.v:1790.9-1790.9|upstream/picorv32.v:1767.5-1802.12
	// cell $flatten\cpu.$procmux$2618
	i_flatten_5c_cpu_2e__24_auto_24_wreduce_2e_cc_3a_513_3a_run_24_4601.slice<3,0>() = (p_cpu_2e_is__sll__srl__sra.curr ? value<4>{0x4u} : (p_cpu_2e_is__sb__sh__sw.curr ? value<4>{0x2u} : value<4>{0x8u}));
	// connection
	i_flatten_5c_cpu_2e__24_auto_24_wreduce_2e_cc_3a_513_3a_run_24_4601.slice<7,4>() = value<4>{0u};
	// \full_case: 1
	// \src: upstream/picorv32.v:581.20-581.20|upstream/picorv32.v:581.4-636.11
	// cell $flatten\cpu.$procmux$4087_CMP0
	i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_380_24_952__Y = logic_not<1>(p_cpu_2e_mem__state.curr);
	// \src: upstream/picorv32.v:583.10-583.57
	// cell $flatten\cpu.$logic_or$upstream/picorv32.v:583$1032
	i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_380_24_954__Y = logic_or<1>(i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_380_24_953__Y, p_cpu_2e_mem__do__rdata.curr);
	// \src: upstream/picorv32.v:1895.23-1895.49
	// cell $flatten\cpu.$ternary$upstream/picorv32.v:1895$1530
	i_flatten_5c_cpu_2e__24_or_24_upstream_2f_picorv32_2e_v_3a_1521_24_1415__Y.slice<35,33>().concat(i_flatten_5c_cpu_2e__24_or_24_upstream_2f_picorv32_2e_v_3a_1867_24_1517__Y.slice<32>()).concat(i_flatten_5c_cpu_2e__24_or_24_upstream_2f_picorv32_2e_v_3a_1521_24_1415__Y.slice<31,0>()) = (p_cpu_2e_irq__active.curr ? value<36>{0u,0x8u} : value<36>{0u,0u});
	// connection
	i_flatten_5c_cpu_2e__24_or_24_upstream_2f_picorv32_2e_v_3a_1521_24_1415__Y.slice<32>() = value<1>{0x1u};
	// \full_case: 1
	// \src: upstream/picorv32.v:408.7-408.7|upstream/picorv32.v:403.3-427.10
	// cell $flatten\cpu.$procmux$4379_CMP0
	i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1930_24_1548__Y = eq_uu<1>(p_cpu_2e_mem__wordsize.curr, value<1>{0x1u});
	// \full_case: 1
	// \src: upstream/picorv32.v:416.7-416.7|upstream/picorv32.v:403.3-427.10
	// cell $flatten\cpu.$procmux$4387_CMP0
	i_flatten_5c_cpu_2e__24_procmux_24_4372__CMP = eq_uu<1>(p_cpu_2e_mem__wordsize.curr, value<2>{0x2u});
	// \full_case: 1
	// \src: upstream/picorv32.v:403.22-403.22|upstream/picorv32.v:403.3-427.10
	// cell $flatten\cpu.$procmux$4389_CMP0
	i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1923_24_1541__Y = logic_not<1>(p_cpu_2e_mem__wordsize.curr);
	// cell $flatten\cpu.$auto$opt_reduce.cc:131:opt_pmux$4594
	i_flatten_5c_cpu_2e__24_auto_24_opt__reduce_2e_cc_3a_137_3a_opt__pmux_24_4591 = reduce_or<1>(i_flatten_5c_cpu_2e__24_procmux_24_1759__CMP.concat(i_flatten_5c_cpu_2e__24_procmux_24_1737__CMP).val());
	// \full_case: 1
	// \parallel_case: 1
	// \src: upstream/picorv32.v:1757.7-1757.7|upstream/picorv32.v:1486.3-1913.10
	// cell $flatten\cpu.$procmux$2339_CMP0
	i_flatten_5c_cpu_2e__24_procmux_24_1747__CMP = eq_uu<1>(p_cpu_2e_cpu__state.curr, value<5>{0x10u});
	// \full_case: 1
	// \parallel_case: 1
	// \src: upstream/picorv32.v:1577.7-1577.7|upstream/picorv32.v:1486.3-1913.10
	// cell $flatten\cpu.$procmux$2353_CMP0
	i_flatten_5c_cpu_2e__24_procmux_24_1748__CMP = eq_uu<1>(p_cpu_2e_cpu__state.curr, value<6>{0x20u});
	// \full_case: 1
	// \parallel_case: 1
	// \src: upstream/picorv32.v:1827.7-1827.7|upstream/picorv32.v:1486.3-1913.10
	// cell $flatten\cpu.$procmux$2810_CMP0
	i_flatten_5c_cpu_2e__24_procmux_24_2047__CMP = eq_uu<1>(p_cpu_2e_cpu__state.curr, value<3>{0x4u});
	// \full_case: 1
	// \parallel_case: 1
	// \src: upstream/picorv32.v:1803.7-1803.7|upstream/picorv32.v:1486.3-1913.10
	// cell $flatten\cpu.$procmux$2814_CMP0
	i_flatten_5c_cpu_2e__24_procmux_24_1786__CMP = eq_uu<1>(p_cpu_2e_cpu__state.curr, value<4>{0x8u});
	// \src: upstream/picorv32.v:1897.18-1897.39
	// cell $flatten\cpu.$add$upstream/picorv32.v:1897$1535
	i_flatten_5c_cpu_2e__24_add_24_upstream_2f_picorv32_2e_v_3a_1867_24_1518__Y = add_uu<32>(p_cpu_2e_reg__op1.curr, p_cpu_2e_decoded__imm.curr);
	// connection
	i_flatten_5c_cpu_2e__24_or_24_upstream_2f_picorv32_2e_v_3a_1867_24_1517__Y.slice<35,33>().concat(i_flatten_5c_cpu_2e__24_or_24_upstream_2f_picorv32_2e_v_3a_1867_24_1517__Y.slice<31,0>()) = i_flatten_5c_cpu_2e__24_or_24_upstream_2f_picorv32_2e_v_3a_1521_24_1415__Y.slice<35,34>().concat(value<1>{0x1u}).concat(i_flatten_5c_cpu_2e__24_or_24_upstream_2f_picorv32_2e_v_3a_1521_24_1415__Y.slice<31,0>()).val();
	// cells $flatten\cpu.$procmux$2028 $flatten\cpu.$procmux$2025 $flatten\cpu.$procmux$2022 $flatten\cpu.$ternary$upstream/picorv32.v:1500$1404
	i_flatten_5c_cpu_2e__24_3_5c_current__pc_5b_31_3a_0_5d_ = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1313_24_1358__Y ? (p_cpu_2e_latched__branch.curr ? (p_cpu_2e_latched__store.curr ? i_flatten_5c_cpu_2e__24_and_24_upstream_2f_picorv32_2e_v_3a_1500_24_1403__Y.slice<31,1>().concat(value<1>{0u}).val() : p_cpu_2e_reg__next__pc.curr) : p_cpu_2e_reg__next__pc.curr) : value<32>{0u}) : value<32>{0u});
	// connection
	i_flatten_5c_cpu_2e__24_ternary_24_upstream_2f_picorv32_2e_v_3a_1321_24_1363__Y.slice<31,1>() = i_flatten_5c_cpu_2e__24_and_24_upstream_2f_picorv32_2e_v_3a_1500_24_1403__Y.slice<31,1>().val();
	// \src: upstream/picorv32.v:1560.35-1560.59
	// cell $flatten\cpu.$ternary$upstream/picorv32.v:1560$1443
	i_flatten_5c_cpu_2e__24_auto_24_wreduce_2e_cc_3a_513_3a_run_24_4602.slice<2,0>() = (p_cpu_2e_compressed__instr.curr ? value<3>{0x2u} : value<3>{0x4u});
	// connection
	i_flatten_5c_cpu_2e__24_auto_24_wreduce_2e_cc_3a_513_3a_run_24_4602.slice<31,3>() = value<29>{0u};
	// \src: upstream/picorv32.v:1245.23-1245.46
	// cell $flatten\cpu.$logic_or$upstream/picorv32.v:1245$1578
	i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_1245_24_1578__Y = logic_or<1>(p_cpu_2e_instr__sra.curr, p_cpu_2e_instr__srai.curr);
	// \src: upstream/picorv32.v:1846.7-1846.30
	// cell $flatten\cpu.$logic_or$upstream/picorv32.v:1846$1505
	i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_1838_24_1498__Y = logic_or<1>(p_cpu_2e_instr__slli.curr, p_cpu_2e_instr__sll.curr);
	// \src: upstream/picorv32.v:1847.7-1847.30
	// cell $flatten\cpu.$logic_or$upstream/picorv32.v:1847$1507
	i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_1839_24_1500__Y = logic_or<1>(p_cpu_2e_instr__srli.curr, p_cpu_2e_instr__srl.curr);
	// cells $flatten\cpu.$procmux$4381 $flatten\cpu.$procmux$4366 $flatten\cpu.$procmux$4367_CMP0 $flatten\cpu.$procmux$4368_CMP0 $flatten\cpu.$procmux$4369_CMP0 $flatten\cpu.$procmux$4370_CMP0 $flatten\cpu.$procmux$4375 $flatten\cpu.$procmux$4377_CMP0
	p_cpu_2e_mem__rdata__word = (i_flatten_5c_cpu_2e__24_procmux_24_4372__CMP ? (eq_uu<1>(p_cpu_2e_reg__op1.curr.slice<1,0>().val(), value<2>{0x3u}) ? value<24>{0u}.concat(p_cpu_2e_mem__rdata.slice<31,24>()).val() : (eq_uu<1>(p_cpu_2e_reg__op1.curr.slice<1,0>().val(), value<2>{0x2u}) ? value<24>{0u}.concat(p_cpu_2e_mem__rdata.slice<23,16>()).val() : (eq_uu<1>(p_cpu_2e_reg__op1.curr.slice<1,0>().val(), value<1>{0x1u}) ? value<24>{0u}.concat(p_cpu_2e_mem__rdata.slice<15,8>()).val() : (logic_not<1>(p_cpu_2e_reg__op1.curr.slice<1,0>().val()) ? value<24>{0u}.concat(p_cpu_2e_mem__rdata.slice<7,0>()).val() : value<32>{0u})))) : (i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1930_24_1548__Y ? (p_cpu_2e_reg__op1.curr.slice<1>().val() ? value<16>{0u}.concat(p_cpu_2e_mem__rdata.slice<31,16>()).val() : (not_u<1>(p_cpu_2e_reg__op1.curr.slice<1>().val()) ? value<16>{0u}.concat(p_cpu_2e_mem__rdata.slice<15,0>()).val() : value<32>{0u})) : (i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1923_24_1541__Y ? p_cpu_2e_mem__rdata : value<32>{0u})));
	// cells $flatten\cpu.$procmux$3242 $flatten\cpu.$logic_not$upstream/picorv32.v:1260$1332 $flatten\cpu.$logic_not$upstream/picorv32.v:1258$1331 $flatten\cpu.$logic_not$upstream/picorv32.v:1256$1330
	p_cpu_2e_alu__out__0 = (p_cpu_2e_is__sltiu__bltu__sltu.curr ? p_cpu_2e_alu__ltu : (p_cpu_2e_is__slti__blt__slt.curr ? p_cpu_2e_alu__lts : (p_cpu_2e_instr__bgeu.curr ? logic_not<1>(p_cpu_2e_alu__ltu) : (p_cpu_2e_instr__bge.curr ? logic_not<1>(p_cpu_2e_alu__lts) : (p_cpu_2e_instr__bne.curr ? logic_not<1>(p_cpu_2e_alu__eq) : (p_cpu_2e_instr__beq.curr ? p_cpu_2e_alu__eq : value<1>{0u}))))));
	// \full_case: 1
	// \parallel_case: 1
	// \src: upstream/picorv32.v:1790.9-1790.9|upstream/picorv32.v:1767.5-1802.12
	// cell $flatten\cpu.$procmux$2819
	i_flatten_5c_cpu_2e__24_procmux_24_2819__Y = (p_cpu_2e_is__sll__srl__sra.curr ? p_cpu_2e_mem__do__rinst.curr : (p_cpu_2e_is__sb__sh__sw.curr ? value<1>{0x1u} : p_cpu_2e_mem__do__prefetch.curr));
	// \full_case: 1
	// \src: upstream/picorv32.v:1567.10-1567.19|upstream/picorv32.v:1567.6-1575.9
	// cell $flatten\cpu.$procmux$2500
	i_flatten_5c_cpu_2e__24_procmux_24_2500__Y = (p_cpu_2e_instr__jal.curr ? value<1>{0x1u} : value<1>{0u});
	// cells $flatten\cpu.$logic_and$upstream/picorv32.v:379$949 $flatten\cpu.$logic_and$upstream/picorv32.v:379$948
	p_cpu_2e_mem__la__write = logic_and<1>(logic_and<1>(p_cpu_2e_resetn, i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_380_24_952__Y), p_cpu_2e_mem__do__wdata.curr);
	// \src: upstream/picorv32.v:1317.33-1317.54
	// cell $flatten\cpu.$ternary$upstream/picorv32.v:1317$1359
	i_flatten_5c_cpu_2e__24_auto_24_wreduce_2e_cc_3a_513_3a_run_24_4603.slice<2,0>() = (p_cpu_2e_latched__compr.curr ? value<3>{0x2u} : value<3>{0x4u});
	// connection
	i_flatten_5c_cpu_2e__24_auto_24_wreduce_2e_cc_3a_513_3a_run_24_4603.slice<31,3>() = value<29>{0u};
	// \src: upstream/picorv32.v:1895.22-1895.106
	// cell $flatten\cpu.$or$upstream/picorv32.v:1895$1534
	i_flatten_5c_cpu_2e__24_or_24_upstream_2f_picorv32_2e_v_3a_1867_24_1520__Y = or_uu<36>(i_flatten_5c_cpu_2e__24_or_24_upstream_2f_picorv32_2e_v_3a_1521_24_1415__Y.slice<35,34>().concat(value<1>{0x1u}).concat(i_flatten_5c_cpu_2e__24_or_24_upstream_2f_picorv32_2e_v_3a_1867_24_1517__Y.slice<32>()).concat(i_flatten_5c_cpu_2e__24_or_24_upstream_2f_picorv32_2e_v_3a_1521_24_1415__Y.slice<31,0>()).val(), i_flatten_5c_cpu_2e__24_add_24_upstream_2f_picorv32_2e_v_3a_1867_24_1518__Y);
	// \src: upstream/picorv32.v:1835.37-1835.48
	// cell $flatten\cpu.$ge$upstream/picorv32.v:1835$1496
	i_flatten_5c_cpu_2e__24_ge_24_upstream_2f_picorv32_2e_v_3a_1835_24_1496__Y = ge_uu<1>(p_cpu_2e_reg__sh.curr, value<3>{0x4u});
	// memory \cpu.cpuregs read port 0
	auto tmp_0 = memory_index(p_cpu_2e_decoded__rs1.curr, 0, 32);
	CXXRTL_ASSERT(tmp_0.valid && "out of bounds read");
	if(tmp_0.valid) {
		value<32> tmp_1 = memory_p_cpu_2e_cpuregs[tmp_0.index];
		i_flatten_5c_cpu_2e__24_memrd_24__5c_cpuregs_24_upstream_2f_picorv32_2e_v_3a_1352_24_1379__DATA = tmp_1;
	} else {
		i_flatten_5c_cpu_2e__24_memrd_24__5c_cpuregs_24_upstream_2f_picorv32_2e_v_3a_1352_24_1379__DATA = value<32> {};
	}
	// memory \cpu.cpuregs read port 1
	auto tmp_2 = memory_index(p_cpu_2e_decoded__rs2.curr, 0, 32);
	CXXRTL_ASSERT(tmp_2.valid && "out of bounds read");
	if(tmp_2.valid) {
		value<32> tmp_3 = memory_p_cpu_2e_cpuregs[tmp_2.index];
		i_flatten_5c_cpu_2e__24_memrd_24__5c_cpuregs_24_upstream_2f_picorv32_2e_v_3a_1353_24_1382__DATA = tmp_3;
	} else {
		i_flatten_5c_cpu_2e__24_memrd_24__5c_cpuregs_24_upstream_2f_picorv32_2e_v_3a_1353_24_1382__DATA = value<32> {};
	}
	// \src: upstream/picorv32.v:1842.16-1842.26
	// cell $flatten\cpu.$sub$upstream/picorv32.v:1842$1504
	i_flatten_5c_cpu_2e__24_auto_24_wreduce_2e_cc_3a_513_3a_run_24_4600.slice<4,0>() = sub_uu<5>(p_cpu_2e_reg__sh.curr, value<3>{0x4u});
	// \src: upstream/picorv32.v:1850.16-1850.26
	// cell $flatten\cpu.$sub$upstream/picorv32.v:1850$1511
	i_flatten_5c_cpu_2e__24_auto_24_wreduce_2e_cc_3a_513_3a_run_24_4599.slice<4,0>() = sub_uu<5>(p_cpu_2e_reg__sh.curr, value<1>{0x1u});
	// \full_case: 1
	// \parallel_case: 1
	// \src: upstream/picorv32.v:1486.19-1486.19|upstream/picorv32.v:1486.3-1913.10
	// cell $flatten\cpu.$procmux$2366_CMP0
	i_flatten_5c_cpu_2e__24_procmux_24_2052__CMP = eq_uu<1>(p_cpu_2e_cpu__state.curr, value<8>{0x80u});
	// \src: upstream/picorv32.v:1446.22-1446.46
	// cell $flatten\cpu.$logic_and$upstream/picorv32.v:1446$1397
	i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1446_24_1397__Y = logic_and<1>(p_cpu_2e_mem__do__rinst.curr, p_cpu_2e_mem__done);
	// cells $flatten\cpu.$procmux$2666 $flatten\cpu.$procmux$2596 $flatten\cpu.$procmux$2656 $flatten\cpu.$procmux$2654 $flatten\cpu.$procmux$2637 $flatten\cpu.$procmux$2611 $flatten\cpu.$procmux$2609 $flatten\cpu.$procmux$2605 $flatten\cpu.$procmux$2601 $flatten\cpu.$procmux$2599
	i_flatten_5c_cpu_2e__24_procmux_24_2666__Y = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1313_24_1358__Y ? (p_cpu_2e_decoder__trigger.curr ? (p_cpu_2e_instr__jal.curr ? p_cpu_2e_cpu__state.curr : value<8>{0x20u}) : p_cpu_2e_cpu__state.curr) : (i_flatten_5c_cpu_2e__24_procmux_24_1748__CMP ? (p_cpu_2e_instr__trap ? value<8>{0x80u} : (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1696_24_1467__Y ? value<8>{0x1u} : (p_cpu_2e_is__slli__srli__srai.curr ? value<8>{0x4u} : (i_flatten_5c_cpu_2e__24_auto_24_opt__reduce_2e_cc_3a_137_3a_opt__pmux_24_4569 ? value<8>{0x8u} : value<4>{0u}.concat(i_flatten_5c_cpu_2e__24_auto_24_wreduce_2e_cc_3a_513_3a_run_24_4601.slice<3,0>()).val())))) : (i_flatten_5c_cpu_2e__24_procmux_24_1747__CMP ? value<4>{0u}.concat(i_flatten_5c_cpu_2e__24_auto_24_wreduce_2e_cc_3a_513_3a_run_24_4601.slice<3,0>()).val() : (i_flatten_5c_cpu_2e__24_procmux_24_1786__CMP ? (p_cpu_2e_is__beq__bne__blt__bge__bltu__bgeu.curr ? (p_cpu_2e_mem__done ? value<8>{0x40u} : p_cpu_2e_cpu__state.curr) : value<8>{0x40u}) : (i_flatten_5c_cpu_2e__24_procmux_24_2047__CMP ? (i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1831_24_1495__Y ? value<8>{0x40u} : p_cpu_2e_cpu__state.curr) : (i_flatten_5c_cpu_2e__24_auto_24_opt__reduce_2e_cc_3a_137_3a_opt__pmux_24_4591 ? (i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_1857_24_1513__Y ? (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1872_24_1523__Y ? value<8>{0x40u} : p_cpu_2e_cpu__state.curr) : p_cpu_2e_cpu__state.curr) : p_cpu_2e_cpu__state.curr)))))) : value<8>{0x40u});
	// \src: upstream/picorv32.v:1102.5-1102.33
	// cell $flatten\cpu.$eq$upstream/picorv32.v:1102$1298
	i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1040_24_1134__Y = logic_not<1>(p_cpu_2e_mem__rdata__q.curr.slice<14,12>().val());
	// \src: upstream/picorv32.v:1111.5-1111.33
	// cell $flatten\cpu.$eq$upstream/picorv32.v:1111$1308
	i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1041_24_1136__Y = eq_uu<1>(p_cpu_2e_mem__rdata__q.curr.slice<14,12>().val(), value<1>{0x1u});
	// \src: upstream/picorv32.v:1103.5-1103.33
	// cell $flatten\cpu.$eq$upstream/picorv32.v:1103$1297
	i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1049_24_1150__Y = eq_uu<1>(p_cpu_2e_mem__rdata__q.curr.slice<14,12>().val(), value<2>{0x2u});
	// \src: upstream/picorv32.v:1104.5-1104.33
	// cell $flatten\cpu.$eq$upstream/picorv32.v:1104$1296
	i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1059_24_1166__Y = eq_uu<1>(p_cpu_2e_mem__rdata__q.curr.slice<14,12>().val(), value<2>{0x3u});
	// \src: upstream/picorv32.v:1105.5-1105.33
	// cell $flatten\cpu.$eq$upstream/picorv32.v:1105$1295
	i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1042_24_1138__Y = eq_uu<1>(p_cpu_2e_mem__rdata__q.curr.slice<14,12>().val(), value<3>{0x4u});
	// \src: upstream/picorv32.v:1112.5-1112.33
	// cell $flatten\cpu.$eq$upstream/picorv32.v:1112$1305
	i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1043_24_1140__Y = eq_uu<1>(p_cpu_2e_mem__rdata__q.curr.slice<14,12>().val(), value<3>{0x5u});
	// \src: upstream/picorv32.v:1106.5-1106.33
	// cell $flatten\cpu.$eq$upstream/picorv32.v:1106$1294
	i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1044_24_1142__Y = eq_uu<1>(p_cpu_2e_mem__rdata__q.curr.slice<14,12>().val(), value<3>{0x6u});
	// \src: upstream/picorv32.v:1107.5-1107.33
	// cell $flatten\cpu.$eq$upstream/picorv32.v:1107$1293
	i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1045_24_1144__Y = eq_uu<1>(p_cpu_2e_mem__rdata__q.curr.slice<14,12>().val(), value<3>{0x7u});
	// \src: upstream/picorv32.v:1111.37-1111.69
	// cell $flatten\cpu.$eq$upstream/picorv32.v:1111$1309
	i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1064_24_1176__Y = logic_not<1>(p_cpu_2e_mem__rdata__q.curr.slice<31,25>().val());
	// \src: upstream/picorv32.v:1113.37-1113.69
	// cell $flatten\cpu.$eq$upstream/picorv32.v:1113$1303
	i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1066_24_1184__Y = eq_uu<1>(p_cpu_2e_mem__rdata__q.curr.slice<31,25>().val(), value<6>{0x20u});
	// cells $flatten\cpu.$logic_or$upstream/picorv32.v:574$1029 $flatten\cpu.$logic_and$upstream/picorv32.v:380$965 $flatten\cpu.$logic_and$upstream/picorv32.v:380$955
	i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_574_24_1029__Y = logic_or<1>(logic_and<1>(p_cpu_2e_resetn, logic_and<1>(i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_380_24_952__Y, i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_380_24_954__Y)), p_cpu_2e_mem__la__write);
	// cells $flatten\cpu.$ternary$upstream/picorv32.v:1353$1384 $flatten\cpu.$reduce_bool$upstream/picorv32.v:1353$1383
	p_cpu_2e_cpuregs__rs2 = (reduce_bool<1>(p_cpu_2e_decoded__rs2.curr) ? i_flatten_5c_cpu_2e__24_memrd_24__5c_cpuregs_24_upstream_2f_picorv32_2e_v_3a_1353_24_1382__DATA : value<32>{0u});
	// \src: upstream/picorv32.v:1949.7-1949.14
	// cell $flatten\cpu.$logic_not$upstream/picorv32.v:1949$1567
	i_flatten_5c_cpu_2e__24_logic__not_24_upstream_2f_picorv32_2e_v_3a_1949_24_1567__Y = logic_not<1>(p_cpu_2e_resetn);
	// cells $flatten\cpu.$procmux$2105 $flatten\cpu.$procmux$2103
	i_flatten_5c_cpu_2e__24_3_5c_set__mem__do__rdata_5b_0_3a_0_5d_ = (i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_1857_24_1513__Y ? (p_cpu_2e_mem__do__rdata.curr ? value<1>{0u} : value<1>{0x1u}) : value<1>{0u});
	// cells $flatten\cpu.$procmux$1756 $flatten\cpu.$procmux$1806
	i_flatten_5c_cpu_2e__24_3_5c_set__mem__do__wdata_5b_0_3a_0_5d_ = (i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_1857_24_1513__Y ? (p_cpu_2e_mem__do__wdata.curr ? value<1>{0u} : value<1>{0x1u}) : value<1>{0u});
	// \src: upstream/picorv32.v:384.39-384.96
	// cell $flatten\cpu.$ternary$upstream/picorv32.v:384$970
	p_cpu_2e_mem__rdata__latched = (p_cpu_2e_mem__xfer ? p_cpu_2e_mem__rdata : p_cpu_2e_mem__rdata__q.curr);
	// \src: upstream/picorv32.v:1069.19-1069.65
	// cell $flatten\cpu.$logic_and$upstream/picorv32.v:1069$1191
	i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1068_24_1187__Y = logic_and<1>(p_cpu_2e_is__alu__reg__reg.curr, i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1040_24_1134__Y);
	// \src: upstream/picorv32.v:1075.19-1075.65
	// cell $flatten\cpu.$logic_and$upstream/picorv32.v:1075$1215
	i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1074_24_1211__Y = logic_and<1>(p_cpu_2e_is__alu__reg__reg.curr, i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1043_24_1140__Y);
	// \full_case: 1
	// \src: upstream/picorv32.v:620.8-620.8|upstream/picorv32.v:581.4-636.11
	// cell $flatten\cpu.$procmux$4076_CMP0
	i_flatten_5c_cpu_2e__24_procmux_24_4076__CMP = eq_uu<1>(p_cpu_2e_mem__state.curr, value<2>{0x2u});
	// \full_case: 1
	// \src: upstream/picorv32.v:594.8-594.8|upstream/picorv32.v:581.4-636.11
	// cell $flatten\cpu.$procmux$4082_CMP0
	i_flatten_5c_cpu_2e__24_procmux_24_4082__CMP = eq_uu<1>(p_cpu_2e_mem__state.curr, value<1>{0x1u});
	// cells $flatten\cpu.$procmux$4093 $flatten\cpu.$and$upstream/picorv32.v:576$1030 $flatten\cpu.$procmux$4386 $flatten\cpu.$shl$upstream/picorv32.v:419$984 $flatten\cpu.$ternary$upstream/picorv32.v:411$983
	i_flatten_5c_cpu_2e__24_procmux_24_4093__Y = (i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_574_24_1029__Y ? and_uu<4>((i_flatten_5c_cpu_2e__24_procmux_24_4372__CMP ? shl_uu<4>(value<1>{0x1u}, p_cpu_2e_reg__op1.curr.slice<1,0>().val()) : (i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1930_24_1548__Y ? (p_cpu_2e_reg__op1.curr.slice<1>().val() ? value<4>{0xcu} : value<4>{0x3u}) : (i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1923_24_1541__Y ? value<4>{0xfu} : value<4>{0u}))), p_cpu_2e_mem__la__write.repeat<4>().val()) : p_cpu_2e_mem__wstrb.curr);
	// \src: upstream/picorv32.v:1949.7-1949.26
	// cell $flatten\cpu.$logic_or$upstream/picorv32.v:1949$1568
	i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_1949_24_1568__Y = logic_or<1>(i_flatten_5c_cpu_2e__24_logic__not_24_upstream_2f_picorv32_2e_v_3a_1949_24_1567__Y, p_cpu_2e_mem__done);
	// cells $flatten\cpu.$logic_and$upstream/picorv32.v:1037$1133 $flatten\cpu.$logic_not$upstream/picorv32.v:1037$1132
	i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y = logic_and<1>(p_cpu_2e_decoder__trigger.curr, logic_not<1>(p_cpu_2e_decoder__pseudo__trigger.curr));
	// \src: upstream/picorv32.v:1066.19-1066.65
	// cell $flatten\cpu.$logic_and$upstream/picorv32.v:1066$1183
	i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1065_24_1179__Y = logic_and<1>(p_cpu_2e_is__alu__reg__imm.curr, i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1043_24_1140__Y);
	// cells $flatten\cpu.$reduce_or$upstream/picorv32.v:1110$1311 $flatten\cpu.$logic_and$upstream/picorv32.v:1113$1304 $flatten\cpu.$logic_and$upstream/picorv32.v:1112$1307 $flatten\cpu.$logic_and$upstream/picorv32.v:1111$1310
	i_flatten_5c_cpu_2e__24_reduce__or_24_upstream_2f_picorv32_2e_v_3a_1095_24_1291__Y = reduce_or<1>(logic_and<1>(i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1041_24_1136__Y, i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1064_24_1176__Y).concat(logic_and<1>(i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1043_24_1140__Y, i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1064_24_1176__Y)).concat(logic_and<1>(i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1043_24_1140__Y, i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1066_24_1184__Y)).val());
	// \src: upstream/picorv32.v:566.7-566.22
	// cell $flatten\cpu.$logic_or$upstream/picorv32.v:566$1025
	i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_566_24_1025__Y = logic_or<1>(i_flatten_5c_cpu_2e__24_logic__not_24_upstream_2f_picorv32_2e_v_3a_1949_24_1567__Y, p_cpu_2e_trap.curr);
	// connection
	p_cpu_2e_clk = p_clk;
	// \src: upstream/picorv32.v:866.7-866.31|upstream/picorv32.v:866.3-1035.6
	// cell $flatten\cpu.$procmux$3318
	i_flatten_5c_cpu_2e__24_0_5c_decoded__rs1_5b_4_3a_0_5d_.slice<4>() = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1446_24_1397__Y ? p_cpu_2e_mem__rdata__latched.slice<19>().val() : p_cpu_2e_decoded__rs1.curr.slice<4>().val());
	// \src: upstream/picorv32.v:866.7-866.31|upstream/picorv32.v:866.3-1035.6
	// cell $flatten\cpu.$procmux$3405
	i_flatten_5c_cpu_2e__24_0_5c_decoded__rs1_5b_4_3a_0_5d_.slice<3,0>() = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1446_24_1397__Y ? p_cpu_2e_mem__rdata__latched.slice<18,15>().val() : p_cpu_2e_decoded__rs1.curr.slice<3,0>().val());
	// \src: upstream/picorv32.v:866.7-866.31|upstream/picorv32.v:866.3-1035.6
	// cell $flatten\cpu.$procmux$3322
	i_flatten_5c_cpu_2e__24_0_5c_decoded__imm__j_5b_31_3a_0_5d_.slice<10>() = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1446_24_1397__Y ? p_cpu_2e_mem__rdata__latched.slice<30>().val() : p_cpu_2e_decoded__imm__j.curr.slice<10>().val());
	// \src: upstream/picorv32.v:866.7-866.31|upstream/picorv32.v:866.3-1035.6
	// cell $flatten\cpu.$procmux$3326
	i_flatten_5c_cpu_2e__24_0_5c_decoded__imm__j_5b_31_3a_0_5d_.slice<7>() = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1446_24_1397__Y ? p_cpu_2e_mem__rdata__latched.slice<27>().val() : p_cpu_2e_decoded__imm__j.curr.slice<7>().val());
	// \src: upstream/picorv32.v:866.7-866.31|upstream/picorv32.v:866.3-1035.6
	// cell $flatten\cpu.$procmux$3330
	i_flatten_5c_cpu_2e__24_0_5c_decoded__imm__j_5b_31_3a_0_5d_.slice<6>() = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1446_24_1397__Y ? p_cpu_2e_mem__rdata__latched.slice<26>().val() : p_cpu_2e_decoded__imm__j.curr.slice<6>().val());
	// \src: upstream/picorv32.v:866.7-866.31|upstream/picorv32.v:866.3-1035.6
	// cell $flatten\cpu.$procmux$3334
	i_flatten_5c_cpu_2e__24_0_5c_decoded__imm__j_5b_31_3a_0_5d_.slice<3,1>() = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1446_24_1397__Y ? p_cpu_2e_mem__rdata__latched.slice<23,21>().val() : p_cpu_2e_decoded__imm__j.curr.slice<3,1>().val());
	// \src: upstream/picorv32.v:866.7-866.31|upstream/picorv32.v:866.3-1035.6
	// cell $flatten\cpu.$procmux$3338
	i_flatten_5c_cpu_2e__24_0_5c_decoded__imm__j_5b_31_3a_0_5d_.slice<5>() = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1446_24_1397__Y ? p_cpu_2e_mem__rdata__latched.slice<25>().val() : p_cpu_2e_decoded__imm__j.curr.slice<5>().val());
	// \src: upstream/picorv32.v:866.7-866.31|upstream/picorv32.v:866.3-1035.6
	// cell $flatten\cpu.$procmux$3342
	i_flatten_5c_cpu_2e__24_0_5c_decoded__imm__j_5b_31_3a_0_5d_.slice<9,8>() = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1446_24_1397__Y ? p_cpu_2e_mem__rdata__latched.slice<29,28>().val() : p_cpu_2e_decoded__imm__j.curr.slice<9,8>().val());
	// \src: upstream/picorv32.v:866.7-866.31|upstream/picorv32.v:866.3-1035.6
	// cell $flatten\cpu.$procmux$3346
	i_flatten_5c_cpu_2e__24_0_5c_decoded__imm__j_5b_31_3a_0_5d_.slice<31,20>() = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1446_24_1397__Y ? p_cpu_2e_mem__rdata__latched.slice<31>().val().repeat<12>().val() : p_cpu_2e_decoded__imm__j.curr.slice<31,20>().val());
	// \src: upstream/picorv32.v:866.7-866.31|upstream/picorv32.v:866.3-1035.6
	// cell $flatten\cpu.$procmux$3350
	i_flatten_5c_cpu_2e__24_0_5c_decoded__imm__j_5b_31_3a_0_5d_.slice<4>() = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1446_24_1397__Y ? p_cpu_2e_mem__rdata__latched.slice<24>().val() : p_cpu_2e_decoded__imm__j.curr.slice<4>().val());
	// \src: upstream/picorv32.v:866.7-866.31|upstream/picorv32.v:866.3-1035.6
	// cell $flatten\cpu.$procmux$3354
	i_flatten_5c_cpu_2e__24_0_5c_decoded__imm__j_5b_31_3a_0_5d_.slice<11>() = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1446_24_1397__Y ? p_cpu_2e_mem__rdata__latched.slice<20>().val() : p_cpu_2e_decoded__imm__j.curr.slice<11>().val());
	// \src: upstream/picorv32.v:866.7-866.31|upstream/picorv32.v:866.3-1035.6
	// cell $flatten\cpu.$procmux$3357
	i_flatten_5c_cpu_2e__24_0_5c_decoded__imm__j_5b_31_3a_0_5d_.slice<0>() = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1446_24_1397__Y ? value<1>{0u} : p_cpu_2e_decoded__imm__j.curr.slice<0>().val());
	// \src: upstream/picorv32.v:866.7-866.31|upstream/picorv32.v:866.3-1035.6
	// cell $flatten\cpu.$procmux$3559
	i_flatten_5c_cpu_2e__24_0_5c_decoded__imm__j_5b_31_3a_0_5d_.slice<19,12>() = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1446_24_1397__Y ? p_cpu_2e_mem__rdata__latched.slice<19,12>().val() : p_cpu_2e_decoded__imm__j.curr.slice<19,12>().val());
	// \src: upstream/picorv32.v:431.7-431.15|upstream/picorv32.v:431.3-434.6
	// cell $flatten\cpu.$procmux$4148
	i_flatten_5c_cpu_2e__24_0_5c_mem__rdata__q_5b_31_3a_0_5d_.slice<31>() = (p_cpu_2e_mem__xfer ? p_cpu_2e_mem__rdata.slice<31>().val() : p_cpu_2e_mem__rdata__q.curr.slice<31>().val());
	// \src: upstream/picorv32.v:431.7-431.15|upstream/picorv32.v:431.3-434.6
	// cell $flatten\cpu.$procmux$4190
	i_flatten_5c_cpu_2e__24_0_5c_mem__rdata__q_5b_31_3a_0_5d_.slice<7>() = (p_cpu_2e_mem__xfer ? p_cpu_2e_mem__rdata.slice<7>().val() : p_cpu_2e_mem__rdata__q.curr.slice<7>().val());
	// \src: upstream/picorv32.v:431.7-431.15|upstream/picorv32.v:431.3-434.6
	// cell $flatten\cpu.$procmux$4205
	i_flatten_5c_cpu_2e__24_0_5c_mem__rdata__q_5b_31_3a_0_5d_.slice<24,20>() = (p_cpu_2e_mem__xfer ? p_cpu_2e_mem__rdata.slice<24,20>().val() : p_cpu_2e_mem__rdata__q.curr.slice<24,20>().val());
	// \src: upstream/picorv32.v:431.7-431.15|upstream/picorv32.v:431.3-434.6
	// cell $flatten\cpu.$procmux$4237
	i_flatten_5c_cpu_2e__24_0_5c_mem__rdata__q_5b_31_3a_0_5d_.slice<19,15>() = (p_cpu_2e_mem__xfer ? p_cpu_2e_mem__rdata.slice<19,15>().val() : p_cpu_2e_mem__rdata__q.curr.slice<19,15>().val());
	// \src: upstream/picorv32.v:431.7-431.15|upstream/picorv32.v:431.3-434.6
	// cell $flatten\cpu.$procmux$4252
	i_flatten_5c_cpu_2e__24_0_5c_mem__rdata__q_5b_31_3a_0_5d_.slice<6,0>() = (p_cpu_2e_mem__xfer ? p_cpu_2e_mem__rdata.slice<6,0>().val() : p_cpu_2e_mem__rdata__q.curr.slice<6,0>().val());
	// \src: upstream/picorv32.v:431.7-431.15|upstream/picorv32.v:431.3-434.6
	// cell $flatten\cpu.$procmux$4254
	i_flatten_5c_cpu_2e__24_0_5c_mem__rdata__q_5b_31_3a_0_5d_.slice<14,12>() = (p_cpu_2e_mem__xfer ? p_cpu_2e_mem__rdata.slice<14,12>().val() : p_cpu_2e_mem__rdata__q.curr.slice<14,12>().val());
	// \src: upstream/picorv32.v:431.7-431.15|upstream/picorv32.v:431.3-434.6
	// cell $flatten\cpu.$procmux$4305
	i_flatten_5c_cpu_2e__24_0_5c_mem__rdata__q_5b_31_3a_0_5d_.slice<11,8>() = (p_cpu_2e_mem__xfer ? p_cpu_2e_mem__rdata.slice<11,8>().val() : p_cpu_2e_mem__rdata__q.curr.slice<11,8>().val());
	// \src: upstream/picorv32.v:431.7-431.15|upstream/picorv32.v:431.3-434.6
	// cell $flatten\cpu.$procmux$4320
	i_flatten_5c_cpu_2e__24_0_5c_mem__rdata__q_5b_31_3a_0_5d_.slice<30,25>() = (p_cpu_2e_mem__xfer ? p_cpu_2e_mem__rdata.slice<30,25>().val() : p_cpu_2e_mem__rdata__q.curr.slice<30,25>().val());
	// memory \cpu.cpuregs write port 0
	if (posedge_p_clk) {
		// \full_case: 1
		// \src: upstream/picorv32.v:1338.7-1338.44|upstream/picorv32.v:1338.3-1344.42
		// cell $flatten\cpu.$procmux$3200
		auto tmp_4 = memory_index((i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1338_24_1374__Y ? p_cpu_2e_latched__rd.curr : value<5>{0u}), 0, 32);
		CXXRTL_ASSERT(tmp_4.valid && "out of bounds write");
		if (tmp_4.valid) {
			// cells $flatten\cpu.$procmux$3197 $flatten\cpu.$procmux$3221 $flatten\cpu.$procmux$3213 $flatten\cpu.$add$upstream/picorv32.v:1317$1360
			memory_p_cpu_2e_cpuregs.update(tmp_4.index, (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1338_24_1374__Y ? (i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1313_24_1358__Y ? (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1320_24_1362__Y ? i_flatten_5c_cpu_2e__24_and_24_upstream_2f_picorv32_2e_v_3a_1500_24_1403__Y.slice<31,1>().concat(i_flatten_5c_cpu_2e__24_ternary_24_upstream_2f_picorv32_2e_v_3a_1321_24_1363__Y.slice<0>()).val() : (p_cpu_2e_latched__branch.curr ? add_uu<32>(p_cpu_2e_reg__pc.curr, i_flatten_5c_cpu_2e__24_auto_24_wreduce_2e_cc_3a_513_3a_run_24_4603.slice<2,0>().val()) : value<32>{0u})) : value<32>{0u}) : value<32>{0u}), i_flatten_5c_cpu_2e__24_0_24_memwr_24__5c_cpuregs_24_upstream_2f_picorv32_2e_v_3a_1344_24_902__EN_5b_31_3a_0_5d__24_1372.curr.slice<0>().val().repeat<32>().val(), 0);
		}
	}
	// cells $flatten\cpu.$procdff$4412 $flatten\cpu.$procmux$2368 $flatten\cpu.$procmux$2365
	if (posedge_p_clk) {
		p_cpu_2e_trap.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_procmux_24_2052__CMP ? value<1>{0x1u} : value<1>{0u}) : value<1>{0u});
	}
	// cells $flatten\cpu.$procdff$4413 $flatten\cpu.$procmux$3191
	if (posedge_p_clk) {
		p_cpu_2e_pcpi__valid.next = (p_cpu_2e_resetn ? p_cpu_2e_pcpi__valid.curr : value<1>{0u});
	}
	// cells $flatten\cpu.$procdff$4414 $flatten\cpu.$procmux$3170
	if (posedge_p_clk) {
		p_cpu_2e_eoi.next = (p_cpu_2e_resetn ? p_cpu_2e_eoi.curr : value<32>{0u});
	}
	// cells $flatten\cpu.$procdff$4415 $flatten\cpu.$procmux$2121 $flatten\cpu.$procmux$2107 $flatten\cpu.$procmux$2117
	if (posedge_p_clk) {
		p_cpu_2e_trace__valid.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_procmux_24_1737__CMP ? i_flatten_5c_cpu_2e__24_3_5c_set__mem__do__rdata_5b_0_3a_0_5d_ : (i_flatten_5c_cpu_2e__24_procmux_24_1759__CMP ? i_flatten_5c_cpu_2e__24_3_5c_set__mem__do__wdata_5b_0_3a_0_5d_ : (i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1313_24_1358__Y ? (p_cpu_2e_latched__trace.curr ? value<1>{0x1u} : value<1>{0u}) : value<1>{0u}))) : value<1>{0u});
	}
	// cells $flatten\cpu.$procdff$4416 $flatten\cpu.$procmux$3147 $flatten\cpu.$procmux$3130 $flatten\cpu.$procmux$3128 $flatten\cpu.$procmux$3126 $flatten\cpu.$procmux$3137 $flatten\cpu.$procmux$3135 $flatten\cpu.$procmux$3143 $flatten\cpu.$procmux$3141 $flatten\cpu.$or$upstream/picorv32.v:1523$1421 $flatten\cpu.$or$upstream/picorv32.v:1521$1417
	if (posedge_p_clk) {
		p_cpu_2e_trace__data.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_procmux_24_1737__CMP ? (i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_1857_24_1513__Y ? (p_cpu_2e_mem__do__rdata.curr ? p_cpu_2e_trace__data.curr : i_flatten_5c_cpu_2e__24_or_24_upstream_2f_picorv32_2e_v_3a_1867_24_1520__Y) : p_cpu_2e_trace__data.curr) : (i_flatten_5c_cpu_2e__24_procmux_24_1759__CMP ? (i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_1857_24_1513__Y ? (p_cpu_2e_mem__do__wdata.curr ? p_cpu_2e_trace__data.curr : i_flatten_5c_cpu_2e__24_or_24_upstream_2f_picorv32_2e_v_3a_1867_24_1520__Y) : p_cpu_2e_trace__data.curr) : (i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1313_24_1358__Y ? (p_cpu_2e_latched__trace.curr ? (p_cpu_2e_latched__branch.curr ? or_uu<36>(i_flatten_5c_cpu_2e__24_or_24_upstream_2f_picorv32_2e_v_3a_1521_24_1415__Y.slice<35,33>().concat(value<1>{0x1u}).concat(i_flatten_5c_cpu_2e__24_or_24_upstream_2f_picorv32_2e_v_3a_1521_24_1415__Y.slice<31,0>()).val(), i_flatten_5c_cpu_2e__24_3_5c_current__pc_5b_31_3a_0_5d_.slice<31,1>().concat(value<1>{0u}).val()) : or_uu<36>(i_flatten_5c_cpu_2e__24_or_24_upstream_2f_picorv32_2e_v_3a_1521_24_1415__Y.slice<35,33>().concat(i_flatten_5c_cpu_2e__24_or_24_upstream_2f_picorv32_2e_v_3a_1867_24_1517__Y.slice<32>()).concat(i_flatten_5c_cpu_2e__24_or_24_upstream_2f_picorv32_2e_v_3a_1521_24_1415__Y.slice<31,0>()).val(), i_flatten_5c_cpu_2e__24_and_24_upstream_2f_picorv32_2e_v_3a_1500_24_1403__Y.slice<31,1>().concat(i_flatten_5c_cpu_2e__24_ternary_24_upstream_2f_picorv32_2e_v_3a_1321_24_1363__Y.slice<0>()).val())) : p_cpu_2e_trace__data.curr) : p_cpu_2e_trace__data.curr))) : p_cpu_2e_trace__data.curr);
	}
	// cells $flatten\cpu.$procdff$4419 $flatten\cpu.$procmux$3120 $flatten\cpu.$procmux$3117
	if (posedge_p_clk) {
		p_cpu_2e_reg__pc.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1313_24_1358__Y ? i_flatten_5c_cpu_2e__24_3_5c_current__pc_5b_31_3a_0_5d_ : p_cpu_2e_reg__pc.curr) : value<32>{0u});
	}
	// cells $flatten\cpu.$procdff$4420 $flatten\cpu.$procmux$3108 $flatten\cpu.$procmux$3105 $flatten\cpu.$procmux$3094 $flatten\cpu.$procmux$3092 $flatten\cpu.$add$upstream/picorv32.v:1560$1444 $flatten\cpu.$add$upstream/picorv32.v:1569$1445
	if (posedge_p_clk) {
		p_cpu_2e_reg__next__pc.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1313_24_1358__Y ? (p_cpu_2e_decoder__trigger.curr ? (p_cpu_2e_instr__jal.curr ? add_uu<32>(i_flatten_5c_cpu_2e__24_3_5c_current__pc_5b_31_3a_0_5d_, p_cpu_2e_decoded__imm__j.curr) : add_uu<32>(i_flatten_5c_cpu_2e__24_3_5c_current__pc_5b_31_3a_0_5d_, i_flatten_5c_cpu_2e__24_auto_24_wreduce_2e_cc_3a_513_3a_run_24_4602.slice<2,0>().val())) : i_flatten_5c_cpu_2e__24_3_5c_current__pc_5b_31_3a_0_5d_) : p_cpu_2e_reg__next__pc.curr) : value<32>{0u});
	}
	// cells $flatten\cpu.$procdff$4421 $flatten\cpu.$procmux$3082 $flatten\cpu.$procmux$3041 $flatten\cpu.$procmux$3039 $flatten\cpu.$procmux$3037 $flatten\cpu.$procmux$3047 $flatten\cpu.$procmux$3045 $flatten\cpu.$procmux$3064 $flatten\cpu.$procmux$3061 $flatten\cpu.$procmux$3051 $flatten\cpu.$procmux$3057 $flatten\cpu.$procmux$3071 $flatten\cpu.$ternary$upstream/picorv32.v:1352$1381 $flatten\cpu.$reduce_bool$upstream/picorv32.v:1352$1380 $flatten\cpu.$ternary$upstream/picorv32.v:1642$1457
	if (posedge_p_clk) {
		p_cpu_2e_reg__op1.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_procmux_24_1737__CMP ? (i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_1857_24_1513__Y ? (p_cpu_2e_mem__do__rdata.curr ? p_cpu_2e_reg__op1.curr : i_flatten_5c_cpu_2e__24_add_24_upstream_2f_picorv32_2e_v_3a_1867_24_1518__Y) : p_cpu_2e_reg__op1.curr) : (i_flatten_5c_cpu_2e__24_procmux_24_1759__CMP ? (i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_1857_24_1513__Y ? (p_cpu_2e_mem__do__wdata.curr ? p_cpu_2e_reg__op1.curr : i_flatten_5c_cpu_2e__24_add_24_upstream_2f_picorv32_2e_v_3a_1867_24_1518__Y) : p_cpu_2e_reg__op1.curr) : (i_flatten_5c_cpu_2e__24_procmux_24_2047__CMP ? (i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1831_24_1495__Y ? p_cpu_2e_reg__op1.curr : (i_flatten_5c_cpu_2e__24_ge_24_upstream_2f_picorv32_2e_v_3a_1835_24_1496__Y ? (i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_1245_24_1578__Y ? p_cpu_2e_reg__op1.curr.slice<31>().val().repeat<4>().concat(p_cpu_2e_reg__op1.curr.slice<31,4>()).val() : (i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_1839_24_1500__Y ? value<4>{0u}.concat(p_cpu_2e_reg__op1.curr.slice<31,4>()).val() : (i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_1838_24_1498__Y ? p_cpu_2e_reg__op1.curr.slice<27,0>().concat(value<4>{0u}).val() : p_cpu_2e_reg__op1.curr))) : (i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_1245_24_1578__Y ? p_cpu_2e_reg__op1.curr.slice<31>().concat(p_cpu_2e_reg__op1.curr.slice<31,1>()).val() : (i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_1839_24_1500__Y ? value<1>{0u}.concat(p_cpu_2e_reg__op1.curr.slice<31,1>()).val() : (i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_1838_24_1498__Y ? p_cpu_2e_reg__op1.curr.slice<30,0>().concat(value<1>{0u}).val() : p_cpu_2e_reg__op1.curr))))) : (i_flatten_5c_cpu_2e__24_procmux_24_1748__CMP ? (p_cpu_2e_is__lui__auipc__jal.curr ? (p_cpu_2e_instr__lui.curr ? value<32>{0u} : p_cpu_2e_reg__pc.curr) : (p_cpu_2e_instr__trap ? value<32>{0u} : (reduce_bool<1>(p_cpu_2e_decoded__rs1.curr) ? i_flatten_5c_cpu_2e__24_memrd_24__5c_cpuregs_24_upstream_2f_picorv32_2e_v_3a_1352_24_1379__DATA : value<32>{0u}))) : p_cpu_2e_reg__op1.curr)))) : p_cpu_2e_reg__op1.curr);
	}
	// cells $flatten\cpu.$procdff$4422 $flatten\cpu.$procmux$3032 $flatten\cpu.$procmux$3015 $flatten\cpu.$procmux$3018 $flatten\cpu.$auto$opt_reduce.cc:131:opt_pmux$4574
	if (posedge_p_clk) {
		p_cpu_2e_reg__op2.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_procmux_24_1747__CMP ? p_cpu_2e_cpuregs__rs2 : (i_flatten_5c_cpu_2e__24_procmux_24_1748__CMP ? (reduce_or<1>(i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1696_24_1467__Y.concat(p_cpu_2e_is__slli__srli__srai.curr).concat(p_cpu_2e_instr__trap).val()) ? value<32>{0u} : (i_flatten_5c_cpu_2e__24_auto_24_opt__reduce_2e_cc_3a_137_3a_opt__pmux_24_4569 ? p_cpu_2e_decoded__imm.curr : p_cpu_2e_cpuregs__rs2)) : p_cpu_2e_reg__op2.curr)) : p_cpu_2e_reg__op2.curr);
	}
	// cells $flatten\cpu.$procdff$4423 $flatten\cpu.$procmux$2326 $flatten\cpu.$procmux$2280 $flatten\cpu.$add$upstream/picorv32.v:1806$1490 $flatten\cpu.$procmux$2284 $flatten\cpu.$procmux$2278 $flatten\cpu.$procmux$2276 $flatten\cpu.$procmux$2272
	if (posedge_p_clk) {
		p_cpu_2e_reg__out.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_procmux_24_1786__CMP ? add_uu<32>(p_cpu_2e_reg__pc.curr, p_cpu_2e_decoded__imm.curr) : (i_flatten_5c_cpu_2e__24_procmux_24_2047__CMP ? (i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1831_24_1495__Y ? p_cpu_2e_reg__op1.curr : value<32>{0u}) : (i_flatten_5c_cpu_2e__24_procmux_24_1759__CMP ? p_cpu_2e_reg__op2.curr : (i_flatten_5c_cpu_2e__24_procmux_24_1737__CMP ? (i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_1857_24_1513__Y ? (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1872_24_1523__Y ? (p_cpu_2e_latched__is__lb.curr ? p_cpu_2e_mem__rdata__word.slice<7>().val().repeat<24>().concat(p_cpu_2e_mem__rdata__word.slice<7,0>()).val() : (p_cpu_2e_latched__is__lh.curr ? p_cpu_2e_mem__rdata__word.slice<15>().val().repeat<16>().concat(p_cpu_2e_mem__rdata__word.slice<15,0>()).val() : (p_cpu_2e_latched__is__lu.curr ? p_cpu_2e_mem__rdata__word : value<32>{0u}))) : value<32>{0u}) : value<32>{0u}) : value<32>{0u})))) : value<32>{0xff00u});
	}
	// cells $flatten\cpu.$procdff$4424 $flatten\cpu.$procmux$2355 $flatten\cpu.$procmux$2337 $flatten\cpu.$procmux$2335 $flatten\cpu.$procmux$2332 $flatten\cpu.$procmux$2341 $flatten\cpu.$auto$opt_reduce.cc:131:opt_pmux$4584
	if (posedge_p_clk) {
		p_cpu_2e_reg__sh.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_procmux_24_2047__CMP ? (i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1831_24_1495__Y ? value<5>{0u} : (i_flatten_5c_cpu_2e__24_ge_24_upstream_2f_picorv32_2e_v_3a_1835_24_1496__Y ? i_flatten_5c_cpu_2e__24_auto_24_wreduce_2e_cc_3a_513_3a_run_24_4600.slice<4,0>().val() : i_flatten_5c_cpu_2e__24_auto_24_wreduce_2e_cc_3a_513_3a_run_24_4599.slice<4,0>().val())) : (i_flatten_5c_cpu_2e__24_procmux_24_1747__CMP ? p_cpu_2e_cpuregs__rs2.slice<4,0>().val() : (i_flatten_5c_cpu_2e__24_procmux_24_1748__CMP ? (p_cpu_2e_is__slli__srli__srai.curr ? p_cpu_2e_decoded__rs2.curr : (reduce_or<1>(i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1696_24_1467__Y.concat(p_cpu_2e_is__jalr__addi__slti__sltiu__xori__ori__andi.curr).concat(p_cpu_2e_is__lui__auipc__jal.curr).concat(p_cpu_2e_instr__trap).val()) ? value<5>{0u} : p_cpu_2e_cpuregs__rs2.slice<4,0>().val())) : value<5>{0u}))) : value<5>{0u});
	}
	// cells $flatten\cpu.$procdff$4426 $flatten\cpu.$procmux$2988
	if (posedge_p_clk) {
		p_cpu_2e_irq__active.next = (p_cpu_2e_resetn ? p_cpu_2e_irq__active.curr : value<1>{0u});
	}
	// cells $flatten\cpu.$procdff$4430 $flatten\cpu.$procmux$2927 $flatten\cpu.$procmux$2911 $flatten\cpu.$procmux$2909 $flatten\cpu.$procmux$2907 $flatten\cpu.$procmux$2903 $flatten\cpu.$logic_or$upstream/picorv32.v:1887$1528 $flatten\cpu.$logic_or$upstream/picorv32.v:1886$1527 $flatten\cpu.$procmux$2922 $flatten\cpu.$procmux$2920 $flatten\cpu.$procmux$2916
	if (posedge_p_clk) {
		p_cpu_2e_mem__wordsize.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_procmux_24_1737__CMP ? (i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_1857_24_1513__Y ? (p_cpu_2e_mem__do__rdata.curr ? p_cpu_2e_mem__wordsize.curr : (p_cpu_2e_instr__lw.curr ? value<2>{0u} : (logic_or<1>(p_cpu_2e_instr__lh.curr, p_cpu_2e_instr__lhu.curr) ? value<2>{0x1u} : (logic_or<1>(p_cpu_2e_instr__lb.curr, p_cpu_2e_instr__lbu.curr) ? value<2>{0x2u} : p_cpu_2e_mem__wordsize.curr)))) : p_cpu_2e_mem__wordsize.curr) : (i_flatten_5c_cpu_2e__24_procmux_24_1759__CMP ? (i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_1857_24_1513__Y ? (p_cpu_2e_mem__do__wdata.curr ? p_cpu_2e_mem__wordsize.curr : (p_cpu_2e_instr__sw.curr ? value<2>{0u} : (p_cpu_2e_instr__sh.curr ? value<2>{0x1u} : (p_cpu_2e_instr__sb.curr ? value<2>{0x2u} : p_cpu_2e_mem__wordsize.curr)))) : p_cpu_2e_mem__wordsize.curr) : (i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1313_24_1358__Y ? value<2>{0u} : p_cpu_2e_mem__wordsize.curr))) : p_cpu_2e_mem__wordsize.curr);
	}
	// cells $flatten\cpu.$procdff$4431 $flatten\cpu.$procmux$2897 $flatten\cpu.$procmux$2895 $flatten\cpu.$procmux$2892 $flatten\cpu.$procmux$2884 $flatten\cpu.$procmux$2882 $flatten\cpu.$logic_and$upstream/picorv32.v:1573$1448 $flatten\cpu.$logic_not$upstream/picorv32.v:1573$1446 $flatten\cpu.$logic_not$upstream/picorv32.v:1573$1447
	if (posedge_p_clk) {
		p_cpu_2e_mem__do__prefetch.next = (i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_1949_24_1568__Y ? value<1>{0u} : (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1313_24_1358__Y ? (p_cpu_2e_decoder__trigger.curr ? (p_cpu_2e_instr__jal.curr ? p_cpu_2e_mem__do__prefetch.curr : logic_and<1>(logic_not<1>(p_cpu_2e_instr__jalr.curr), logic_not<1>(p_cpu_2e_instr__retirq.curr))) : p_cpu_2e_mem__do__prefetch.curr) : p_cpu_2e_mem__do__prefetch.curr) : p_cpu_2e_mem__do__prefetch.curr));
	}
	// cells $flatten\cpu.$procdff$4432 $flatten\cpu.$procmux$2872 $flatten\cpu.$procmux$2870 $flatten\cpu.$procmux$2868 $flatten\cpu.$procmux$2809 $flatten\cpu.$procmux$2855 $flatten\cpu.$logic_and$upstream/picorv32.v:1492$1401 $flatten\cpu.$logic_not$upstream/picorv32.v:1492$1399 $flatten\cpu.$logic_not$upstream/picorv32.v:1492$1400 $flatten\cpu.$procmux$2835 $flatten\cpu.$auto$opt_reduce.cc:131:opt_pmux$4586 $flatten\cpu.$procmux$2807 $flatten\cpu.$procmux$2095 $flatten\cpu.$procmux$2070 $flatten\cpu.$procmux$1780 $flatten\cpu.$procmux$1959 $flatten\cpu.$auto$opt_reduce.cc:131:opt_pmux$4572
	if (posedge_p_clk) {
		p_cpu_2e_mem__do__rinst.next = ((p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_procmux_24_1786__CMP ? (p_cpu_2e_is__beq__bne__blt__bge__bltu__bgeu.curr ? (p_cpu_2e_alu__out__0 ? value<1>{0x1u} : value<1>{0u}) : value<1>{0u}) : (reduce_or<1>(i_flatten_5c_cpu_2e__24_procmux_24_2052__CMP.concat(i_flatten_5c_cpu_2e__24_procmux_24_2047__CMP).concat(i_flatten_5c_cpu_2e__24_procmux_24_1759__CMP).concat(i_flatten_5c_cpu_2e__24_procmux_24_1748__CMP).concat(i_flatten_5c_cpu_2e__24_procmux_24_1747__CMP).concat(i_flatten_5c_cpu_2e__24_procmux_24_1737__CMP).concat(i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1313_24_1358__Y).val()) ? value<1>{0u} : value<1>{0u})) : value<1>{0u}) ? value<1>{0x1u} : (i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_1949_24_1568__Y ? value<1>{0u} : (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1313_24_1358__Y ? (p_cpu_2e_decoder__trigger.curr ? i_flatten_5c_cpu_2e__24_procmux_24_2500__Y : logic_and<1>(logic_not<1>(p_cpu_2e_decoder__trigger.curr), logic_not<1>(p_cpu_2e_do__waitirq.curr))) : (i_flatten_5c_cpu_2e__24_procmux_24_1748__CMP ? (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1696_24_1467__Y ? value<1>{0x1u} : (reduce_or<1>(p_cpu_2e_is__slli__srli__srai.curr.concat(p_cpu_2e_instr__trap).val()) ? p_cpu_2e_mem__do__rinst.curr : (i_flatten_5c_cpu_2e__24_auto_24_opt__reduce_2e_cc_3a_137_3a_opt__pmux_24_4569 ? p_cpu_2e_mem__do__prefetch.curr : i_flatten_5c_cpu_2e__24_procmux_24_2819__Y))) : (i_flatten_5c_cpu_2e__24_procmux_24_1747__CMP ? i_flatten_5c_cpu_2e__24_procmux_24_2819__Y : (i_flatten_5c_cpu_2e__24_procmux_24_2047__CMP ? (i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1831_24_1495__Y ? p_cpu_2e_mem__do__prefetch.curr : p_cpu_2e_mem__do__rinst.curr) : p_cpu_2e_mem__do__rinst.curr)))) : p_cpu_2e_mem__do__rinst.curr)));
	}
	// cells $flatten\cpu.$procdff$4433 $flatten\cpu.$procmux$2801 $flatten\cpu.$procmux$2799 $flatten\cpu.$procmux$2092 $flatten\cpu.$procmux$2057 $flatten\cpu.$auto$opt_reduce.cc:131:opt_pmux$4578
	if (posedge_p_clk) {
		p_cpu_2e_mem__do__rdata.next = ((p_cpu_2e_resetn ? (reduce_or<1>(i_flatten_5c_cpu_2e__24_procmux_24_2052__CMP.concat(i_flatten_5c_cpu_2e__24_procmux_24_2047__CMP).concat(i_flatten_5c_cpu_2e__24_procmux_24_1786__CMP).concat(i_flatten_5c_cpu_2e__24_procmux_24_1759__CMP).concat(i_flatten_5c_cpu_2e__24_procmux_24_1748__CMP).concat(i_flatten_5c_cpu_2e__24_procmux_24_1747__CMP).concat(i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1313_24_1358__Y).val()) ? value<1>{0u} : (i_flatten_5c_cpu_2e__24_procmux_24_1737__CMP ? i_flatten_5c_cpu_2e__24_3_5c_set__mem__do__rdata_5b_0_3a_0_5d_ : value<1>{0u})) : value<1>{0u}) ? value<1>{0x1u} : (i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_1949_24_1568__Y ? value<1>{0u} : p_cpu_2e_mem__do__rdata.curr));
	}
	// cells $flatten\cpu.$procdff$4434 $flatten\cpu.$procmux$2797 $flatten\cpu.$procmux$2795 $flatten\cpu.$procmux$2089 $flatten\cpu.$procmux$2044 $flatten\cpu.$auto$opt_reduce.cc:131:opt_pmux$4580
	if (posedge_p_clk) {
		p_cpu_2e_mem__do__wdata.next = ((p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_procmux_24_1759__CMP ? i_flatten_5c_cpu_2e__24_3_5c_set__mem__do__wdata_5b_0_3a_0_5d_ : (reduce_or<1>(i_flatten_5c_cpu_2e__24_procmux_24_2052__CMP.concat(i_flatten_5c_cpu_2e__24_procmux_24_2047__CMP).concat(i_flatten_5c_cpu_2e__24_procmux_24_1786__CMP).concat(i_flatten_5c_cpu_2e__24_procmux_24_1748__CMP).concat(i_flatten_5c_cpu_2e__24_procmux_24_1747__CMP).concat(i_flatten_5c_cpu_2e__24_procmux_24_1737__CMP).concat(i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1313_24_1358__Y).val()) ? value<1>{0u} : value<1>{0u})) : value<1>{0u}) ? value<1>{0x1u} : (i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_1949_24_1568__Y ? value<1>{0u} : p_cpu_2e_mem__do__wdata.curr));
	}
	// cells $flatten\cpu.$procdff$4435 $flatten\cpu.$procmux$2186 $flatten\cpu.$procmux$2167 $flatten\cpu.$procmux$2179 $flatten\cpu.$procmux$2177 $flatten\cpu.$procmux$2172 $flatten\cpu.$procmux$2170
	if (posedge_p_clk) {
		p_cpu_2e_decoder__trigger.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_procmux_24_1786__CMP ? (p_cpu_2e_is__beq__bne__blt__bge__bltu__bgeu.curr ? (p_cpu_2e_alu__out__0 ? value<1>{0u} : i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1446_24_1397__Y) : i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1446_24_1397__Y) : (i_flatten_5c_cpu_2e__24_auto_24_opt__reduce_2e_cc_3a_137_3a_opt__pmux_24_4591 ? (i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_1857_24_1513__Y ? (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1872_24_1523__Y ? value<1>{0x1u} : i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1446_24_1397__Y) : i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1446_24_1397__Y) : i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1446_24_1397__Y)) : i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1446_24_1397__Y);
	}
	// cells $flatten\cpu.$procdff$4437 $flatten\cpu.$procmux$2159 $flatten\cpu.$procmux$2150 $flatten\cpu.$procmux$2155 $flatten\cpu.$procmux$2146
	if (posedge_p_clk) {
		p_cpu_2e_decoder__pseudo__trigger.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_auto_24_opt__reduce_2e_cc_3a_137_3a_opt__pmux_24_4591 ? (i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_1857_24_1513__Y ? (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1872_24_1523__Y ? value<1>{0x1u} : value<1>{0u}) : value<1>{0u}) : value<1>{0u}) : value<1>{0u});
	}
	// cells $flatten\cpu.$procdff$4443 $flatten\cpu.$procmux$2687 $flatten\cpu.$procmux$2681 $flatten\cpu.$procmux$2679 $flatten\cpu.$procmux$2673 $flatten\cpu.$logic_and$upstream/picorv32.v:1923$1543 $flatten\cpu.$ne$upstream/picorv32.v:1923$1542 $flatten\cpu.$logic_and$upstream/picorv32.v:1930$1550 $flatten\cpu.$logic_and$upstream/picorv32.v:1922$1540 $flatten\cpu.$logic_or$upstream/picorv32.v:1922$1539 $flatten\cpu.$logic_and$upstream/picorv32.v:1938$1558 $flatten\cpu.$logic_and$upstream/picorv32.v:1938$1556 $flatten\cpu.$reduce_or$upstream/picorv32.v:1938$1557
	if (posedge_p_clk) {
		p_cpu_2e_cpu__state.next = (logic_and<1>(logic_and<1>(p_cpu_2e_resetn, p_cpu_2e_mem__do__rinst.curr), reduce_or<1>(p_cpu_2e_reg__pc.curr.slice<1,0>().val())) ? value<8>{0x80u} : (logic_and<1>(p_cpu_2e_resetn, logic_or<1>(p_cpu_2e_mem__do__rdata.curr, p_cpu_2e_mem__do__wdata.curr)) ? (logic_and<1>(i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1930_24_1548__Y, p_cpu_2e_reg__op1.curr.slice<0>().val()) ? value<8>{0x80u} : (logic_and<1>(i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1923_24_1541__Y, reduce_bool<1>(p_cpu_2e_reg__op1.curr.slice<1,0>().val())) ? value<8>{0x80u} : i_flatten_5c_cpu_2e__24_procmux_24_2666__Y)) : i_flatten_5c_cpu_2e__24_procmux_24_2666__Y));
	}
	// cells $flatten\cpu.$procdff$4448 $flatten\cpu.$procmux$2573 $flatten\cpu.$procmux$2531 $flatten\cpu.$procmux$2535 $flatten\cpu.$auto$opt_reduce.cc:131:opt_pmux$4570
	if (posedge_p_clk) {
		p_cpu_2e_latched__store.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1313_24_1358__Y ? value<1>{0u} : (i_flatten_5c_cpu_2e__24_procmux_24_1786__CMP ? (p_cpu_2e_is__beq__bne__blt__bge__bltu__bgeu.curr ? p_cpu_2e_alu__out__0 : value<1>{0x1u}) : (reduce_or<1>(i_flatten_5c_cpu_2e__24_procmux_24_2047__CMP.concat(i_flatten_5c_cpu_2e__24_procmux_24_1737__CMP).val()) ? value<1>{0x1u} : p_cpu_2e_latched__store.curr))) : value<1>{0x1u});
	}
	// cells $flatten\cpu.$procdff$4449 $flatten\cpu.$procmux$2528 $flatten\cpu.$procmux$2524 $flatten\cpu.$procmux$2519
	if (posedge_p_clk) {
		p_cpu_2e_latched__stalu.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_procmux_24_1786__CMP ? (p_cpu_2e_is__beq__bne__blt__bge__bltu__bgeu.curr ? p_cpu_2e_latched__stalu.curr : value<1>{0x1u}) : (i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1313_24_1358__Y ? value<1>{0u} : p_cpu_2e_latched__stalu.curr)) : value<1>{0u});
	}
	// cells $flatten\cpu.$procdff$4450 $flatten\cpu.$procmux$2512 $flatten\cpu.$procmux$2488 $flatten\cpu.$procmux$2502 $flatten\cpu.$procmux$2483
	if (posedge_p_clk) {
		p_cpu_2e_latched__branch.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1313_24_1358__Y ? (p_cpu_2e_decoder__trigger.curr ? i_flatten_5c_cpu_2e__24_procmux_24_2500__Y : value<1>{0u}) : (i_flatten_5c_cpu_2e__24_procmux_24_1786__CMP ? (p_cpu_2e_is__beq__bne__blt__bge__bltu__bgeu.curr ? p_cpu_2e_alu__out__0 : p_cpu_2e_instr__jalr.curr) : p_cpu_2e_latched__branch.curr)) : value<1>{0u});
	}
	// cells $flatten\cpu.$procdff$4451 $flatten\cpu.$procmux$2476 $flatten\cpu.$procmux$2473
	if (posedge_p_clk) {
		p_cpu_2e_latched__compr.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1313_24_1358__Y ? p_cpu_2e_compressed__instr.curr : p_cpu_2e_latched__compr.curr) : p_cpu_2e_latched__compr.curr);
	}
	// cells $flatten\cpu.$procdff$4452 $flatten\cpu.$procmux$2461 $flatten\cpu.$procmux$2458 $flatten\cpu.$procmux$2450
	if (posedge_p_clk) {
		p_cpu_2e_latched__trace.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1313_24_1358__Y ? (p_cpu_2e_decoder__trigger.curr ? value<1>{0x1u} : value<1>{0u}) : p_cpu_2e_latched__trace.curr) : value<1>{0u});
	}
	// cells $flatten\cpu.$procdff$4453 $flatten\cpu.$procmux$2439 $flatten\cpu.$procmux$2435 $flatten\cpu.$procmux$2433 $flatten\cpu.$procmux$2431
	if (posedge_p_clk) {
		p_cpu_2e_latched__is__lu.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_procmux_24_1737__CMP ? (i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_1857_24_1513__Y ? (p_cpu_2e_mem__do__rdata.curr ? p_cpu_2e_latched__is__lu.curr : p_cpu_2e_is__lbu__lhu__lw.curr) : p_cpu_2e_latched__is__lu.curr) : (i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1313_24_1358__Y ? value<1>{0u} : p_cpu_2e_latched__is__lu.curr)) : value<1>{0u});
	}
	// cells $flatten\cpu.$procdff$4454 $flatten\cpu.$procmux$2426 $flatten\cpu.$procmux$2422 $flatten\cpu.$procmux$2420 $flatten\cpu.$procmux$2418
	if (posedge_p_clk) {
		p_cpu_2e_latched__is__lh.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_procmux_24_1737__CMP ? (i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_1857_24_1513__Y ? (p_cpu_2e_mem__do__rdata.curr ? p_cpu_2e_latched__is__lh.curr : p_cpu_2e_instr__lh.curr) : p_cpu_2e_latched__is__lh.curr) : (i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1313_24_1358__Y ? value<1>{0u} : p_cpu_2e_latched__is__lh.curr)) : value<1>{0u});
	}
	// cells $flatten\cpu.$procdff$4455 $flatten\cpu.$procmux$2413 $flatten\cpu.$procmux$2409 $flatten\cpu.$procmux$2407 $flatten\cpu.$procmux$2405
	if (posedge_p_clk) {
		p_cpu_2e_latched__is__lb.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_procmux_24_1737__CMP ? (i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_1857_24_1513__Y ? (p_cpu_2e_mem__do__rdata.curr ? p_cpu_2e_latched__is__lb.curr : p_cpu_2e_instr__lb.curr) : p_cpu_2e_latched__is__lb.curr) : (i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1313_24_1358__Y ? value<1>{0u} : p_cpu_2e_latched__is__lb.curr)) : value<1>{0u});
	}
	// cells $flatten\cpu.$procdff$4456 $flatten\cpu.$procmux$2400 $flatten\cpu.$procmux$2383 $flatten\cpu.$procmux$2378
	if (posedge_p_clk) {
		p_cpu_2e_latched__rd.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1313_24_1358__Y ? p_cpu_2e_decoded__rd.curr : (i_flatten_5c_cpu_2e__24_procmux_24_1786__CMP ? (p_cpu_2e_is__beq__bne__blt__bge__bltu__bgeu.curr ? value<5>{0u} : p_cpu_2e_latched__rd.curr) : p_cpu_2e_latched__rd.curr)) : value<5>{0x2u});
	}
	// \src: upstream/picorv32.v:1402.2-1975.5
	// cell $flatten\cpu.$procdff$4460
	if (posedge_p_clk) {
		p_cpu_2e_do__waitirq.next = value<1>{0u};
	}
	// cells $flatten\cpu.$procdff$4461 $flatten\cpu.$procmux$3233 $flatten\cpu.$and$upstream/picorv32.v:1279$1344 $flatten\cpu.$or$upstream/picorv32.v:1277$1342 $flatten\cpu.$xor$upstream/picorv32.v:1275$1340 $flatten\cpu.$ternary$upstream/picorv32.v:1240$1573 $flatten\cpu.$add$upstream/picorv32.v:1240$1572 $flatten\cpu.$sub$upstream/picorv32.v:1240$1571 $flatten\cpu.$logic_or$upstream/picorv32.v:1278$1343 $flatten\cpu.$logic_or$upstream/picorv32.v:1276$1341 $flatten\cpu.$logic_or$upstream/picorv32.v:1274$1339
	if (posedge_p_clk) {
		p_cpu_2e_alu__out__q.next = (logic_or<1>(p_cpu_2e_instr__andi.curr, p_cpu_2e_instr__and.curr) ? and_uu<32>(p_cpu_2e_reg__op1.curr, p_cpu_2e_reg__op2.curr) : (logic_or<1>(p_cpu_2e_instr__ori.curr, p_cpu_2e_instr__or.curr) ? or_uu<32>(p_cpu_2e_reg__op1.curr, p_cpu_2e_reg__op2.curr) : (logic_or<1>(p_cpu_2e_instr__xori.curr, p_cpu_2e_instr__xor.curr) ? xor_uu<32>(p_cpu_2e_reg__op1.curr, p_cpu_2e_reg__op2.curr) : (p_cpu_2e_is__compare.curr ? value<31>{0u}.concat(p_cpu_2e_alu__out__0).val() : (p_cpu_2e_is__lui__auipc__jal__jalr__addi__add__sub.curr ? (p_cpu_2e_instr__sub.curr ? sub_uu<32>(p_cpu_2e_reg__op1.curr, p_cpu_2e_reg__op2.curr) : add_uu<32>(p_cpu_2e_reg__op1.curr, p_cpu_2e_reg__op2.curr)) : value<32>{0u})))));
	}
	// cells $flatten\cpu.$procdff$4469 $flatten\cpu.$procmux$3789
	if (posedge_p_clk) {
		p_cpu_2e_pcpi__insn.next = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? value<32>{0u} : p_cpu_2e_pcpi__insn.curr);
	}
	// cells $flatten\cpu.$procdff$4470 $flatten\cpu.$procmux$3787 $flatten\cpu.$eq$upstream/picorv32.v:867$1062
	if (posedge_p_clk) {
		p_cpu_2e_instr__lui.next = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1446_24_1397__Y ? eq_uu<1>(p_cpu_2e_mem__rdata__latched.slice<6,0>().val(), value<6>{0x37u}) : p_cpu_2e_instr__lui.curr);
	}
	// cells $flatten\cpu.$procdff$4471 $flatten\cpu.$procmux$3769 $flatten\cpu.$eq$upstream/picorv32.v:868$1063
	if (posedge_p_clk) {
		p_cpu_2e_instr__auipc.next = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1446_24_1397__Y ? eq_uu<1>(p_cpu_2e_mem__rdata__latched.slice<6,0>().val(), value<5>{0x17u}) : p_cpu_2e_instr__auipc.curr);
	}
	// cells $flatten\cpu.$procdff$4472 $flatten\cpu.$procmux$3767 $flatten\cpu.$eq$upstream/picorv32.v:869$1064
	if (posedge_p_clk) {
		p_cpu_2e_instr__jal.next = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1446_24_1397__Y ? eq_uu<1>(p_cpu_2e_mem__rdata__latched.slice<6,0>().val(), value<7>{0x6fu}) : p_cpu_2e_instr__jal.curr);
	}
	// cells $flatten\cpu.$procdff$4473 $flatten\cpu.$procmux$3755 $flatten\cpu.$logic_and$upstream/picorv32.v:870$1067 $flatten\cpu.$eq$upstream/picorv32.v:870$1065 $flatten\cpu.$eq$upstream/picorv32.v:870$1066
	if (posedge_p_clk) {
		p_cpu_2e_instr__jalr.next = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1446_24_1397__Y ? logic_and<1>(eq_uu<1>(p_cpu_2e_mem__rdata__latched.slice<6,0>().val(), value<7>{0x67u}), logic_not<1>(p_cpu_2e_mem__rdata__latched.slice<14,12>().val())) : p_cpu_2e_instr__jalr.curr);
	}
	// cells $flatten\cpu.$procdff$4474 $flatten\cpu.$procmux$3742 $flatten\cpu.$procmux$3740 $flatten\cpu.$logic_and$upstream/picorv32.v:1040$1135
	if (posedge_p_clk) {
		p_cpu_2e_instr__beq.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? logic_and<1>(p_cpu_2e_is__beq__bne__blt__bge__bltu__bgeu.curr, i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1040_24_1134__Y) : p_cpu_2e_instr__beq.curr) : value<1>{0u});
	}
	// cells $flatten\cpu.$procdff$4475 $flatten\cpu.$procmux$3738 $flatten\cpu.$procmux$3736 $flatten\cpu.$logic_and$upstream/picorv32.v:1041$1137
	if (posedge_p_clk) {
		p_cpu_2e_instr__bne.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? logic_and<1>(p_cpu_2e_is__beq__bne__blt__bge__bltu__bgeu.curr, i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1041_24_1136__Y) : p_cpu_2e_instr__bne.curr) : value<1>{0u});
	}
	// cells $flatten\cpu.$procdff$4476 $flatten\cpu.$procmux$3734 $flatten\cpu.$procmux$3732 $flatten\cpu.$logic_and$upstream/picorv32.v:1042$1139
	if (posedge_p_clk) {
		p_cpu_2e_instr__blt.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? logic_and<1>(p_cpu_2e_is__beq__bne__blt__bge__bltu__bgeu.curr, i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1042_24_1138__Y) : p_cpu_2e_instr__blt.curr) : value<1>{0u});
	}
	// cells $flatten\cpu.$procdff$4477 $flatten\cpu.$procmux$3730 $flatten\cpu.$procmux$3728 $flatten\cpu.$logic_and$upstream/picorv32.v:1043$1141
	if (posedge_p_clk) {
		p_cpu_2e_instr__bge.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? logic_and<1>(p_cpu_2e_is__beq__bne__blt__bge__bltu__bgeu.curr, i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1043_24_1140__Y) : p_cpu_2e_instr__bge.curr) : value<1>{0u});
	}
	// cells $flatten\cpu.$procdff$4478 $flatten\cpu.$procmux$3726 $flatten\cpu.$procmux$3724 $flatten\cpu.$logic_and$upstream/picorv32.v:1044$1143
	if (posedge_p_clk) {
		p_cpu_2e_instr__bltu.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? logic_and<1>(p_cpu_2e_is__beq__bne__blt__bge__bltu__bgeu.curr, i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1044_24_1142__Y) : p_cpu_2e_instr__bltu.curr) : value<1>{0u});
	}
	// cells $flatten\cpu.$procdff$4479 $flatten\cpu.$procmux$3722 $flatten\cpu.$procmux$3720 $flatten\cpu.$logic_and$upstream/picorv32.v:1045$1145
	if (posedge_p_clk) {
		p_cpu_2e_instr__bgeu.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? logic_and<1>(p_cpu_2e_is__beq__bne__blt__bge__bltu__bgeu.curr, i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1045_24_1144__Y) : p_cpu_2e_instr__bgeu.curr) : value<1>{0u});
	}
	// cells $flatten\cpu.$procdff$4480 $flatten\cpu.$procmux$3718 $flatten\cpu.$logic_and$upstream/picorv32.v:1047$1147
	if (posedge_p_clk) {
		p_cpu_2e_instr__lb.next = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? logic_and<1>(p_cpu_2e_is__lb__lh__lw__lbu__lhu.curr, i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1040_24_1134__Y) : p_cpu_2e_instr__lb.curr);
	}
	// cells $flatten\cpu.$procdff$4481 $flatten\cpu.$procmux$3716 $flatten\cpu.$logic_and$upstream/picorv32.v:1048$1149
	if (posedge_p_clk) {
		p_cpu_2e_instr__lh.next = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? logic_and<1>(p_cpu_2e_is__lb__lh__lw__lbu__lhu.curr, i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1041_24_1136__Y) : p_cpu_2e_instr__lh.curr);
	}
	// cells $flatten\cpu.$procdff$4482 $flatten\cpu.$procmux$3714 $flatten\cpu.$logic_and$upstream/picorv32.v:1049$1151
	if (posedge_p_clk) {
		p_cpu_2e_instr__lw.next = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? logic_and<1>(p_cpu_2e_is__lb__lh__lw__lbu__lhu.curr, i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1049_24_1150__Y) : p_cpu_2e_instr__lw.curr);
	}
	// cells $flatten\cpu.$procdff$4483 $flatten\cpu.$procmux$3712 $flatten\cpu.$logic_and$upstream/picorv32.v:1050$1153
	if (posedge_p_clk) {
		p_cpu_2e_instr__lbu.next = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? logic_and<1>(p_cpu_2e_is__lb__lh__lw__lbu__lhu.curr, i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1042_24_1138__Y) : p_cpu_2e_instr__lbu.curr);
	}
	// cells $flatten\cpu.$procdff$4484 $flatten\cpu.$procmux$3710 $flatten\cpu.$logic_and$upstream/picorv32.v:1051$1155
	if (posedge_p_clk) {
		p_cpu_2e_instr__lhu.next = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? logic_and<1>(p_cpu_2e_is__lb__lh__lw__lbu__lhu.curr, i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1043_24_1140__Y) : p_cpu_2e_instr__lhu.curr);
	}
	// cells $flatten\cpu.$procdff$4485 $flatten\cpu.$procmux$3708 $flatten\cpu.$logic_and$upstream/picorv32.v:1053$1157
	if (posedge_p_clk) {
		p_cpu_2e_instr__sb.next = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? logic_and<1>(p_cpu_2e_is__sb__sh__sw.curr, i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1040_24_1134__Y) : p_cpu_2e_instr__sb.curr);
	}
	// cells $flatten\cpu.$procdff$4486 $flatten\cpu.$procmux$3706 $flatten\cpu.$logic_and$upstream/picorv32.v:1054$1159
	if (posedge_p_clk) {
		p_cpu_2e_instr__sh.next = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? logic_and<1>(p_cpu_2e_is__sb__sh__sw.curr, i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1041_24_1136__Y) : p_cpu_2e_instr__sh.curr);
	}
	// cells $flatten\cpu.$procdff$4487 $flatten\cpu.$procmux$3704 $flatten\cpu.$logic_and$upstream/picorv32.v:1055$1161
	if (posedge_p_clk) {
		p_cpu_2e_instr__sw.next = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? logic_and<1>(p_cpu_2e_is__sb__sh__sw.curr, i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1049_24_1150__Y) : p_cpu_2e_instr__sw.curr);
	}
	// cells $flatten\cpu.$procdff$4488 $flatten\cpu.$procmux$3702 $flatten\cpu.$procmux$3700 $flatten\cpu.$logic_and$upstream/picorv32.v:1057$1163
	if (posedge_p_clk) {
		p_cpu_2e_instr__addi.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? logic_and<1>(p_cpu_2e_is__alu__reg__imm.curr, i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1040_24_1134__Y) : p_cpu_2e_instr__addi.curr) : value<1>{0u});
	}
	// cells $flatten\cpu.$procdff$4489 $flatten\cpu.$procmux$3698 $flatten\cpu.$procmux$3696 $flatten\cpu.$logic_and$upstream/picorv32.v:1058$1165
	if (posedge_p_clk) {
		p_cpu_2e_instr__slti.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? logic_and<1>(p_cpu_2e_is__alu__reg__imm.curr, i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1049_24_1150__Y) : p_cpu_2e_instr__slti.curr) : value<1>{0u});
	}
	// cells $flatten\cpu.$procdff$4490 $flatten\cpu.$procmux$3694 $flatten\cpu.$procmux$3692 $flatten\cpu.$logic_and$upstream/picorv32.v:1059$1167
	if (posedge_p_clk) {
		p_cpu_2e_instr__sltiu.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? logic_and<1>(p_cpu_2e_is__alu__reg__imm.curr, i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1059_24_1166__Y) : p_cpu_2e_instr__sltiu.curr) : value<1>{0u});
	}
	// cells $flatten\cpu.$procdff$4491 $flatten\cpu.$procmux$3690 $flatten\cpu.$procmux$3688 $flatten\cpu.$logic_and$upstream/picorv32.v:1060$1169
	if (posedge_p_clk) {
		p_cpu_2e_instr__xori.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? logic_and<1>(p_cpu_2e_is__alu__reg__imm.curr, i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1042_24_1138__Y) : p_cpu_2e_instr__xori.curr) : value<1>{0u});
	}
	// cells $flatten\cpu.$procdff$4492 $flatten\cpu.$procmux$3686 $flatten\cpu.$procmux$3684 $flatten\cpu.$logic_and$upstream/picorv32.v:1061$1171
	if (posedge_p_clk) {
		p_cpu_2e_instr__ori.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? logic_and<1>(p_cpu_2e_is__alu__reg__imm.curr, i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1044_24_1142__Y) : p_cpu_2e_instr__ori.curr) : value<1>{0u});
	}
	// cells $flatten\cpu.$procdff$4493 $flatten\cpu.$procmux$3682 $flatten\cpu.$procmux$3680 $flatten\cpu.$logic_and$upstream/picorv32.v:1062$1173
	if (posedge_p_clk) {
		p_cpu_2e_instr__andi.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? logic_and<1>(p_cpu_2e_is__alu__reg__imm.curr, i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1045_24_1144__Y) : p_cpu_2e_instr__andi.curr) : value<1>{0u});
	}
	// cells $flatten\cpu.$procdff$4494 $flatten\cpu.$procmux$3678 $flatten\cpu.$logic_and$upstream/picorv32.v:1064$1177 $flatten\cpu.$logic_and$upstream/picorv32.v:1064$1175
	if (posedge_p_clk) {
		p_cpu_2e_instr__slli.next = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? logic_and<1>(logic_and<1>(p_cpu_2e_is__alu__reg__imm.curr, i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1041_24_1136__Y), i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1064_24_1176__Y) : p_cpu_2e_instr__slli.curr);
	}
	// cells $flatten\cpu.$procdff$4495 $flatten\cpu.$procmux$3676 $flatten\cpu.$logic_and$upstream/picorv32.v:1065$1181
	if (posedge_p_clk) {
		p_cpu_2e_instr__srli.next = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? logic_and<1>(i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1065_24_1179__Y, i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1064_24_1176__Y) : p_cpu_2e_instr__srli.curr);
	}
	// cells $flatten\cpu.$procdff$4496 $flatten\cpu.$procmux$3674 $flatten\cpu.$logic_and$upstream/picorv32.v:1066$1185
	if (posedge_p_clk) {
		p_cpu_2e_instr__srai.next = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? logic_and<1>(i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1065_24_1179__Y, i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1066_24_1184__Y) : p_cpu_2e_instr__srai.curr);
	}
	// cells $flatten\cpu.$procdff$4497 $flatten\cpu.$procmux$3672 $flatten\cpu.$procmux$3670 $flatten\cpu.$logic_and$upstream/picorv32.v:1068$1189
	if (posedge_p_clk) {
		p_cpu_2e_instr__add.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? logic_and<1>(i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1068_24_1187__Y, i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1064_24_1176__Y) : p_cpu_2e_instr__add.curr) : value<1>{0u});
	}
	// cells $flatten\cpu.$procdff$4498 $flatten\cpu.$procmux$3668 $flatten\cpu.$procmux$3666 $flatten\cpu.$logic_and$upstream/picorv32.v:1069$1193
	if (posedge_p_clk) {
		p_cpu_2e_instr__sub.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? logic_and<1>(i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1068_24_1187__Y, i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1066_24_1184__Y) : p_cpu_2e_instr__sub.curr) : value<1>{0u});
	}
	// cells $flatten\cpu.$procdff$4499 $flatten\cpu.$procmux$3664 $flatten\cpu.$procmux$3662 $flatten\cpu.$logic_and$upstream/picorv32.v:1070$1197 $flatten\cpu.$logic_and$upstream/picorv32.v:1070$1195
	if (posedge_p_clk) {
		p_cpu_2e_instr__sll.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? logic_and<1>(logic_and<1>(p_cpu_2e_is__alu__reg__reg.curr, i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1041_24_1136__Y), i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1064_24_1176__Y) : p_cpu_2e_instr__sll.curr) : value<1>{0u});
	}
	// cells $flatten\cpu.$procdff$4500 $flatten\cpu.$procmux$3660 $flatten\cpu.$procmux$3658 $flatten\cpu.$logic_and$upstream/picorv32.v:1071$1201 $flatten\cpu.$logic_and$upstream/picorv32.v:1071$1199
	if (posedge_p_clk) {
		p_cpu_2e_instr__slt.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? logic_and<1>(logic_and<1>(p_cpu_2e_is__alu__reg__reg.curr, i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1049_24_1150__Y), i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1064_24_1176__Y) : p_cpu_2e_instr__slt.curr) : value<1>{0u});
	}
	// cells $flatten\cpu.$procdff$4501 $flatten\cpu.$procmux$3656 $flatten\cpu.$procmux$3654 $flatten\cpu.$logic_and$upstream/picorv32.v:1072$1205 $flatten\cpu.$logic_and$upstream/picorv32.v:1072$1203
	if (posedge_p_clk) {
		p_cpu_2e_instr__sltu.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? logic_and<1>(logic_and<1>(p_cpu_2e_is__alu__reg__reg.curr, i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1059_24_1166__Y), i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1064_24_1176__Y) : p_cpu_2e_instr__sltu.curr) : value<1>{0u});
	}
	// cells $flatten\cpu.$procdff$4502 $flatten\cpu.$procmux$3652 $flatten\cpu.$procmux$3650 $flatten\cpu.$logic_and$upstream/picorv32.v:1073$1209 $flatten\cpu.$logic_and$upstream/picorv32.v:1073$1207
	if (posedge_p_clk) {
		p_cpu_2e_instr__xor.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? logic_and<1>(logic_and<1>(p_cpu_2e_is__alu__reg__reg.curr, i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1042_24_1138__Y), i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1064_24_1176__Y) : p_cpu_2e_instr__xor.curr) : value<1>{0u});
	}
	// cells $flatten\cpu.$procdff$4503 $flatten\cpu.$procmux$3648 $flatten\cpu.$procmux$3646 $flatten\cpu.$logic_and$upstream/picorv32.v:1074$1213
	if (posedge_p_clk) {
		p_cpu_2e_instr__srl.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? logic_and<1>(i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1074_24_1211__Y, i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1064_24_1176__Y) : p_cpu_2e_instr__srl.curr) : value<1>{0u});
	}
	// cells $flatten\cpu.$procdff$4504 $flatten\cpu.$procmux$3644 $flatten\cpu.$procmux$3642 $flatten\cpu.$logic_and$upstream/picorv32.v:1075$1217
	if (posedge_p_clk) {
		p_cpu_2e_instr__sra.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? logic_and<1>(i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1074_24_1211__Y, i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1066_24_1184__Y) : p_cpu_2e_instr__sra.curr) : value<1>{0u});
	}
	// cells $flatten\cpu.$procdff$4505 $flatten\cpu.$procmux$3640 $flatten\cpu.$procmux$3638 $flatten\cpu.$logic_and$upstream/picorv32.v:1076$1221 $flatten\cpu.$logic_and$upstream/picorv32.v:1076$1219
	if (posedge_p_clk) {
		p_cpu_2e_instr__or.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? logic_and<1>(logic_and<1>(p_cpu_2e_is__alu__reg__reg.curr, i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1044_24_1142__Y), i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1064_24_1176__Y) : p_cpu_2e_instr__or.curr) : value<1>{0u});
	}
	// cells $flatten\cpu.$procdff$4506 $flatten\cpu.$procmux$3636 $flatten\cpu.$procmux$3634 $flatten\cpu.$logic_and$upstream/picorv32.v:1077$1225 $flatten\cpu.$logic_and$upstream/picorv32.v:1077$1223
	if (posedge_p_clk) {
		p_cpu_2e_instr__and.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? logic_and<1>(logic_and<1>(p_cpu_2e_is__alu__reg__reg.curr, i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1045_24_1144__Y), i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1064_24_1176__Y) : p_cpu_2e_instr__and.curr) : value<1>{0u});
	}
	// cells $flatten\cpu.$procdff$4507 $flatten\cpu.$procmux$3632
	if (posedge_p_clk) {
		p_cpu_2e_instr__rdcycle.next = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? value<1>{0u} : p_cpu_2e_instr__rdcycle.curr);
	}
	// cells $flatten\cpu.$procdff$4508 $flatten\cpu.$procmux$3630
	if (posedge_p_clk) {
		p_cpu_2e_instr__rdcycleh.next = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? value<1>{0u} : p_cpu_2e_instr__rdcycleh.curr);
	}
	// cells $flatten\cpu.$procdff$4509 $flatten\cpu.$procmux$3628
	if (posedge_p_clk) {
		p_cpu_2e_instr__rdinstr.next = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? value<1>{0u} : p_cpu_2e_instr__rdinstr.curr);
	}
	// cells $flatten\cpu.$procdff$4510 $flatten\cpu.$procmux$3626
	if (posedge_p_clk) {
		p_cpu_2e_instr__rdinstrh.next = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? value<1>{0u} : p_cpu_2e_instr__rdinstrh.curr);
	}
	// cells $flatten\cpu.$procdff$4512 $flatten\cpu.$procmux$3622 $flatten\cpu.$procmux$3620 $flatten\cpu.$logic_and$upstream/picorv32.v:1088$1262 $flatten\cpu.$eq$upstream/picorv32.v:1088$1260
	if (posedge_p_clk) {
		p_cpu_2e_instr__fence.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? logic_and<1>(eq_uu<1>(p_cpu_2e_mem__rdata__q.curr.slice<6,0>().val(), value<4>{0xfu}), i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1040_24_1134__Y) : p_cpu_2e_instr__fence.curr) : value<1>{0u});
	}
	// cells $flatten\cpu.$procdff$4513 $flatten\cpu.$procmux$3618
	if (posedge_p_clk) {
		p_cpu_2e_instr__getq.next = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? value<1>{0u} : p_cpu_2e_instr__getq.curr);
	}
	// cells $flatten\cpu.$procdff$4514 $flatten\cpu.$procmux$3616
	if (posedge_p_clk) {
		p_cpu_2e_instr__setq.next = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? value<1>{0u} : p_cpu_2e_instr__setq.curr);
	}
	// cells $flatten\cpu.$procdff$4515 $flatten\cpu.$procmux$3614
	if (posedge_p_clk) {
		p_cpu_2e_instr__retirq.next = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1446_24_1397__Y ? value<1>{0u} : p_cpu_2e_instr__retirq.curr);
	}
	// cells $flatten\cpu.$procdff$4516 $flatten\cpu.$procmux$3612
	if (posedge_p_clk) {
		p_cpu_2e_instr__maskirq.next = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? value<1>{0u} : p_cpu_2e_instr__maskirq.curr);
	}
	// cells $flatten\cpu.$procdff$4517 $flatten\cpu.$procmux$3610
	if (posedge_p_clk) {
		p_cpu_2e_instr__waitirq.next = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1446_24_1397__Y ? value<1>{0u} : p_cpu_2e_instr__waitirq.curr);
	}
	// cells $flatten\cpu.$procdff$4518 $flatten\cpu.$procmux$3608
	if (posedge_p_clk) {
		p_cpu_2e_instr__timer.next = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? value<1>{0u} : p_cpu_2e_instr__timer.curr);
	}
	// cells $flatten\cpu.$procdff$4519 $flatten\cpu.$procmux$3606
	if (posedge_p_clk) {
		p_cpu_2e_decoded__rd.next = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1446_24_1397__Y ? p_cpu_2e_mem__rdata__latched.slice<11,7>().val() : p_cpu_2e_decoded__rd.curr);
	}
	// \src: upstream/picorv32.v:858.2-1167.5
	// cell $flatten\cpu.$procdff$4520
	if (posedge_p_clk) {
		p_cpu_2e_decoded__rs1.next = i_flatten_5c_cpu_2e__24_0_5c_decoded__rs1_5b_4_3a_0_5d_;
	}
	// cells $flatten\cpu.$procdff$4521 $flatten\cpu.$procmux$3555
	if (posedge_p_clk) {
		p_cpu_2e_decoded__rs2.next = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1446_24_1397__Y ? p_cpu_2e_mem__rdata__latched.slice<24,20>().val() : p_cpu_2e_decoded__rs2.curr);
	}
	// cells $flatten\cpu.$procdff$4522 $flatten\cpu.$procmux$3526 $flatten\cpu.$procmux$3520 $flatten\cpu.$reduce_or$upstream/picorv32.v:1125$1315 $flatten\cpu.$reduce_or$upstream/picorv32.v:1123$1313
	if (posedge_p_clk) {
		p_cpu_2e_decoded__imm.next = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? (p_cpu_2e_is__sb__sh__sw.curr ? p_cpu_2e_mem__rdata__q.curr.slice<31>().val().repeat<20>().concat(p_cpu_2e_mem__rdata__q.curr.slice<31,25>()).concat(p_cpu_2e_mem__rdata__q.curr.slice<11,7>()).val() : (p_cpu_2e_is__beq__bne__blt__bge__bltu__bgeu.curr ? p_cpu_2e_mem__rdata__q.curr.slice<31>().val().repeat<20>().concat(p_cpu_2e_mem__rdata__q.curr.slice<7>()).concat(p_cpu_2e_mem__rdata__q.curr.slice<30,25>()).concat(p_cpu_2e_mem__rdata__q.curr.slice<11,8>()).concat(value<1>{0u}).val() : (reduce_or<1>(p_cpu_2e_is__alu__reg__imm.curr.concat(p_cpu_2e_is__lb__lh__lw__lbu__lhu.curr).concat(p_cpu_2e_instr__jalr.curr).val()) ? p_cpu_2e_mem__rdata__q.curr.slice<31>().val().repeat<20>().concat(p_cpu_2e_mem__rdata__q.curr.slice<31,20>()).val() : (reduce_or<1>(p_cpu_2e_instr__auipc.curr.concat(p_cpu_2e_instr__lui.curr).val()) ? p_cpu_2e_mem__rdata__q.curr.slice<31,12>().concat(value<12>{0u}).val() : (p_cpu_2e_instr__jal.curr ? p_cpu_2e_decoded__imm__j.curr : value<32>{0u}))))) : p_cpu_2e_decoded__imm.curr);
	}
	// \src: upstream/picorv32.v:858.2-1167.5
	// cell $flatten\cpu.$procdff$4523
	if (posedge_p_clk) {
		p_cpu_2e_decoded__imm__j.next = i_flatten_5c_cpu_2e__24_0_5c_decoded__imm__j_5b_31_3a_0_5d_;
	}
	// cells $flatten\cpu.$procdff$4524 $flatten\cpu.$procmux$3513
	if (posedge_p_clk) {
		p_cpu_2e_compressed__instr.next = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1446_24_1397__Y ? value<1>{0u} : p_cpu_2e_compressed__instr.curr);
	}
	// cells $flatten\cpu.$procdff$4525 $flatten\cpu.$reduce_or$upstream/picorv32.v:859$1055
	if (posedge_p_clk) {
		p_cpu_2e_is__lui__auipc__jal.next = reduce_or<1>(p_cpu_2e_instr__jal.curr.concat(p_cpu_2e_instr__auipc.curr).concat(p_cpu_2e_instr__lui.curr).val());
	}
	// cells $flatten\cpu.$procdff$4526 $flatten\cpu.$procmux$3509 $flatten\cpu.$eq$upstream/picorv32.v:875$1077
	if (posedge_p_clk) {
		p_cpu_2e_is__lb__lh__lw__lbu__lhu.next = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1446_24_1397__Y ? eq_uu<1>(p_cpu_2e_mem__rdata__latched.slice<6,0>().val(), value<2>{0x3u}) : p_cpu_2e_is__lb__lh__lw__lbu__lhu.curr);
	}
	// cells $flatten\cpu.$procdff$4527 $flatten\cpu.$procmux$3493 $flatten\cpu.$logic_and$upstream/picorv32.v:1095$1292
	if (posedge_p_clk) {
		p_cpu_2e_is__slli__srli__srai.next = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? logic_and<1>(p_cpu_2e_is__alu__reg__imm.curr, i_flatten_5c_cpu_2e__24_reduce__or_24_upstream_2f_picorv32_2e_v_3a_1095_24_1291__Y) : p_cpu_2e_is__slli__srli__srai.curr);
	}
	// cells $flatten\cpu.$procdff$4528 $flatten\cpu.$procmux$3491 $flatten\cpu.$logic_or$upstream/picorv32.v:1101$1301 $flatten\cpu.$logic_and$upstream/picorv32.v:1101$1300 $flatten\cpu.$reduce_or$upstream/picorv32.v:1101$1299
	if (posedge_p_clk) {
		p_cpu_2e_is__jalr__addi__slti__sltiu__xori__ori__andi.next = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? logic_or<1>(p_cpu_2e_instr__jalr.curr, logic_and<1>(p_cpu_2e_is__alu__reg__imm.curr, reduce_or<1>(i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1059_24_1166__Y.concat(i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1049_24_1150__Y).concat(i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1045_24_1144__Y).concat(i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1044_24_1142__Y).concat(i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1042_24_1138__Y).concat(i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1040_24_1134__Y).val()))) : p_cpu_2e_is__jalr__addi__slti__sltiu__xori__ori__andi.curr);
	}
	// cells $flatten\cpu.$procdff$4529 $flatten\cpu.$procmux$3489 $flatten\cpu.$eq$upstream/picorv32.v:876$1078
	if (posedge_p_clk) {
		p_cpu_2e_is__sb__sh__sw.next = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1446_24_1397__Y ? eq_uu<1>(p_cpu_2e_mem__rdata__latched.slice<6,0>().val(), value<6>{0x23u}) : p_cpu_2e_is__sb__sh__sw.curr);
	}
	// cells $flatten\cpu.$procdff$4530 $flatten\cpu.$procmux$3478 $flatten\cpu.$logic_and$upstream/picorv32.v:1110$1312
	if (posedge_p_clk) {
		p_cpu_2e_is__sll__srl__sra.next = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? logic_and<1>(p_cpu_2e_is__alu__reg__reg.curr, i_flatten_5c_cpu_2e__24_reduce__or_24_upstream_2f_picorv32_2e_v_3a_1095_24_1291__Y) : p_cpu_2e_is__sll__srl__sra.curr);
	}
	// cells $flatten\cpu.$procdff$4531 $flatten\cpu.$procmux$3407 $flatten\cpu.$reduce_or$upstream/picorv32.v:860$1056
	if (posedge_p_clk) {
		p_cpu_2e_is__lui__auipc__jal__jalr__addi__add__sub.next = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? value<1>{0u} : reduce_or<1>(p_cpu_2e_instr__sub.curr.concat(p_cpu_2e_instr__add.curr).concat(p_cpu_2e_instr__addi.curr).concat(p_cpu_2e_instr__jalr.curr).concat(p_cpu_2e_instr__jal.curr).concat(p_cpu_2e_instr__auipc.curr).concat(p_cpu_2e_instr__lui.curr).val()));
	}
	// cells $flatten\cpu.$procdff$4532 $flatten\cpu.$reduce_or$upstream/picorv32.v:861$1057
	if (posedge_p_clk) {
		p_cpu_2e_is__slti__blt__slt.next = reduce_or<1>(p_cpu_2e_instr__slt.curr.concat(p_cpu_2e_instr__slti.curr).concat(p_cpu_2e_instr__blt.curr).val());
	}
	// cells $flatten\cpu.$procdff$4533 $flatten\cpu.$reduce_or$upstream/picorv32.v:862$1058
	if (posedge_p_clk) {
		p_cpu_2e_is__sltiu__bltu__sltu.next = reduce_or<1>(p_cpu_2e_instr__sltu.curr.concat(p_cpu_2e_instr__sltiu.curr).concat(p_cpu_2e_instr__bltu.curr).val());
	}
	// cells $flatten\cpu.$procdff$4534 $flatten\cpu.$procmux$3476 $flatten\cpu.$procmux$3474 $flatten\cpu.$eq$upstream/picorv32.v:874$1076
	if (posedge_p_clk) {
		p_cpu_2e_is__beq__bne__blt__bge__bltu__bgeu.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1446_24_1397__Y ? eq_uu<1>(p_cpu_2e_mem__rdata__latched.slice<6,0>().val(), value<7>{0x63u}) : p_cpu_2e_is__beq__bne__blt__bge__bltu__bgeu.curr) : value<1>{0u});
	}
	// cells $flatten\cpu.$procdff$4535 $flatten\cpu.$reduce_or$upstream/picorv32.v:863$1059
	if (posedge_p_clk) {
		p_cpu_2e_is__lbu__lhu__lw.next = reduce_or<1>(p_cpu_2e_instr__lhu.curr.concat(p_cpu_2e_instr__lbu.curr).concat(p_cpu_2e_instr__lw.curr).val());
	}
	// cells $flatten\cpu.$procdff$4536 $flatten\cpu.$procmux$3464 $flatten\cpu.$eq$upstream/picorv32.v:877$1079
	if (posedge_p_clk) {
		p_cpu_2e_is__alu__reg__imm.next = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1446_24_1397__Y ? eq_uu<1>(p_cpu_2e_mem__rdata__latched.slice<6,0>().val(), value<5>{0x13u}) : p_cpu_2e_is__alu__reg__imm.curr);
	}
	// cells $flatten\cpu.$procdff$4537 $flatten\cpu.$procmux$3428 $flatten\cpu.$eq$upstream/picorv32.v:878$1080
	if (posedge_p_clk) {
		p_cpu_2e_is__alu__reg__reg.next = (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1446_24_1397__Y ? eq_uu<1>(p_cpu_2e_mem__rdata__latched.slice<6,0>().val(), value<6>{0x33u}) : p_cpu_2e_is__alu__reg__reg.curr);
	}
	// cells $flatten\cpu.$procdff$4538 $flatten\cpu.$procmux$3517 $flatten\cpu.$procmux$3515 $flatten\cpu.$reduce_or$upstream/picorv32.v:864$1060
	if (posedge_p_clk) {
		p_cpu_2e_is__compare.next = (p_cpu_2e_resetn ? (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1037_24_1133__Y ? value<1>{0u} : reduce_or<1>(p_cpu_2e_is__beq__bne__blt__bge__bltu__bgeu.curr.concat(p_cpu_2e_instr__sltu.curr).concat(p_cpu_2e_instr__slt.curr).concat(p_cpu_2e_instr__sltiu.curr).concat(p_cpu_2e_instr__slti.curr).val())) : value<1>{0u});
	}
	// cells $flatten\cpu.$procdff$4554 $flatten\cpu.$procmux$4146 $flatten\cpu.$procmux$4130 $flatten\cpu.$procmux$4140 $flatten\cpu.$procmux$4138 $flatten\cpu.$procmux$4135 $flatten\cpu.$auto$opt_reduce.cc:131:opt_pmux$4596 $flatten\cpu.$procmux$4144 $flatten\cpu.$logic_or$upstream/picorv32.v:569$1028
	if (posedge_p_clk) {
		p_cpu_2e_mem__valid.next = (i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_566_24_1025__Y ? (logic_or<1>(i_flatten_5c_cpu_2e__24_logic__not_24_upstream_2f_picorv32_2e_v_3a_1949_24_1567__Y, p_cpu_2e_mem__ready) ? value<1>{0u} : p_cpu_2e_mem__valid.curr) : (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_380_24_952__Y ? (p_cpu_2e_mem__do__wdata.curr ? value<1>{0x1u} : (i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_380_24_954__Y ? value<1>{0x1u} : p_cpu_2e_mem__valid.curr)) : (reduce_or<1>(i_flatten_5c_cpu_2e__24_procmux_24_4082__CMP.concat(i_flatten_5c_cpu_2e__24_procmux_24_4076__CMP).val()) ? (p_cpu_2e_mem__xfer ? value<1>{0u} : p_cpu_2e_mem__valid.curr) : p_cpu_2e_mem__valid.curr)));
	}
	// cells $flatten\cpu.$procdff$4555 $flatten\cpu.$procmux$4125 $flatten\cpu.$procmux$4122 $flatten\cpu.$procmux$4120 $flatten\cpu.$procmux$4118
	if (posedge_p_clk) {
		p_cpu_2e_mem__instr.next = (i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_566_24_1025__Y ? p_cpu_2e_mem__instr.curr : (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_380_24_952__Y ? (p_cpu_2e_mem__do__wdata.curr ? value<1>{0u} : (i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_380_24_954__Y ? i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_380_24_953__Y : p_cpu_2e_mem__instr.curr)) : p_cpu_2e_mem__instr.curr));
	}
	// cells $flatten\cpu.$procdff$4556 $flatten\cpu.$procmux$4113 $flatten\cpu.$procmux$4110 $flatten\cpu.$ternary$upstream/picorv32.v:382$968 $flatten\cpu.$add$upstream/picorv32.v:382$967 $flatten\cpu.$ternary$upstream/picorv32.v:1213$1328 $flatten\cpu.$logic_and$upstream/picorv32.v:1213$1326
	if (posedge_p_clk) {
		p_cpu_2e_mem__addr.next = (i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_566_24_1025__Y ? p_cpu_2e_mem__addr.curr : (i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_574_24_1029__Y ? (i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_380_24_953__Y ? add_uu<30>((logic_and<1>(p_cpu_2e_latched__store.curr, p_cpu_2e_latched__branch.curr) ? p_cpu_2e_reg__out.curr.slice<31,1>().concat(value<1>{0u}).val() : p_cpu_2e_reg__next__pc.curr).slice<31,2>().val(), value<1>{0u}).concat(value<2>{0u}).val() : p_cpu_2e_reg__op1.curr.slice<31,2>().concat(value<2>{0u}).val()) : p_cpu_2e_mem__addr.curr));
	}
	// cells $flatten\cpu.$procdff$4557 $flatten\cpu.$procmux$4108 $flatten\cpu.$procmux$4105 $flatten\cpu.$procmux$4391
	if (posedge_p_clk) {
		p_cpu_2e_mem__wdata.next = (i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_566_24_1025__Y ? p_cpu_2e_mem__wdata.curr : (p_cpu_2e_mem__la__write ? (i_flatten_5c_cpu_2e__24_procmux_24_4372__CMP ? p_cpu_2e_reg__op2.curr.slice<7,0>().concat(p_cpu_2e_reg__op2.curr.slice<7,0>()).concat(p_cpu_2e_reg__op2.curr.slice<7,0>()).concat(p_cpu_2e_reg__op2.curr.slice<7,0>()).val() : (i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1930_24_1548__Y ? p_cpu_2e_reg__op2.curr.slice<15,0>().concat(p_cpu_2e_reg__op2.curr.slice<15,0>()).val() : (i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1923_24_1541__Y ? p_cpu_2e_reg__op2.curr : value<32>{0u}))) : p_cpu_2e_mem__wdata.curr));
	}
	// cells $flatten\cpu.$procdff$4558 $flatten\cpu.$procmux$4103 $flatten\cpu.$procmux$4100 $flatten\cpu.$procmux$4098
	if (posedge_p_clk) {
		p_cpu_2e_mem__wstrb.next = (i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_566_24_1025__Y ? p_cpu_2e_mem__wstrb.curr : (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_380_24_952__Y ? (i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_380_24_954__Y ? value<4>{0u} : i_flatten_5c_cpu_2e__24_procmux_24_4093__Y) : i_flatten_5c_cpu_2e__24_procmux_24_4093__Y));
	}
	// cells $flatten\cpu.$procdff$4559 $flatten\cpu.$procmux$4091 $flatten\cpu.$procmux$4072 $flatten\cpu.$procmux$4070 $flatten\cpu.$procmux$4074 $flatten\cpu.$procmux$4080 $flatten\cpu.$ternary$upstream/picorv32.v:617$1043 $flatten\cpu.$procmux$4085 $flatten\cpu.$procmux$4083 $flatten\cpu.$procmux$4073_CMP0 $flatten\cpu.$procmux$4089
	if (posedge_p_clk) {
		p_cpu_2e_mem__state.next = (i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_566_24_1025__Y ? (p_cpu_2e_resetn ? p_cpu_2e_mem__state.curr : value<2>{0u}) : (eq_uu<1>(p_cpu_2e_mem__state.curr, value<2>{0x3u}) ? (p_cpu_2e_mem__do__rinst.curr ? value<2>{0u} : p_cpu_2e_mem__state.curr) : (i_flatten_5c_cpu_2e__24_procmux_24_4076__CMP ? (p_cpu_2e_mem__xfer ? value<2>{0u} : p_cpu_2e_mem__state.curr) : (i_flatten_5c_cpu_2e__24_procmux_24_4082__CMP ? (p_cpu_2e_mem__xfer ? (i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_376_24_934__Y ? value<2>{0u} : value<2>{0x3u}) : p_cpu_2e_mem__state.curr) : (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_380_24_952__Y ? (p_cpu_2e_mem__do__wdata.curr ? value<2>{0x2u} : (i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_380_24_954__Y ? value<2>{0x1u} : p_cpu_2e_mem__state.curr)) : p_cpu_2e_mem__state.curr)))));
	}
	// \src: upstream/picorv32.v:430.2-544.5
	// cell $flatten\cpu.$procdff$4564
	if (posedge_p_clk) {
		p_cpu_2e_mem__rdata__q.next = i_flatten_5c_cpu_2e__24_0_5c_mem__rdata__q_5b_31_3a_0_5d_;
	}
	// connection
	p_trap = p_cpu_2e_trap.curr;
	// connection
	p_trace__valid = p_cpu_2e_trace__valid.curr;
	// connection
	p_trace__data = p_cpu_2e_trace__data.curr;
	// connection
	p_mem__wstrb = p_cpu_2e_mem__wstrb.curr;
	// connection
	p_mem__wdata = p_cpu_2e_mem__wdata.curr;
	// connection
	p_mem__valid = p_cpu_2e_mem__valid.curr;
	// connection
	p_mem__instr = p_cpu_2e_mem__instr.curr;
	// connection
	p_mem__addr = p_cpu_2e_mem__addr.curr;
	return converged;
}

void p_core__wrapper::debug_eval() {
	// \src: upstream/picorv32.v:1321.23-1321.58
	value<32> i_flatten_5c_cpu_2e__24_ternary_24_upstream_2f_picorv32_2e_v_3a_1321_24_1363__Y;
	value<1> i_flatten_5c_cpu_2e__24_procmux_24_4372__CMP;
	// \src: upstream/picorv32.v:1353.32-1353.39
	value<32> i_flatten_5c_cpu_2e__24_memrd_24__5c_cpuregs_24_upstream_2f_picorv32_2e_v_3a_1353_24_1382__DATA;
	// \src: upstream/picorv32.v:1352.32-1352.39
	value<32> i_flatten_5c_cpu_2e__24_memrd_24__5c_cpuregs_24_upstream_2f_picorv32_2e_v_3a_1352_24_1379__DATA;
	// \src: upstream/picorv32.v:380.86-380.117
	value<1> i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_380_24_953__Y;
	// \src: upstream/picorv32.v:380.35-380.81
	value<1> i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_380_24_952__Y;
	// \src: upstream/picorv32.v:1320.5-1320.37
	value<1> i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1320_24_1362__Y;
	// \src: upstream/picorv32.v:1930.8-1930.25
	value<1> i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1930_24_1548__Y;
	// \src: upstream/picorv32.v:1923.8-1923.25
	value<1> i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1923_24_1541__Y;
	// \src: upstream/picorv32.v:1313.7-1313.35
	value<1> i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1313_24_1358__Y;
	// \src: upstream/picorv32.v:1317.33-1317.54
	value<32> i_flatten_5c_cpu_2e__24_auto_24_wreduce_2e_cc_3a_513_3a_run_24_4603;
	// \src: upstream/picorv32.v:1500.36-1500.78
	value<32> i_flatten_5c_cpu_2e__24_and_24_upstream_2f_picorv32_2e_v_3a_1500_24_1403__Y;
	// \full_case: 1
	// \parallel_case: 1
	// \src: upstream/picorv32.v:1489.7-1489.7|upstream/picorv32.v:1486.3-1913.10
	// cell $flatten\cpu.$procmux$3168_CMP0
	i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1313_24_1358__Y = eq_uu<1>(p_cpu_2e_cpu__state.curr, value<7>{0x40u});
	// cells $flatten\cpu.$logic_and$upstream/picorv32.v:1320$1362 $flatten\cpu.$logic_not$upstream/picorv32.v:1320$1361
	i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1320_24_1362__Y = logic_and<1>(p_cpu_2e_latched__store.curr, logic_not<1>(p_cpu_2e_latched__branch.curr));
	// cells $flatten\cpu.$procmux$3224 $flatten\cpu.$procmux$3204 $flatten\cpu.$auto$opt_reduce.cc:131:opt_pmux$4582
	p_cpu_2e_cpuregs__write = (i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1313_24_1358__Y ? (reduce_or<1>(i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1320_24_1362__Y.concat(p_cpu_2e_latched__branch.curr).val()) ? value<1>{0x1u} : value<1>{0u}) : value<1>{0u});
	// \src: upstream/picorv32.v:373.21-373.43
	// cell $flatten\cpu.$logic_and$upstream/picorv32.v:373$928
	p_cpu_2e_mem__xfer = logic_and<1>(p_cpu_2e_mem__valid.curr, p_mem__ready);
	// \src: upstream/picorv32.v:1523.53-1523.88
	// cell $flatten\cpu.$ternary$upstream/picorv32.v:1523$1420
	i_flatten_5c_cpu_2e__24_and_24_upstream_2f_picorv32_2e_v_3a_1500_24_1403__Y.slice<31,1>().concat(i_flatten_5c_cpu_2e__24_ternary_24_upstream_2f_picorv32_2e_v_3a_1321_24_1363__Y.slice<0>()) = (p_cpu_2e_latched__stalu.curr ? p_cpu_2e_alu__out__q.curr : p_cpu_2e_reg__out.curr);
	// connection
	i_flatten_5c_cpu_2e__24_and_24_upstream_2f_picorv32_2e_v_3a_1500_24_1403__Y.slice<0>() = value<1>{0u};
	// cells $flatten\cpu.$logic_and$upstream/picorv32.v:376$940 $flatten\cpu.$logic_or$upstream/picorv32.v:376$939 $flatten\cpu.$logic_and$upstream/picorv32.v:376$936 $flatten\cpu.$logic_and$upstream/picorv32.v:376$933 $flatten\cpu.$reduce_or$upstream/picorv32.v:376$932 $flatten\cpu.$logic_or$upstream/picorv32.v:376$935 $flatten\cpu.$logic_and$upstream/picorv32.v:376$938 $flatten\cpu.$reduce_and$upstream/picorv32.v:376$937
	p_cpu_2e_mem__done = logic_and<1>(p_resetn, logic_or<1>(logic_and<1>(logic_and<1>(p_cpu_2e_mem__xfer, reduce_or<1>(p_cpu_2e_mem__state.curr)), logic_or<1>(logic_or<1>(p_cpu_2e_mem__do__rinst.curr, p_cpu_2e_mem__do__rdata.curr), p_cpu_2e_mem__do__wdata.curr)), logic_and<1>(reduce_and<1>(p_cpu_2e_mem__state.curr), p_cpu_2e_mem__do__rinst.curr)));
	// \src: upstream/picorv32.v:679.54-685.84
	// cell $flatten\cpu.$logic_not$upstream/picorv32.v:679$1044
	p_cpu_2e_instr__trap = logic_not<1>(p_cpu_2e_instr__lui.curr.concat(p_cpu_2e_instr__auipc.curr).concat(p_cpu_2e_instr__jal.curr).concat(p_cpu_2e_instr__jalr.curr).concat(p_cpu_2e_instr__beq.curr).concat(p_cpu_2e_instr__bne.curr).concat(p_cpu_2e_instr__blt.curr).concat(p_cpu_2e_instr__bge.curr).concat(p_cpu_2e_instr__bltu.curr).concat(p_cpu_2e_instr__bgeu.curr).concat(p_cpu_2e_instr__lb.curr).concat(p_cpu_2e_instr__lh.curr).concat(p_cpu_2e_instr__lw.curr).concat(p_cpu_2e_instr__lbu.curr).concat(p_cpu_2e_instr__lhu.curr).concat(p_cpu_2e_instr__sb.curr).concat(p_cpu_2e_instr__sh.curr).concat(p_cpu_2e_instr__sw.curr).concat(p_cpu_2e_instr__addi.curr).concat(p_cpu_2e_instr__slti.curr).concat(p_cpu_2e_instr__sltiu.curr).concat(p_cpu_2e_instr__xori.curr).concat(p_cpu_2e_instr__ori.curr).concat(p_cpu_2e_instr__andi.curr).concat(p_cpu_2e_instr__slli.curr).concat(p_cpu_2e_instr__srli.curr).concat(p_cpu_2e_instr__srai.curr).concat(p_cpu_2e_instr__add.curr).concat(p_cpu_2e_instr__sub.curr).concat(p_cpu_2e_instr__sll.curr).concat(p_cpu_2e_instr__slt.curr).concat(p_cpu_2e_instr__sltu.curr).concat(p_cpu_2e_instr__xor.curr).concat(p_cpu_2e_instr__srl.curr).concat(p_cpu_2e_instr__sra.curr).concat(p_cpu_2e_instr__or.curr).concat(p_cpu_2e_instr__and.curr).concat(p_cpu_2e_instr__rdcycle.curr).concat(p_cpu_2e_instr__rdcycleh.curr).concat(p_cpu_2e_instr__rdinstr.curr).concat(p_cpu_2e_instr__rdinstrh.curr).concat(p_cpu_2e_instr__fence.curr).concat(p_cpu_2e_instr__getq.curr).concat(p_cpu_2e_instr__setq.curr).concat(p_cpu_2e_instr__retirq.curr).concat(p_cpu_2e_instr__maskirq.curr).concat(p_cpu_2e_instr__waitirq.curr).concat(p_cpu_2e_instr__timer.curr).val());
	// \src: upstream/picorv32.v:585.20-585.51
	// cell $flatten\cpu.$logic_or$upstream/picorv32.v:585$1034
	i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_380_24_953__Y = logic_or<1>(p_cpu_2e_mem__do__prefetch.curr, p_cpu_2e_mem__do__rinst.curr);
	// \src: upstream/picorv32.v:1241.13-1241.31
	// cell $flatten\cpu.$eq$upstream/picorv32.v:1241$1574
	p_cpu_2e_alu__eq = eq_uu<1>(p_cpu_2e_reg__op1.curr, p_cpu_2e_reg__op2.curr);
	// \src: upstream/picorv32.v:1242.14-1242.49
	// cell $flatten\cpu.$lt$upstream/picorv32.v:1242$1575
	p_cpu_2e_alu__lts = lt_ss<1>(p_cpu_2e_reg__op1.curr, p_cpu_2e_reg__op2.curr);
	// \src: upstream/picorv32.v:1243.14-1243.31
	// cell $flatten\cpu.$lt$upstream/picorv32.v:1243$1576
	p_cpu_2e_alu__ltu = lt_uu<1>(p_cpu_2e_reg__op1.curr, p_cpu_2e_reg__op2.curr);
	// \full_case: 1
	// \src: upstream/picorv32.v:581.20-581.20|upstream/picorv32.v:581.4-636.11
	// cell $flatten\cpu.$procmux$4087_CMP0
	i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_380_24_952__Y = logic_not<1>(p_cpu_2e_mem__state.curr);
	// \full_case: 1
	// \src: upstream/picorv32.v:408.7-408.7|upstream/picorv32.v:403.3-427.10
	// cell $flatten\cpu.$procmux$4379_CMP0
	i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1930_24_1548__Y = eq_uu<1>(p_cpu_2e_mem__wordsize.curr, value<1>{0x1u});
	// \full_case: 1
	// \src: upstream/picorv32.v:416.7-416.7|upstream/picorv32.v:403.3-427.10
	// cell $flatten\cpu.$procmux$4387_CMP0
	i_flatten_5c_cpu_2e__24_procmux_24_4372__CMP = eq_uu<1>(p_cpu_2e_mem__wordsize.curr, value<2>{0x2u});
	// \full_case: 1
	// \src: upstream/picorv32.v:403.22-403.22|upstream/picorv32.v:403.3-427.10
	// cell $flatten\cpu.$procmux$4389_CMP0
	i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1923_24_1541__Y = logic_not<1>(p_cpu_2e_mem__wordsize.curr);
	// connection
	i_flatten_5c_cpu_2e__24_ternary_24_upstream_2f_picorv32_2e_v_3a_1321_24_1363__Y.slice<31,1>() = i_flatten_5c_cpu_2e__24_and_24_upstream_2f_picorv32_2e_v_3a_1500_24_1403__Y.slice<31,1>().val();
	// cells $flatten\cpu.$procmux$4381 $flatten\cpu.$procmux$4366 $flatten\cpu.$procmux$4367_CMP0 $flatten\cpu.$procmux$4368_CMP0 $flatten\cpu.$procmux$4369_CMP0 $flatten\cpu.$procmux$4370_CMP0 $flatten\cpu.$procmux$4375 $flatten\cpu.$procmux$4377_CMP0
	p_cpu_2e_mem__rdata__word = (i_flatten_5c_cpu_2e__24_procmux_24_4372__CMP ? (eq_uu<1>(p_cpu_2e_reg__op1.curr.slice<1,0>().val(), value<2>{0x3u}) ? value<24>{0u}.concat(p_mem__rdata.slice<31,24>()).val() : (eq_uu<1>(p_cpu_2e_reg__op1.curr.slice<1,0>().val(), value<2>{0x2u}) ? value<24>{0u}.concat(p_mem__rdata.slice<23,16>()).val() : (eq_uu<1>(p_cpu_2e_reg__op1.curr.slice<1,0>().val(), value<1>{0x1u}) ? value<24>{0u}.concat(p_mem__rdata.slice<15,8>()).val() : (logic_not<1>(p_cpu_2e_reg__op1.curr.slice<1,0>().val()) ? value<24>{0u}.concat(p_mem__rdata.slice<7,0>()).val() : value<32>{0u})))) : (i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1930_24_1548__Y ? (p_cpu_2e_reg__op1.curr.slice<1>().val() ? value<16>{0u}.concat(p_mem__rdata.slice<31,16>()).val() : (not_u<1>(p_cpu_2e_reg__op1.curr.slice<1>().val()) ? value<16>{0u}.concat(p_mem__rdata.slice<15,0>()).val() : value<32>{0u})) : (i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1923_24_1541__Y ? p_mem__rdata : value<32>{0u})));
	// cells $flatten\cpu.$procmux$3242 $flatten\cpu.$logic_not$upstream/picorv32.v:1260$1332 $flatten\cpu.$logic_not$upstream/picorv32.v:1258$1331 $flatten\cpu.$logic_not$upstream/picorv32.v:1256$1330
	p_cpu_2e_alu__out__0 = (p_cpu_2e_is__sltiu__bltu__sltu.curr ? p_cpu_2e_alu__ltu : (p_cpu_2e_is__slti__blt__slt.curr ? p_cpu_2e_alu__lts : (p_cpu_2e_instr__bgeu.curr ? logic_not<1>(p_cpu_2e_alu__ltu) : (p_cpu_2e_instr__bge.curr ? logic_not<1>(p_cpu_2e_alu__lts) : (p_cpu_2e_instr__bne.curr ? logic_not<1>(p_cpu_2e_alu__eq) : (p_cpu_2e_instr__beq.curr ? p_cpu_2e_alu__eq : value<1>{0u}))))));
	// cells $flatten\cpu.$logic_and$upstream/picorv32.v:379$949 $flatten\cpu.$logic_and$upstream/picorv32.v:379$948
	p_cpu_2e_mem__la__write = logic_and<1>(logic_and<1>(p_resetn, i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_380_24_952__Y), p_cpu_2e_mem__do__wdata.curr);
	// cells $flatten\cpu.$procmux$4386 $flatten\cpu.$shl$upstream/picorv32.v:419$984 $flatten\cpu.$ternary$upstream/picorv32.v:411$983
	p_cpu_2e_mem__la__wstrb = (i_flatten_5c_cpu_2e__24_procmux_24_4372__CMP ? shl_uu<4>(value<1>{0x1u}, p_cpu_2e_reg__op1.curr.slice<1,0>().val()) : (i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1930_24_1548__Y ? (p_cpu_2e_reg__op1.curr.slice<1>().val() ? value<4>{0xcu} : value<4>{0x3u}) : (i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1923_24_1541__Y ? value<4>{0xfu} : value<4>{0u})));
	// cells $flatten\cpu.$logic_and$upstream/picorv32.v:380$965 $flatten\cpu.$logic_and$upstream/picorv32.v:380$955
	p_cpu_2e_mem__la__read = logic_and<1>(p_resetn, logic_and<1>(i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_380_24_952__Y, logic_or<1>(i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_380_24_953__Y, p_cpu_2e_mem__do__rdata.curr)));
	// \src: upstream/picorv32.v:1317.33-1317.54
	// cell $flatten\cpu.$ternary$upstream/picorv32.v:1317$1359
	i_flatten_5c_cpu_2e__24_auto_24_wreduce_2e_cc_3a_513_3a_run_24_4603.slice<2,0>() = (p_cpu_2e_latched__compr.curr ? value<3>{0x2u} : value<3>{0x4u});
	// connection
	i_flatten_5c_cpu_2e__24_auto_24_wreduce_2e_cc_3a_513_3a_run_24_4603.slice<31,3>() = value<29>{0u};
	// memory \cpu.cpuregs read port 0
	auto tmp_5 = memory_index(p_cpu_2e_decoded__rs1.curr, 0, 32);
	CXXRTL_ASSERT(tmp_5.valid && "out of bounds read");
	if(tmp_5.valid) {
		value<32> tmp_6 = memory_p_cpu_2e_cpuregs[tmp_5.index];
		i_flatten_5c_cpu_2e__24_memrd_24__5c_cpuregs_24_upstream_2f_picorv32_2e_v_3a_1352_24_1379__DATA = tmp_6;
	} else {
		i_flatten_5c_cpu_2e__24_memrd_24__5c_cpuregs_24_upstream_2f_picorv32_2e_v_3a_1352_24_1379__DATA = value<32> {};
	}
	// memory \cpu.cpuregs read port 1
	auto tmp_7 = memory_index(p_cpu_2e_decoded__rs2.curr, 0, 32);
	CXXRTL_ASSERT(tmp_7.valid && "out of bounds read");
	if(tmp_7.valid) {
		value<32> tmp_8 = memory_p_cpu_2e_cpuregs[tmp_7.index];
		i_flatten_5c_cpu_2e__24_memrd_24__5c_cpuregs_24_upstream_2f_picorv32_2e_v_3a_1353_24_1382__DATA = tmp_8;
	} else {
		i_flatten_5c_cpu_2e__24_memrd_24__5c_cpuregs_24_upstream_2f_picorv32_2e_v_3a_1353_24_1382__DATA = value<32> {};
	}
	// cells $flatten\cpu.$ternary$upstream/picorv32.v:1213$1328 $flatten\cpu.$logic_and$upstream/picorv32.v:1213$1326
	p_cpu_2e_next__pc = (logic_and<1>(p_cpu_2e_latched__store.curr, p_cpu_2e_latched__branch.curr) ? p_cpu_2e_reg__out.curr.slice<31,1>().concat(value<1>{0u}).val() : p_cpu_2e_reg__next__pc.curr);
	// cells $flatten\cpu.$ternary$upstream/picorv32.v:1352$1381 $flatten\cpu.$reduce_bool$upstream/picorv32.v:1352$1380
	p_cpu_2e_cpuregs__rs1 = (reduce_bool<1>(p_cpu_2e_decoded__rs1.curr) ? i_flatten_5c_cpu_2e__24_memrd_24__5c_cpuregs_24_upstream_2f_picorv32_2e_v_3a_1352_24_1379__DATA : value<32>{0u});
	// cells $flatten\cpu.$ternary$upstream/picorv32.v:1353$1384 $flatten\cpu.$reduce_bool$upstream/picorv32.v:1353$1383
	p_cpu_2e_cpuregs__rs2 = (reduce_bool<1>(p_cpu_2e_decoded__rs2.curr) ? i_flatten_5c_cpu_2e__24_memrd_24__5c_cpuregs_24_upstream_2f_picorv32_2e_v_3a_1353_24_1382__DATA : value<32>{0u});
	// \src: upstream/picorv32.v:384.39-384.96
	// cell $flatten\cpu.$ternary$upstream/picorv32.v:384$970
	p_cpu_2e_mem__rdata__latched = (p_cpu_2e_mem__xfer ? p_mem__rdata : p_cpu_2e_mem__rdata__q.curr);
	// cells $flatten\cpu.$ternary$upstream/picorv32.v:382$968 $flatten\cpu.$add$upstream/picorv32.v:382$967 $flatten\cpu.$ternary$upstream/picorv32.v:1213$1328 $flatten\cpu.$logic_and$upstream/picorv32.v:1213$1326
	p_cpu_2e_mem__la__addr = (i_flatten_5c_cpu_2e__24_logic__or_24_upstream_2f_picorv32_2e_v_3a_380_24_953__Y ? add_uu<30>(p_cpu_2e_next__pc.slice<31,2>().val(), value<1>{0u}).concat(value<2>{0u}).val() : p_cpu_2e_reg__op1.curr.slice<31,2>().concat(value<2>{0u}).val());
	// \full_case: 1
	// \src: upstream/picorv32.v:416.7-416.7|upstream/picorv32.v:403.3-427.10
	// cell $flatten\cpu.$procmux$4391
	p_cpu_2e_mem__la__wdata = (i_flatten_5c_cpu_2e__24_procmux_24_4372__CMP ? p_cpu_2e_reg__op2.curr.slice<7,0>().concat(p_cpu_2e_reg__op2.curr.slice<7,0>()).concat(p_cpu_2e_reg__op2.curr.slice<7,0>()).concat(p_cpu_2e_reg__op2.curr.slice<7,0>()).val() : (i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1930_24_1548__Y ? p_cpu_2e_reg__op2.curr.slice<15,0>().concat(p_cpu_2e_reg__op2.curr.slice<15,0>()).val() : (i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1923_24_1541__Y ? p_cpu_2e_reg__op2.curr : value<32>{0u})));
	// cells $flatten\cpu.$procmux$3221 $flatten\cpu.$procmux$3213 $flatten\cpu.$add$upstream/picorv32.v:1317$1360
	p_cpu_2e_cpuregs__wrdata = (i_flatten_5c_cpu_2e__24_eq_24_upstream_2f_picorv32_2e_v_3a_1313_24_1358__Y ? (i_flatten_5c_cpu_2e__24_logic__and_24_upstream_2f_picorv32_2e_v_3a_1320_24_1362__Y ? i_flatten_5c_cpu_2e__24_and_24_upstream_2f_picorv32_2e_v_3a_1500_24_1403__Y.slice<31,1>().concat(i_flatten_5c_cpu_2e__24_ternary_24_upstream_2f_picorv32_2e_v_3a_1321_24_1363__Y.slice<0>()).val() : (p_cpu_2e_latched__branch.curr ? add_uu<32>(p_cpu_2e_reg__pc.curr, i_flatten_5c_cpu_2e__24_auto_24_wreduce_2e_cc_3a_513_3a_run_24_4603.slice<2,0>().val()) : value<32>{0u})) : value<32>{0u});
	// cells $flatten\cpu.$ternary$upstream/picorv32.v:1240$1573 $flatten\cpu.$add$upstream/picorv32.v:1240$1572 $flatten\cpu.$sub$upstream/picorv32.v:1240$1571
	p_cpu_2e_alu__add__sub = (p_cpu_2e_instr__sub.curr ? sub_uu<32>(p_cpu_2e_reg__op1.curr, p_cpu_2e_reg__op2.curr) : add_uu<32>(p_cpu_2e_reg__op1.curr, p_cpu_2e_reg__op2.curr));
	// cells $flatten\cpu.$procmux$3233 $flatten\cpu.$and$upstream/picorv32.v:1279$1344 $flatten\cpu.$or$upstream/picorv32.v:1277$1342 $flatten\cpu.$xor$upstream/picorv32.v:1275$1340 $flatten\cpu.$ternary$upstream/picorv32.v:1240$1573 $flatten\cpu.$add$upstream/picorv32.v:1240$1572 $flatten\cpu.$sub$upstream/picorv32.v:1240$1571 $flatten\cpu.$logic_or$upstream/picorv32.v:1278$1343 $flatten\cpu.$logic_or$upstream/picorv32.v:1276$1341 $flatten\cpu.$logic_or$upstream/picorv32.v:1274$1339
	p_cpu_2e_alu__out = (logic_or<1>(p_cpu_2e_instr__andi.curr, p_cpu_2e_instr__and.curr) ? and_uu<32>(p_cpu_2e_reg__op1.curr, p_cpu_2e_reg__op2.curr) : (logic_or<1>(p_cpu_2e_instr__ori.curr, p_cpu_2e_instr__or.curr) ? or_uu<32>(p_cpu_2e_reg__op1.curr, p_cpu_2e_reg__op2.curr) : (logic_or<1>(p_cpu_2e_instr__xori.curr, p_cpu_2e_instr__xor.curr) ? xor_uu<32>(p_cpu_2e_reg__op1.curr, p_cpu_2e_reg__op2.curr) : (p_cpu_2e_is__compare.curr ? value<31>{0u}.concat(p_cpu_2e_alu__out__0).val() : (p_cpu_2e_is__lui__auipc__jal__jalr__addi__add__sub.curr ? p_cpu_2e_alu__add__sub : value<32>{0u})))));
}

CXXRTL_EXTREMELY_COLD
void p_core__wrapper::debug_info(debug_items *items, debug_scopes *scopes, std::string path, metadata_map &&cell_attrs) {
	assert(path.empty() || path[path.size() - 1] == ' ');
	if (scopes) {
		scopes->add(path.empty() ? path : path.substr(0, path.size() - 1), "core_wrapper", metadata_map({
			{ "top", UINT64_C(1) },
			{ "src", "core_wrapper.v:1.1-13.10" },
		}), std::move(cell_attrs));
		scopes->add(path, "cpu", "picorv32", "dynports\000u\000\000\000\000\000\000\000\001hdlname\000spicorv32\000src\000supstream/picorv32.v:62.1-2167.10\000", "src\000score_wrapper.v:8.43-12.52\000");
	}
	if (items) {
		items->add(path, "cpu trap", "src\000supstream/picorv32.v:91.13-91.17\000", p_cpu_2e_trap, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu trace_valid", "src\000supstream/picorv32.v:158.20-158.31\000", p_cpu_2e_trace__valid, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu trace_data", "src\000supstream/picorv32.v:159.20-159.30\000", p_cpu_2e_trace__data, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu resetn", "src\000supstream/picorv32.v:90.13-90.19\000", debug_alias(), p_resetn);
		items->add(path, "cpu reg_sh", "src\000supstream/picorv32.v:177.12-177.18\000", p_cpu_2e_reg__sh, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu reg_pc", "src\000supstream/picorv32.v:176.13-176.19\000", p_cpu_2e_reg__pc, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu reg_out", "src\000supstream/picorv32.v:176.52-176.59\000", p_cpu_2e_reg__out, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu reg_op2", "src\000supstream/picorv32.v:176.43-176.50\000", p_cpu_2e_reg__op2, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu reg_op1", "src\000supstream/picorv32.v:176.34-176.41\000", p_cpu_2e_reg__op1, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu reg_next_pc", "src\000supstream/picorv32.v:176.21-176.32\000", p_cpu_2e_reg__next__pc, 0, debug_item::DRIVEN_SYNC);
		static const value<1> const_p_cpu_2e_pcpi__wr = value<1>{0u};
		items->add(path, "cpu pcpi_wr", "src\000supstream/picorv32.v:114.20-114.27\000", const_p_cpu_2e_pcpi__wr);
		static const value<1> const_p_cpu_2e_pcpi__wait = value<1>{0u};
		items->add(path, "cpu pcpi_wait", "src\000supstream/picorv32.v:116.20-116.29\000", const_p_cpu_2e_pcpi__wait);
		items->add(path, "cpu pcpi_valid", "src\000supstream/picorv32.v:110.20-110.30\000", p_cpu_2e_pcpi__valid, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu pcpi_rs2", "src\000supstream/picorv32.v:113.20-113.28\000", debug_alias(), p_cpu_2e_reg__op2);
		items->add(path, "cpu pcpi_rs1", "src\000supstream/picorv32.v:112.20-112.28\000", debug_alias(), p_cpu_2e_reg__op1);
		static const value<1> const_p_cpu_2e_pcpi__ready = value<1>{0u};
		items->add(path, "cpu pcpi_ready", "src\000supstream/picorv32.v:117.20-117.30\000", const_p_cpu_2e_pcpi__ready);
		static const value<32> const_p_cpu_2e_pcpi__rd = value<32>{0u};
		items->add(path, "cpu pcpi_rd", "src\000supstream/picorv32.v:115.20-115.27\000", const_p_cpu_2e_pcpi__rd);
		static const value<1> const_p_cpu_2e_pcpi__mul__wr = value<1>{0u};
		items->add(path, "cpu pcpi_mul_wr", "src\000supstream/picorv32.v:257.14-257.25\000", const_p_cpu_2e_pcpi__mul__wr);
		static const value<1> const_p_cpu_2e_pcpi__mul__wait = value<1>{0u};
		items->add(path, "cpu pcpi_mul_wait", "src\000supstream/picorv32.v:259.14-259.27\000", const_p_cpu_2e_pcpi__mul__wait);
		static const value<1> const_p_cpu_2e_pcpi__mul__ready = value<1>{0u};
		items->add(path, "cpu pcpi_mul_ready", "src\000supstream/picorv32.v:260.14-260.28\000", const_p_cpu_2e_pcpi__mul__ready);
		static const value<32> const_p_cpu_2e_pcpi__mul__rd = value<32>{0u};
		items->add(path, "cpu pcpi_mul_rd", "src\000supstream/picorv32.v:258.14-258.25\000", const_p_cpu_2e_pcpi__mul__rd);
		static const value<1> const_p_cpu_2e_pcpi__int__wr = value<1>{0u};
		items->add(path, "cpu pcpi_int_wr", "src\000supstream/picorv32.v:267.13-267.24\000", const_p_cpu_2e_pcpi__int__wr);
		static const value<1> const_p_cpu_2e_pcpi__int__wait = value<1>{0u};
		items->add(path, "cpu pcpi_int_wait", "src\000supstream/picorv32.v:269.13-269.26\000", const_p_cpu_2e_pcpi__int__wait);
		static const value<1> const_p_cpu_2e_pcpi__int__ready = value<1>{0u};
		items->add(path, "cpu pcpi_int_ready", "src\000supstream/picorv32.v:270.13-270.27\000", const_p_cpu_2e_pcpi__int__ready);
		static const value<32> const_p_cpu_2e_pcpi__int__rd = value<32>{0u};
		items->add(path, "cpu pcpi_int_rd", "src\000supstream/picorv32.v:268.13-268.24\000", const_p_cpu_2e_pcpi__int__rd);
		items->add(path, "cpu pcpi_insn", "src\000supstream/picorv32.v:111.20-111.29\000", p_cpu_2e_pcpi__insn, 0, debug_item::DRIVEN_SYNC);
		static const value<1> const_p_cpu_2e_pcpi__div__wr = value<1>{0u};
		items->add(path, "cpu pcpi_div_wr", "src\000supstream/picorv32.v:262.14-262.25\000", const_p_cpu_2e_pcpi__div__wr);
		static const value<1> const_p_cpu_2e_pcpi__div__wait = value<1>{0u};
		items->add(path, "cpu pcpi_div_wait", "src\000supstream/picorv32.v:264.14-264.27\000", const_p_cpu_2e_pcpi__div__wait);
		static const value<1> const_p_cpu_2e_pcpi__div__ready = value<1>{0u};
		items->add(path, "cpu pcpi_div_ready", "src\000supstream/picorv32.v:265.14-265.28\000", const_p_cpu_2e_pcpi__div__ready);
		static const value<32> const_p_cpu_2e_pcpi__div__rd = value<32>{0u};
		items->add(path, "cpu pcpi_div_rd", "src\000supstream/picorv32.v:263.14-263.25\000", const_p_cpu_2e_pcpi__div__rd);
		items->add(path, "cpu next_pc", "src\000supstream/picorv32.v:194.14-194.21\000", debug_eval_outline, p_cpu_2e_next__pc);
		items->add(path, "cpu mem_xfer", "src\000supstream/picorv32.v:360.7-360.15\000", debug_eval_outline, p_cpu_2e_mem__xfer);
		items->add(path, "cpu mem_wstrb", "src\000supstream/picorv32.v:99.20-99.29\000", p_cpu_2e_mem__wstrb, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu mem_wordsize", "src\000supstream/picorv32.v:352.12-352.24\000", p_cpu_2e_mem__wordsize, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu mem_wdata", "src\000supstream/picorv32.v:98.20-98.29\000", p_cpu_2e_mem__wdata, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu mem_valid", "src\000supstream/picorv32.v:93.20-93.29\000", p_cpu_2e_mem__valid, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu mem_state", "src\000supstream/picorv32.v:351.12-351.21\000", p_cpu_2e_mem__state, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu mem_ready", "src\000supstream/picorv32.v:95.20-95.29\000", debug_alias(), p_mem__ready);
		items->add(path, "cpu mem_rdata_word", "src\000supstream/picorv32.v:353.13-353.27\000", debug_eval_outline, p_cpu_2e_mem__rdata__word);
		items->add(path, "cpu mem_rdata_q", "src\000supstream/picorv32.v:354.13-354.24\000", p_cpu_2e_mem__rdata__q, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu mem_rdata_latched_noshuffle", "src\000supstream/picorv32.v:369.14-369.41\000", debug_eval_outline, p_cpu_2e_mem__rdata__latched);
		items->add(path, "cpu mem_rdata_latched", "src\000supstream/picorv32.v:370.14-370.31\000", debug_eval_outline, p_cpu_2e_mem__rdata__latched);
		items->add(path, "cpu mem_rdata", "src\000supstream/picorv32.v:100.20-100.29\000", debug_alias(), p_mem__rdata);
		items->add(path, "cpu mem_la_wstrb", "src\000supstream/picorv32.v:107.20-107.32\000", debug_eval_outline, p_cpu_2e_mem__la__wstrb);
		items->add(path, "cpu mem_la_write", "src\000supstream/picorv32.v:104.20-104.32\000", debug_eval_outline, p_cpu_2e_mem__la__write);
		items->add(path, "cpu mem_la_wdata", "src\000supstream/picorv32.v:106.20-106.32\000", debug_eval_outline, p_cpu_2e_mem__la__wdata);
		static const value<1> const_p_cpu_2e_mem__la__use__prefetched__high__word = value<1>{0u};
		items->add(path, "cpu mem_la_use_prefetched_high_word", "src\000supstream/picorv32.v:372.7-372.38\000", const_p_cpu_2e_mem__la__use__prefetched__high__word);
		items->add(path, "cpu mem_la_read", "src\000supstream/picorv32.v:103.20-103.31\000", debug_eval_outline, p_cpu_2e_mem__la__read);
		static const value<1> const_p_cpu_2e_mem__la__firstword__xfer = value<1>{0u};
		items->add(path, "cpu mem_la_firstword_xfer", "src\000supstream/picorv32.v:363.7-363.28\000", const_p_cpu_2e_mem__la__firstword__xfer);
		static const value<1> const_p_cpu_2e_mem__la__firstword = value<1>{0u};
		items->add(path, "cpu mem_la_firstword", "src\000supstream/picorv32.v:362.7-362.23\000", const_p_cpu_2e_mem__la__firstword);
		items->add(path, "cpu mem_la_addr", "src\000supstream/picorv32.v:105.20-105.31\000", debug_eval_outline, p_cpu_2e_mem__la__addr);
		items->add(path, "cpu mem_instr", "src\000supstream/picorv32.v:94.20-94.29\000", p_cpu_2e_mem__instr, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu mem_done", "src\000supstream/picorv32.v:376.7-376.15\000", debug_eval_outline, p_cpu_2e_mem__done);
		items->add(path, "cpu mem_do_wdata", "src\000supstream/picorv32.v:358.6-358.18\000", p_cpu_2e_mem__do__wdata, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu mem_do_rinst", "src\000supstream/picorv32.v:356.6-356.18\000", p_cpu_2e_mem__do__rinst, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu mem_do_rdata", "src\000supstream/picorv32.v:357.6-357.18\000", p_cpu_2e_mem__do__rdata, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu mem_do_prefetch", "src\000supstream/picorv32.v:355.6-355.21\000", p_cpu_2e_mem__do__prefetch, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu mem_addr", "src\000supstream/picorv32.v:97.20-97.28\000", p_cpu_2e_mem__addr, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu latched_trace", "src\000supstream/picorv32.v:1206.6-1206.19\000", p_cpu_2e_latched__trace, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu latched_store", "src\000supstream/picorv32.v:1202.6-1202.19\000", p_cpu_2e_latched__store, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu latched_stalu", "src\000supstream/picorv32.v:1203.6-1203.19\000", p_cpu_2e_latched__stalu, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu latched_rd", "src\000supstream/picorv32.v:1210.26-1210.36\000", p_cpu_2e_latched__rd, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu latched_is_lu", "src\000supstream/picorv32.v:1207.6-1207.19\000", p_cpu_2e_latched__is__lu, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu latched_is_lh", "src\000supstream/picorv32.v:1208.6-1208.19\000", p_cpu_2e_latched__is__lh, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu latched_is_lb", "src\000supstream/picorv32.v:1209.6-1209.19\000", p_cpu_2e_latched__is__lb, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu latched_compr", "src\000supstream/picorv32.v:1205.6-1205.19\000", p_cpu_2e_latched__compr, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu latched_branch", "src\000supstream/picorv32.v:1204.6-1204.20\000", p_cpu_2e_latched__branch, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu is_sltiu_bltu_sltu", "src\000supstream/picorv32.v:672.6-672.24\000", p_cpu_2e_is__sltiu__bltu__sltu, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu is_slti_blt_slt", "src\000supstream/picorv32.v:671.6-671.21\000", p_cpu_2e_is__slti__blt__slt, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu is_slli_srli_srai", "src\000supstream/picorv32.v:666.6-666.23\000", p_cpu_2e_is__slli__srli__srai, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu is_sll_srl_sra", "src\000supstream/picorv32.v:669.6-669.20\000", p_cpu_2e_is__sll__srl__sra, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu is_sb_sh_sw", "src\000supstream/picorv32.v:668.6-668.17\000", p_cpu_2e_is__sb__sh__sw, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu is_lui_auipc_jal_jalr_addi_add_sub", "src\000supstream/picorv32.v:670.6-670.40\000", p_cpu_2e_is__lui__auipc__jal__jalr__addi__add__sub, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu is_lui_auipc_jal", "src\000supstream/picorv32.v:664.6-664.22\000", p_cpu_2e_is__lui__auipc__jal, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu is_lbu_lhu_lw", "src\000supstream/picorv32.v:674.6-674.19\000", p_cpu_2e_is__lbu__lhu__lw, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu is_lb_lh_lw_lbu_lhu", "src\000supstream/picorv32.v:665.6-665.25\000", p_cpu_2e_is__lb__lh__lw__lbu__lhu, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu is_jalr_addi_slti_sltiu_xori_ori_andi", "src\000supstream/picorv32.v:667.6-667.43\000", p_cpu_2e_is__jalr__addi__slti__sltiu__xori__ori__andi, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu is_compare", "src\000supstream/picorv32.v:677.6-677.16\000", p_cpu_2e_is__compare, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu is_beq_bne_blt_bge_bltu_bgeu", "src\000supstream/picorv32.v:673.6-673.34\000", p_cpu_2e_is__beq__bne__blt__bge__bltu__bgeu, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu is_alu_reg_reg", "src\000supstream/picorv32.v:676.6-676.20\000", p_cpu_2e_is__alu__reg__reg, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu is_alu_reg_imm", "src\000supstream/picorv32.v:675.6-675.20\000", p_cpu_2e_is__alu__reg__imm, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu irq_active", "src\000supstream/picorv32.v:197.6-197.16\000", p_cpu_2e_irq__active, 0, debug_item::DRIVEN_SYNC);
		static const value<32> const_p_cpu_2e_irq = value<32>{0u};
		items->add(path, "cpu irq", "src\000supstream/picorv32.v:120.20-120.23\000", const_p_cpu_2e_irq);
		items->add(path, "cpu instr_xori", "src\000supstream/picorv32.v:649.43-649.53\000", p_cpu_2e_instr__xori, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_xor", "src\000supstream/picorv32.v:650.62-650.71\000", p_cpu_2e_instr__xor, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_waitirq", "src\000supstream/picorv32.v:652.59-652.72\000", p_cpu_2e_instr__waitirq, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_trap", "src\000supstream/picorv32.v:653.7-653.17\000", debug_eval_outline, p_cpu_2e_instr__trap);
		items->add(path, "cpu instr_timer", "src\000supstream/picorv32.v:652.74-652.85\000", p_cpu_2e_instr__timer, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_sw", "src\000supstream/picorv32.v:648.78-648.86\000", p_cpu_2e_instr__sw, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_sub", "src\000supstream/picorv32.v:650.17-650.26\000", p_cpu_2e_instr__sub, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_srli", "src\000supstream/picorv32.v:649.90-649.100\000", p_cpu_2e_instr__srli, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_srl", "src\000supstream/picorv32.v:650.73-650.82\000", p_cpu_2e_instr__srl, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_srai", "src\000supstream/picorv32.v:649.102-649.112\000", p_cpu_2e_instr__srai, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_sra", "src\000supstream/picorv32.v:650.84-650.93\000", p_cpu_2e_instr__sra, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_sltu", "src\000supstream/picorv32.v:650.50-650.60\000", p_cpu_2e_instr__sltu, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_sltiu", "src\000supstream/picorv32.v:649.30-649.41\000", p_cpu_2e_instr__sltiu, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_slti", "src\000supstream/picorv32.v:649.18-649.28\000", p_cpu_2e_instr__slti, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_slt", "src\000supstream/picorv32.v:650.39-650.48\000", p_cpu_2e_instr__slt, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_slli", "src\000supstream/picorv32.v:649.78-649.88\000", p_cpu_2e_instr__slli, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_sll", "src\000supstream/picorv32.v:650.28-650.37\000", p_cpu_2e_instr__sll, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_sh", "src\000supstream/picorv32.v:648.68-648.76\000", p_cpu_2e_instr__sh, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_setq", "src\000supstream/picorv32.v:652.18-652.28\000", p_cpu_2e_instr__setq, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_sb", "src\000supstream/picorv32.v:648.58-648.66\000", p_cpu_2e_instr__sb, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_retirq", "src\000supstream/picorv32.v:652.30-652.42\000", p_cpu_2e_instr__retirq, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_rdinstrh", "src\000supstream/picorv32.v:651.52-651.66\000", p_cpu_2e_instr__rdinstrh, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_rdinstr", "src\000supstream/picorv32.v:651.37-651.50\000", p_cpu_2e_instr__rdinstr, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_rdcycleh", "src\000supstream/picorv32.v:651.21-651.35\000", p_cpu_2e_instr__rdcycleh, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_rdcycle", "src\000supstream/picorv32.v:651.6-651.19\000", p_cpu_2e_instr__rdcycle, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_ori", "src\000supstream/picorv32.v:649.55-649.64\000", p_cpu_2e_instr__ori, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_or", "src\000supstream/picorv32.v:650.95-650.103\000", p_cpu_2e_instr__or, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_maskirq", "src\000supstream/picorv32.v:652.44-652.57\000", p_cpu_2e_instr__maskirq, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_lw", "src\000supstream/picorv32.v:648.26-648.34\000", p_cpu_2e_instr__lw, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_lui", "src\000supstream/picorv32.v:646.6-646.15\000", p_cpu_2e_instr__lui, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_lhu", "src\000supstream/picorv32.v:648.47-648.56\000", p_cpu_2e_instr__lhu, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_lh", "src\000supstream/picorv32.v:648.16-648.24\000", p_cpu_2e_instr__lh, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_lbu", "src\000supstream/picorv32.v:648.36-648.45\000", p_cpu_2e_instr__lbu, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_lb", "src\000supstream/picorv32.v:648.6-648.14\000", p_cpu_2e_instr__lb, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_jalr", "src\000supstream/picorv32.v:646.41-646.51\000", p_cpu_2e_instr__jalr, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_jal", "src\000supstream/picorv32.v:646.30-646.39\000", p_cpu_2e_instr__jal, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_getq", "src\000supstream/picorv32.v:652.6-652.16\000", p_cpu_2e_instr__getq, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_fence", "src\000supstream/picorv32.v:651.88-651.99\000", p_cpu_2e_instr__fence, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_bne", "src\000supstream/picorv32.v:647.17-647.26\000", p_cpu_2e_instr__bne, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_bltu", "src\000supstream/picorv32.v:647.50-647.60\000", p_cpu_2e_instr__bltu, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_blt", "src\000supstream/picorv32.v:647.28-647.37\000", p_cpu_2e_instr__blt, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_bgeu", "src\000supstream/picorv32.v:647.62-647.72\000", p_cpu_2e_instr__bgeu, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_bge", "src\000supstream/picorv32.v:647.39-647.48\000", p_cpu_2e_instr__bge, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_beq", "src\000supstream/picorv32.v:647.6-647.15\000", p_cpu_2e_instr__beq, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_auipc", "src\000supstream/picorv32.v:646.17-646.28\000", p_cpu_2e_instr__auipc, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_andi", "src\000supstream/picorv32.v:649.66-649.76\000", p_cpu_2e_instr__andi, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_and", "src\000supstream/picorv32.v:650.105-650.114\000", p_cpu_2e_instr__and, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_addi", "src\000supstream/picorv32.v:649.6-649.16\000", p_cpu_2e_instr__addi, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu instr_add", "src\000supstream/picorv32.v:650.6-650.15\000", p_cpu_2e_instr__add, 0, debug_item::DRIVEN_SYNC);
		static const value<32> const_p_cpu_2e_i = value<32>{0x20u};
		items->add(path, "cpu i", "src\000supstream/picorv32.v:205.10-205.11\000", const_p_cpu_2e_i);
		items->add(path, "cpu eoi", "src\000supstream/picorv32.v:121.20-121.23\000", p_cpu_2e_eoi, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu do_waitirq", "src\000supstream/picorv32.v:1219.6-1219.16\000", p_cpu_2e_do__waitirq, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu decoder_trigger", "src\000supstream/picorv32.v:658.6-658.21\000", p_cpu_2e_decoder__trigger, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu decoder_pseudo_trigger", "src\000supstream/picorv32.v:660.6-660.28\000", p_cpu_2e_decoder__pseudo__trigger, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu decoded_rs2", "src\000supstream/picorv32.v:656.12-656.23\000", p_cpu_2e_decoded__rs2, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu decoded_rs1", "src\000supstream/picorv32.v:655.38-655.49\000", p_cpu_2e_decoded__rs1, 0, debug_item::DRIVEN_SYNC);
		static const value<5> const_p_cpu_2e_decoded__rs = value<5>{0u};
		items->add(path, "cpu decoded_rs", "src\000supstream/picorv32.v:1307.26-1307.36\000", const_p_cpu_2e_decoded__rs);
		items->add(path, "cpu decoded_rd", "src\000supstream/picorv32.v:655.26-655.36\000", p_cpu_2e_decoded__rd, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu decoded_imm_j", "src\000supstream/picorv32.v:657.26-657.39\000", p_cpu_2e_decoded__imm__j, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu decoded_imm", "src\000supstream/picorv32.v:657.13-657.24\000", p_cpu_2e_decoded__imm, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu dbg_mem_wstrb", "src\000supstream/picorv32.v:188.14-188.27\000", debug_alias(), p_cpu_2e_mem__wstrb);
		items->add(path, "cpu dbg_mem_wdata", "src\000supstream/picorv32.v:187.14-187.27\000", debug_alias(), p_cpu_2e_mem__wdata);
		items->add(path, "cpu dbg_mem_valid", "src\000supstream/picorv32.v:183.7-183.20\000", debug_alias(), p_cpu_2e_mem__valid);
		items->add(path, "cpu dbg_mem_ready", "src\000supstream/picorv32.v:185.7-185.20\000", debug_alias(), p_mem__ready);
		items->add(path, "cpu dbg_mem_rdata", "src\000supstream/picorv32.v:189.14-189.27\000", debug_alias(), p_mem__rdata);
		items->add(path, "cpu dbg_mem_instr", "src\000supstream/picorv32.v:184.7-184.20\000", debug_alias(), p_cpu_2e_mem__instr);
		items->add(path, "cpu dbg_mem_addr", "src\000supstream/picorv32.v:186.14-186.26\000", debug_alias(), p_cpu_2e_mem__addr);
		items->add(path, "cpu cpuregs_write", "src\000supstream/picorv32.v:1303.6-1303.19\000", debug_eval_outline, p_cpu_2e_cpuregs__write);
		items->add(path, "cpu cpuregs_wrdata", "src\000supstream/picorv32.v:1304.13-1304.27\000", debug_eval_outline, p_cpu_2e_cpuregs__wrdata);
		items->add(path, "cpu cpuregs_rs2", "src\000supstream/picorv32.v:1306.13-1306.24\000", debug_eval_outline, p_cpu_2e_cpuregs__rs2);
		items->add(path, "cpu cpuregs_rs1", "src\000supstream/picorv32.v:1305.13-1305.24\000", debug_eval_outline, p_cpu_2e_cpuregs__rs1);
		items->add(path, "cpu cpu_state", "src\000supstream/picorv32.v:1181.12-1181.21\000", p_cpu_2e_cpu__state, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu compressed_instr", "src\000supstream/picorv32.v:662.6-662.22\000", p_cpu_2e_compressed__instr, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu clk", "src\000supstream/picorv32.v:90.8-90.11\000", debug_alias(), p_clk);
		items->add(path, "cpu alu_out_q", "src\000supstream/picorv32.v:1221.22-1221.31\000", p_cpu_2e_alu__out__q, 0, debug_item::DRIVEN_SYNC);
		items->add(path, "cpu alu_out_0", "src\000supstream/picorv32.v:1222.6-1222.15\000", debug_eval_outline, p_cpu_2e_alu__out__0);
		items->add(path, "cpu alu_out", "src\000supstream/picorv32.v:1221.13-1221.20\000", debug_eval_outline, p_cpu_2e_alu__out);
		items->add(path, "cpu alu_ltu", "src\000supstream/picorv32.v:1227.14-1227.21\000", debug_eval_outline, p_cpu_2e_alu__ltu);
		items->add(path, "cpu alu_lts", "src\000supstream/picorv32.v:1227.23-1227.30\000", debug_eval_outline, p_cpu_2e_alu__lts);
		items->add(path, "cpu alu_eq", "src\000supstream/picorv32.v:1227.6-1227.12\000", debug_eval_outline, p_cpu_2e_alu__eq);
		items->add(path, "cpu alu_add_sub", "src\000supstream/picorv32.v:1225.13-1225.24\000", debug_eval_outline, p_cpu_2e_alu__add__sub);
		items->add(path, "flatten\\cpu.$0$memwr$\\cpuregs$upstream/picorv32.v:1344$902_EN[31:0]$1372", "src\000supstream/picorv32.v:1337.2-1346.5\000", i_flatten_5c_cpu_2e__24_0_24_memwr_24__5c_cpuregs_24_upstream_2f_picorv32_2e_v_3a_1344_24_902__EN_5b_31_3a_0_5d__24_1372, 0, debug_item::GENERATED|debug_item::DRIVEN_COMB);
		items->add(path, "clk", "src\000score_wrapper.v:1.27-1.30\000", p_clk, 0, debug_item::INPUT|debug_item::UNDRIVEN);
		items->add(path, "mem_addr", "src\000score_wrapper.v:2.48-2.56\000", p_mem__addr, 0, debug_item::OUTPUT|debug_item::DRIVEN_COMB);
		items->add(path, "mem_instr", "src\000score_wrapper.v:2.24-2.33\000", p_mem__instr, 0, debug_item::OUTPUT|debug_item::DRIVEN_COMB);
		items->add(path, "mem_rdata", "src\000score_wrapper.v:1.61-1.70\000", p_mem__rdata, 0, debug_item::INPUT|debug_item::UNDRIVEN);
		items->add(path, "mem_ready", "src\000score_wrapper.v:1.38-1.47\000", p_mem__ready, 0, debug_item::INPUT|debug_item::UNDRIVEN);
		items->add(path, "mem_valid", "src\000score_wrapper.v:2.14-2.23\000", p_mem__valid, 0, debug_item::OUTPUT|debug_item::DRIVEN_COMB);
		items->add(path, "mem_wdata", "src\000score_wrapper.v:2.57-2.66\000", p_mem__wdata, 0, debug_item::OUTPUT|debug_item::DRIVEN_COMB);
		items->add(path, "mem_wstrb", "src\000score_wrapper.v:2.80-2.89\000", p_mem__wstrb, 0, debug_item::OUTPUT|debug_item::DRIVEN_COMB);
		items->add(path, "resetn", "src\000score_wrapper.v:1.31-1.37\000", p_resetn, 0, debug_item::INPUT|debug_item::UNDRIVEN);
		items->add(path, "trace_data", "src\000score_wrapper.v:3.35-3.45\000", p_trace__data, 0, debug_item::OUTPUT|debug_item::DRIVEN_COMB);
		items->add(path, "trace_valid", "src\000score_wrapper.v:3.9-3.20\000", p_trace__valid, 0, debug_item::OUTPUT|debug_item::DRIVEN_COMB);
		items->add(path, "trap", "src\000score_wrapper.v:2.9-2.13\000", p_trap, 0, debug_item::OUTPUT|debug_item::DRIVEN_COMB);
		items->add(path, "cpu cpuregs", "src\000supstream/picorv32.v:203.13-203.20\000", memory_p_cpu_2e_cpuregs, 0);
	}
}

} // namespace cxxrtl_design

extern "C"
cxxrtl_toplevel cxxrtl_design_create() {
	return new _cxxrtl_toplevel { std::unique_ptr<cxxrtl_design::p_core__wrapper>(new cxxrtl_design::p_core__wrapper) };
}
