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

#Find entities using compounds
for entity in ENTITIES_TO_SEARCH:
    matches = comps[comps['text'].str.match(entity.regex, case=False)].iloc[0]
    pixels=15
    nearby = comps[(abs(comps['top']-matches['top'])<pixels) & (abs(comps['bottom']-matches['bottom'])<pixels) & (comps['left']>matches['right'])]
    nearby = nearby.iloc[0]
    #Search right and bottom of matches
    print(matches['text'], nearby['text'],'\n\n')

