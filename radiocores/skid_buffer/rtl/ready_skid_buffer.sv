module ready_skid_buffer (
    input logic clk,
    input logic rst,

    input  logic       i_valid_i,
    input  logic [7:0] i_data_i,
    output logic       i_ready_o,

    input  logic       e_ready_i,
    output logic       e_valid_o,
    output logic [7:0] e_data_o
);

  logic idle, i_ready_q;

  // Ingress ready control
  var_hold_set #(
      .RESET_VALUE(1'b1)
  ) is_ready_i0 (
      .clk(clk),
      .rst(rst),
      .hold_i(!i_valid_i),
      .set_i(e_ready_i),
      .hold_o(idle),
      .var_o(i_ready_q)
  );

  // Data buffer
  logic [7:0] data_q;

  always_ff @(posedge clk or posedge rst)
    if (rst)
      data_q <= 8'b0;
    else if (i_valid_i && i_ready_q)
      data_q <= i_data_i;

  // Outputs
  assign i_ready_o = i_ready_q;
  assign e_valid_o = !idle;
  assign e_data_o  = i_ready_q ? i_data_i : data_q;

endmodule
