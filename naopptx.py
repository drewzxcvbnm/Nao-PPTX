import qi
from services import asr
import preader

def main():
    asr.pause(1)
    path = r"C:\Users\tsi_nao\Desktop\TEXTANNOTATION.pptx"
    pr = preader.PresentationReader(path)
    pr.readSlides()
    pr.close()


main()
