module skid_buffer (
    input logic clk,
    input logic rst,
    rv_if.ingress rv_i,
    rv_if.egress rv_e
);

  rv_if my_rv ();
  logic [7:0] data_buf, data_sel;

  is_ready is_ready_i0 (
      .clk (clk),
      .rst (rst),
      .rv_i(rv_i),
      .rv_e(my_rv.egress_rv),
      .data(data_buf)
  );

  always_comb begin
    data_sel = rv_i.ready ? rv_i.data : data_buf;
  end

  is_valid is_valid_i0 (
      .clk (clk),
      .rst (rst),
      .rv_i(my_rv.ingress_rv),
      .data(data_sel),
      .rv_e(rv_e)
  );

endmodule
