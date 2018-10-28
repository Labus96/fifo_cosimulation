module fifo
  #( parameter DATA_WIDTH = 32 
  ,  parameter FIFO_SIZE = 3
  ,  parameter ADDR_WIDTH = $clog2( FIFO_SIZE )    
  )
  ( input                     clk
  , input                     rst
  , input  [DATA_WIDTH-1:0]   data_in
  , input                     signal_wr
  , input                     signal_oe
  , output [DATA_WIDTH-1:0]   data_out  
  );

reg [DATA_WIDTH - 1:0] fifo_buf [0:FIFO_SIZE-1];            
reg [ADDR_WIDTH-1:0]                fifo_buf_read;    
reg [ADDR_WIDTH-1:0]                fifo_buf_write;         

always @(posedge clk) begin

  if ( rst == 1 ) begin
    fifo_buf_write <= 0;
    fifo_buf_read <= 0; 

  end else if ( signal_wr == 1 ) begin
    fifo_buf[fifo_buf_write] <=  data_in ;    
    fifo_buf_write <= fifo_buf_write == FIFO_SIZE - 1 ? 0 : fifo_buf_write + 1;

  end else if ( signal_oe == 1 ) begin    
    fifo_buf_read <= fifo_buf_read == FIFO_SIZE - 1 ? 0 : fifo_buf_read + 1;    
  end 

end

assign  data_out  = signal_oe ? fifo_buf[fifo_buf_read] : 0; 

endmodule