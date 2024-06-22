`ifndef GRAY2BIN_SV
`define GRAY2BIN_SV

`include "gray2bin_if.svh"
`include "node_if.svh"
`include "node.sv"

module gray2bin #(
    parameter int MODULATION_ORDER = 16
) (
    gray2bin_if.in  in_if,  // Input interface
    gray2bin_if.out out_if  // Output interface
);

  localparam int NumNodes = $clog2(MODULATION_ORDER)/2;

  // Inter-node SVIF array
  node_if #(MODULATION_ORDER) my_if[NumNodes:0] (
      .clk(in_if.clk),
      .rst(in_if.rst)
  );

  assign {my_if[0].gray_code, my_if[0].binary_code} = {2{in_if.gray_code}};
  assign my_if[0].dv = in_if.i_dv;

  // Gray to binary conversion nodes
  generate
    for (genvar i = 0; i < NumNodes; i++) begin : gen_nodes
      node #(MODULATION_ORDER) node_i (
          .in_if (my_if[i]),
          .out_if(my_if[i+1])
      );
    end
  endgenerate

  // Output FF
  always_ff @(posedge in_if.clk) begin
    if (in_if.rst) out_if.o_dv <= '0;
    else out_if.o_dv <= my_if[NumNodes].dv;
    if (my_if[NumNodes].dv) out_if.binary_code <= my_if[NumNodes].binary_code;
  end

endmodule

`endif  // GRAY2BIN_SV
