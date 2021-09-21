# coding=utf-8
import qi
import argparse

EVENT_ARG_DELIMITER = "○"

parser = argparse.ArgumentParser()
parser.add_argument("--ip", help="IP address for NAO", required=True)
parser.add_argument("--pr", help="Path of presentation", default="naoPPTX.pptx")

args = parser.parse_args()
session = qi.Session()
session.connect("tcp://" + args.ip + ":" + "9559")

tts = session.service("ALTextToSpeech")
atts = session.service("ALAnimatedSpeech")
alife = session.service("ALAutonomousLife")
motion = session.service("ALMotion")
asr = session.service("ALSpeechRecognition")
touch = session.service("ALTouch")
mem = session.service("ALMemory")
posture = session.service("ALRobotPosture")
behman = session.service("ALBehaviorManager")
