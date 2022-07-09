#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import speech_recognition as sr

def googlesr():
    i = 0
    rospy.init_node('googlesr', anonymous=True)
    pub = rospy.Publisher('result', String, queue_size=10)
    while not rospy.is_shutdown():
        # obtain audio.;//////////////////////////////////////////////////////// from the microphone
        r = sr.Recognizer()
        
        with sr.Microphone() as source:
            print(">>> Say something!")
            #audio = r.listen(source)
            audio = r.record(source, duration=5)
            
        # recognize speech using Google Speech Recognition
        try:
            result = r.recognize_google(audio)
	    pub.publish(result)
            print("SR result: " + result)
	    if result == 'hello' or result == 'hi':
	        rospy.sleep(3)
            elif "I am " in result:
                rospy.sleep(10)
            elif result == "cheese":
                rospy.sleep(3)
        except sr.UnknownValueError:
            print("SR could not understand audio")
	    result = "."
            pub.publish(result)
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        result = "hi"
        #pub.publish(result)

if __name__ == '__main__':
    try:
        googlesr()
    except rospy.ROSInterruptException:
        pass
