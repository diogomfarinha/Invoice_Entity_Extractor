#Local application imports
from ocr import OCR, Text
from entities import ENTITIES_TO_SEARCH

#Invoice path
invoice_path='invoices/invoice1.png'

#Extract text from image
ocr = OCR(invoice_path)

#Get word compounds
ocr.show_text(Text.COMPOUND)
comps=ocr.compounds
comps

#Find entities using compounds
for entity in ENTITIES_TO_SEARCH:
    matches=comps[comps['text'].str.match(entity.regex, case=False)]
    #Search right and bottom of matches
    print(matches['text'],'\n\n')

