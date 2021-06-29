import qi
from services import asr, alife
import preader
import sys
import pythoncom

def main():
    asr.pause(1)
    alife.setState("safeguard")
    path = r"C:\Users\tsi_nao\Desktop\Nao-PPTX\naoPPTX.pptx"
    pr = preader.PresentationReader(path)
    pr.readSlides()
    pr.close()
    sys.exit(0)



main()
