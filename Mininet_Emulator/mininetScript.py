#!/usr/bin/python
import Sim_GUI as sgui
import Sim_GUI_2 as sgui2
import os
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
import time
from mininet.term import makeTerm

exec(open("./settings").read())


def myTopology():

    info( '********* Project 1Task 1  **********************\n' )
    net = Mininet( topo=None, build=False, ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0', controller=OVSController, protocol='tcp', port=6633)

    info( '*** Add switches\n')
    s0 = net.addSwitch('s0', cls=OVSKernelSwitch, failMode='standalone', stp=1)
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, failMode='standalone', stp=1)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch, failMode='standalone', stp=1)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch, failMode='standalone', stp=1)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch, failMode='standalone', stp=1)
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch, failMode='standalone', stp=1)

    info( '*** Add hosts\n')
    MS = net.addHost('MS', ip='10.0.0.1/8')
    SS = net.addHost('SS', ip='10.0.0.3/8')
    Server = net.addHost('Server', ip='10.0.0.2/8')

    info( '*** Add links between hosts and switches\n')
    linkConfig_HToS = {'delay':'0', 'bw' : 100}


    L9 = net.addLink(MS, s1,cls=TCLink , **linkConfig_HToS)
    L10 = net.addLink(SS, s5,cls=TCLink , **linkConfig_HToS)
    L11 = net.addLink(Server, s3,cls=TCLink , **linkConfig_HToS)

    info( '*** Add links between switches\n')
    Ls3 = net.addLink(s0, s3, cls=TCLink , **linkConfig_s0s5)
    Ls2 = net.addLink(s0, s1, cls=TCLink , **linkConfig_s0s1)
    Ls1 = net.addLink(s1, s3, cls=TCLink , **linkConfig_s1s5)
    Ls4 = net.addLink(s1, s2, cls=TCLink , **linkConfig_s1s2)
    Ls5 = net.addLink(s2, s4, cls=TCLink , **linkConfig_s2s6)
    Ls6 = net.addLink(s3, s4, cls=TCLink , **linkConfig_s5s6)
    Ls8 = net.addLink(s3, s5, cls=TCLink , **linkConfig_s5s8)
    Ls7 = net.addLink(s4, s5, cls=TCLink , **linkConfig_s6s8)

    info( '*** Starting network\n')
    net.build()

    info( '*** Starting controllers\n')
    c0.start()

    info( '*** Starting switches\n')
    net.get('s0').start([c0])
    net.get('s2').start([c0])
    net.get('s1').start([c0])
    net.get('s3').start([c0])
    net.get('s4').start([c0])
    net.get('s5').start([c0])

    net.start()
    net.staticArp()


    info( '*** Waiting for STP to converge \n')
    time.sleep(35)

    net.pingAll()

    return(net)

def Exp01_Haptic_Data(net):

    print ("*** Loading Testbed Experiment Number 01 (START) >>>")

    slave = net.get("SS")
    server = net.get("Server")
    master = net.get("MS")

    makeTerm(slave,cmd='python3 ../1_Exp_Haptic_Data/haptic_slaveside.py; read')
    time.sleep(1)
    makeTerm(server, cmd='python3 ../1_Exp_Haptic_Data/haptic_serverside.py; read')
    time.sleep(1)
    makeTerm(master, cmd='python3 ../1_Exp_Haptic_Data/ms_comm.py; read')

    print("***  Exeriment Number 01 (END) ***"
          "\n <<<<< Select Next Options >>>>>>"
          "\n (1)-Display Results "
          "\n (2)-Exp#2: Mouse Control Feedback "
          "\n (3)-Exp#3: Direct Control "
          "\n (2)-Exit")

    event4 = next(sgui.send())
    if event4 == 'Display Result':
        sgui2.window.un_hide()
        sgui2.graph_plotting_Exp1()
        sgui2.window.hide()

    print("\n <<<<< Select Next Options >>>>>>"
          "\n(1)-Exp#1: Haptic Data Transfer"
          "\n (2)-Exp#2: Mouse Control Feedback "
          "\n (3)-Exp#3: Direct Control "
          "\n (2)-Exit")

    event5 = next(sgui.send())
    if event5 == 'Exit Mininet' or sgui.sg.WIN_CLOSED:
        print('ExitMininet')
        exit()
    if event5 == 'EXP#1':
        sgui2.window.un_hide()
        sgui2.select_packet_HD()
        sgui2.window.hide()
        Exp01_Haptic_Data(net)
    if event5 == 'EXP#2':
        sgui2.window.un_hide()
        sgui2.select_packet_MD()
        sgui2.window.hide()
        Exp02_Mouse_VREP_Feedback(net)
    if event5 == 'EXP#3':
        Exp03_Direct_MC(net)



