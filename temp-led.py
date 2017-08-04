# -*- coding: utf-8 -*-
import time
import tm1637
import RPi.GPIO as GPIO
SENSOR=4#温度传感器
DIGITALCLK=23#数码管时钟
DIGITALDATA=24#数码管数据
SETTEMP=33#高于此值开启设备
while(True):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    time.sleep(1)
    data=[]
    Display = tm1637.TM1637(DIGITALCLK,DIGITALDATA,tm1637.BRIGHT_TYPICAL)
    Display.ShowDoublepoint(1)
    Display.SetBrightnes(1)
    j=0
    #start work
    GPIO.setup(SENSOR,GPIO.OUT)
    GPIO.output(SENSOR,GPIO.LOW)
    time.sleep(0.02)
    GPIO.output(SENSOR,GPIO.HIGH)
    i=1
    #wait to response
    GPIO.setup(SENSOR,GPIO.IN)
    while GPIO.input(SENSOR)==1:
        continue
    while GPIO.input(SENSOR)==0:
        continue
    while GPIO.input(SENSOR)==1:
        continue
    #get data
    while j<40:
        k=0
        while GPIO.input(SENSOR)==0:
            continue        
        while GPIO.input(SENSOR)==1:
            k+=1
            if k>100:break
        if k<3:
            data.append(0)
        else:
            data.append(1)
        j+=1
    time.sleep(1)
    #get temperature
    humidity_bit=data[0:8]
    humidity_point_bit=data[8:16]
    temperature_bit=data[16:24]
    temperature_point_bit=data[24:32]
    check_bit=data[32:40]
    humidity=0
    humidity_point=0
    temperature=0
    temperature_point=0
    check=0
    for i in range(8):
        humidity+=humidity_bit[i]*2**(7-i)
        humidity_point+=humidity_point_bit[i]*2**(7-i)
        temperature+=temperature_bit[i]*2**(7-i)
        temperature_point+=temperature_point_bit[i]*2**(7-i)
        check+=check_bit[i]*2**(7-i)
    tmp=humidity+humidity_point+temperature+temperature_point
    if check==tmp:
        if temperature>SETTEMP :
            print "温度高于 ", SETTEMP," 开启继电器"
        temp1=temperature/10
        temp0=temperature%10
        humi1=humidity/10
        humi0=humidity%10
        show = [humi1,humi0,temp1,temp0] 
        #print "温度为：", temperature,"湿度为：",humidity,"%"
        Display.Show(show)
        Display.ShowDoublepoint(0)
        time.sleep(3)
        todaytime = time.strftime('%H:%M:%S',time.localtime(time.time()))
        todaystr  = todaytime.split(":");
        show = [int(todaystr[0][0]), int(todaystr[0][1]), int(todaystr[1][0]), int(todaystr[1][1]) ]
        #print "当前时间为：", todaytime
        Display.ShowDoublepoint(1)
        Display.Show(show)        
        time.sleep(1)
    GPIO.cleanup()