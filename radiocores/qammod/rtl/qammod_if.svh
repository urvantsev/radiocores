`ifndef QAMMOD_IF_SVH
`define QAMMOD_IF_SVH

interface qammod_if #(
    parameter int MODULATION_ORDER = 16
) (
    input logic clk,
    input logic rst
);
  logic [2*$clog2(MODULATION_ORDER)-1:0] s;
  logic [$clog2(MODULATION_ORDER)/2-1:0] i;
  logic [$clog2(MODULATION_ORDER)/2-1:0] q;
  logic i_dv;
  logic o_dv;

  // Modports for input and output directions
  modport in(input clk, rst, s, i_dv);
  modport out(output i, q, o_dv);

endinterface

`endif  // QAMMOD_IF_SVH
