from aip import AipFace
from picamera import PiCamera
import urllib.request
import RPi.GPIO as GPIO
import base64
import time
import os
import shutil

APP_ID = '24071959'
API_KEY = 'n3OKBNugZCta6EtSK8amY300'
SECRET_KEY ='w7u45GDKnxAWWHZ3hq9xhiPX1Wu7wuPn'
client = AipFace(APP_ID, API_KEY, SECRET_KEY)
IMAGE_TYPE='BASE64'
camera = PiCamera()
GROUP = 'zcy_01'

def getimage():
    camera.resolution = (1024,768)
    camera.start_preview()          
    time.sleep(2)
    camera.capture('faceimage.jpg')
    time.sleep(2)

def transimage():
    f = open('faceimage.jpg','rb')
    img = base64.b64encode(f.read())
    return img

def go_api(image):
    result = client.search(str(image, 'utf-8'), IMAGE_TYPE, GROUP); 
    if result['error_msg'] == 'SUCCESS':                         
        name = result['result']['user_list'][0]['user_id']         
        score = result['result']['user_list'][0]['score']        
        
        curren_time = time.localtime(time.time())      
        y = curren_time.tm_year
        m = curren_time.tm_mon
        d = curren_time.tm_mday
        h = curren_time.tm_hour
        mi = curren_time.tm_min
        s = curren_time.tm_sec
        
        portfolio = str(y) + "_" + str(m) + "_" + str(d)  
        picname = str(h) + "_" + str(mi) + "_" + str(s)   
      
        if score > 80:
            if name == 'Kiro' or name == 'Yu_Jin':
                time.sleep(5)
        else:
            name = 'Unknown'
            path = "/home/pi/share_files/AIFace/Strangers/" + portfolio
            if not(os.path.exists(path)):
                os.makedirs(path)
            shutil.copyfile("faceimage.jpg",path + "/" + picname + ".jpg")
            return 0
        
        f = open('/home/pi/share_files/AIFace/Login.txt','a')
        f.write("Person: " + name + "     " + "Time:" + str(time.asctime(curren_time)) + '\n')
        f.close()
        return 1
    elif result['error_msg'] == 'pic not has face':
        # print('检测不到人脸')
        time.sleep(5)
        return 0
    else:
        # print(result['error_code']+' ' + result['error_code'])
        return 0

if __name__ == '__main__':
    while True:
        print('准备')
        if True:
            getimage()            
            img = transimage()    
            res = go_api(img)     
        if(res == 1):            
            print("开门")
        else:
            print("关门")
        print('稍等进入下一个')
        time.sleep(5)