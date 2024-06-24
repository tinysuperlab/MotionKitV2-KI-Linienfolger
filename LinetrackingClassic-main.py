###############################################
# LinetrackingClassic                         #
# (c) 2024 Thomas Kaffka, Düsseldorf, Germany #
# 22.06.2024                                  #
###############################################
from calliopemini import *
from MotionKit import*

go = 0
count = 0

def PrintXML(lr, ll, mr, ml):
    print('  <Example>')
    print('    <ExampleX value1="{}" value2="{}" />'.format(lr,ll))
    print('    <ExampleY value1="{}" value2="{}" />'.format(mr,ml))
    print('  </Example>')

while True:
    if (button_a.is_pressed()):
        go = 1
    if (button_b.is_pressed() or count == 500):
        go = 0
        motorR(0,0)
        motorL(0,0)
    if (go == 0):
        continue
    sleep(200)
    count += 1
    motorR(0,20)
    motorL(0,20)
    line_right = read_lineFollowR()
    line_left = read_lineFollowL()
    if (line_right == 0 and line_left == 0):
        PrintXML(0.1, 0.1, 0.9, 0.9)
    elif  (line_right == 1 and line_left == 0):
        motorL(0,0)
        PrintXML(0.9, 0.1, 0.9, 0.1)
    elif  (line_right == 0 and line_left == 1):
        motorR(0,0)
        PrintXML(0.1, 0.9, 0.1, 0.9)
    elif  (line_right == 1 and line_left == 1):
        PrintXML(0.9, 0.9, 0.9, 0.9)
