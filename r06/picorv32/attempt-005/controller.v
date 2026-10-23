module controller(input clk,rst,commandreset,start,stop,input[31:0] cfgd,gnum,gden,
 output reg licensed,output reg[1:0] settled,output reg busy,valid,output reg[3:0] reason,
 output reg[31:0] heldd,previousd,phase,pulses,output reg[63:0] timer,output reg pulse);
 wire[63:0] gd={32'b0,gnum}*{32'b0,previousd};
 wire[63:0] dg={32'b0,gden}*{32'b0,cfgd};
 wire[63:0] gd2={32'b0,gnum}*{32'b0,cfgd};
 wire[63:0] dg2={32'b0,gden}*{32'b0,previousd};
 task fail;input[3:0] why;begin valid<=0;busy<=0;licensed<=0;reason<=why;pulse<=0;end endtask
 always @(posedge clk) begin
  pulse<=0;
  if(rst)begin licensed<=0;settled<=0;busy<=0;valid<=0;reason<=0;heldd<=0;previousd<=1000;phase<=0;pulses<=0;timer<=0;end
  else if(commandreset)begin
   if(busy)fail(5);
   else begin
    heldd<=cfgd;phase<=0;pulses<=0;timer<=0;settled<=0;valid<=0;reason<=0;licensed<=1;
    if(cfgd==0||cfgd>2000||gnum==0||gnum>1000||gden==0||gden>1000)fail(6);
    else if(gd<dg||gd2<dg2)fail(3);
   end
  end else if(start)begin
   if(busy)fail(8);
   else if(reason!=0)fail(reason);
   else if(!licensed)fail(1);
   else if(settled<2)fail(2);
   else begin busy<=1;valid<=1;licensed<=0;phase<=0;pulses<=0;timer<=0;previousd<=heldd;end
  end else if(busy)begin
   if(cfgd!=heldd)fail(4);
   else if(stop)busy<=0;
   else if(timer==64'hffffffffffffffff||pulses==32'hffffffff)fail(7);
   else begin timer<=timer+1; if(phase==heldd-1)begin phase<=0;pulse<=1;pulses<=pulses+1;end else phase<=phase+1;end
  end else if(licensed)begin
   if(cfgd!=heldd)begin settled<=0;end else if(settled<2)settled<=settled+1;
  end
 end
endmodule
