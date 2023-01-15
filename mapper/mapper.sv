module mapper (
    input  logic clk,
    input  logic rst,
    input  logic [15:0] i_data_i,
    input  logic [15:0] i_data_q,
    output logic [15:0] o_data_i,
    output logic [15:0] o_data_q
);

    gray2bin u0 (
        .clk(clk),
        .rst(rst),
        .i_gray_data(i_data_i),
        .o_binary_data(o_data_i)
    );

endmodule