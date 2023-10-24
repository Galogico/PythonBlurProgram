from PIL import Image
import math
import numpy as np
from tqdm import tqdm


def gaussian_2d(x, y, std_dev):
    """Calculate Gaussian based on x, y"""
    # separei pra ficar mais facil de checar
    # Formula desse site
    # https://www.geeksforgeeks.org/apply-a-gauss-filter-to-an-image-with-python/
    a = 1 / (2 * math.pi * std_dev**2)
    e = math.exp(-(x**2 + y**2) / (2 * std_dev**2))
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
            row.append(gaussian_2d(x, y, std_dev))
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
    return kernel, total


def create_box_kernel(size=5):
    """Create a box kernel"""
    k = []
    for _ in range(size):
        k.append([1] * size)
    return k, size**2


def apply_kernel_around_pixel(x, y, img, rgb, kernel, size, total):
    """tentativa de aplicar o kernel"""
    new_pixel = 0
    for i in range(0, size):
        for j in range(0, size):
            new_pixel += kernel[i][j] * img[x + i - size // 2][y + j - size // 2][rgb]
    return new_pixel / total


def apply_filter(im, kernel, total):
    """Apply filter"""
    w, h = im.size
    img = np.array(im)
    size = len(kernel[0])
    for rgb in tqdm(range(3)):
        for i in range(size // 2, h - size // 2):
            for j in range(size // 2, w - size // 2):
                img[i][j][rgb] = apply_kernel_around_pixel(
                    i, j, img, rgb, kernel, size, total
                )
    return img


def load_image(filename):
    """Load image"""
    im = Image.open(filename)
    return im


def save_array_image(image_arr, out_name="output.jpg"):
    """save image from numpy array"""
    img = Image.fromarray(image_arr)
    img.save(out_name)
    print("image saved.")


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
    kernel, total = create_box_kernel(size=3)
    img = load_image("./image/eye.jpg")

    save_array_image(img)

    # passar varias vezes
    # vezes = 10
    # kernel, total = create_box_kernel(size=3)
    # img = load_image("./image/eye.jpg")
    # img = apply_filter(img, kernel, total)
    # for i in range(vezes):
    #     if i == vezes - 1:
    #         break
    # img = Image.fromarray(img)
