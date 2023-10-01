interface node_if #(
    parameter int MODULATION_ORDER = 16
) (
    input clk,
    input rst_n
);

  logic [$clog2(MODULATION_ORDER)-1:0] gray_code;
  logic [$clog2(MODULATION_ORDER)-1:0] binary_code;

  modport in(input clk, rst_n, gray_code, binary_code);
  modport out(output gray_code, binary_code);

endinterface

module gray2bin #(
    parameter int MODULATION_ORDER = 16
) (
    input logic clk,
    input logic rst_n,
    input logic [$clog2(MODULATION_ORDER)-1:0] i_gray_code,
    output logic [$clog2(MODULATION_ORDER)-1:0] o_binary_code
);

  localparam int NumNodes = $clog2(MODULATION_ORDER) - 1;

  // Input flip-flop
  logic [$clog2(MODULATION_ORDER)-1:0] input_ff;

  always_ff @(posedge clk) begin
    if (~rst_n) input_ff <= '0;
    else input_ff <= i_gray_code;
  end

  // Inter-node SVIF
  node_if my_if[NumNodes:0] (
      .clk  (clk),
      .rst_n(rst_n)
  );

  assign {my_if[0].gray_code, my_if[0].binary_code} = {2{input_ff}};

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

  // Output flip-flop
  always_ff @(posedge clk) begin
    o_binary_code <= my_if[NumNodes].binary_code;
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

  always_ff @(posedge in_if.clk) begin
    if (~in_if.rst_n) begin
      gray_code   <= '0;
      binary_code <= '0;
    end else begin
      gray_code   <= in_if.gray_code >> 1;
      binary_code <= in_if.binary_code;
    end
  end

  always_comb begin
    out_if.gray_code   = gray_code;
    out_if.binary_code = binary_code ^ gray_code;
  end

endmodule
