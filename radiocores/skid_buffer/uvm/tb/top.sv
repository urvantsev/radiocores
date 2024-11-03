module tb_skid_buffer;

  // Clock and reset signals
  logic clk;
  logic rst;

  // DUT interface signals
  logic       i_valid_i;
  logic [7:0] i_data_i;
  logic       i_ready_o;

  logic       e_ready_i;
  logic       e_valid_o;
  logic [7:0] e_data_o;

  // Instantiate the DUT (Device Under Test)
  skid_buffer dut (
      .clk       (clk),
      .rst       (rst),
      .i_valid_i (i_valid_i),
      .i_data_i  (i_data_i),
      .i_ready_o (i_ready_o),
      .e_ready_i (e_ready_i),
      .e_valid_o (e_valid_o),
      .e_data_o  (e_data_o)
  );

  // Clock generation: 10ns period (100MHz)
  always #5 clk = ~clk;

  // Initial block for reset and basic stimulus
  initial begin
      // Initialize signals
      clk       = 0;
      rst       = 1;
      i_valid_i = 0;
      i_data_i  = 8'h00;
      e_ready_i = 0;

      // Apply reset for a few cycles
      @(posedge clk);  // Wait for rising edge of clock
      rst = 1;
      @(posedge clk);
      rst = 0;

      // Test sequence
      @(posedge clk);
      i_valid_i = 1;
      i_data_i  = 8'hAA;  // Example data
      e_ready_i = 0;

      // Hold e_ready_i low for multiple cycles while i_valid_i is high
      repeat(3) @(posedge clk);

      // Set e_ready_i high to allow data to pass through
      @(posedge clk);
      e_ready_i = 1;

      // Deassert i_valid_i after one cycle of e_ready_i being high
      @(posedge clk);
      i_valid_i = 0;
      e_ready_i = 0;

      // Send another data burst with i_valid_i high and introduce backpressure on e_ready_i again
      @(posedge clk);
      i_valid_i = 1;
      i_data_i  = 8'h55;

      // Keep e_ready_i low for multiple cycles again
      @(posedge clk);
      e_ready_i = 0;
      repeat(2) @(posedge clk);

      // Release backpressure by setting e_ready_i high
      @(posedge clk);
      e_ready_i = 1;

      // Deassert signals to complete the sequence
      @(posedge clk);
      i_valid_i = 0;
      e_ready_i = 0;

      // End simulation
      #100 $finish;
  end

  // Monitor output signals
  initial begin
      $monitor("Time=%0t | i_valid_i=%b | i_data_i=%h | i_ready_o=%b | e_ready_i=%b | e_valid_o=%b | e_data_o=%h",
               $time, i_valid_i, i_data_i, i_ready_o, e_ready_i, e_valid_o, e_data_o);
  end

endmodule
