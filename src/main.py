from services import asr, alife, args
import preader
import sys
from presentation import Presentation

if __name__ == '__main__':
    asr.pause(1)
    alife.setState("safeguard")
    path = args.pr
    presentation = Presentation(path)
    reading_service = preader.PresentationReadingService()
    reading_service.read_presentation(presentation)
    presentation.__del__()
    reading_service.__del__()
    sys.exit(0)
