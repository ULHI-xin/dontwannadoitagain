from PIL import Image
from PIL import ImageChops
import math, operator


def imgchop_diff(file1, file2):
    img1 = Image.open(file1)
    img2 = Image.open(file2)

    h = ImageChops.difference(img1, img2).convert('L').histogram()
    print len(h)
    print h
    return ImageChops.difference(img1, img2),\
        math.sqrt(
            reduce(operator.add,
                   map(lambda _h, i: _h * (i ** 2), h, range(256))) /
            (float(img1.size[0]) * img1.size[1]))


import sys

file1 = sys.argv[1]
file2 = sys.argv[2]
path = file1[:file1.rfind('/')]
filename1 = file1[file1.rfind('/')+1:]
filename2 = file2[file2.rfind('/')+1:]
diff, rms = imgchop_diff(sys.argv[1], sys.argv[2])
diff.save("{}/[{:.2f}]{}-{}".format(path, rms, filename1, filename2))

