
# coding: utf-8

# Utilities to make thesis life easier
# @Author: Mark Hupkens - 4167813


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time

from ema_workbench.analysis.plotting import lines
from ema_workbench.analysis.plotting_util import KDE
from ema_workbench.analysis import prim
from ema_workbench.util import ema_logging
ema_logging.log_to_stderr(ema_logging.INFO)
from ema_workbench.util import load_results
from ema_workbench.analysis.plotting import lines, plot_lines_with_envelopes, envelopes  


# ### Plotting lines and saving results

# In[2]:


def plot_all_lines(results, outcomes, grouped, save, title):
    if grouped == True:
        for kpi in list(outcomes.keys())[1:]: # drop first entry (TIME)
                fig, axes = lines(results, density=u'kde', show_envelope=False,outcomes_to_show=kpi, group_by='policy')

                if save==True:
                    plt.savefig('plots/scenario_policies/'+time.strftime('%Y%m%d')+ title +'_lines_grouped_' + kpi + '.png',dpi=1200)
                else: 
                    print(kpi + ' was not saved')
    else:
        for kpi in list(outcomes.keys())[1:]: # drop first entry (TIME)
            fig, axes = lines(results, density=u'kde', show_envelope=False,outcomes_to_show=kpi)

            if save==True:
                plt.savefig('plots/scenario_policies/'+time.strftime('%Y%m%d')+ title + '_lines_' + kpi + '.png',dpi=1200)
            else: 
                print(kpi + ' was not saved')

def plot_all_envelopes(results, outcomes, grouped, save, title):
    if grouped == True:
        for kpi in list(outcomes.keys())[1:]: # drop first entry (TIME)
                fig, axes = envelopes(results, density=u'kde',outcomes_to_show=kpi, group_by='policy', fill=True)

                if save==True:
                    plt.savefig('plots/scenario_basecase/'+time.strftime('%Y%m%d') + title + '_lines_grouped_' + kpi + '.png',dpi=1200)
                else: 
                    print(kpi + ' was not saved')
    else:
        for kpi in list(outcomes.keys())[1:]: # drop first entry (TIME)
            fig, axes = envelopes(results, density=u'kde',outcomes_to_show=kpi, fill=True)

            if save==True:
                plt.savefig('plots/scenario_policies/'+time.strftime('%Y%m%d') + title + '_lines_' + kpi + '.png',dpi=1200)
            else: 
                print(kpi + ' was not saved')                

# ### Slicing

# In[3]:


# experiments, outcomes = policy_results

def slice_results(experiments, outcomes, policy):
    '''Selects policy from experiments and keeps only outcomes of selected policy'''

    import numpy as np
    global sliced_results
    new_experiments=experiments.copy()
    new_outcomes=outcomes.copy()

    ids_removed = []    # list for removed ids
    ids_not_removed = [] # ids for remaining runs

    counter=0     # As we delete lines, the index of the new ndarray changes. This counter accounts for that.

    for i in range(len(experiments)):
        if experiments['policy'][i] != policy:  
            counter+=1
            ids_removed.append(i)
            for key in outcomes.keys():
                new_outcomes[key]=np.delete(new_outcomes[key], i-(counter-1), 0)
            new_experiments=np.delete(new_experiments, i-(counter-1), 0)
        else:
            ids_not_removed.append(i)
    sliced_results=(new_experiments, new_outcomes)
    return sliced_results
   
def plot_individual_policies_lines(experiments, outcomes, policy,outcomes_to_show):
    '''Plot individual policy experiment sets'''
    sliced_result = slice_results(experiments, outcomes, policy)
    
    fig = lines(sliced_result, outcomes_to_show=outcomes_to_show, density=KDE)
    print('Plot of policy: ', policy)
    
def plot_individual_policies_envelopes(experiments, outcomes, policy,outcomes_to_show):
    '''Plot individual policy experiment sets'''
    sliced_result = slice_results(experiments, outcomes, policy)
    
    ig,axes = envelopes(sliced_result, outcomes_to_show=outcomes_to_show, fill=True , group_by=False, density=KDE)
    print('Plot of policy: ', policy)

# ### Buurt selector

# Import data and Define functions to clean data and select buurten from municipalities
import ipywidgets as widgets


# Functions for case selection

def merge_and_clean_mapping():
    '''Merge mappings and entities of modelsetup files to get neighbourhoods'''
    # Import data
    df_buurt = pd.read_excel('C:/Users/LocalAdmin/Desktop/ETModel/model/backup/MSETMnlEPdataMHv02.xlsx',sheetname='buurt')
    df_wijk = pd.read_excel('C:/Users/LocalAdmin/Desktop/ETModel/model/backup/MSETMnlEPdataMHv02.xlsx',sheetname='wijk')
    df_gem = pd.read_excel('C:/Users/LocalAdmin/Desktop/ETModel/model/backup/MSETMnlEPdataMHv02.xlsx',sheetname='gemeente')
    
    df_mapping = df_buurt.iloc[:, 0:2].merge(df_wijk.iloc[:, 0:2],left_on='Mapping', right_on='Entities',how='inner')
    df_mapping.drop('Entities_y',axis=1,inplace=True)
    df_mapping.rename(columns={'Entities_x':'Buurt','Mapping_x':'Wijk','Mapping_y':'Gemeente'},inplace=True)
    df_mapping['Gemeente_name'] = df_mapping['Gemeente'].str.split(' G').str[0]
    return df_mapping

def get_buurten(gemeente):
    '''Return and save list of buurten and selected municipality'''
    global neighbourhood_list
    global selected_gemeente
    
    df = merge_and_clean_mapping()
    df_y = df.loc[df.Gemeente_name==gemeente]
    neighbourhood_list = list(df_y.Buurt)
    selected_gemeente = gemeente
    print('Number of neighbourhoods in',' ',selected_gemeente,' :',len(neighbourhood_list))
    return neighbourhood_list

def create_dropdown_values():
    global gemeente_list
    df_wijk = pd.read_excel('C:/Users/LocalAdmin/Desktop/ETModel/model/backup/MSETMnlEPdataMHv02.xlsx',sheetname='wijk')
    gemeente_list = df_wijk.Mapping.str.split(' G').str[0].unique()
    return gemeente_list

def select_buurten():
    '''Create interactive dropdown to select buurten from municipalities'''
    gemeente = create_dropdown_values()
    widgets.interact_manual(get_buurten, gemeente=gemeente)

def return_experimented_policies(experiments):
    l=[]
    for i in range(len(experiments)):
        l.append(experiments[i][-2])
    policies = set(l)
    return policies