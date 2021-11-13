# coding=utf-8
import qi
from args import ARGS

session = qi.Session()
session.connect("tcp://" + ARGS.ip + ":" + "9559")

tts = session.service("ALTextToSpeech")
atts = session.service("ALAnimatedSpeech")
alife = session.service("ALAutonomousLife")
motion = session.service("ALMotion")
asr = session.service("ALSpeechRecognition")
touch = session.service("ALTouch")
mem = session.service("ALMemory")
posture = session.service("ALRobotPosture")
behman = session.service("ALBehaviorManager")
