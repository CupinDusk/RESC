// New logical reference design, author owned. Not GPU/native implementation.
// Only clk rising edges are time. jobpulse is a one-reference-edge clock enable.
module reference_job(
  input wire clk, input wire rst, input wire commandreset, input wire start,
  input wire [31:0] cfgn, input wire [31:0] cfgd,
  output reg licensed, output reg [1:0] settled,
  output reg busy, output reg done, output reg valid,
  output reg [3:0] reason,
  output reg [31:0] nlatched, output reg [31:0] heldd,
  output reg [31:0] previousd, output reg [31:0] remaining,
  output reg [31:0] phase, output reg [31:0] pulses,
  output reg [63:0] timer, output reg jobpulse
);
  wire [39:0] dx = {8'b0, cfgd};
  wire [39:0] px = {8'b0, previousd};
  wire guardok = (dx * 40'd200 <= px * 40'd201) &&
                 (px * 40'd200 <= dx * 40'd201);
  always @(posedge clk) begin
    if (rst) begin
      licensed <= 0; settled <= 0; busy <= 0; done <= 0;
      valid <= 0; reason <= 0; nlatched <= 0; heldd <= 0;
      previousd <= 32'd1000; remaining <= 0; phase <= 0;
      pulses <= 0; timer <= 0; jobpulse <= 0;
    end else begin
      jobpulse <= 0;
      if (commandreset) begin
        if (busy) begin
          busy <= 0; done <= 0; valid <= 0; reason <= 4'd5;
          licensed <= 0; settled <= 0;
        end else begin
          licensed <= 1; settled <= 0; done <= 0;
          valid <= 0; reason <= 0; nlatched <= cfgn; heldd <= cfgd;
          remaining <= 0; phase <= 0; pulses <= 0; timer <= 0;
        end
      end else if (busy) begin
        if (cfgd != heldd) begin
          busy <= 0; done <= 0; valid <= 0; reason <= 4'd4;
        end else if (start) begin
          busy <= 0; done <= 0; valid <= 0; reason <= 4'd8;
        end else if (timer == 64'hffffffffffffffff || pulses == 32'hffffffff) begin
          busy <= 0; done <= 0; valid <= 0; reason <= 4'd7;
        end else begin
          timer <= timer + 64'd1;
          if (phase == heldd - 32'd1) begin
            phase <= 0; pulses <= pulses + 32'd1; jobpulse <= 1;
            remaining <= remaining - 32'd1;
            if (remaining == 32'd1) begin busy <= 0; done <= 1; end
          end else phase <= phase + 32'd1;
        end
      end else if (start) begin
        licensed <= 0; done <= 0; valid <= 0;
        if (!licensed) reason <= 4'd1;
        else if (settled != 2 || cfgd != heldd) reason <= 4'd2;
        else if (nlatched == 0 || heldd == 0) reason <= 4'd6;
        else if (!guardok) reason <= 4'd3;
        else begin
          busy <= 1; valid <= 1; reason <= 0;
          previousd <= heldd; remaining <= nlatched;
          timer <= 0; phase <= 0; pulses <= 0;
        end
      end else if (licensed) begin
        if (cfgd != heldd) settled <= 0;
        else if (settled < 2) settled <= settled + 1;
      end
    end
  end
endmodule
