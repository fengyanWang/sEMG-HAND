#coding:UTF-8
#
import open_myo as myo
from open_myo import Pose

from handCtrl import myHandCtrl

#通过myo自身分类器的分类结果，来控制灵巧手
class handCtr(object):

    def __init__(self):

        self.myo_mac_addr = myo.get_myo()  #获取当前的myo的mac地址
        self.myo_device = myo.Device() 

        self.actionCout = 0  #实现灯闪的效果

        # self.mHandCtrl = myHandCtrl() 

        self.pose = 0  #分类的动作结果
    
    #控制开始程序    
    def start(self):

        print("MAC address: %s" % self.myo_mac_addr)
        self.myo_device.services.sleep_mode(1) # never sleep
        self.myo_device.services.set_leds([128, 128, 255], [128, 128, 255])  # purple logo and bar LEDs)
        self.myo_device.services.vibrate(1) # short vibration
        self.fw = self.myo_device.services.firmware() #获取myo的固件版本
        print("Firmware version: %d.%d.%d.%d" % (self.fw[0], self.fw[1], self.fw[2], self.fw[3]))
        self.batt = self.myo_device.services.battery() #获取myo的电量
        print("Battery level: %d" % self.batt)
        self.myo_device.services.classifier_notifications() #告知服务器需要myo的分类结果
        self.myo_device.services.set_mode(myo.EmgMode.OFF, myo.ImuMode.OFF, myo.ClassifierMode.ON) #设置myo的模式为分了模式
        self.myo_device.add_sync_event_handler(self.process_sync) #进行同步操作
        self.myo_device.add_classifier_event_hanlder(self.process_classifier) #添加分类函数

    #同步程序
    #arm：myo佩戴在哪个手臂上
    #x_direction:myo的佩戴方向
    def process_sync(self , arm, x_direction):
        print(arm, x_direction)

    #获取myo的电量
    #batt:myo电量，是一个0-100的数字
    def process_battery(self,batt):
        print("Battery level: %d" % batt)
    #控制myo上的led灯变颜色
    def led_emg(self ):
        if(self.actionCout %2 == 0):
            self.myo_device.services.set_leds([255, 0, 0], [128, 128, 255]) #log灯的颜色发生改变，bar的颜色不变
        else:
            self.myo_device.services.set_leds([128, 128, 255], [128, 128, 255])
        if self.actionCout == 100:
            self.actionCout = 0
    #分类函数
    #pose:分类的结果，为枚举类型
    def process_classifier(self,pose):
        self.actionCout += 1
        self.led_emg()
        self.pose = pose
        #根据分类结果，调相应的操作函数
        if(self.pose==Pose.FIST):
            print("im in!!!")
            self.fistAction()
        
        if(self.pose==Pose.REST):
            self.restAction()
        
        if(self.pose==Pose.WAVE_OUT):
            self.waveOutAction()

        if(self.pose==Pose.WAVE_IN):
            self.waveInAction()

        if(self.pose==Pose.DOUBLE_TAP):
            self.doubleTapAction()

        if(self.pose==Pose.FINGERS_SPREAD):
            self.fingersSpreadAction()
        
     #握拳对应的操作函数  
    def fistAction(self):
        print ("im fist!!!!")
        self.mHandCtrl.handMovementCtrol(movementType = "setHandNormalizationAngle" , parameterList = [0,0,0,0,0,600])
        


     #静息对应的操作函数 
    def restAction(self):
        
        print ("im REST!!!!")
        self.mHandCtrl.handMovementCtrol(movementType = "setHandNormalizationAngle" , parameterList = [750,750,750,750,750,600])
        
        
    #手掌外翻对应的操作函数    
    def waveOutAction(self):
        #剪刀
        print ("im WAVE_OUT!!!!")
        self.mHandCtrl.handMovementCtrol(movementType = "setHandNormalizationAngle" , parameterList = [0,0,1000,1000,0,600])
       
    #手掌内翻对应的操作函数
    def waveInAction(self):
        #ok手势
        print ("im WAVE_IN!!!!")
        self.mHandCtrl.handMovementCtrol(movementType = "setHandNormalizationAngle" , parameterList = [1000,1000,1000,0,0,600])
     
    #捏合对应的操作函数    
    def doubleTapAction(self):
        
        print ("im DOUBLE_TAP!!!!")
        self.mHandCtrl.handMovementCtrol(movementType = "setHandTargetPosition" , parameterList = [1906,1431,511,1998,494,1999])

    #伸掌对应的操作函数
    def fingersSpreadAction(self):

        print ("im FINGERS_SPREAD!!!!")
        self.mHandCtrl.handMovementCtrol(movementType = "setHandNormalizationAngle" , parameterList = [1000,1000,1000,1000,1000,0])

    #运行程序
    def run(self):
        while True:
            if self.myo_device.services.waitForNotifications(1):
                continue    
            print("Waiting")

if __name__ == "__main__":

    myHandCtrl = handCtr()
    myHandCtrl.start()
    try:
        myHandCtrl.run()
    except KeyboardInterrupt:
        pass


