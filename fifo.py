import os
from myhdl import Cosimulation, Simulation, Signal, delay, always, intbv, now

def clk_driver(clk, period=10):
    ''' Clock driver '''
    @always(delay(period//2))
    def driver():
        clk.next = not clk
        print 'clk_drive value:' + str(clk)
    return driver   

# def set_signal_value(sig, value):
#     print 'start set_signal_value ' + str(sig)
#     @always(clk.posedge)
#     def signal_driver():
#         sig = Signal(value)       
#     return signal_driver


def testbench(clk, rst):
    print 'start testbanch\n'
    @always(clk.posedge)
    def set_testbanch():
        rst.next = not rst
        print 'rst value in tetbanch: ' + str(rst)   
    return set_testbanch
   
def fifo(clk, rst, data_in, signal_wr, signal_oe, data_out):
    ''' A Cosimulation object, used to simulate Verilog modules '''
    os.system('iverilog -o fifo fifo.v top_fifo.v')
    print '_________________________________'
    print 'Start Cosimulation'
    print 'clk: ' + str(clk)
    print 'rst: ' + str(rst)
    print 'data_in: ' + str(data_in)
    print 'signal_wr: ' + str(signal_wr)
    print 'signal_oe: ' + str(signal_oe)
    print 'data_out: ' + str(data_out)
    print '_________________________________\n'
    
    return Cosimulation('vvp -m ./myhdl.vpi fifo', clk=clk, rst=rst, data_in=data_in, signal_wr=signal_wr, signal_oe=signal_oe, data_out=data_out)
    
#yield clk.negedge

clk = Signal(0)
rst = Signal(0)
data_in = Signal(intbv(0x12)[32:])
signal_wr = Signal(1)
signal_oe = Signal(0)
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

print 'start clk_driver_inst\n'
clk_driver_inst = clk_driver(clk)

print 'start testbench_inst\n'
testbench_inst = testbench(clk, rst)

print 'start fifo_inst\n'
fifo_inst = fifo(clk, rst, data_in, signal_wr, signal_oe, data_out)

print 'Star simulation'
sim = Simulation(clk_driver_inst, testbench_inst, fifo_inst)
sim.run(50)
print 'Finish'

