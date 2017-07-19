from collections import OrderedDict

from bokeh.plotting import figure, show, output_file, ColumnDataSource
from bokeh.models import HoverTool
from bokeh.embed import components
import bokeh
import random

import math

import sys
import glob
import serial
import json
import struct
import time

import matplotlib.pyplot as plt
import sys

import time
import math
from threading import Thread, Lock
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room,close_room, rooms, disconnect
from datetime import datetime

def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in list(range(256))]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            #print("checking port "+port)
            s = serial.Serial(port)
            #print("closing port "+port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result
#-------------------

# ports = serial_ports() #generate list of currently connected serial ports 
# print (ports)

# ser = ports[0]

# s = serial.Serial(ser)
# print(s)

left_nodes = 62
right_nodes = 62
left_bus = 2
right_bus = 2
node_v_spacing = 0.18
bus_h_spacing = 0.18
midline_gap = 0.25
node_to_bus_gap = 0.15


node_length = 1.0
node_height = 0.15
bus_height = node_v_spacing*left_nodes
bb_node = [[0,0,node_length,node_length],[0,node_height,node_height,0]]
bb_bus = [[0,0,node_height,node_height],[0,bus_height,bus_height,0]]

image_height = 0.3+bus_height
image_width = 0.3+midline_gap + 2*node_length+2*node_to_bus_gap+4*node_height

BB_x = []
BB_y = []

orientation='horizontal'

if orientation =='vertical':
    for q in range(left_nodes):
        BB_x.append([t for t in bb_node[0]])
        BB_y.append([t+q*node_v_spacing for t in bb_node[1]])
    for q in range(right_nodes):
        BB_x.append([t+node_length+midline_gap for t in bb_node[0]])
        BB_y.append([t+q*node_v_spacing for t in bb_node[1]])
    
    BB_x.append([t-node_to_bus_gap-node_height - bus_h_spacing for t in bb_bus[0]])
    BB_x.append([t-node_to_bus_gap-node_height for t in bb_bus[0]])
    BB_x.append([t+node_to_bus_gap+2*node_length + midline_gap for t in bb_bus[0]])
    BB_x.append([t+bus_h_spacing+node_to_bus_gap+2*node_length + midline_gap for t in bb_bus[0]])
    for y in range(4):
        BB_y.append(bb_bus[1])
    image_height = 0.3+bus_height
    image_width = 0.3+midline_gap + 2*node_length+2*node_to_bus_gap+4*node_height
    pixel_scaler = 500/6
else:
    for q in range(left_nodes):
        BB_y.append([t for t in bb_node[0]])
        BB_x.append([t+q*node_v_spacing for t in bb_node[1]])
    for q in range(right_nodes):
        BB_y.append([t+node_length+midline_gap for t in bb_node[0]])
        BB_x.append([t+q*node_v_spacing for t in bb_node[1]])
    
    BB_y.append([t-node_to_bus_gap -node_height- bus_h_spacing for t in bb_bus[0]])
    BB_y.append([t-node_to_bus_gap-node_height for t in bb_bus[0]])
    BB_y.append([t+node_to_bus_gap+2*node_length + midline_gap for t in bb_bus[0]])
    BB_y.append([t+bus_h_spacing+node_to_bus_gap+2*node_length + midline_gap for t in bb_bus[0]])
    for y in range(4):
        BB_x.append(bb_bus[1])
    image_width = 0.3+bus_height
    image_height = 0.3+midline_gap + 2*node_length+2*node_to_bus_gap+4*node_height
    pixel_scaler = 500/5

def color_getter(value,maximum):
    integer = int(math.floor(value*255/maximum))
    #print (integer)
    hexval = hex(integer)[2:]
    #print (hexval)
    if len(str(hexval))==1:
        return "#" +"0" +hexval+"0000"
    else:
        return "#" +hexval+"0000"

async_mode = None
if async_mode is None:
    try:
        import eventlet
        async_mode = 'eventlet'
    except ImportError:
        pass

    if async_mode is None:
        try:
            from gevent import monkey
            async_mode = 'gevent'
        except ImportError:
            pass

    if async_mode is None:
        async_mode = 'threading'

    print('async_mode is ' + async_mode)

# monkey patching is necessary because this application uses a background
# thread
if async_mode == 'eventlet':
    import eventlet
    eventlet.monkey_patch()
elif async_mode == 'gevent':
    from gevent import monkey
    monkey.patch_all()

