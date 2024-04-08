import socket
import cv2
import numpy as np
import struct
from time import sleep

net = cv2.dnn.readNet('yolov3-tiny.weights','yolov3-tiny.cfg')
with open('coco.names','r') as f:
    classes = f.read().splitlines()
buffSize  = 65536
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = ('192.168.137.1', 8080)
#address = ('127.0.0.1', 8080)
s.bind(address)  
s.listen(1)   
print ('Waiting for images...')

# Initialize frame rate calculation
frame_rate_calc = 1
freq = cv2.getTickFrequency()

conn, addr = s.accept()
while True:
    # Start timer (for calculating frame rate)
    t1 = cv2.getTickCount()
    data1 = conn.recv(4) #先接收的是字节长度
    #data2 = conn.recv(buffSize) #接收编码图像数据
    if len(data1)==1 and data1[0]==1: #如果收到关闭消息则停止程序
        conn.close()
        cv2.destroyAllWindows()
        exit()
    if len(data1)!=4: #进行简单的校验，长度值是int类型，占四个字节
        length=0
    else:
        length=struct.unpack('i',data1)[0] #长度值
    data2 = b''
    recv_size = 0
    #2.接收真实的数据
    #循环接收直到接收到数据的长度等于数据的真实长度（总长度）
    while recv_size < length:
        data = conn.recv(1024)
        recv_size += len(data)
        data2 += data
    data3=np.array(bytearray(data2)) #格式转换
    img=cv2.imdecode(data3,1) #解码
    #print('have received one frame')
    #start
    height,width,_ = img.shape
    blob = cv2.dnn.blobFromImage(img,1/255,(416,416),(0,0,0),swapRB = True,crop = False)

    net.setInput(blob)

    layersNames = net.getLayerNames()
    output_layer_names = [layersNames[i[0]-1] for i in net.getUnconnectedOutLayers()]
    prediction = net.forward(output_layer_names)

    boxes = []
    objectness = []
    class_probs = []
    class_ids = []
    class_names = []

    for scale in prediction:
        for bbox in scale:
            obj = bbox[4]
            class_scores = bbox[5:]
            #class_id = np.argmax(class_scores)
            class_id = 0
            class_name = classes[class_id]
            class_prob = class_scores[class_id]

            center_x = int(bbox[0] * width)
            center_y = int(bbox[1] * height)
            w = int(bbox[2] * width)
            h = int(bbox[3] * height)

            x = int(center_x - w/2)
            y = int(center_y - h/2)

            boxes.append([x,y,w,h])
            objectness.append(float(obj))
            class_ids.append(class_id)
            class_names.append(class_name)
            class_probs.append(class_prob)
    confidences = np.array(class_probs) * np.array(objectness)

    #CONF_THRES = 0.1
    #NHS_THRES = 0.4
    #indexs = cv2.dnn.NMSBoxes(boxes,confidences,CONF_THRES,NHS_THRES)

    x,y,w,h = 0,0,0,0
    '''if(len(indexs)>0):
        i = np.argmax(confidences)
        x,y,w,h = boxes[i]
        confidence = str(round(confidences[i],2))
        #color = colors[i%len(colors)]
        cv2.rectangle(img,(x,y),(x+w,y+h),(125,255,255),8)
        string = '{} {}'.format(class_names[i],confidence)
        cv2.putText(img, string, (x,y+20), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255),5)'''
    i = np.argmax(confidences)
    if(i > 0):
        x,y,w,h = boxes[i]
        confidence = str(round(confidences[i],2))
        #color = colors[i%len(colors)]
        cv2.rectangle(img,(x,y),(x+w,y+h),(125,255,255),8)
        string = '{} {}'.format(class_names[i],confidence)
        cv2.putText(img, string, (x,y+20), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255),5)
        print(frame_rate_calc)
    #over
    # Calculate framerate
    t2 = cv2.getTickCount()
    time1 = (t2-t1)/freq
    frame_rate_calc= 1/time1

    cv2.imshow('frames',img) #窗口显示

    conn.send(struct.pack("i",x))
    if cv2.waitKey(1)==27: #按下“ESC”退出
        break
conn.close()
cv2.destroyAllWindows()