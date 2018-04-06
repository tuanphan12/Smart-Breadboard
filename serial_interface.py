'''Automatically find Teensy on COM Port

    Written by Joe Steinmeyer, 2017
    Edited by Joel Voldman, 2017
'''

import serial.tools.list_ports

teensy_port = list(serial.tools.list_ports.grep("Teensy"))
if len(teensy_port) == 1:
    print("Automatically found Teensy: {}".format(teensy_port[0].description))
else:
    ports = list(serial.tools.list_ports.comports())
    port_dict = {i:[ports[i],ports[i].vid] for i in range(len(ports))}
    teensy_id=None
    for p in port_dict:
        print("{}:   {} (Vendor ID: {})".format(p,port_dict[p][0],port_dict[p][1]))
        if port_dict[p][1]==5824:
            teensy_id = p
    if teensy_id== None:
        print("No Teensy Found!")
    else:
        print("Teensy Found: Device {}".format(p))
        port = port_dict[teensy_id] 

print (p)

'''
#Then connect as usual!
#I have a few different serial port threading objects you can use that are pretty robust!jj
'''
