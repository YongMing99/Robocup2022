#! /usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2017, Yuki Furuta.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Kei Okada nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


from __future__ import print_function

try:
    input = raw_input
except:
    pass

import rospy, os, sys
import message_filters
from std_msgs.msg import String
from sensor_msgs.msg import Image
from opencv_apps.msg import FaceArrayStamped
from opencv_apps.srv import FaceRecognitionTrain, FaceRecognitionTrainRequest

class FaceRecognitionTrainer(object):
    def __init__(self):
        self.queue_size = rospy.get_param("~queue_size", 100)
        
        self.img_sub = message_filters.Subscriber("image", Image)
        self.face_sub = message_filters.Subscriber("faces", FaceArrayStamped)
        rospy.init_node("face_recognition_trainer")
        rospy.Subscriber('result', String, self.run)
        
        self.req = FaceRecognitionTrainRequest()
        self.label = ""
        self.ok = False

        self.sync = message_filters.TimeSynchronizer([self.img_sub, self.face_sub],
                                                     self.queue_size)
        self.sync.registerCallback(self.callback)
    def callback(self, img, faces):
        if len(faces.faces) <= 0:
            return
        if self.ok:
            faces.faces.sort(key=lambda f: f.face.width * f.face.height)
            self.req.images.append(img)
            self.req.rects.append(faces.faces[0].face)
            self.req.labels.append(self.label)
            self.ok = False
    def run(self, msg):
        print(msg.data)
        rospy.wait_for_service("train")
        train = rospy.ServiceProxy("train", FaceRecognitionTrain)
        if 'name' in msg.data:
            name = msg.data.split("is ")
            print(name[1])
            self.label = name[1]
            while len(self.label) <= 0:
                self.label = name[1]
            print("Please stand at the center of the camera and say cheese: ")

        elif msg.data == 'cheese':
            self.count = 1
            while self.count<=5:
                print("taking picture no",self.count)
                self.count+=1
                rospy.sleep(1)
            print("sending to trainer...")
                
            res = train(self.req)
            if res.ok:
                print("OK. Trained successfully!")
            else:
                print("NG. Error: %s" % res.error)

if __name__ == '__main__':
    try:
        FaceRecognitionTrainer()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("Talkback node terminated.")
