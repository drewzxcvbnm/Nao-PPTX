# flake8: noqa E402
import sys

sys.coinit_flags = 0
import preader
from pynput import keyboard
from threading import Thread
from general import kill_process
from presentation import Presentation
from services import asr, alife, tts
from args import ARGS

kill_process("POWERPNT.exe")


def app_exit():
    presentation.__del__()
    reading_service.__del__()
    tts.stopAll()
    alife.setState("interactive")
    kill_process("POWERPNT.exe")
    sys.exit(0)


def on_press(key):
    if key == keyboard.Key.esc:
        app_exit()


listener = keyboard.Listener(on_press=lambda k: Thread(target=lambda: on_press(k)).start())
path = ARGS.pr
presentation = Presentation(path)
reading_service = preader.PresentationReadingService()

if __name__ == '__main__':
    listener.start()  # start to listen on a separate thread
    asr.pause(1)
    alife.setState("safeguard")
    reading_service.read_presentation(presentation)
    app_exit()
