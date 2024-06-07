`ifndef NODE_IF_SVH
`define NODE_IF_SVH

interface node_if #(
    parameter int MODULATION_ORDER = 16
) (
    input logic clk,
    input logic rst
);
  logic [$clog2(MODULATION_ORDER)-1:0] gray_code;
  logic [$clog2(MODULATION_ORDER)-1:0] binary_code;
  logic dv;

  // Modports for input and output directions
  modport in(input clk, rst, gray_code, dv, binary_code);
  modport out(output gray_code, dv, binary_code);

endinterface

`endif  // NODE_IF_SVH
