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

  // Instantiate internal ingress and egress interfaces
  rv_if ingress_if (.clk(clk), .rst(rst));
  rv_if egress_if (.clk(clk), .rst(rst));

  // Connect top-level ingress signals to ingress_if interface
  assign ingress_if.valid = i_valid;
  assign i_ready = ingress_if.ready;
  assign ingress_if.data = i_data;

  // Connect top-level egress signals to egress_if interface
  assign e_valid = egress_if.valid;
  assign egress_if.ready = e_ready;
  assign e_data = egress_if.data;

  // Instantiate skid_buffer and connect internal interfaces
  skid_buffer u_skid_buffer (
      .clk (clk),
      .rst (rst),
      .rv_i(ingress_if),
      .rv_e(egress_if)
  );

endmodule
