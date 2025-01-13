module skid_buffer (
    rv_if.in  rv_i,
    rv_if.out rv_o
);

  rv_if intf (
    .clk(rv_i.clk),
    .rst(rv_i.rst)
  );

  is_ready breg_i0 (
    .rv_i(rv_i),
    .rv_o(intf)
  );

  is_valid oreg_i0 (
    .rv_i(intf),
    .rv_o(rv_o)
  );

endmodule
