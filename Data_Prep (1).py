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

# chargepoint.com
dir_ev = './data/chargepoints.com_scrape.csv'

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

# EV-data chargepoints
evdf = pd.read_csv(dir_ev, sep=',')

# BAG data
#bag = 

# EP-online "geregistreerde labels woningbouw per 01012019"
#reg_labels19 = 
  

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
Gcodes_missing = set(Gnames.loc[:,'Gcode']).symmetric_difference(GWBcodes.loc[:,'Gcode'])
print(len(Gcodes_missing),' Gcodes could not be matched')
Wcodes_missing = set(Wnames.loc[:,'Wcode']).symmetric_difference(GWBcodes.loc[:,'Wcode'])
print(len(Wcodes_missing),' Wcodes could not be matched')
Bcodes_missing = set(Bnames.loc[:,'Bcode']).symmetric_difference(GWBcodes.loc[:,'Bcode'])
print(len(Bcodes_missing),' Bcodes could not be matched')

#test match of GWBcodes.Zipcode and masterdf.Zipcode
mismatchZip1 = set(masterdf.loc[:,'Zipcode']).difference(GWBcodes.loc[:,'Zipcode'])
mismatchZip2 = set(GWBcodes.loc[:,'Zipcode']).difference(masterdf.loc[:,'Zipcode'])
print(len(mismatchZip1),' Zipcodes are in the masterdf but not in the GWBcodes-set')
print(len(mismatchZip2),' Zipcodes are in the GWBcodes-set but not in the masterdf')

### EV-data cleaning
evdf = evdf.dropna(axis=0, how='all')
print(evdf.columns)
evdf = evdf.dropna(axis=1, how='all')
print(evdf.columns)


# steps:
# 1. ['Street Address'] 
#   - cut street name until first digit
#   - cut everything after space of house number
#   - house no. can include appartment letter
# =============================================================================
# ### notes
!new idea:
!    split one by one on sep=' '
!    after each split check for isalnum
!    if true -> keep and delete the rest:
!    else continue
# #for i in evdf.index:
#     evdf.loc[i,'House No'] = int(''.join(filter(str.isdigit, str(
#             evdf['Street Address'][i]))))
# 
# # str(evdf['Street Address'][2]).split()
# for i in a:
#     if i.isdigit():
#         print(i)
#         break
#     elif list(i)[0]
#     else:
#         print('no digit')
# 
# =============================================================================


#==============================================================================
# Filling the masterdf
#==============================================================================

##add new columns to fill
#append_master_cols = ['Neighbourhood','District','Municipality']
#for i in append_master_cols:
 #   masterdf[i]=np.nan
  #  print('column ',i,' added')

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
print('mdndf["Address"] created')

#merging masterdf and mdndf on 'Address'-cols
masterdf = pd.merge(masterdf,mdndf, how='left',on='Address')
print('masterdf successfully merged with mdndf')
del(mdndf)
print('mdndf removed from memory')

# =============================================================================
# OUTPUT
masterdf.to_csv(dir_masterdf_output,sep=';', index=False)
# 
# =============================================================================
#==============================================================================
# TO DO
#==============================================================================
# - match G / W / B codes, names 2018
# - 