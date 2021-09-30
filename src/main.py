import qi
from services import asr, alife, posture, args
import preader
import sys
from presentation import Presentation
import pythoncom

if __name__ == '__main__':
    asr.pause(1)
    alife.setState("safeguard")
    path = args.pr
    presentation = Presentation(path)
    reading_service = preader.PresentationReadingService()
    reading_service.read_presentation(presentation)
    sys.exit(0)
