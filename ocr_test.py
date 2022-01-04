#Local application imports
from ocr import OCR, Text
from entities import ENTITIES_TO_SEARCH

#Invoice path
invoice_path='invoices/invoice1.png'

#Extract text from image
ocr = OCR(invoice_path)
ocr.show_text(Text.COMPOUND)
ocr_data=ocr.data

#Find entities using compounds
for entity in ENTITIES_TO_SEARCH:
    matches=ocr_data['text'].str.match(entity.regex)

#matches=ocr['text'].apply(lambda x: bool(re.match(x, ENTITIES_TO_SEARCH[0].regex, re.IGNORECASE)))
#match=ocr[matches]

#line=ocr[(ocr['block_num']==5) & (ocr['par_num']==1) & (ocr['line_num']==1)]
