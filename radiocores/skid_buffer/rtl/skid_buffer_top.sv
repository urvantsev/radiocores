module skid_buffer_top (
    input logic clk,
    input logic rst,

    // Ingress (input) signals
    input  logic       i_valid,
    output logic       i_ready,
    input  logic [7:0] i_data,

    // Egress (output) signals
    output logic       e_valid,
    input  logic       e_ready,
    output logic [7:0] e_data
);

  rv_if rv_i (
    .clk(clk),
    .rst(rst)
  );

  rv_if rv_o (
    .clk(clk),
    .rst(rst)
  );

  // Connect top-level ingress signals to rv_i interface
  assign rv_i.valid = i_valid;
  assign i_ready    = rv_i.ready;
  assign rv_i.data  = i_data;

  // Connect top-level egress signals to rv_o interface
  assign e_valid    = rv_o.valid;
  assign rv_o.ready = e_ready;
  assign e_data     = rv_o.data;

  // Instantiate skid_buffer and connect internal interfaces
  skid_buffer u_skid_buffer (
      .rv_i(rv_i),
      .rv_e(rv_o)
  );

endmodule
