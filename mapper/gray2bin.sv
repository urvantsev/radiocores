interface node_if #(
        parameter int data_width = 16
    )(
        input clk,
        input rst
    );

    logic [data_width-1:0] gray_code;
    logic [data_width-1:0] binary_code;

    modport in  (input  clk, rst, gray_code, binary_code);
    modport out (output gray_code, binary_code);

endinterface

module gray2bin #(
        parameter int modulation_order = 16,
        parameter int data_width = 16
    )(
        input  logic clk,
        input  logic rst,
        input  logic [data_width-1:0] i_gray_code,
        output logic [data_width-1:0] o_binary_code
    );

    localparam int num_nodes = $clog2(modulation_order) - 1;

    // Input flip-flop
    logic [data_width-1:0] input_ff;

    always_ff @(posedge clk) begin
        if (~rst) input_ff <= 16'b0;
        else input_ff <= i_gray_code;
    end

    // Inter-node SVIF
    node_if my_if[num_nodes:0](clk, rst);

    assign { my_if[0].gray_code, my_if[0].binary_code } = {2{input_ff}};

    // Gray to binary conversion nodes
    generate
        // Generate nodes
        for (genvar i = 0; i < num_nodes; i++) begin: nodes
            node node_i(
                .in_if(my_if[i]),
                .out_if(my_if[i+1])
            );
        end: nodes;
    endgenerate

    // Output flip-flop
    always_ff @(posedge clk) begin
        o_binary_code <= my_if[num_nodes].binary_code;
    end

endmodule

module node #(
        parameter int data_width = 16
    )(
        node_if.in  in_if,
        node_if.out out_if
    );

    logic [data_width-1:0] gray_code;
    logic [data_width-1:0] binary_code;

    always_ff @(posedge in_if.clk) begin
        if (~in_if.rst) begin
            gray_code  <= {data_width{1'b0}};
            binary_code <= {data_width{1'b0}};
        end else begin
            gray_code <= in_if.gray_code >> 1;
            binary_code <= in_if.binary_code;
        end
    end

    always_comb begin
        out_if.gray_code = gray_code;
        out_if.binary_code = binary_code ^ gray_code;
    end

endmodule
