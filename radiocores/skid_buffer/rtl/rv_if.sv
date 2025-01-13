interface rv_if #(
    parameter int DATA_WIDTH = 8
) (
    input logic clk,
    input logic rst
);

  logic                  valid;
  logic                  ready;
  logic [DATA_WIDTH-1:0] data;

  modport in (
    input  clk, rst, valid, data,
    output ready
  );

  clocking cb_in @(posedge clk);
    input ready;
    output rst, valid, data;
  endclocking

  modport out (
    input  ready,
    output valid, data
  );

  clocking cb_out @(posedge clk);
    input valid, data;
    output ready;
  endclocking

  // Write enable check for input
  function automatic logic is_wren();
    return valid && ready;
  endfunction

endinterface
