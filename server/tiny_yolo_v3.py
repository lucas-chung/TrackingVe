import numpy as np
import cv2

#net = cv2.dnn.readNet('yolov3-tiny.weights','yolov3-tiny.cfg')
net = cv2.dnn.readNet('yolov3.weights','yolov3.cfg')

with open('coco.names','r') as f:
    classes = f.read().splitlines()
img = cv2.imread('person.png')
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

CONF_THRES = 0.1
NHS_THRES = 0.4

#print(np.array(class_probs).shape)
#indexs = cv2.dnn.NMSBoxes(boxes,confidences,CONF_THRES,NHS_THRES)
i = np.argmax(confidences)
if(i > 0):
    x,y,w,h = boxes[i]
    confidence = str(round(confidences[i],2))
    #color = colors[i%len(colors)]
    cv2.rectangle(img,(x,y),(x+w,y+h),(125,255,255),8)
    string = '{} {}'.format(class_names[i],confidence)
    cv2.putText(img, string, (x,y+20), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255),5)
cv2.imwrite('result1.jpg',img)