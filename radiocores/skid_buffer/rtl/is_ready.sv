module is_ready (
    rv_if.in  rv_i,
    rv_if.out rv_o
);

  // Ready signal control logic
  drop_set is_ready_i0 (
      .clk(rv_i.clk),
      .ce (rv_i.valid),
      .rst(rv_o.ready),
      .ind(rv_o.valid),
      .q  (rv_i.ready)
  );

  // Buffer
  logic [7:0] data_q;

  always_ff @(posedge rv_i.clk) begin
    if (rv_i.is_wren())
        data_q <= rv_i.data;

    if (rv_i.rst)
        data_q <= '0;
  end

  // Mux
  assign rv_o.data = rv_i.ready ? rv_i.data : data_q;

endmodule
