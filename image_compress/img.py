#!/usr/bin/python
from wand.image import Image
import os
import re
import time
import shutil

# set the image file extension you want to compression
file_type_reg = "(.jpg|.png|.JPG|.PNG)$"

# source folder path
source = "./images/"

# compression images output target path
target = "./target/"

# max witdh
max_width = 930

# default image compression quality
compression_quality = 70




def mkdir_p(path):
    if os.path.isdir(path) is True:
        print path + " already exists"
        exit()
    os.mkdir(path)

def compression(source_path):
    try:
        with Image(filename = source_path) as img:
            print source_path
            _img = img.clone()
            # get image width
            _img_width = _img.width
            _img_height = _img.height
            if _img.width > max_width:
                # resize image
                _proportion = float(_img_width)/float(max_width)
                _img.resize(max_width, int(_img_height / _proportion));
            # reset image quality
            _img.compression_quality = compression_quality
            _target_path = re.sub(r"^" + re.escape(source), target, source_path);
            _dir = os.path.split(_target_path)[0]
            if os.path.isdir(_dir) is False:
                os.makedirs(_dir)
            _img.save(filename = _target_path)
            print "File: " + _target_path + " saved!"
    except:
        copy_file(source_path)

def copy_file(cp_path):
    _target_path = re.sub(r"^" + re.escape(source), target, cp_path);
    _path = os.path.dirname(_target_path)
    if not os.path.exists(_path):
        os.mkdir(_path)
    shutil.copy2(cp_path, _target_path)
    print "File: " + _target_path + " copied!"

def recursion(path):
    file_list = os.listdir(path)
    for file_item in file_list:
        _path = path + file_item
        if os.path.isdir(_path) is True:
            recursion(_path + "/")
        else:
            # validate file type
            if len(re.findall(file_type_reg, _path)) == 1:
                compression(_path)
            else:
                # if file is not matched, just execution copy operation
                copy_file(_path)

if __name__ == "__main__":
    start_time = int(time.time())
    mkdir_p(target)
    recursion(source)
    end_time = int(time.time())
    print "image compression completed, cost " + str(end_time - start_time) + " seconds."
