# Project description

Invoice_Entity_Extractor is an entity extractor for invoices. It uses Python-tesseract
to extract text from images and simple regex matching to find the respective entities.

# Usage

Go to src/ocr_test.py for example usage. 
The main features of this project are the following:

+ Create an OCR object with structured text extracted from an image:
```python
from ocr import OCR

invoice_path='invoices/invoice1.png'

ocr = OCR(invoice_path)
```

+ Visualize the text structure using predefined layers (e.g, blocks, lines, compounds) 
```python
ocr.show_text(Text.BLOCK)
```
![alt text](https://github.com/diogomfarinha/Invoice_Entity_Extractor/blob/master/images/blocks.JPG)

```python
ocr.show_text(Text.COMPOUND)
```
![alt text](https://github.com/diogomfarinha/Invoice_Entity_Extractor/blob/master/images/compounds.JPG)

+ Create and customize entities for extraction
```python      
PO={'name':'PO',
    'regex':r'po(#|number)?'}

INVOICE_NO={'name':'Invoice Number',
            'regex':r'invoice (#|number)'}

INVOICE_DATE={'name':'Invoice Date',
            'regex':r'(invoice )?date'}

DUE_DATE={'name':'Due Date',
            'regex':r'due date'}

TOTAL={'name':'Total',
       'regex':r'total'}
```

+ Extract entities from structured text
```python
results = ocr.search_entities(ENTITIES_TO_SEARCH)
```
```
PO: 2312/2019
Invoice Number: us-001
Invoice Date: 11/02/2019
Due Date: 11/03/2019
Total: $154.06
```

# Installation
### Install Python-tesseract
https://pypi.org/project/pytesseract/

### Install the project requirements
`pip install -r requirements.txt`


