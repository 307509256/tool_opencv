#-*- coding:utf-8 -*-

import os
import re
import xml.dom.minidom

from PIL import Image

IMG_FOLDER_PATH = "/home/gongjia/tool_opencv/out"

def gci(path, file_list = None):

    if file_list == None:
        file_list = []

    #遍历path下所有文件，包括子目录
    files = os.listdir(path)
    for fi in files:
        fi_d = os.path.join(path,fi)
        if os.path.isdir(fi_d):
            gci(fi_d, file_list)
        else:
            file_list.append(os.path.join(path, fi_d))

    return file_list

def get_size(path):
    try:
        im = Image.open(path)
    except Exception, e:
        print "---- bad image: %s" % os.path.basename(path)
        return (0, 0)
    return im.size

def generate_xml():

    file_list = gci(IMG_FOLDER_PATH)

    FOLDER = "JPEGImages"
    DEPTH = 3
    SEGMENTED = 0
    POSE = 'Unspecified'
    TRUNCATED = 0
    DIFFICULT = 0

    for f in file_list:
        print f

        doc = xml.dom.minidom.Document()
        root = doc.createElement('annotation')
        doc.appendChild(root)

        # 类别,我从文件路径中获取
        classification = re.search(r'.*/(.*)/', f).group(1)

        # folder
        folder = doc.createElement('folder')
        folder.appendChild(doc.createTextNode(FOLDER))

        # filename
        filename = doc.createElement('filename')
        filename.appendChild(doc.createTextNode(os.path.basename(f)))

        # path
        path = doc.createElement('path')
        path.appendChild(doc.createTextNode(f))

        # source
        #   |--database
        source = doc.createElement('source')
        database = doc.createElement('database')
        database.appendChild(doc.createTextNode('Unknown'))
        source.appendChild(database)

        # size
        #   |--width
        #   |--height
        #   |--depth
        size = doc.createElement('size')
        width = doc.createElement('width')
        height = doc.createElement('height')
        depth = doc.createElement('depth')
        # 读取图片的尺寸
        f_width, f_height = get_size(f)
        if f_width == 0 and f_height == 0:
            continue
        width.appendChild(doc.createTextNode(str(f_width)))
        height.appendChild(doc.createTextNode(str(f_height)))
        depth.appendChild(doc.createTextNode(str(DEPTH)))
        size.appendChild(width)
        size.appendChild(height)
        size.appendChild(depth)

        # segmented
        segmented = doc.createElement('segmented')
        segmented.appendChild(doc.createTextNode(str(SEGMENTED)))

        # object
        #   |--name
        #   |--pose
        #   |--truncated
        #   |--difficult
        #   |--bndbox
        #       |--xmin
        #       |--ymin
        #       |--xmax
        #       |--ymax
        object1 = doc.createElement('object')
        name = doc.createElement('name')
        pose = doc.createElement('pose')
        truncated = doc.createElement('truncated')
        difficult = doc.createElement('difficult')

        name.appendChild(doc.createTextNode(str(classification)))
        pose.appendChild(doc.createTextNode(str(POSE)))
        truncated.appendChild(doc.createTextNode(str(TRUNCATED)))
        difficult.appendChild(doc.createTextNode(str(DIFFICULT)))

        bndbox = doc.createElement('bndbox')
        xmin = doc.createElement('xmin')
        ymin = doc.createElement('ymin')
        xmax = doc.createElement('xmax')
        ymax = doc.createElement('ymax')
        xmin.appendChild(doc.createTextNode(str(1)))
        ymin.appendChild(doc.createTextNode(str(1)))
        xmax.appendChild(doc.createTextNode(str(f_width)))
        ymax.appendChild(doc.createTextNode(str(f_height)))
        bndbox.appendChild(xmin)
        bndbox.appendChild(ymin)
        bndbox.appendChild(xmax)
        bndbox.appendChild(ymax)

        object1.appendChild(name)
        object1.appendChild(pose)
        object1.appendChild(truncated)
        object1.appendChild(difficult)
        object1.appendChild(bndbox)

        root.appendChild(folder)
        root.appendChild(filename)
        root.appendChild(path)
        root.appendChild(source)
        root.appendChild(size)
        root.appendChild(segmented)
        root.appendChild(object1)

        folder_name = classification + '_xml'
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)

        xml_name = re.search(r'(.*)\.', os.path.basename(f)).group(1)

        fp = open('%s/%s.xml' % (folder_name, xml_name), 'w')
        doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="utf-8")

generate_xml()