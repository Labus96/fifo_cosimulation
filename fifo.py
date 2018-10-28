import os
from myhdl import Cosimulation, Simulation, Signal, delay, always, intbv, now

def clk_driver(clk, period=10):
    @always(delay(period/2))
    def clk_drvr():
        clk.next = not clk
    return clk_drvr   

def reset_driver(clk, reset):
    @always(delay(10))
    def rst_drv():
        rst.next = bool(0)
    return rst_drv

def write_driiver(clk, signal_wr):
    @always(clk.posedge)
    def wrt_dvr():
        signal_wr.next = not signal_wr        
    return wrt_dvr

def data_in_driver(clk, data_in):
    @always(clk.posedge)    
    def set_data_in():
        data_in.next += 4
    return set_data_in

def oe_driiver(clk, signal_oe):
    @always(delay(20))
    def oe_dvr():
        signal_oe.next = not signal_oe        
    return oe_dvr
   
def fifo(clk, rst, data_in, signal_wr, signal_oe, data_out):
    ''' A Cosimulation object, used to simulate Verilog modules '''
    os.system('iverilog -o fifo fifo.v top_fifo.v')    
    return Cosimulation('vvp -m ./myhdl.vpi fifo', clk=clk, rst=rst, data_in=data_in, signal_wr=signal_wr, signal_oe=signal_oe, data_out=data_out)
    

clk = Signal(bool(0))
rst = Signal(bool(1))
data_in = Signal(intbv(0)[32:])
signal_wr = Signal(bool(0))
signal_oe = Signal(bool(0))
data_out = Signal(intbv(0)[32:])

print '_________________________________'
print 'Start signals values:'
print 'clk: ' + str(clk)
print 'rst: ' + str(rst)
print 'data_in: ' + str(data_in)
print 'signal_wr: ' + str(signal_wr)
print 'signal_oe: ' + str(signal_oe)
print 'data_out: ' + str(data_out)
print '_________________________________\n'


clk_driver_inst = clk_driver(clk)
reset_driver_inst = reset_driver(clk,rst)
data_in_driver_inst = data_in_driver(clk, data_in)
write_driiver_inst = write_driiver(clk, signal_wr)
oe_driiver_inst = oe_driiver(clk, signal_oe)
fifo_inst = fifo(clk, rst, data_in, signal_wr, signal_oe, data_out)
sim = Simulation(clk_driver_inst, data_in_driver_inst, write_driiver_inst, reset_driver_inst, oe_driiver_inst, fifo_inst)
sim.run(120)


