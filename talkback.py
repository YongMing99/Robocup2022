#!/usr/bin/env python

"""
    talkback.py - Version 1.1 2013-12-20
    
    Use the sound_play client to say back what is heard by the pocketsphinx recognizer.
    
"""

import rospy, os, sys
from std_msgs.msg import String
from sound_play.libsoundplay import SoundClient
from gtts import gTTS

class TalkBack:
    def __init__(self, script_path):
        rospy.init_node('talkback')

        rospy.on_shutdown(self.cleanup)
        
        # Create the sound client object
        self.soundhandle = SoundClient()
        
        # Wait a moment to let the client connect to the
        # sound_play server
        rospy.sleep(1)
        
        # Make sure any lingering sound_play processes are stopped.
        self.soundhandle.stopAll()
        
        # Announce that we are ready for input
        #self.soundhandle.playWave('say-beep.wav')
        #rospy.sleep(2)
        #self.soundhandle.say('Ready')
        
        rospy.loginfo("Say one of the navigation commands...")

        # Subscribe to the recognizer output and set the callback function
        rospy.Subscriber('result', String, self.talkback)
        
    def talkback(self, msg):
        soundhandle = SoundClient()
        times = 1
        # Print the recognized words on the screen
        rospy.loginfo(msg.data)
        
        # Speak the recognized words in the selected voice
        if msg.data == 'hello' or msg.data == 'hi':
            text = "Hello. Welcome"
            tts = gTTS(text)
            tts.save("speech.mp3")
            os.system("mpg321 speech.mp3")
            os.remove("speech.mp3")

        elif 'name' in msg.data:
            name = msg.data.split("is ")
            text = "Nice to meet you" + name[1]+ ".My name is tuah bot"
            tts = gTTS(text)
            tts.save("speech.mp3")
            os.system("mpg321 speech.mp3")
            os.remove("speech.mp3")

        rospy.sleep(5)

    def cleanup(self):
        self.soundhandle.stopAll()
        rospy.loginfo("Shutting down talkback node...")

if __name__=="__main__":
    try:
        TalkBack(sys.path[0])
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("Talkback node terminated.")
