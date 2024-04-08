import socket
import cv2
import numpy
import struct
import time
import  RPi.GPIO as GPIO
import  car_control as car

car.Init()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address_server = ('192.168.137.1', 8080)
sock.connect(address_server)
print("begin to send messages")
capture=cv2.VideoCapture(0) #VideoCapture对象，可获取摄像头设备的数据
try:
  while True:
    t1 = time.time()
    success,frame=capture.read()
    while not success and frame is None:
        success,frame=capture.read() #获取视频帧
    result,imgencode=cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,50]) #编码
    sock.send(struct.pack('i',imgencode.shape[0])) #发送编码后的字节长度，这个值不是固定的
    sock.send(imgencode) #发送视频帧数据
    #print('have sent one frame')
    x = struct.unpack("i",sock.recv(4))[0]
    car.Move(x,0)
except Exception as e:
  print(e)
  sock.sendall(struct.pack('b',1)) #发送关闭消息
  capture.release()
  sock.close()
  car.Stop()
  GPIO.cleanup()