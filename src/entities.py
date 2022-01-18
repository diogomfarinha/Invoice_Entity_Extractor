#Main entity class
class Entity:
     
    def __init__(self,**kwargs):
        self.__dict__.update(kwargs)


#Entities configuration        
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

#Entities to search
ENTITIES_TO_SEARCH=[Entity(**PO),Entity(**INVOICE_NO),Entity(**INVOICE_DATE),Entity(**DUE_DATE),Entity(**TOTAL)]