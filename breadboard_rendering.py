from collections import OrderedDict

from bokeh.plotting import figure, show, output_file, ColumnDataSource
from bokeh.models import HoverTool
import bokeh
import random

import math

from datetime import datetime

current = datetime.now().isoformat()
current = current.replace(":","_")

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

data = (1505591002.0681381, 'student5a', "{'user': 'student5a', 'board': \
    '[(0, 24), (1, 22), (2, 21), (3, 23), (4, 22), (5, 22), (6, 21), (7, 23), (8, 22), (9, 23), (10, 20), (11, 406), (12, 27), (13, 23), (14, 405), (15, 1015), (16, 1), (17, 407), (18, 22), (19, 23), (20, 22), (21, 22), (22, 23), (23, 23), (24, 22), (25, 22), (26, 23), (27, 22), (28, 20), (29, 23), (30, 23), (31, 21), (32, 23), (33, 24), (34, 23), (35, 10), (36, 22), (37, 10), (38, 23), (39, 24), (40, 23), (41, 22), (42, 24), (43, 23), (44, 7), (45, 7), (46, 7), (47, 1), (48, 7), (49, 1), (50, 645), (51, 979), (52, 981), (53, 15), (54, 1), (55, 8), (56, 11), (57, 1), (58, 9), (59, 478), (60, 32), (61, 1), (62, 31), (63, 1), (64, 31), (65, 30), (66, 31), (67, 32), (68, 1), (69, 31), (70, 1), (71, 30), (72, 1), (73, 30), (74, 391), (75, 37), (76, 383), (77, 37), (78, 381), (79, 406), (80, 279), (81, 16), (82, 1), (83, 24), (84, 22), (85, 21), (86, 23), (87, 23), (88, 24), (89, 22), (90, 21), (91, 21), (92, 20), (93, 21), (94, 23), (95, 24), (96, 22), (97, 24), (98, 22), (99, 11), (100, 22), (101, 10), (102, 21), (103, 24), (104, 24), (105, 22), (106, 19), (107, 23), (108, 1), (109, 6), (110, 7), (111, 7), (112, 439), (113, 439), (114, 490), (115, 1), (116, 1), (117, 7), (118, 7), (119, 1015), (120, 8), (121, 6), (122, 7), (123, 1), (124, 435), (125, 736), (126, 29), (127, 22)]'}")

isolate = data[2]
#print (data[2])
new = (isolate.split(':'))
new1 = new[2].split('[')
#print (new1[1])
new2 = new1[1].split(']')
#print (final[0])
new3 = new2[0]
#print (new3)
data_list = (((((new3.replace(')', "")).replace('(',"")).replace(" ", "")).split(",")))
#print ((data_list))

# x = 
# #x = x[1]
# #print(x)
# x = x.split("&")
# x = x[:-1]
bins=[]
# for y in x:
#     parts = y.split(":")
#     #print(parts[0])
#     #print(parts[1])
#     bins.append((int(parts[0]),int(parts[1])))
#for random testing:
#voltage = [3.3*random.random() for x in range(len(names))]
counter = 0
while (counter < 128):
    bins.append((int(data_list[counter*2]),int(data_list[counter*2+1])))
    counter += 1
print (bins)

node_voltage = list()
time_x = list()

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


output_file("bb_image_{}.html".format(current), title="Breadboard Visualizer v1.0")

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

hover = p.select(dict(type=HoverTool))
hover.point_policy = "follow_mouse"
hover.tooltips = OrderedDict([
    ("Name", "@name"),
    ("Voltage)", "@voltage V"),
])

show(p)