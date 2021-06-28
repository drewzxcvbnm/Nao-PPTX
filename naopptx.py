import qi
from services import asr, alife
import preader

def main():
    asr.pause(1)
    alife.setState("safeguard")
    path = r"C:\Users\tsi_nao\Desktop\Nao-PPTX\naoPPTX.pptx"
    pr = preader.PresentationReader(path)
    pr.readSlides()
    pr.close()


main()
