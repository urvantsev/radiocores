module is_valid (
    input logic clk,
    input logic rst,

    // Separate rv and data at the input
    rv_if.ingress_rv rv_i,
    input logic [7:0] data,

    // Full rv_if at the output
    rv_if.egress rv_e
);

  // Egress valid control
  drop_set is_valid_i0 (
      .clk(clk),
      .q  (rv_e.valid),
      .ce (rv_e.ready),
      .rst(rv_i.valid),
      .ind(rv_i.ready)
  );

  logic data_q;

  always_ff @(posedge clk)
    if (rst) begin
      data_q <= '0;
    end else if (rv_i.is_wren()) begin
      data_q <= data;
    end

  assign rv_e.data = data_q;

endmodule