#Start up Flask server:
app = Flask(__name__, template_folder = './',static_url_path='/static')
app.config['SECRET_KEY'] = 'secret!' #shhh don't tell anyone. Is a secret
socketio = SocketIO(app, async_mode = async_mode)
thread = None

def dataThread():
    unique = 456
    ports = serial_ports() #generate list of currently connected serial ports 
    print (ports)
    ser = ports[1]
    s = serial.Serial(ser)
    print(s)
    print("ALL GOOD")
    while True:
        #current = datetime.now().isoformat()
        #current = current.replace(":","_")
        #string_to_write = input() #7,3;single\n" 
        string_to_write = "all*"
        print(string_to_write)

        s.write(bytes(string_to_write,'UTF-8'))
        print("sleeping now")
        time.sleep(4)   #time running in the arduino code. Modify if needed
        print("post_sleep")
        no_more_data = False

        #this is a serious cludge:
        all_data = ""

        while not no_more_data:
            #print("going")
            time.sleep(0.1)
            data_left = s.inWaiting()
            if (data_left >0): 
                all_data += s.read(data_left).decode()
            else:
                no_more_data = True

        print(all_data)
        x = all_data
        #x = x[1]
        #print(x)
        x = x.split("&")
        x = x[:-1]
        bins=[]
        for y in x:
            parts = y.split(":")
            #print(parts[0])
            #print(parts[1])
            bins.append((int(parts[0]),int(parts[1])))

        #for random testing:
        #voltage = [3.3*random.random() for x in range(len(names))]
        print (bins)
        node_voltage = list()
        time_x = list()
        count = 0

        #Create place holders when all is not called
        #organizing to operate different modes
        old_voltage = [0]*128  #create a list of zeros of 128 elements
        for y in bins:
            old_voltage[y[0]] = 3.3*y[1]/1023

        old_names = list(range(128))

        #print (old_names)

        #Reorganizing orders to match with the breadboard layout
        names = list()
        voltage = list()
        for i in old_names:
            index = old_names.index(i)
            if index >= 62:
                if index == 125:
                    names.append(63)
                    voltage.append(old_voltage[63])
                elif index == 124:
                    names.append(62)
                    voltage.append(old_voltage[62])
                elif (index == 126):
                    names.append(127)
                    voltage.append(old_voltage[127])
                elif (index == 127):
                    names.append(126)
                    voltage.append(old_voltage[126])
                else:
                    names.append(i + 2)
                    voltage.append(old_voltage[index + 2])
            else:
                names.append(i)
                voltage.append(old_voltage[index])

        #print (names)
        #print (voltage)

        #colors = ["#F1EEF6", "#D4B9DA", "#C994C7", "#DF65B0", "#DD1C77", "#980043"]    
        colors = [color_getter(v,3.3) for v in voltage]
        #print (colors)
        source = ColumnDataSource(
            data = dict(
                x=BB_x,
                y=BB_y,
                color=colors,
                name=names,
                voltage=voltage,
            )
        )


        #output_file("bb_test_{}.html".format(current), title="Breadboard Visualizer v1.0")

        TOOLS="hover,save"

        p = figure(title="Breadboard Voltages", tools=TOOLS)
        p.toolbar.logo=None
        #print(pixel_scaler*image_width)
        #print(pixel_scaler*image_height)

        p.patches('x', 'y',
            fill_color='color', fill_alpha=0.7,
            line_color="white", line_width=0.0,
            source=source)
        p.xgrid.grid_line_color = None
        p.ygrid.grid_line_color = None

        p.plot_height=int(pixel_scaler*image_height)
        p.plot_width=int(pixel_scaler*image_width)
        p.axis.visible = False
        hover = p.select(dict(type=HoverTool))
        hover.point_policy = "follow_mouse"
        hover.tooltips = OrderedDict([
            ("Name", "@name"),
            ("Voltage)", "@voltage V"),
        ])
        
        script, div = components(p)
        prep = script + div

        #val1 = amp1*math.sin(omega1*time.time())
        #val2 = amp2*math.sin(omega2*time.time())
        socketio.emit('update_{}'.format(unique),prep,broadcast =True)
        print('sending')

@app.route('/')
def index():
    global thread
    print ("A user connected")
    if thread is None:
        thread = Thread(target=dataThread)
        thread.daemon = True
        thread.start()
    return render_template('div_render.example_1.html')


if __name__ == '__main__':
    socketio.run(app, port=3000, debug=True)

