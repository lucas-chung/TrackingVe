# yolo-v3

#### 介绍

我们通过搭载摄像头的树莓派智能小车采集实时视频流，然后借助无线传输将数据传至服务器，服务器凭借其更优的运算性能，运行yolo-v3目标检测算法对每一帧进行分析处理，并将输出结果进行后处理，获得目标检测框的中心坐标，最后将坐标返回至小车控制系统中，系统会据此作出判断，执行相关动作。

#### 软件架构


服务器：

Listen()//持续监听是否有连接请求

bind_socket(“ip_address”,“port”)//若有客户端请求，绑定其ip地址及端口

while(true){

handle_picture()//处理树莓派传输而来的图像数据

	send_coordinate()//发送坐标信息给树莓派

}


客户端：

set_socket()//连接服务器

while(true){

	send_picture()//发送图像数据给主机

	receive_ coordinate()//接收坐标数据

	move()//控制小车

}

#### 使用说明

1.  先下载tiny-yolo-v3.cfg和coco.names，与server.py放在同一文件
    链接：https://pan.baidu.com/s/146BnJqHDr2yaSAkQD0J9sA 
    提取码：1234
2.  在主机输入 python3 server.py
3.  在客户端输入python3 client1.py

