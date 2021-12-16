#Main entity class
class Entity:
     
    def __init__(self,**kwargs):
        self.__dict__.update(kwargs)


#Entities configuration        
PO={'name':'PO',
    'regex':r'po(#|number)?',
    'colour':'#00B1EB'}

INVOICE_NO={'name':'Invoice Number',
            'regex':r'invoice (#|number)',
            'colour':'#00B1EB'}

INVOICE_DATE={'name':'Invoice Date',
            'regex':r'invoice date',
            'colour':'#00B1EB'}

DUE_DATE={'name':'Due Date',
            'regex':r'due date',
            'colour':'#00B1EB'}

TOTAL={'name':'Total',
       'regex':r'total',
       'colour':'#00B1EB'}

#Entities to search
ENTITIES_TO_SEARCH=[Entity(**PO),Entity(**INVOICE_NO),Entity(**INVOICE_DATE),Entity(**DUE_DATE),Entity(**TOTAL)]