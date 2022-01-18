#Standard library imports
from enum import Enum, unique
from random import randint
from PIL import Image, ImageDraw

#Third party imports
import pytesseract
import pandas as pd

#Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Diogo\AppData\Local\Programs\Tesseract-OCR\tesseract.exe' #TODO: Change to a config file


@unique
class Text(Enum):
    BLOCK = 1
    PARAGRAPH = 2
    LINE = 3
    COMPOUND = 4
    WORD = 5
    


class OCR:
    
    def __init__(self,image_path): #TODO: Allow PDF path and convert it to images
        self.image_path=image_path
        self.data = self.extract_data_from_image()
        self.generate_word_compound_numbers()
        self.compounds = self.create_compounds_table()
        
    
    #Use Tesseract to OCR the image
    def extract_data_from_image(self):
        #Image to data
        data = pytesseract.image_to_data(self.image_path,output_type=pytesseract.Output.DATAFRAME)

        #Process data
        data = data.dropna()
        data['text'] = data['text'].str.strip()
        data = data[data['text']!='']
        data['right']=data['left']+data['width']
        data['bottom']=data['top']+data['height']
        data = data.drop(['page_num','conf','level','width','height'],axis=1)
        
        return data
    
    #Generate word compounds (small chunks of text)
    def generate_word_compound_numbers(self, pixel_limit=30):
        #Iterate through all blocks, paragraphs and lines to create word compounds
        self.data['compound_num']=0
        blocks=set(self.data['block_num'])
        for block in blocks:
            filtered_block=self.data[self.data['block_num']==block]
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
                            if filtered_word['left'].iloc[0]-right>pixel_limit:
                                compound_num+=1
                            self.data.at[filtered_word.index[0],'compound_num']=compound_num
                            right=filtered_word['right'].iloc[0]
       
    #Filter data dataframe
    def filter_data(self,text_enum,return_text_column=False):
        #Get box filter
        if text_enum==Text.BLOCK:
            box_filter=['block_num']    
        elif text_enum==Text.PARAGRAPH:
            box_filter=['block_num','par_num']
        elif text_enum==Text.LINE:
            box_filter=['block_num','par_num','line_num']   
        elif text_enum==Text.COMPOUND:
            box_filter=['block_num','par_num','line_num','compound_num']    
        elif text_enum==Text.WORD:
            box_filter=['block_num','par_num','line_num','compound_num','word_num']
        else:
            raise ValueError('Text enum was not used. ')
         
        #Get boxes boundaries
        box_data = {}
        box_data['left'] = list(self.data.groupby(box_filter)['left'].min())
        box_data['right'] = list(self.data.groupby(box_filter)['right'].max())
        box_data['top'] = list(self.data.groupby(box_filter)['top'].min())
        box_data['bottom'] = list(self.data.groupby(box_filter)['bottom'].max())
        
        if return_text_column:
            box_data['text'] = list(self.data.groupby(['block_num','par_num','line_num','compound_num']).agg({'text': ' '.join})['text'])
        
        return box_data  
      
    #Create compounds dataframe
    def create_compounds_table(self):
        box_data = self.filter_data(Text.COMPOUND,return_text_column=True)
        return pd.DataFrame(box_data)
        
    
    #Show text boxes
    def show_text(self,text):
        #Get box boundaries
        box_data  = self.filter_data(text)
        boxes=[(box_data['left'][i],box_data['right'][i],box_data['top'][i],box_data['bottom'][i]) for i in range(len(box_data['left']))]

        #Show boxes
        image = Image.open(self.image_path)
        draw = ImageDraw.Draw(image)
        t=int(image.width/200)#Rectangle border thickness. Rough estimation
        for box in boxes:
            draw.rectangle([(box[0]-t, box[2]-t), (box[1]+t, box[3]+t)],outline=(randint(0,256),randint(0,256),randint(0,256)),width=t)
        image.show()
                
    #Search entities in word compounds
    def search_entities(self,entities):
        results = {}
        for entity in entities:
            #Find regex matches
            matches = self.compounds[self.compounds['text'].str.match(entity.regex, case=False)]
            if len(matches)>0:
                matches = matches.iloc[0] #TODO: Search all the matches, not just the 1st one
                
                #Find value to the right of the regex match
                pixels=15
                nearby = self.compounds[(abs(self.compounds['top']-matches['top'])<pixels) & (abs(self.compounds['bottom']-matches['bottom'])<pixels) & (self.compounds['left']>matches['right'])]
                if len(nearby)>0:
                    value = nearby.iloc[0]['text']  
                else: #TODO: Also search under the match and not just to the right
                    value = 'NO VALUE FOUND'
            else:
                value = 'NO MATCH FOUND'
            results[entity.name] = value
        return results

