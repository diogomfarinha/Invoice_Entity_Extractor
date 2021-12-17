import pytesseract
from pytesseract import Output
from PIL import Image
from PIL import ImageDraw
from entities import ENTITIES_TO_SEARCH
import re
from random import randint

#Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Diogo\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

#Invoice path
invoice_path='invoices/invoice1.png'

#Image to data
ocr = pytesseract.image_to_data(invoice_path,output_type=Output.DATAFRAME)

#Process data
ocr = ocr.dropna()
ocr['text'] = ocr['text'].str.strip()
ocr = ocr[ocr['text']!='']
ocr['right']=ocr['left']+ocr['width']
ocr['bottom']=ocr['top']+ocr['height']
ocr = ocr.drop(['page_num','conf','level','width','height'],axis=1)

#Generate compound numbers
def generate_compounds(df):
    df['compound_num']=0
    blocks=set(df['block_num'])
    for block in blocks:
        filtered_block=df[df['block_num']==block]
        paragraphs=set(filtered_block['par_num'])
        for par in paragraphs:
            filtered_par=filtered_block[filtered_block['par_num']==par]
            lines=set(filtered_par['line_num'])
            for line in lines:
                filtered_line=filtered_par[filtered_par['line_num']==line]
                if len(filtered_line):
                    word_nums=list(filtered_line['word_num'])
                    word_nums.sort()
                    compound_num=1
                    right=filtered_line[filtered_line['word_num']==word_nums[0]]['left'].iloc[0]
                    for num in word_nums:
                        filtered_word=filtered_line[filtered_line['word_num']==num]
                        if filtered_word['left'].iloc[0]-right>30:
                            compound_num+=1
                        df.at[filtered_word.index[0],'compound_num']=compound_num
                        right=filtered_word['right'].iloc[0]
    return df
ocr = generate_compounds(ocr)
ocr = ocr[['block_num','par_num','line_num','compound_num','word_num','left','right','top','bottom','text']]

                 if filtered_line:
                
                 compound_num=1
                 for row in df.iterrows():
#Get boxes
box_type=['block_num']
box_type=['block_num','par_num','line_num','word_num']
box_type=['block_num','par_num','line_num','compound_num']
left = ocr.groupby(box_type)['left'].min()
right = ocr.groupby(box_type)['right'].max()
top = ocr.groupby(box_type)['top'].min()
bottom = ocr.groupby(box_type)['bottom'].max()
boxes=[(left[i],right[i],top[i],bottom[i]) for i in left.index]

#Show boxes
image = Image.open(invoice_path)
draw = ImageDraw.Draw(image)
t=int(image.width/200)#Rectangle border thickness. Rough estimation
for box in boxes:
    #draw.rectangle([(box[0]-t, box[2]-t), (box[1]+t, box[3]+t)],outline='#2FF2DE',width=t)
    draw.rectangle([(box[0]-t, box[2]-t), (box[1]+t, box[3]+t)],outline=(randint(0,256),randint(0,256),randint(0,256)),width=t)
image.show()

#Find entities
for entity in ENTITIES_TO_SEARCH:
    z=left = ocr.groupby(box_type)['text']
    matches=ocr['text'].str.match(entity.regex)

matches=ocr['text'].apply(lambda x: bool(re.match(x, ENTITIES_TO_SEARCH[0].regex, re.IGNORECASE)))
match=ocr[matches]

line=ocr[(ocr['block_num']==5) & (ocr['par_num']==1) & (ocr['line_num']==1)]
