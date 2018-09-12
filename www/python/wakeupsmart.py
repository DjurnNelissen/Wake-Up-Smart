from sense_hat import SenseHat
import datetime
import time
import common

sense = SenseHat()
sense.rotation = 180
sense.low_light = True
time.sleep(2)
sense.low_light = False

c = common.common()

# unit: 60/29
u = 60.0/29

zero = [[0,0,1,1,0,0],[0,1,0,0,1,0],[0,1,0,0,1,0],[0,1,0,0,1,0],[0,1,0,0,1,0],[0,0,1,1,0,0]]
one=[[0,0,0,1,0,0],[0,0,1,1,0,0],[0,0,0,1,0,0],[0,0,0,1,0,0],[0,0,0,1,0,0],[0,0,1,1,1,0]]
two=[[0,0,1,1,0,0],[0,1,0,0,1,0],[0,0,0,0,1,0],[0,0,0,1,0,0],[0,0,1,0,0,0],[0,1,1,1,1,0]]
three=[[0,0,1,1,0,0],[0,1,0,0,1,0],[0,0,0,1,0,0],[0,0,0,0,1,0],[0,1,0,0,1,0],[0,0,1,1,0,0]]
four=[[0,0,0,0,1,0],[0,0,0,1,1,0],[0,0,1,0,1,0],[0,1,1,1,1,0],[0,0,0,0,1,0],[0,0,0,0,1,0]]
five=[[0,1,1,1,1,0],[0,1,0,0,0,0],[0,1,1,1,0,0],[0,0,0,0,1,0],[0,1,0,0,1,0],[0,0,1,1,0,0]]
six=[[0,0,1,1,0,0],[0,1,0,0,0,0],[0,1,1,1,0,0],[0,1,0,0,1,0],[0,1,0,0,1,0],[0,0,1,1,0,0]]
seven=[[0,1,1,1,1,0],[0,0,0,0,1,0],[0,0,0,1,0,0],[0,0,0,1,0,0],[0,0,1,0,0,0],[0,0,1,0,0,0]]
eight=[[0,0,1,1,0,0],[0,1,0,0,1,0],[0,0,1,1,0,0],[0,1,0,0,1,0],[0,1,0,0,1,0],[0,0,1,1,0,0]]
nine=[[0,0,1,1,0,0],[0,1,0,0,1,0],[0,1,0,0,1,0],[0,0,1,1,1,0],[0,0,0,0,1,0],[0,0,1,1,0,0]]
ten=[[0,1,0,0,1,0],[1,1,0,1,0,1],[0,1,0,1,0,1],[0,1,0,1,0,1],[0,1,0,1,0,1],[0,1,0,0,1,0]]
eleven=[[0,1,0,0,1,0],[1,1,0,1,1,0],[0,1,0,0,1,0],[0,1,0,0,1,0],[0,1,0,0,1,0],[0,1,0,0,1,0]]
twelve=[[0,1,0,0,1,0],[1,1,0,1,0,1],[0,1,0,0,0,1],[0,1,0,0,1,0],[0,1,0,1,0,0],[0,1,0,1,1,1]]

nums = [zero, one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve]

# hour background color
z = [0,0,0]

# hour number color
w = [255,255,255]

# minute background color
e = [0,0,0]

# minute dot color
x = [255,0,0]

def row_one(m):
    result = [0,0,0,0,0,0,0,0]
    if m > u*4 and m < u*25:
        result = [0,0,0,0,1,1,1,1]
    else:
        if m < u:
            result = [0,0,0,0,0,0,0,0]
        elif m < u*2:
            result = [0,0,0,0,1,0,0,0]
        elif m < u*3:
            result = [0,0,0,0,1,1,0,0]
        elif m < u*4:
            result = [0,0,0,0,1,1,1,0]
        elif m < u*25:
            result = [0,0,0,0,1,1,1,1]
        elif m < u*26:
            result = [1,0,0,0,1,1,1,1]
        elif m < u*27:
            result = [1,1,0,0,1,1,1,1]
        elif m < u*28:
            result = [1,1,1,0,1,1,1,1]
        else:
            result = [1,1,1,1,1,1,1,1]
    return result

def row_eight(m):
    result = [1,1,1,1,1,1,1,1]
    if m < u*18:
        if m < u*11:
            result = [0,0,0,0,0,0,0,0]
        elif m < u*12:
            result = [0,0,0,0,0,0,0,1]
        elif m < u*13:
            result = [0,0,0,0,0,0,1,1]
        elif m < u*14:
            result = [0,0,0,0,0,1,1,1]
        elif m < u*15:
            result = [0,0,0,0,1,1,1,1]
        elif m < u*16:
            result = [0,0,0,1,1,1,1,1]
        elif m < u*17:
            result = [0,0,1,1,1,1,1,1]
        else:
            result = [0,1,1,1,1,1,1,1]
    return result

def convert_to_color(arr, background, color):
    return [background if j == 0 else color for j in arr]

def update_clock(hh, mm):
    if hh > 12:
        hh = hh - 12

    img = []

    # row 1
    row1 = row_one(mm)
    img.extend(convert_to_color(row1, e, x))

    # row 2-7
    for i in range(6):
        if mm > (u*(24-i)):
            img.append(x)
        else:
            img.append(e)

        # hour number
        img.extend(convert_to_color(nums[hh][i], z, w))

        if mm > (u*(5+i)):
            img.append(x)
        else:
            img.append(e)

    #row 8
    row8 = row_eight(mm)
    img.extend(convert_to_color(row8, e, x))

    sense.set_pixels(img)

def getColors():
    global w
    w = convertHexToRGB(c.get_setting_value('kleur_primary'))
    global x
    x = convertHexToRGB(c.get_setting_value('kleur_secondary'))

def convertHexToRGB (rgb):
    print(rgb)
    h = rgb.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2 ,4))

getColors()
try:
    while True:
        getColors()
        now = datetime.datetime.now()
        update_clock(now.hour, now.minute*1.0)
        time.sleep(10)
except KeyboardInterrupt:


    sense.clear()
