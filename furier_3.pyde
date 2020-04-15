fX = []
fY = []
val=[]
valX = []
valY = []
angle = 0
points = []
userDraw=True
take=False

def setup():
    size(800, 800)
    stroke(255)
    background(51)
    
def draw():
    global angle,fX, fY, points,take,userDraw,val
    if userDraw:
        x_val=mouseX-floor(width/2)
        y_val=mouseY-floor(height/2)
        if take and [x_val,y_val] not in val:
            stroke(255)
            strokeWeight(3)
            point(mouseX,mouseY)
            val.append([x_val,y_val])
    else:
        background(51)
        x1, y1 = epicycle(100, 500, fY, PI / 2)
        x2, y2 = epicycle(550, 100, fX, 0)
        stroke(0,255,255)
        line(x1, y1, x2, y1)
        line(x2, y2, x2, y1)
        points.insert(0, [x2, y1])
        if len(points) > 1000:
            points.pop()
        for p in range(len(points)):
            stroke(255,100,200)
            strokeWeight(3)
            point(points[p][0], points[p][1])
        dt = 2 * PI / len(fY)
        angle -= dt

def mousePressed():
    global take
    take=True

def mouseReleased():
    global val,take,valX,valY,fX,fY,userDraw
    take=False
    userDraw=False
    for v in val:
        valX.append(v[0])
        valY.append(v[1])
    fY.extend(dft(valY))
    fX.extend(dft(valX))

def epicycle(x, y, f, rotation):
    for i in range(len(f)):
        freq = f[i]['freq']
        prevx = x
        prevy = y
        radious = f[i]['amp']
        phase = f[i]['phase']
        x += radious * cos(freq * angle + phase + rotation)
        y += radious * sin(freq * angle + phase + rotation)
        noFill()
        stroke(255,100)
        strokeWeight(1)
        ellipse(prevx, prevy, radious * 2, radious * 2)
        line(prevx, prevy, x, y)
    return x, y

def dft(x):
    X = []
    N = len(x)
    for k in range(N):
        re = 0
        im = 0
        for n in range(N):
            phi = (2 * PI * k * n) / N
            re += x[n] * cos(phi)
            im -= x[n] * sin(phi)

        re = re / N
        im = im / N
        X.append({
            're': re,
            'im': im,
            'freq': k,
            'amp': sqrt(re * re + im * im),
            'phase': atan2(im, re)
        })
    return X
