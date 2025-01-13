module is_valid (
    rv_if.in  rv_i,
    rv_if.out rv_o
);

  // Egress valid control
  drop_set is_valid_i0 (
      .clk(rv_i.clk),
      // .q  (rv_o.valid),
      .q  (),
      .ce (rv_o.ready),
      .rst(rv_i.valid),
      .ind(rv_i.ready)
  );

  always_ff @(posedge rv_i.clk) begin
    rv_o.valid <= rv_i.valid;
  end

  logic [7:0] data_q;

  always_ff @(posedge rv_i.clk) begin
    if (rv_i.is_wren())
      data_q <= rv_i.data;

    if (rv_i.rst)
      data_q <= '0;
  end

  assign rv_o.data = data_q;

endmodule
