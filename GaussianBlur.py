from PIL import Image
import math
import numpy as np


def gaussian_2d(x, y, std_dev):
    """Calculate Gaussian based on x, y"""
    # separei pra ficar mais facil de checar
    # Formula desse site
    # https://www.geeksforgeeks.org/apply-a-gauss-filter-to-an-image-with-python/
    a = 1 / (2 * math.pi * std_dev**2)
    e =  math.exp(-(x**2 + y**2) / (2*std_dev**2))
    return a * e

def create_gaussian_kernel(size=5, std_dev=3):
    """Create kernel 2d"""
    center = size // 2
    # Create a matrix
    kernel = []
    for i in range(size):
        row = []
        for j in range(size):
            x = i - center
            y = j - center
            row.append(gaussian_2d(x,y, std_dev))
        kernel.append(row)
    # increase to > 1
    factor = min(list(min(kernel)))
    for i in range(size):
        for j in range(size):
            kernel[i][j] /= factor
    # total
    total = 0
    for i in range(size):
        for j in range(size):
            total += kernel[i][j]
    print(total)
    return kernel, total

def create_box_kernel(size=5):
    """Create a box kernel"""
    kernel = []
    for _ in range(size):
        kernel.append([1] * size)
    return kernel, size**2


def save_array_image(image_arr):
    """ save image from numpy array"""
    img = Image.fromarray(image_arr.astype('uint8'), 'RGB')
    img.save("output.jpg")
    


def apply_kernel_around(img, rgb, x, y, kernel, size, total):
    """ tentativa de aplicar o kernel"""
    new_pixel = 0
    for i in range(0, size):
        for j in range(0, size):
            new_pixel += kernel[i][j] * img[i-size//2][j-size//2][rgb] 
            print(f"image coord: rgb {rgb} x:{x-i-size//2}, y: {y-j-size//2} = {new_pixel/total}")
    return new_pixel / total



def run_gaussian_filter(size=3, std=.5):
    """ run gaussian filter in image no padding yet"""

    kernel, total = create_gaussian_kernel(size, std)
    
    try:
        im = Image.open(r"./image/eye.jpg")
    except Exception as e:
        print(f"{'*' * 40}\n{e}\n{type(e)}\nProblem reading image:")
    
    w, h = im.size

    img = np.array(im)
    for rgb in range(3):
        for i in range(size // 2 + 1, h - size // 2 ):
            for j in range(size // 2 + 1, w - size //2): # Nao faz as bordas
                img[i][j][rgb] = apply_kernel_around(img, rgb, i, j, kernel, size, total)

    save_array_image(img)

    

    

# rList = []
# gList = []
# bList = []
# r = 0
# g = 0
# b = 0
# hIndex = -1

# # original Image
# im = Image.open(r"./image/eye.jpg")
# locateH = 0
# locateW = 0
# px = im.load()

# # Blurred image
# im2 = Image.open(r"./image/eye_copy.jpg")

# w, h = im.size
# pxs = h*w

# for i in range(pxs):
#     hIndex = -1
#     for n in range(3):
#         if locateH +1 < h-1:
#             r, g, b = px[locateW - 1, locateH + hIndex]
#             rList.append(r*1/9)
#             gList.append(g*1/9)
#             bList.append(b*1/9)
#         else:
#             rList.append(0)
#             gList.append(0)
#             bList.append(0)

#         r,g,b = 0,0,0
#         if locateH +1 < h-1:
#             r, g, b = px[locateW, locateH + hIndex]
#             rList.append(r*1/9)
#             gList.append(g*1/9)
#             bList.append(b*1/9)
#         else:
#             rList.append(0)
#             gList.append(0)
#             bList.append(0)
#         r,g,b = 0,0,0

#         if locateW + 1 < w - 1 or locateH +1 < h-1:
#             r, g, b = px[locateW, locateH]
#             rList.append(r*1/9)
#             gList.append(g*1/9)
#             bList.append(b*1/9)
#         else:
#             rList.append(0)
#             gList.append(0)
#             bList.append(0)

#         print(rList)

#         hIndex += 1
#         r,g,b = 0,0,0


#     r = sum(rList)
#     g = sum(gList)
#     b = sum(bList)
#     im2.putpixel((locateW, locateH), (int(r),int(g),int(b)))

#     rList = []
#     gList = []
#     bList = []

#     if locateW == w -1:
#         locateH += 1
#         locateW = 0
#     else:
#         locateW += 1

# im2.save("mageee.jpg")


if __name__ == "__main__":
    run_gaussian_filter(size=3, std=.5)