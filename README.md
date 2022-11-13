# 项目环境配置：

## 1 基础环境配置

### 1 安装Python3
#### Debian系列:
`sudo apt install python3`
#### RedHat系列:
`yum install python3`
#### Arch系列:
`pacman install python3`
#### 查看是否安装成功:
`python3 --version`

若弹出版本信息则说明安装成功

### 2 安装pip
#### Debian系列:
`sudo apt install pip`
#### RedHat系列:
`yum install pip`
#### Arch系列:
`pacman install pip`
#### 查看是否安装成功:
`pip --version`

若弹出版本信息则说明安装成功
***

## 2 Flask 安装环境
### 1 安装虚拟环境
`sudo pip install virtualenv`

`sudo pip install virtualenvwrapper`
#### 查看是否安装成功:
`virtualenv --version`

若弹出版本信息则说明安装成功
### 2 配置环境变量
#### 1、创建目录用来存放虚拟环境
`mkdir` 

`$HOME/.virtualenvs`
#### 2、打开~/.bashrc文件，并添加如下：
`export WORKON_HOME=$HOME/.virtualenvs`

`source /usr/local/bin/virtualenvwrapper.sh`
#### 3、运行
`source ~/.bashrc`
### 3 进入虚拟环境
`workon Flask_py`
***

## 3 安装Flask及依赖包
`pip install flask`

####  查看是否安装成功
`flask --version`

#### 安装后续所需的模块

`pip install -r requirements.txt`


# 项目启动命令
#### 在项目文件夹下打开终端
`python3 app.py`


