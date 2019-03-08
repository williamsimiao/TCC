# https://github.com/wbsoft/python-poppler-qt5
import popplerqt5
import sys
import os
input_filename = sys.argv[1]

d = popplerqt4.Poppler.Document.load(input_filename)
it = document.newFontIterator()
while it.hasNext():
    fonts = it.next()  # list of FontInfo objects
    print(fonts)