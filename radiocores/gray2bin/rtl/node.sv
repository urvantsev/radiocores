`ifndef NODE_SV
`define NODE_SV

`include "node_if.svh"

module node #(
    parameter int MODULATION_ORDER = 16
) (
    node_if.in  in_if,
    node_if.out out_if
);

  logic [$clog2(MODULATION_ORDER)-1:0] gray_code;
  logic [$clog2(MODULATION_ORDER)-1:0] binary_code;
  logic dv;

  always_ff @(posedge in_if.clk) begin
    if (in_if.rst) dv <= '0;
    else dv <= in_if.dv;

    if (in_if.dv) begin
      gray_code   <= in_if.gray_code >> 1;
      binary_code <= in_if.binary_code;
    end
  end

  always_comb begin
    out_if.gray_code = gray_code;
    out_if.binary_code = binary_code ^ gray_code;
    out_if.dv = dv;
  end

endmodule

`endif  // NODE_SV
