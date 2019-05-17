# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 12:01:40 2019

@author: Ingo Schönwandt
"""
#==============================================================================
# packages
#==============================================================================
import pandas as pd
import numpy as np
import os
import re

#==============================================================================
# DIRECTORIES
#==============================================================================

# master df file path
dir_masterdf_output = './data/masterdf.csv'

# EP-online "Voorlopige_labels_okt2018" (assumed energy labels)
# URL: https://www.rvo.nl/onderwerpen/duurzaam-ondernemen/gebouwen/hulpmiddelen-tools-en-inspiratie-gebouwen/ep-online
dir_hstock = './data/labels_preliminary2018'

# EP-online "geregistreerde labels woningbouw per 01012019" (actual recordings)
# URL: https://www.rvo.nl/onderwerpen/duurzaam-ondernemen/gebouwen/hulpmiddelen-tools-en-inspiratie-gebouwen/ep-online
dir_actual_labels2019 = './data/labels_actual2019'

# Buurt/Wijk/Gemeente names 2018
# URL: https://www.cbs.nl/nl-nl/maatwerk/2018/36/buurt-wijk-en-gemeente-2018-voor-postcode-huisnummer
# from 01.08.2018 (BAG)
dir_GWBcodes = './data/GWB_names_2018/pc6hnr20180801_gwb-vs2.csv'
dir_neighbourhoodnames = './data/GWB_names_2018/buurtnaam2018.csv'
dir_districtnames = './data/GWB_names_2018/wijknaam2018.csv'
dir_municipalitynames = './data/GWB_names_2018/gemeentenaam2018.csv'

# BAG data
dir_bag = './data/bagadres-full.csv'

#==============================================================================
# Functions
#==============================================================================

def import_xls_csv (input_path,output_df,input_type='csv', output_type='csv',
                    sheet_names=None,output_path=None):
    '''enter:
        input_path: input excel file or input path to csv-collection folder,
        output_path: to indicate output location,
        input_type: 'csv' or 'xls', 
        output_type: 'csv' or 'xls',
        output_df: to indicate output-df,
        sheet_names: if input_type=xls --> list of names or numbers of sheets in excel that shall be combined
        output_path: define path for output file
    '''
    #print(output_df)
    df_tmp = []
    if input_type == 'xls':
        for sheet in sheet_names:
            data_tmp = pd.read_excel(input_path,sheet_name = sheet, skiprows=1)
            df_tmp.append(data_tmp)
            print(sheet,' added')
    elif input_type == 'csv':
        for name in os.listdir(input_path):
            data_tmp = pd.read_csv(input_path + '/' + name,sep=';')
            df_tmp.append(data_tmp)
            print(name,' added')
    else:
        print('select xls or csv input_type')
    
    output_df = pd.concat(df_tmp, ignore_index=True)
    
    if output_path != None:
        if output_type=='xls':
            output_df.to_excel(output_path,index=False,header=None)
        elif output_type == 'csv':
            output_df.to_csv(output_path,sep=';', index=False)
    else:
        print('no output file defined')
    return output_df
        

def get_housenum(df):
    '''
    For cleaning the charging station data.
    Extracts the house numbers from the 'Street Address'.
    Merges 'Zipcode' and 'House No' into 'Address'
    '''
    df['Street Address'] = df['Street Address'].astype(str)
    df['House No']=np.nan
    df['Address']=np.nan
    for row in df.index:
        cell = df.loc[row,'Street Address'].split()
        count = 1
        a = re.search('A[0-9]{1,2}',evdf.loc[row,'Street Address'])
        b = re.search('[B-Z]{1}[0-9]{1,4}',evdf.loc[row,'Street Address'])
        c = re.search('to[0-9]{1,4}',evdf.loc[row,'Street Address'])
        d = re.search('nabij[0-9]{1,4}',evdf.loc[row,'Street Address'])
        e = re.search('[0-9]{1,3}\s[A-Z]{1}',evdf.loc[row,'Street Address'])
        if df.loc[row,'Street Address'][4:].replace(' ','').isalpha():
            df.loc[row,'House No'] = cell[-1].lower()
        elif a != None:
            df.loc[row,'House No'] = df.loc[row,'Street Address']
        elif b != None:
            df.loc[row,'House No'] = np.nan
        elif c != None:
            df.loc[row,'House No'] = re.search('[0-9]{1,4}',evdf.loc[row,'Street Address']).group(0)
        elif d != None:
            df.loc[row,'House No'] = re.search('[0-9]{1,4}',evdf.loc[row,'Street Address']).group(0)
        elif e != None:
            df.loc[row,'House No'] = re.search('[0-9]{1,3}\s[A-Z]{1}',evdf.loc[row,'Street Address']).group(0)
        elif df.loc[row,'Street Address'] == 'nan':
            df.loc[row,'House No'] = np.nan
        elif count <= range(len(cell))[1]:
            for element in range(len(cell)):
                if cell[count][0].isnumeric():
                    df.loc[row,'House No'] = cell[count].upper()
                    break
                else:
                    count += 1
        else:
            problem_cell = df.loc[row,'Street Address']
            print('No house number could be extracted from',problem_cell,
                  'in row:',row,' of the data frame.')
    print('"House No" filled for all rows')
                
    df.loc[:,'Address'] = df['Zipcode']+'_'+df['House No'].map(str)
    df = df.drop(columns=['Zipcode','House No'])
    print('["Address"] created and ["Zipcode", "House No"] dropped')
    print('Housenumbers extracted from Street Address.')

def clean_subline_seps(df):
    '''
    CSV files containing quotations that contain separators may cause problems on import.
    The lines will be extracted, repaired, and returned into place. 
    However, they will be put back into the first cell of their row. This will required additional, manual cleaning.
    However, this time an easy find/replace all is possible in notepad.
    '''
    df['id'] = df['id'].astype(str)
    line_index=[]
    for line in df.loc[df['id'].str.contains('"'),:].index:
        #print(line)
        line_index.append(line)
        total = len(list(df.loc[line,'id']))
        flag1 = df.loc[line,'id'].index('"')
        flag2 = total-list(reversed(df.loc[line,'id'])).index('"')
        string = re.sub(r'[^\w\s]','',df.loc[line,'id'][flag1:flag2])
        df.loc[line,'id'] = df.loc[line,'id'][:flag1]+string+df.loc[line,'id'][flag2:]
    return df

def extract_zip_from_address(df):
    for i in df.index:
        print(i)
        df['Street Address'] = df['Street Address'].astype(str)
        a = re.search('[0-9]{4}[A-Z]{2}',df.loc[i,'Street Address'])
        b = re.search('[0-9]{4}\s[A-Z]{2}',df.loc[i,'Street Address'])
        if a != None:
            df.loc[i,'Zipcode'] = a.group(0)
            df.loc[i,'Street Address'] = df.loc[i,'Street Address'].replace(
                df.loc[i,'Zipcode'],"")
        elif b != None:
            df.loc[i,'Zipcode'] = b.group(0)
            df.loc[i,'Street Address'] = df.loc[i,'Street Address'].replace(
                df.loc[i,'Zipcode'],"")
        else:
            continue
    print('Zipcode was extracted from Address-cells and added to Zipcode cells.')
    return df

#==============================================================================
# Data import
#==============================================================================

# constructing the masterdf
masterdf = pd.DataFrame()
masterdf = import_xls_csv(dir_hstock,masterdf,output_path=None)#dir_masterdf_output)

# Buurt/Wijk/Gemeente names 2018
GWBcodes = pd.read_csv(dir_GWBcodes ,sep=';', encoding='UTF-8')
print('GWBcodes loaded')
Bnames = pd.read_csv(dir_neighbourhoodnames ,sep=';', encoding='Latin-1')
print('Bnames loaded')
Wnames = pd.read_csv(dir_districtnames ,sep=';', encoding='Latin-1')
print('Wnames loaded')
Gnames = pd.read_csv(dir_municipalitynames ,sep=';', encoding='Latin-1')
print('Gnames loaded')

#==============================================================================
# Data cleaning and preparation
#==============================================================================

#renaming columns masterdf
masterdf = masterdf.rename(columns={
        'POSTCODE_WONING':'Zipcode', 'HUISNUMMER_WONING':'House No', 
        'HUISNUMMER_TOEV_WONING':'Appartment No','BOUWJAAR_WONING':'Construction Year', 
        'WONING_TYPE':'Housing Type', 'VOORL_BEREKEND':'Preliminary Evaluation'})
print('masterdf cols renamed')
    
#renaming columns GWBcodes
GWBcodes = GWBcodes.rename(columns={
        'PC6':'Zipcode', 'Huisnummer':'House No', 'Buurt2018':'Neighbourhood Code',
        'Wijk2018':'District Code', 'Gemeente2018':'Municipality Code'})
print('GWBcodes cols renamed')

#renaming columns Gnames
Gnames = Gnames.rename(columns={
        'GWBcode8':'Municipality Code', 'GWBlabel':'Municipality Name'})
print('Gnames cols renamed')
#renaming columns Wnames
Wnames = Wnames.rename(columns={
        'GWBcode8':'District Code', 'GWBlabel':'District Name'})
print('Wnames cols renamed')
#renaming columns Bnames
Bnames = Bnames.rename(columns={
        'GWBcode8':'Neighbourhood Code', 'GWBlabel':'Neighbourhood Name'})
print('Bnames cols renamed')   

#test completeness of G/W/B indices
Gcodes_missing = set(Gnames.loc[:,'Municipality Code']).symmetric_difference(GWBcodes.loc[:,'Municipality Code'])
print(len(Gcodes_missing),' Gcodes could not be matched')
Wcodes_missing = set(Wnames.loc[:,'District Code']).symmetric_difference(GWBcodes.loc[:,'District Code'])
print(len(Wcodes_missing),' Wcodes could not be matched')
Bcodes_missing = set(Bnames.loc[:,'Neighbourhood Code']).symmetric_difference(GWBcodes.loc[:,'Neighbourhood Code'])
print(len(Bcodes_missing),' Bcodes could not be matched')

#test match of GWBcodes.Zipcode and masterdf.Zipcode
mismatchZip1 = set(masterdf.loc[:,'Zipcode']).difference(GWBcodes.loc[:,'Zipcode'])
mismatchZip2 = set(GWBcodes.loc[:,'Zipcode']).difference(masterdf.loc[:,'Zipcode'])
print(len(mismatchZip1),' Zipcodes are in the masterdf but not in the GWBcodes-set')
print(len(mismatchZip2),' Zipcodes are in the GWBcodes-set but not in the masterdf')


#==============================================================================
# Filling the masterdf
#==============================================================================

# merge municipality / district / neighbourhood data ==> mdndf
mdndf = pd.merge(GWBcodes,Gnames,how='left',on='Municipality Code')
print('merged municipality names')
del(GWBcodes)
print ('GWBcodes removed from memory')
del(Gnames)
print ('Gnames removed from memory')
mdndf = pd.merge(mdndf,Wnames,how='left', on='District Code')
print('merged district names')
del(Wnames)
print ('Wnames removed from memory')
mdndf = pd.merge(mdndf,Bnames,how='left', on='Neighbourhood Code')
print('merged neighbourhood names')
del(Bnames)
print ('Bnames removed from memory')

# analysing the naming
print('the district data contains, among others, strange names. Filtered',
      'for "Wijk", "District Names" contain:')
print(mdndf[mdndf["District Name"].str.contains('Wijk')]['District Name'].value_counts())

# make unique address cols
mdndf['Address'] = mdndf['Zipcode']+'_'+mdndf['House No'].map(str)
mdndf = mdndf.drop(columns=['Zipcode','House No'])
print('mdndf["Address"] created and ["Zipcode", "House No"] dropped')
masterdf['Address'] = masterdf['Zipcode']+'_'+masterdf['House No'].map(str)
print('masterdf["Address"] created')

##convert Neighbourhood / District / Municipality Codes to string
#mdndf.loc[:,['Neighbourhood Code', 'District Code', 'Municipality Code']] = mdndf.loc[
#        :,['Neighbourhood Code', 'District Code', 'Municipality Code']].astype(str)
#--> see convert all to string below
#convert all to string
mdndf = mdndf.astype(str)
print('mdndf converted to string')
masterdf = masterdf.astype(str)
print('masterdf converted to string')

#merging masterdf and mdndf on 'Address'-cols
masterdf = pd.merge(masterdf,mdndf, how='left',on='Address')
print('masterdf successfully merged with mdndf')
del(mdndf)
print('mdndf removed from memory')

print('the type for each column in masterdf is:',
      [type(masterdf.iloc[0,i]) for i in range(len(masterdf.columns))])


# =============================================================================
# OUTPUT
# masterdf.to_csv(dir_masterdf_output,sep=';', index=False)
# 
# =============================================================================
