module is_ready (
    input logic clk,
    input logic rst,

    // Full rv_if at the input
    rv_if.ingress rv_i,

    // Separate rv and data at the output
    rv_if.egress_rv rv_e,
    output logic [7:0] data
);

  // Ingress ready control
  drop_set is_ready_i0 (
      .clk(clk),
      .q  (rv_i.ready),
      .ce (rv_i.valid),
      .rst(rv_e.ready),
      .ind(rv_e.valid)
  );

  logic data_q;

  always_ff @(posedge clk)
    if (rst) begin
      data_q <= '0;
    end else if (rv_i.is_wren()) begin
      data_q <= rv_i.data;
    end

  assign data = data_q;

endmodule
