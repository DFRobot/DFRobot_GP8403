# DFRobot_GP8403

* [English Version](./README.md)

这是一款IIC转0-5V或0-10V DAC模块。用户可以通过控制此模块输出0-5V的电压或0-10V电压，它具有以下特点：
1. 能够控制输出0-5V或0-10V电压。
2. 采用I2C接口控制输出电压大小，I2C默认地址为0x58。 
3. 模块掉电后，输出电压配置将丢失，如果想下次上电采用此次配置，需保存配置。


![产品效果图](../../resources/images/DFR0971.png) 

## Product Link（[www.dfrobot.com](www.dfrobot.com)）
    SKU: DFR0971 

## Table of Contents
  - [概述](#概述)
  - [库安装](#库安装)
  - [方法](#方法)
  - [兼容性](#兼容性)
  - [历史](#历史)
  - [创作者](#创作者)

## 概述
提供一个Arduino库给IIC转转0~5V或0~10V DAC模块，以设置和保存该模块输出的电压配置，此库具有以下功能：
1. 直接设置0-5V的电压或0-10V电压；
2. 通过设置DAC范围0 ~ 0xFFF来输出对应的电压；
3. 保存电压配置，掉电后，该配置不丢失。

## 库安装
1. 下载库至树莓派，要使用这个库，首先要将库下载到Raspberry Pi，命令下载方法如下:<br>
```python
sudo git clone https://github.com/DFRobot/DFRobot_GP8403
```
2. 打开并运行例程，要执行一个例程demo_x.py，请在命令行中输入python demo_x.py。例如，要执行 demo_set_current.py例程，你需要输入:<br>

```python
python demo_set_current.py 
或 
python2 demo_set_current.py 
或 
python3 demo_set_current.py
```

## 方法

```python
  '''!
    @param 初始化传感器
  '''
  def begin(self):
    
  '''!
    @brief 设置DAC输出范围
    @param mode 选择DAC输出范围
  '''
  def set_DAC_outrange(self,mode):
    
  '''!
    @brief 选择DAC输出通道和输出范围
    @param data 设置输出数据
    @param channel 输出通道 0:通道0;1:通道1;2:全部通道
  '''
  def set_DAC_out_voltage(self,data,channel)
    
  '''!
    @brief   保存当前电流配置，保存成功后，模块掉电重启后，将启用此配置
  '''
  def store(self)
    
  '''!
    @brief 设置传感器输出正弦波
    @param amp 设点正弦波幅度Vp
    @param freq 设置正弦波频率f
    @param offset 设置正弦波直流偏置Voffset
    @param channel 输出通道 0:通道0;1:通道1;2:全部通道
  '''
  def output_sin(self,amp,freq,offset,channel)
    

  '''!
    @brief 调用函数输出三角波
    @param amp 设点正弦波幅度Vp
    @param freq 设置正弦波频率f
    @param offset 设置正弦波直流偏置Voffset
    @param dutyCycle 设定三角（锯齿）波占空比
    @param channel 输出通道 0:通道0;1:通道1;2:全部通道
  '''
  def output_triangle(self,amp,freq,offset,dutyCycle,channel):
    
  '''!
    @brief 调用函数输出方波
    @param amp 设点正弦波幅度Vp
    @param freq 设置正弦波频率f
    @param offset 设置正弦波直流偏置Voffset
    @param dutyCycle 设定方波波占空比
    @param channel 输出通道 0:通道0;1:通道1;2:全部通道
  '''
  def output_square(self,amp,freq,offset,dutyCycle,channel)
    
```

## 兼容性

| 主板         | 通过 | 未通过 | 未测试 | 备注 |
| ------------ | :--: | :----: | :----: | :--: |
| RaspberryPi2 |      |        |   √    |      |
| RaspberryPi3 |      |        |   √    |      |
| RaspberryPi4 |  √   |        |        |      |

* Python 版本

| Python  | 通过 | 未通过 | 未测试 | 备注 |
| ------- | :--: | :----: | :----: | ---- |
| Python2 |  √   |        |        |      |
| Python3 |  √   |        |        |      |


## 历史

- 2022/03/10 - 1.0.0 版本

## 创作者

Written by tangjie(jie.tang@dfrobot.com), 2022. (Welcome to our [website](https://www.dfrobot.com/))





