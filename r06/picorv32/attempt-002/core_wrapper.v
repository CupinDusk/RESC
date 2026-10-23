module core_wrapper(input clk,resetn,mem_ready,input [31:0] mem_rdata,
 output trap,mem_valid,mem_instr,output [31:0] mem_addr,mem_wdata,output [3:0] mem_wstrb,
 output trace_valid,output [35:0] trace_data);
 picorv32 #(.ENABLE_COUNTERS(0),.ENABLE_COUNTERS64(0),.ENABLE_REGS_16_31(1),.ENABLE_REGS_DUALPORT(1),
 .LATCHED_MEM_RDATA(0),.TWO_STAGE_SHIFT(1),.BARREL_SHIFTER(0),.TWO_CYCLE_COMPARE(0),.TWO_CYCLE_ALU(0),
 .COMPRESSED_ISA(0),.CATCH_MISALIGN(1),.CATCH_ILLINSN(1),.ENABLE_PCPI(0),.ENABLE_MUL(0),
 .ENABLE_FAST_MUL(0),.ENABLE_DIV(0),.ENABLE_IRQ(0),.ENABLE_TRACE(1),.REGS_INIT_ZERO(1),
 .PROGADDR_RESET(0),.STACKADDR(32'hff00)) cpu
 (.clk(clk),.resetn(resetn),.trap(trap),.mem_valid(mem_valid),.mem_instr(mem_instr),.mem_ready(mem_ready),
 .mem_addr(mem_addr),.mem_wdata(mem_wdata),.mem_wstrb(mem_wstrb),.mem_rdata(mem_rdata),
 .pcpi_wr(1'b0),.pcpi_rd(32'b0),.pcpi_wait(1'b0),.pcpi_ready(1'b0),.irq(32'b0),
 .trace_valid(trace_valid),.trace_data(trace_data));
endmodule
