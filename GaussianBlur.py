from PIL import Image

rList = []
gList = []
bList = []
r = 0
g = 0
b = 0
hIndex = -1

# original Image
im = Image.open(r"./image.jpg")
locateH = 0
locateW = 0
px = im.load()

# Blurred image
im2 = Image.open(r"./image2.jpg")

w, h = im.size
pxs = h*w


for i in range(pxs):
    hIndex = -1
    for n in range(3):
        if locateH +1 < h-1:
            r, g, b = px[locateW - 1, locateH + hIndex]
            rList.append(r*1/9)
            gList.append(g*1/9)
            bList.append(b*1/9)
        else:
            rList.append(0)
            gList.append(0)
            bList.append(0)

        r,g,b = 0,0,0
        if locateH +1 < h-1:
            r, g, b = px[locateW, locateH + hIndex]
            rList.append(r*1/9)
            gList.append(g*1/9)
            bList.append(b*1/9)
        else:
            rList.append(0)
            gList.append(0)
            bList.append(0)
        r,g,b = 0,0,0

        if locateW + 1 < w - 1 or locateH +1 < h-1:
            r, g, b = px[locateW, locateH]
            rList.append(r*1/9)
            gList.append(g*1/9)
            bList.append(b*1/9)
        else:
            rList.append(0)
            gList.append(0)
            bList.append(0)

        print(rList)

        hIndex += 1
        r,g,b = 0,0,0


    r = sum(rList)
    g = sum(gList)
    b = sum(bList)
    im2.putpixel((locateW, locateH), (int(r),int(g),int(b)))

    rList = []
    gList = []
    bList = []

    if locateW == w -1:
        locateH += 1
        locateW = 0
    else:
        locateW += 1

im2.save("mageee.jpg")
