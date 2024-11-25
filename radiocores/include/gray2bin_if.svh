`ifndef GRAY2BIN_IF_SVH
`define GRAY2BIN_IF_SVH

interface gray2bin_if #(
    parameter int MODULATION_ORDER = 16
) (
    input logic clk,
    input logic rst
);
  localparam int BitWidth = $clog2(MODULATION_ORDER)/2;
  logic [BitWidth-1:0] gray_code;
  logic [BitWidth-1:0] binary_code;
  logic i_dv;
  logic o_dv;

  // Modports for input and output directions
  modport in(input clk, rst, gray_code, i_dv);
  modport out(output binary_code, o_dv);

endinterface

`endif  // GRAY2BIN_IF_SVH
