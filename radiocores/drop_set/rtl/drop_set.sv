module drop_set (
    input  logic clk,
    input  logic ce,
    input  logic rst,
    output logic ind,
    output logic q
);

  always_ff @(posedge clk) begin
    q <= rst ? 1'b1 : !ind;
  end

  assign ind = ce ? 1'b1 : !q;

endmodule
