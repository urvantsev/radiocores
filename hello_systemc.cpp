#include <systemc.h>

SC_MODULE(HelloSystemC) {
    sc_in<bool> clk;
    sc_out<bool> signal;

    SC_CTOR(HelloSystemC) {
        SC_THREAD(say_hello);
        sensitive << clk.pos();
    }

    void say_hello() {
        while (true) {
            signal.write(!signal.read());
            std::cout << "Hello, SystemC!" << std::endl;
            wait(); // Wait for the next clock cycle
        }
    }
};

int sc_main(int argc, char* argv[]) {
    sc_signal<bool> clk;
    sc_signal<bool> signal;

    HelloSystemC hello("HELLO");
    hello.clk(clk);
    hello.signal(signal);

    // Open VCD file
    sc_trace_file *wf = sc_create_vcd_trace_file("waveform");

    // Dump the desired signals
    sc_trace(wf, clk, "clk");
    sc_trace(wf, signal, "signal");

    // Simulate the clock
    sc_start(1, SC_NS);
    for (int i = 0; i < 10; i++) {
        clk = !clk;
        sc_start(1, SC_NS);
    }

    // Close the VCD file
    sc_close_vcd_trace_file(wf);

    return 0;
}
