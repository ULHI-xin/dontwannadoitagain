import json
from PIL import Image



def get_colors_from_img(imgfile,
                        step, start_x, start_y,
                        valid_pix=lambda p:(len(p) >= 4 and p[3] > 0)):

    def _rgb2hexstr(pix_xy):
        return "%x%x%x" % pix_xy[:3]

    img = Image.open(imgfile)
    pix = img.load()

    result = []
    for y in range(1000):
        pix_y = start_y + step * y
        if pix_y >= img.size[1]:
            break
        for x in range(1000):
            pix_x = start_x + step * x
            if pix_x >= img.size[0]:
                break
            pix_xy = pix[pix_x, pix_y]
            if valid_pix(pix_xy):
                result.append((x, y, _rgb2hexstr(pix_xy)))
            else:
                continue
    print len(result)
    return result


result = get_colors_from_img(
    "/Users/xinzhao/Desktop/mei.png", 10, 8, 5)
result = json.dumps(result)
with open("/Users/xinzhao/Desktop/mei.json", 'w') as fw:
    fw.write(result)
