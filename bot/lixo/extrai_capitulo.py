# This script creates a json file with from a input PDF file,
# the keys are the chapters title ans the value are the chapter body

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
# Open a PDF document.
fp = open('bot/3.pdf', 'rb')
parser = PDFParser(fp)
document = PDFDocument(parser)
# Get the outlines of the document.
outlines = document.get_outlines()
for (level,title,dest,a,se) in outlines:
    print(f"level:{level}")
    print(f"title:{title}")
    print(f"dest:{dest}")
    print(f"a:{a}")
    print(f"se:{se}")
