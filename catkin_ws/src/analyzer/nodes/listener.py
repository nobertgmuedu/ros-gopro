#!/usr/bin/env python
import cv2
import rospy
from std_msgs.msg import Int64
from std_msgs.msg import Float64
from gopro.msg import Status

class Listener:    
    'Init'
    def __init__(self):
        # GoPro video resolutions 
        self.videoResolutions = {'720p SuperView' : (9.0/16.0), '920p' : (3.0/4.0), 'WVGA' : (9.0/16.0)}
        rospy.init_node('Analyzer/Listener', anonymous=True)
        self.initPublish()
        self.facesDetector = FacesDetector(self.analyzePub, 170.0, self.videoResolutions['720p SuperView'])
        self.initSubscribe()
        self.takePicturePub.publish(1)

    'Initialisation of topic subscriptions'
    def initSubscribe(self):
        rospy.Subscriber('/gopro/camera/picture', Image, self.callbackGoProPicture)
        rospy.Subscriber('/gopro/status', Status, self.callbackGoProStatus)

    'Initialisation of topic publications'
    def initPublish(self):
        self.takePicturePub = rospy.Publisher('/gopro/camera/take_picture', Int64, queue_size=10)
        self.horizontalAnglePub = rospy.Publisher('/analyzer/picture/h_angle', Float64, queue_size=10)
        self.horizontalAnglePub = rospy.Publisher('/analyzer/picture/raw', Image, queue_size=10)
        self.vidResPub = rospy.Publisher('/analyzer/picture/vidRes', Float64, queue_size=10)

    'Callback for /gopro/camera/picture topic'
    def callbackGoProPicture(self, data):
        # Get image from GoPro and give it to FacesDetector
        self.facesDetector.image = data
        # Ask new picture
        self.takePicturePub.publish(1)

    'Callback for /gopro/status topic'
    def callbackGoProStatus(self, data):
        cameraSX = data.sx
        if cameraSX :
            # Publish Video Resolution
            if cameraSX.vidres in self.videoResolutions:
                self.horizontalAnglePub.publish(self.videoResolutions[cameraSX.vidres])
            # Publish Horizontal Camera Angle
            self.horizontalAnglePub.publish(float(cameraSX.fov))

    'Launch analysis'
    def start(self):
        rospy.spin()

if __name__ == '__main__':
    listen = Listener()
    listen.start()