def Exp02_Mouse_VREP_Feedback(net):
    print ("*** Exeriment Number 02 (START) >>>")
    slave = net.get("SS")
    server = net.get("Server")
    master = net.get("MS")

    makeTerm(slave,cmd='python3 ../2_Exp_Mouse_VREP_Feedback/sceen_loader/vrepLoader.py; read')
    time.sleep(5)

    makeTerm(slave,cmd='python3 ../2_Exp_Mouse_VREP_Feedback/haptic_app_slave.py; read')
    time.sleep(2)

    makeTerm(server, cmd='python3 ../2_Exp_Mouse_VREP_Feedback/server_com.py; read')
    time.sleep(2)

    makeTerm(master, cmd='python3 ../2_Exp_Mouse_VREP_Feedback/ms_com.py; read')

    print("***  Exeriment Number 02 (END) ***"
          "\n <<<<< Select Next Options >>>>>>"
          "\n (1)-Display Results "
          "\n (2)-Exp#2: Again: Mouse Control Feedback "
          "\n (3)-Exp#3: Direct Control "
          "\n (2)-Exit")

    event4 = next(sgui.send())
    if event4 == 'Display Result':
        sgui2.window.un_hide()
        sgui2.graph_plotting_Exp2()
        sgui2.window.hide()

    print("\n <<<<< Select Next Options >>>>>>"
          "\n (1)-Exp#1: Haptic Data Transfer"
          "\n (2)-Exp#2: Mouse Control Feedback "
          "\n (3)-Exp#3: Direct Control "
          "\n (2)-Exit")

    event5 = next(sgui.send())
    if event5 == 'Exit Mininet' or sgui.sg.WIN_CLOSED:
        #ExitMininet
        print('ExitMininet')
        exit()
    if event5 == 'EXP#1':
        sgui2.window.un_hide()
        sgui2.select_packet_HD()
        sgui2.window.hide()
        Exp01_Haptic_Data(net)
    if event5 == 'EXP#2':
        sgui2.window.un_hide()
        sgui2.select_packet_MD()
        sgui2.window.hide()
        Exp02_Mouse_VREP_Feedback(net)
    if event5 == 'EXP#3':
        Exp03_Direct_MC(net)


def Exp03_Direct_MC(net):
    print ("*** Exeriment Number 02 (START) >>>")
    slave = net.get("SS")
    server = net.get("Server")
    master = net.get("MS")

    makeTerm(slave,cmd='python3 ../3_Exp_Direct_MC/sceen_loader/vrepLoader.py; read')
    time.sleep(5)

    makeTerm(slave,cmd='python3 ../3_Exp_Direct_MC/haptic_app_slave.py; read')
    time.sleep(2)

    makeTerm(server, cmd='python3 ../3_Exp_Direct_MC/server_com.py; read')
    time.sleep(2)

    makeTerm(master, cmd='python3 ../3_Exp_Direct_MC/master_app.py; read')

    print("*****  Exeriment Number 03 (END) *****")

    print("\n <<<<< Select Next Options >>>>>>"
          "\n (1)-Exp#1: Haptic Data Transfer"
          "\n (2)-Exp#2: Mouse Control Feedback "
          "\n (3)-Exp#3: Direct Control "
          "\n (2)-Exit")

    event5 = next(sgui.send())
    if event5 == 'Exit Mininet' or sgui.sg.WIN_CLOSED:
        #ExitMininet
        print('ExitMininet')
        exit()
    if event5 == 'EXP#1':
        sgui2.window.un_hide()
        sgui2.select_packet_HD()
        sgui2.window.hide()
        Exp01_Haptic_Data(net)
    if event5 == 'EXP#2':
        sgui2.window.un_hide()
        sgui2.select_packet_MD()
        sgui2.window.hide()
        Exp02_Mouse_VREP_Feedback(net)
    if event5 == 'EXP#3':
        Exp03_Direct_MC(net)






if __name__ == '__main__':
    net=0
    event1=next(sgui.send())
    if event1=='Start Simulation':
        print("***  Simulation Start ***")
        os.system("sudo mn -c")
        setLogLevel('info')
        net = myTopology()
        # CLI(net)

    print("***  Please Select Exeriment Number "
          "\n (1)-Exp#1: Haptic Data Transfer "
          "\n (2)-Exp#2: Mouse Control Feedback "
          "\n (3)-Exp#3: Direct Control "
          "\n (4)-Exp#4: Not Avbailable yet "
          "\n Exit Mininet   ***")

    event2 = next(sgui.send())
    if event2 == 'EXP#1':
        print("You Selected Exp#1")
        print("Please Select Number of Packets for Exp#1")
        sgui2.select_packet_HD()
        sgui2.window.hide()
        Exp01_Haptic_Data(net)
    if event2 == 'EXP#2':
        print("You Selected Exp#2")
        sgui2.select_packet_MD()
        sgui2.window.hide()
        Exp02_Mouse_VREP_Feedback(net)

    if event2 == 'EXP#3':
        print("You Selected Exp#3")
        Exp03_Direct_MC(net)


    if event2 == 'EXP#4':
        CLI(net)
        print("You Selected Exp#4")


    if event2 == 'Exit Mininet' or sgui.sg.WIN_CLOSED:
        print("You Selected Exit, See You! Again....")
        exit()


