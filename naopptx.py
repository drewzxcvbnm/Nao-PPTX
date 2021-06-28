import qi
from preader import PresentationReader

def main(session):
    global tts, atts
    tts = session.service("ALTextToSpeech")
    atts = session.service("ALAnimatedSpeech")
    alife = session.service("ALAutonomousLife")
    motion = session.service("ALMotion")
    asr = session.service("ALSpeechRecognition")
    touch = session.service("ALTouch")
    asr.pause(1)
    path = r"C:\Users\tsi_nao\Desktop\TEXTANNOTATION.pptx"
    pr = PresentationReader()
    pr.readSlides()
    pr.close()


session = qi.Session()
# session.connect("tcp://" + "192.168.253.155" + ":" + "9559")
session.connect("tcp://" + "192.168.252.226" + ":" + "9559")
main(session)
