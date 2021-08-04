import qi
from services import asr, alife, posture, args
import preader
import sys
import pythoncom

if __name__ == '__main__':
    asr.pause(1)
    alife.setState("safeguard")
    path = args.pr
    pr = preader.PresentationReader(path)
    pr.read_slides()
    pr.close()
    sys.exit(0)
