`ifndef QAMMOD_WRAPPER_SV
`define QAMMOD_WRAPPER_SV

`include "qammod_if.svh"
`include "qammod.sv"

module qammod_wrapper #(
    parameter int MODULATION_ORDER = 64
) (
    input logic clk,
    input logic rst,

    input logic i_dv,
    input logic [2*$clog2(MODULATION_ORDER)-1:0] i_s,

    output logic o_dv,
    output logic [$clog2(MODULATION_ORDER)/2-1:0] o_i,
    output logic [$clog2(MODULATION_ORDER)/2-1:0] o_q
);

  // Instantiate the interface
  qammod_if #(MODULATION_ORDER) my_if (
      .clk(clk),
      .rst(rst)
  );

  // Connect the wrapper signals to the interface
  assign my_if.i_dv = i_dv;
  assign my_if.s = i_s;

  assign o_dv = my_if.o_dv;
  assign o_i = my_if.i;
  assign o_q = my_if.q;


  // Instantiate the qammod module
  qammod #(MODULATION_ORDER) qammod_inst (
      .in_if (my_if.in),
      .out_if(my_if.out)
  );

endmodule

`endif  // QAMMOD_WRAPPER_SV
