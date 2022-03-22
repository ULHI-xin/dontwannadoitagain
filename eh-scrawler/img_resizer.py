import os

from PIL import Image


def resize_jpg(img_jpg):
    if img_jpg.format != 'JPEG':
        return None
    w, h = img_jpg.size
    if min([w, h]) > 1600:
        if w < h:
            w_new, h_new = 1600, int(round(1600 * (h / w)))
        else:
            w_new, h_new = int(round(1600 * (w / h))), 1600
        img_new = img_jpg.resize((w_new, h_new), Image.LANCZOS)
        return img_new
    return None


def resize_img(img, smaller_d):
    w, h = img.size
    if w < h:
        w_new, h_new = smaller_d, int(round(smaller_d * (h / w)))
    else:
        w_new, h_new = int(round(smaller_d * (w / h))), smaller_d
    img_new = img.resize((w_new, h_new), Image.LANCZOS)
    return img_new


def resize_jpg_dir(dir_path):
    for _, _, f in os.walk(dir_path):
        for _f in f:
            if os.path.getsize(_f) > 2000000:
                resize_attempt = resize_jpg(Image.open(_f))
                if resize_attempt:
                    resize_attempt.save(f'resized/{_f}', quality=85)
                    print('resized:', _f)
                    continue
            print('skipped:', _f)


def resize_all_in_dir(dir_des):
    dir_path = f"./{dir_des}"
    for _, _, f in os.walk(dir_path):
        for _f in f:
            full_filename = f"{dir_des}/{_f}"
            img = Image.open(full_filename)
            print(f"Process {dir_des}/{_f}")
            if img.format != 'JPEG' or min(img.size) > 1600 or os.path.getsize(full_filename) > 2000000:
                resized = resize_img(img, smaller_d=1600)
            else:
                resized = img
            save_name = _f.replace('.BMP', '.jpg').replace('.bmp', '.jpg').replace('.png', '.jpg').replace('.PNG', '.jpg')
            print(resized.format, resized.mode)
            if resized.mode != 'RGB':
                resized = resized.convert('RGB')
            print(resized.format, resized.mode)
            resized.save(f"resized/{dir_des}/{save_name}", format='JPEG', quality=85)
