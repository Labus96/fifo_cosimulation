// This is a top module which combines DUT and MyHDL signals

module top_fifo;

reg clk;
reg rst;
reg [31:0] data_in;
reg signal_wr;
reg signal_oe;
wire [31:0] data_out;

fifo dut (.clk(clk), .rst(rst), .data_in(data_in), .signal_wr(signal_wr), .signal_oe(signal_oe), .data_out(data_out));

initial begin
	$from_myhdl(clk, rst, data_in, signal_wr, signal_oe);
	$to_myhdl(data_out);
end

initial begin
    $dumpfile("top_fifo.vcd");
    $dumpvars();
end

endmodule // top_fifo