from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import cv2 as cv
import tkinter
import tkinter.filedialog
from PIL import Image, ImageTk
import numpy as np



import argparse
import os.path
import re
import sys
import tarfile

import numpy as np
from six.moves import urllib
import tensorflow as tf

#综合图像识别和文字分类
import numpy as np
import os, sys
sys.path.append('textcnn')
from textcnn.predict import RefuseClassification
from classify_image import *


#界面设置
window = tkinter.Tk()
window.title('垃圾分类识别界面')
window.geometry('350x400')

#下面这个可以展开全屏
#window.state("zoomed")

#固定窗口，使界面不可放大或缩小
window.resizable(0, 0)
var1 = tkinter.StringVar()
#弄个花里花俏一点的界面增加视觉效果而已
#T = tkinter.Label(window, text="25+100=", textvariable=var1, bg="lightGreen", fg="DimGray", anchor="se")
#T.place(x=0, y=0, width=350, height=120)

#显示图片路径以及识别结果的窗口
tkinter.Label(window, text='图片地址为: ').place(x=50, y=150)
tkinter.Label(window, text='识别结果为: ').place(x=50, y=190)

var_user_name = tkinter.StringVar()
entry_user_name = tkinter.Entry(window, textvariable=var_user_name)
entry_user_name.place(x=120, y=150)

var_user_pd = tkinter.StringVar()
entry_user_pd = tkinter.Entry(window, textvariable=var_user_pd)
entry_user_pd.place(x=120, y=190)

FLAGS = None

# pylint: disable=line-too-long
DATA_URL = 'http://download.tensorflow.org/models/image/imagenet/inception-2015-12-05.tgz'


# pylint: enable=line-too-long

class RafuseRecognize():
    
    def __init__(self):
        
        self.refuse_classification = RefuseClassification()
        self.init_classify_image_model()
        self.node_lookup = NodeLookup(uid_chinese_lookup_path='./data/imagenet_2012_challenge_label_chinese_map.pbtxt', 
                                model_dir = '/tmp/imagenet')#将中文对照表转换为人类可读ID
        
        
    def init_classify_image_model(self):
        
        create_graph('/tmp/imagenet')#从保存的GraphDef文件创建一个图形并返回一个保存程序。

        self.sess = tf.Session()#建立会话
        self.softmax_tensor = self.sess.graph.get_tensor_by_name('softmax:0')
        
        
    def recognize_image(self, image_data):
        
        predictions = self.sess.run(self.softmax_tensor,#执行该变量
                               {'DecodeJpeg/contents:0': image_data})
        predictions = np.squeeze(predictions)#从数组的形状中删除单维度条目，即把shape中为1的维度去掉

        top_k = predictions.argsort()[-5:][::-1]#从小到大排序
        result_list = []
        for node_id in top_k:
            human_string = self.node_lookup.id_to_string(node_id)#转换为string类型
            #print(human_string)
            human_string = ''.join(list(set(human_string.replace('，', ',').split(','))))#添加分隔符
            #print(human_string)
            classification = self.refuse_classification.predict(human_string)#对用户输入的进行分类
            result_list.append('%s  =>  %s' % (human_string, classification))#多种结果产生的列表
            
        return '\n'.join(result_list)
        




#打开文件函数
def choose_fiel():
    selectFileName = tkinter.filedialog.askopenfilename(title='选择文件')  # 选择文件
    var_user_name.set(selectFileName)

#识别图片数字函数
def main(img):
    test = RafuseRecognize()
    image_data = tf.gfile.FastGFile(img, 'rb').read()
    res = test.recognize_image(image_data)
    var_user_pd.set(res)
    

#清零函数，不过没啥意义，就想把界面弄的对称一点而已
def delete():      #删除函数
    content = var_user_pd.get()
    var_user_pd.set(content[0:len(content) - 1])

#显示所要识别的图片函数


#按钮
submit_button = tkinter.Button(window, text="选择文件", command=choose_fiel).place(x=50, y=250)


submit_button = tkinter.Button(window, text="开始识别", command=lambda: main(entry_user_name.get())).place(x=50, y=300)


window.mainloop()
