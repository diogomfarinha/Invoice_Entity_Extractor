import pytesseract
from pytesseract import Output
from PIL import Image
from PIL import ImageDraw

#Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Diogo\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

#Image to data
ocr = pytesseract.image_to_data('invoice1.png',output_type=Output.DATAFRAME)
ocr = ocr.dropna()
ocr['text'] = ocr['text'].str.strip()
ocr = ocr[ocr['text']!='']
ocr['right']=ocr['left']+ocr['width']
ocr['bottom']=ocr['top']+ocr['height']

#Get boxes
box_type=['block_num']
box_type=['block_num','par_num','line_num','word_num']
left = ocr.groupby(box_type)['left'].min()
right = ocr.groupby(box_type)['right'].max()
top = ocr.groupby(box_type)['top'].min()
bottom = ocr.groupby(box_type)['bottom'].max()
boxes=[(left[i],right[i],top[i],bottom[i]) for i in left.index]

#Show boxes
image = Image.open('invoice1.png')
draw = ImageDraw.Draw(image)
t=int(image.width/200)#Rectangle border thickness. Rough estimation
for box in boxes:
    draw.rectangle([(box[0]-t, box[2]-t), (box[1]+t, box[3]+t)],outline='#2FF2DE',width=t)
image.show()

