import win32com.client as win32
from web.webinterface import WebInterface
from pptx import Presentation as PPTXPresentation


class Presentation:

    def __init__(self, path):
        name = path.split('\\')[-1].split('.')[0]
        self.presentation_id = WebInterface.create_presentation(name)
        self.path = path
        self.com_ppoint = win32.gencache.EnsureDispatch('Powerpoint.Application')
        self.com_presentation = self.com_ppoint.Presentations.Open(path)
        self.com_slide_show = self.com_presentation.SlideShowSettings.Run()
        self.pptx_presentation = PPTXPresentation(self.path)
        self.slides = self.pptx_presentation.slides
        self.surveys = {}

    def __del__(self):
        self.com_presentation.Close()
        self.com_ppoint.Quit()
        # TODO: delete presentation and all surveys with WebInterface
