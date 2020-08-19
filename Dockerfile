 # 建立 python3.7 环境
 FROM python:3.7
 
 # 镜像作者大江狗
 MAINTAINER FUKO
 
 # 设置 python 环境变量
 ENV PYTHONUNBUFFERED 1
 
 # 设置pip源为国内源
 COPY pip.conf /root/.pip/pip.conf
 
 RUN mkdir -p /home/ares
 
 RUN mkdir -p /home/script
 
 # 设置容器内工作目录
 WORKDIR /home/ares
 
 # 将当前目录文件加入到容器工作目录中（. 表示当前宿主机目录）
 ADD . /home/ares
 
 # 利用 pip 安装依赖
 RUN pip install -r requirements.txt
 