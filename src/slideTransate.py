
class NextTagParser:

    def parse(self, slideText):
        i = 0
        tag_start_i = -1
        tag_end_i = -1
        while i < len(slideText):
            c = slideText[i]
            if c == '\\':
                i+=2
                continue
            if c == '<':
                tag_start_i = i
                continue
            if c == '>':
                tag_end_i = i
                continue
            if tag_start_i != -1 and tag_end_i != -1:
                tag_start_i = -1
                tag_end_i = -1
                
            i+=1




class SlideTranslationSystem:

    parsers = [NextTagParser()]

    @staticmethod
    def translate(slideText):
        for parser in SlideTranslationSystem.parsers:
            slideText = parser.parse(slideText)
        return slideText 

