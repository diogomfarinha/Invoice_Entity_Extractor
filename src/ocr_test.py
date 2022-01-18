#Local application imports
from ocr import OCR, Text
from entities import ENTITIES_TO_SEARCH

#Invoice path
invoice_path='invoices/invoice1.png'

#Extract text from image
ocr = OCR(invoice_path)

#Show word compounds
ocr.show_text(Text.COMPOUND)

#Find entities in word compounds
results = ocr.search_entities(ENTITIES_TO_SEARCH)
print(*(e.name+': '+results[e.name] for e in ENTITIES_TO_SEARCH),sep='\n')
