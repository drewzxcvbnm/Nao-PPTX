import qi

session = qi.Session()
session.connect("tcp://" + "192.168.253.155" + ":" + "9559")
# session.connect("tcp://" + "192.168.252.226" + ":" + "9559")
# session.connect("tcp://" + "192.168.253.68" + ":" + "9559")
#global tts, atts, touch
tts = session.service("ALTextToSpeech")
atts = session.service("ALAnimatedSpeech")
alife = session.service("ALAutonomousLife")
motion = session.service("ALMotion")
asr = session.service("ALSpeechRecognition")
touch = session.service("ALTouch")
mem = session.service("ALMemory")
posture = session.service( "ALRobotPosture" )


