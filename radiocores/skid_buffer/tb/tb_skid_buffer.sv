module tb_skid_buffer;

    timeunit 1ns;
    timeprecision 1ps;

    localparam int  DataWidth       = 8;
    localparam real ClkPeriod       = 10.0;
    localparam int  NumTransactions = 10;

    // Declare signals
    logic clk, rst;

    // Instantiate interfaces
    rv_if dut_in_if(
        .clk(clk),
        .rst(rst)
    );

    rv_if dut_out_if(
        .clk(clk),
        .rst(rst)
    );

    // Instantiate DUT
    skid_buffer dut (
        .rv_i(dut_in_if),
        .rv_o(dut_out_if)
    );

    // System clock generation
    initial begin
        clk = 0;
        forever #(ClkPeriod / 2.0) clk = ~clk;
    end

    // Packet generator function
    function automatic logic [DataWidth:0] generate_packet(input logic [7:0] value);
        return {1'b1, value};
    endfunction

    // Fetch next packet function
    function automatic logic [DataWidth:0] fetchNextPacket(
        input logic ready,
        input logic [DataWidth:0] currentPacket
    );
        logic valid;
        logic [DataWidth-1:0] data;

        {valid, data} = currentPacket;

        return (!valid || ready) ? generate_packet(data + 1) : currentPacket;
    endfunction

    // Reset generation
    initial begin
        rst = 1;
        #20 rst = 0; // Release reset after 20 ns
    end

    // Declare signals
    logic [DataWidth:0] currentPacket, nextPacket;

    // Packet transaction
    initial begin
        // Wait for reset de-assertion
        @(negedge rst);

        // Hardcoded transactions
        repeat (5) begin
            @(posedge clk);
            nextPacket = fetchNextPacket(dut_in_if.ready, currentPacket);

            // Drive DUT interface
            dut_in_if.valid <= nextPacket[DataWidth];
            dut_in_if.data <= nextPacket[DataWidth-1:0];

            // Update current packet
            currentPacket <= nextPacket;

            // Simulate a delay between transactions
            @(posedge clk);
        end

        // Finish simulation
        #100;
        $stop;
    end

endmodule
