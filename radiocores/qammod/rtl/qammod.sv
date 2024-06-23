`ifndef QAMMOD_SV
`define QAMMOD_SV

`include "qammod_if.svh"
`include "gray2bin_if.svh"
`include "gray2bin.sv"

module qammod #(
    parameter int MODULATION_ORDER = 16
) (
    qammod_if.in  in_if,  // Input interface
    qammod_if.out out_if  // Output interface
);

  localparam int BitWidth = $clog2(MODULATION_ORDER);
  localparam int Offset = (2 ** $clog2(MODULATION_ORDER) / 2 - 1) / 2;

  // We always need to process I/Q, thus hard coded to 2
  localparam int NumInst = 2;

  // Declare interface array
  gray2bin_if #(MODULATION_ORDER) g2b_if[NumInst](
    .clk(in_if.clk),
    .rst(in_if.rst)
 );

 assign g2b_if[1].gray_code = in_if.s[BitWidth-1:BitWidth/2];  // I
 assign g2b_if[0].gray_code = in_if.s[BitWidth/2-1:0];  // Q
 assign g2b_if[0].i_dv      = in_if.i_dv;
 assign g2b_if[1].i_dv      = in_if.i_dv;

  // Generate block to instantiate interfaces and modules
  generate
    for (genvar i = 0; i < NumInst; i++) begin : gen_gray2bin
      // Instantiate the gray2bin module
      gray2bin #(MODULATION_ORDER) gray2bin_inst (
          .in_if (g2b_if[i].in),
          .out_if(g2b_if[i].out)
      );
    end
  endgenerate

  assign out_if.i = g2b_if[1].binary_code;
  assign out_if.q = g2b_if[0].binary_code;
  assign out_if.o_dv = g2b_if[1].o_dv & g2b_if[1].o_dv;

endmodule

`endif  // QAMMOD_SV
