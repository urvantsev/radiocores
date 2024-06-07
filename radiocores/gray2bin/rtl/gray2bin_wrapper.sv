`ifndef GRAY2BIN_WRAPPER_SV
`define GRAY2BIN_WRAPPER_SV

`include "gray2bin_if.svh"
`include "gray2bin.sv"

module gray2bin_wrapper #(
    parameter int MODULATION_ORDER = 16
) (
    input logic clk,
    input logic rst,
    input logic [$clog2(MODULATION_ORDER)-1:0] i_gray_code,
    input logic i_dv,
    output logic [$clog2(MODULATION_ORDER)-1:0] o_binary_code,
    output logic o_dv
);

  // Instantiate the interface
  gray2bin_if #(MODULATION_ORDER) my_if (
      .clk(clk),
      .rst(rst)
  );

  // Connect the wrapper signals to the interface
  assign my_if.gray_code = i_gray_code;
  assign my_if.i_dv = i_dv;
  assign o_binary_code = my_if.binary_code;
  assign o_dv = my_if.o_dv;

  // Instantiate the gray2bin module
  gray2bin #(MODULATION_ORDER) gray2bin_inst (
      .in_if (my_if.in),
      .out_if(my_if.out)
  );

endmodule

`endif  // GRAY2BIN_WRAPPER_SV
