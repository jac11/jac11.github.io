#!/usr/bin/env python


import json
import sys
import os
import glob
import zipfile
import pandas as pd
import re
import argparse
from io import StringIO

class Data_Read:
    def __init__(self) :
        self.Control_input()
        self.convert_excel_to_text(excel_path=self.args.Path, TextPath='Convert_excl.csv', delimiter=',')
        self.file_json_at_one(self.args.jpath)
        self.json_to_text(json_file='all_kitchen_inventory.json')
        self.compuer_all_result(NewUpdate='Convert_excl.csv',Data_Run='all_kitchen_inventory.csv')
    def convert_excel_to_text(self,excel_path,TextPath, delimiter):
        try:
            df = pd.read_excel(excel_path , skiprows=1, header=None)
            df = df.iloc[:, 1:] 
            df.to_csv(TextPath, sep=delimiter, index=False)
            
        except Exception as e:
            print(f"An error occurred: {e}")

    def file_json_at_one(self,file_Path):
    
        combined_data = {}
        for file_name in os.listdir(file_Path):
            if file_name == 'all_kitchen_inventory.json':
                continue  
            category = file_name.replace('.json', '')
            with open(f'{file_Path}/{file_name}', 'r', encoding='utf-8') as f:
                data = json.load(f)
                combined_data[category] = data
        with open('all_kitchen_inventory.json', 'w', encoding='utf-8') as f:
            json.dump(combined_data, f, ensure_ascii=False, indent=2)
        
    def json_to_text(self,json_file):

        with open(json_file,'r',encoding='utf-8') as file:
           data = json.load(file)
        df = pd.DataFrame([{**item, 'category': cat} for cat, items in data.items() for item in items])
        df.to_csv('all_kitchen_inventory.csv', index=False, encoding='utf-8-sig')

    def compuer_all_result(self, NewUpdate, Data_Run):
        # Read files
        with open(NewUpdate, 'r', encoding='utf-8') as f:
            readupdate = f.read()
        
        with open(Data_Run, 'r', encoding='utf-8') as f:
            current_data = f.read()
        
        # Extract codes using regex (5-6 digits)
        pattern = r'\b(\d{5,6})\b'
        
        convert_codes = set(re.findall(pattern, readupdate))
        kitchen_codes = set(re.findall(pattern, current_data))
        
        # Find codes only in Convert that are not in Kitchen (6 digits only)
        code_list = [C for C in convert_codes if C not in kitchen_codes and len(C) >= 6]

        print()
        print(f"📊 Total codes in Convert: {len(convert_codes)}")
        print(f"📊 Total codes in Kitchen: {len(kitchen_codes)}")
        print(f"📊 Codes only in Convert: {len(code_list)}")
        print("=" * 60)
        line_list =[]
        # Print the full lines from NewUpdate for each missing code
        for code in code_list:
            # Find the line containing the code
            lines = readupdate.split('\n')
            for line in lines:
                if code in line:
                    line_list.append(line)
                    print(line)
                    break
        
        # Save results to file
        with open('missing_codes.txt', 'w', encoding='utf-8') as f:
               f.write(str("\n".join(line_list)))
        
        print("\n📁 Missing codes saved to: missing_codes.txt")
        
        return code_list
               

    def Control_input(self):

        parser = argparse.ArgumentParser(description="Usage: [OPtion] [arguments] [ -w ] [arguments]")      
        parser.add_argument("-P","--Path" , metavar='' , action=None ,required=True,help ="Data read Updata") 
        parser.add_argument("-j","--jpath" , metavar='' , action=None ,help ="data Json read" ) 
        self.args = parser.parse_args()     
        if len(sys.argv)!=1 :
              pass
        else:
            parser.print_help()         
            exit()                

if __name__=='__main__':
    Data_Read()