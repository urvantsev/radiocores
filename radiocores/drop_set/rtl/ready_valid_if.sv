interface rv_if #(
    type DATA_TYPE = logic [7:0]  // Default to 8-bit data type
) (
    input logic clk,
    input logic rst
);

  logic valid;
  logic ready;
  DATA_TYPE data;

  modport ingress_rv(input valid, output ready);
  modport egress_rv(output valid, input ready);
  modport ingress(input valid, output ready, input data, import is_wren);
  modport egress(output valid, input ready, output data);

  // Write enable check for Ingress
  function automatic logic is_wren();
    return valid && ready;
  endfunction

endinterface
