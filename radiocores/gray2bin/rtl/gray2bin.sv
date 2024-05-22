interface node_if #(
    parameter int MODULATION_ORDER = 16
) (
    input clk,
    input rst
);

  logic [$clog2(MODULATION_ORDER)-1:0] gray_code;
  logic [$clog2(MODULATION_ORDER)-1:0] binary_code;
  logic dv;
  modport in(input clk, rst, gray_code, binary_code, dv);
  modport out(output gray_code, binary_code, dv);

endinterface

module gray2bin #(
    parameter int MODULATION_ORDER = 16
) (
    input logic clk,
    input logic rst,
    input logic [$clog2(MODULATION_ORDER)-1:0] i_gray_code,
    input logic i_dv,
    output logic [$clog2(MODULATION_ORDER)-1:0] o_binary_code,
    output logic o_dv
);

  localparam int NumNodes = $clog2(MODULATION_ORDER) - 1;

  // Inter-node SVIF
  node_if my_if[NumNodes:0] (
      .clk(clk),
      .rst(rst)
  );

  assign {my_if[0].gray_code, my_if[0].binary_code} = {2{i_gray_code}};
  assign my_if[0].dv = i_dv;

  // Gray to binary conversion nodes
  generate
    // Generate nodes
    for (genvar i = 0; i < NumNodes; i++) begin : gen_nodes
      node node_i (
          .in_if (my_if[i]),
          .out_if(my_if[i+1])
      );
    end : gen_nodes
  endgenerate

  // Output FF
  always_ff @(posedge clk) begin
    if (rst) o_dv <= '0;
    else o_dv <= my_if[NumNodes].dv;

    if (my_if[NumNodes].dv) o_binary_code <= my_if[NumNodes].binary_code;
  end

endmodule

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
