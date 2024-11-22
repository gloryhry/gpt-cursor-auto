# 使用官方带有Chrome的Selenium基础镜像
FROM selenium/standalone-chrome:latest

# 设置工作目录为 /APP
WORKDIR /APP

USER root

# 更新 apt 列表
RUN apt-get update

# 安装Python和pip
RUN apt-get install -y \
    python3 \
    python3-pip && \
    rm -rf /var/lib/apt/lists/*

# 安装必要的Python包
RUN pip3 install --no-cache-dir --break-system-packages \
    DrissionPage==4.1.0.9 \
    PyVirtualDisplay==3.0

# 将当前目录下的所有文件复制到容器的/APP目录下
COPY . /APP

# 设置环境变量的默认值，这些值可以在运行容器时被覆盖
ENV ACCOUNT=default@mailto.plus \
    PASSWORD=default_password \
    FIRST_NAME=DefaultFirstName \
    LAST_NAME=DefaultLastName

# 示例CMD命令，用于启动Python应用，需根据你的具体应用修改
CMD ["python3", "cursor_pro_keep_alive.py"]