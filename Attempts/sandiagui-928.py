#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv 
import sys 
import time 
import os 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#import tkinter as tk
from tkinter import *
from tkinter import messagebox
from pathlib import Path
from itertools import chain
import fastparquet
#import threading
#from ipywidgets import widgets
#from ipywidgets import interact, interactive, fixed, interact_manual
#import xlwt
#from PIL import Image


# In[2]:


#Initializing Dictionaries to hold the Parquet File Name: Path
try: 
    drys_dict = {}
    humids_dict = {}
    dry_count = 0
    humid_count = 0
    dry_paths = []
    humid_paths = []
    
    #Folder Directory 
    PARQUET_FOLDER = os.listdir("//cfs2e.nist.gov/73_EL/731/internal/CONFOCAL/FS2/Data4/Sandia/Parquet Files")

    #Adds all the dry and humid parquet files in a dictionary with variable names and their file paths
    for file in PARQUET_FOLDER: 
        file = file.split("-")
        for i in range(len(PARQUET_FOLDER)): 

            if file[i] == "dry":                 
                file ='-'.join(file)
                dry_count += 1                           
                path_name = "//cfs2e.nist.gov/73_EL/731/internal/CONFOCAL/FS2/Data4/Sandia/Parquet Files/" + file
                dry_paths.append(file)
                drys_dict['DRY_PARQUET_%s' % str(dry_count)] = Path(path_name) #DRY_PARQUET_
            elif file[i] == "humid": 
                file ='-'.join(file)
                humid_count += 1
                path_name = "//cfs2e.nist.gov/73_EL/731/internal/CONFOCAL/FS2/Data4/Sandia/Parquet Files/" + file
                humid_paths.append(file)
                humids_dict['HUMID_PARQUET_%s' % str(humid_count)] = Path(path_name)#HUMID_PARQUET_   
except: 
    
    messagebox.showerror("ERROR #1", "There is a problem in reading the files. Please contact the application developer (Manika Sachdeva) for details.")
    


# In[3]:


#Interface Coding 
root=Tk()
root.title("Sandia Graphs Generator (2018)")
#setting the size of the window so it doesn't change
root.minsize(width=350, height=520)
root.maxsize(width=350, height=520)
root.configure(background='ivory2')

header = Label(root, text="Sandia Graphs Generator", font=("calibri", 23, "bold"), fg="blue", background='ivory2').place(x=10, y =0)


# In[4]:


def info(): 
    try: 
        messagebox.showinfo("Information On Application", )
    except:
        messagebox.showerror("ERROR #2", "Not displaying Info Window. Please contact the application developer (Manika Sachdeva) for details.")
    


# In[5]:


def error(): 
    try:
        messagebox.showinfo("Error Codes", "ERROR #1\nNot Reading in Parquet Files.\n\nERROR #2\nNot Displaying Info Window.\n\nERROR #3\nNot Displaying Error Codes.\n\nERROR #4\nDeveloper Information Not Displaying.")
    except: 
        messagebox.showerror("ERROR #3", "Not displaying Error Codes. Please contact the application developer (Manika Sachdeva) for details.")


# In[6]:


def developer(): 
    try: 
        messagebox.showinfo("Developer Details", "National Institute of Standards and Technology\nEngineering Laboratory\nDivision 731.04\nManika Sachdeva\nmanika.sachdeva@nist.gov\nSupervisor: Dr. Stephanie Watson\n\nLast Update: 9/25/2018")
    except: 
        messagebox.showerror("ERROR #4", "Not displaying Developer Information. Please contact the application developer (Manika Sachdeva) for details.")


# In[7]:


menu_bar = Menu(root)
menu_bar.add_cascade(label="Information", command = info)
menu_bar.add_cascade(label="Error Codes", command = error)
menu_bar.add_cascade(label="Developer", command = developer)
root.config(menu=menu_bar)


# In[8]:


#User Input for dates
start_label = Label(root, text="Please enter the start date: ", font=("calibri", 12), fg="blue", background='ivory2').place(x=10, y = 50)
start_date = StringVar()
entry_box1 = Entry(root, textvariable = start_date, width = 17, bg = "lightblue")
entry_box1.place(x=200, y = 55)

end_label = Label(root, text="Please enter the end date: ", font=("calibri", 12), fg="blue", background='ivory2').place(x=10, y = 90)
end_date = StringVar()
entry_box2 = Entry(root, textvariable = end_date, width = 17, bg = "lightblue", )
entry_box2.place(x=200, y = 95)


# In[9]:


#Dry Chambers Check Boxes
dry_chamber_label = Label(root, text="Dry", font=("calibri", 12), fg="blue", background='ivory2').place(x=10, y = 125)

chamber1_bool = BooleanVar()
chamber3_bool = BooleanVar()
chamber5_bool = BooleanVar()

chamber1 = Checkbutton(root, variable = chamber1_bool, onvalue=True, offvalue=False,text = "Chamber 1", background='ivory2')
chamber1.place(x =10, y = 150)
    
chamber3 = Checkbutton(root, variable = chamber3_bool, onvalue=True, offvalue=False, text = "Chamber 3", background='ivory2')
chamber3.place(x =10, y = 170)

chamber5 = Checkbutton(root,variable = chamber5_bool, onvalue=True, offvalue=False, text = "Chamber 5", background='ivory2')
chamber5.place(x =10, y = 190)


# In[10]:


#Humid Chambers Check Boxes 
humid_chamber_label = Label(root, text="Humid", font=("calibri", 12), fg="blue", background='ivory2').place(x=170, y = 125)

chamber2_bool = BooleanVar()
chamber4_bool= BooleanVar()

chamber2 = Checkbutton(root, variable = chamber2_bool, onvalue=True, offvalue=False, text = "Chamber 2", background='ivory2')
chamber2.place(x =170, y = 150)
    
chamber4 = Checkbutton(root, variable = chamber4_bool, onvalue=True, offvalue=False, text = "Chamber 4", background='ivory2')
chamber4.place(x =170, y = 170)	


# In[11]:


#Dry Temperature options 
dry_temp_label = Label(root, text= "Dry Temps", font = ("calibri", 12), fg = "blue", background='ivory2').place(x=10, y = 215)
            
dry_air_bool = BooleanVar()
dry_air = Checkbutton(root, variable=dry_air_bool, onvalue=True, offvalue=False, text = "Air Temperature (Deg C)", background='ivory2')
dry_air.place(x = 10, y=240)


# In[12]:


#Humid Temperature Options
humid_temp_label = Label(root, text= "Humid Temps", font = ("calibri", 12), fg = "blue", background='ivory2').place(x=170, y = 215)

humid_air_bool = BooleanVar()
humid_air = Checkbutton(root, variable=humid_air_bool, onvalue=True, offvalue=False, text = "Air Temperature (Deg C)", background='ivory2')
humid_air.place(x = 170, y = 240)

humid_water_bool = BooleanVar()
humid_water = Checkbutton(root, variable=humid_water_bool, onvalue=True, offvalue=False, text = "Water Temperature (Deg C)", background='ivory2')
humid_water.place(x=170, y = 260)

humid_pan_bool = BooleanVar()
humid_pan = Checkbutton(root,variable=humid_pan_bool, onvalue=True, offvalue=False,  text = "Pan Temperature (Deg C)", background='ivory2')
humid_pan.place(x=170, y = 280)	


# In[13]:


#Dry Power Options 
dry_power_label = Label(root, text= "Dry Heat Power ", font = ("calibri", 12), fg = "blue", background='ivory2').place(x=10, y = 305)

chamber1_55_bool = BooleanVar()
chamber1_55 = Checkbutton(root, variable=chamber1_55_bool, onvalue=True, offvalue=False, text = "55 C Heat Power (%)", background='ivory2')
chamber1_55.place(x=10, y = 330)

chamber35_81_bool = BooleanVar()
chamber35_81 = Checkbutton(root, variable=chamber35_81_bool, onvalue=True, offvalue=False, text = "81 C Heat Power (%)", background='ivory2')
chamber35_81.place(x=10, y = 350)


# In[14]:


#Humid Power Options
humid_power_label = Label(root, text= "Humid Heat Power ", font = ("calibri", 12), fg = "blue", background='ivory2').place(x=170, y = 305)

chamber24_air_bool = BooleanVar()
chamber24_air = Checkbutton(root, variable=chamber24_air_bool, onvalue=True, offvalue=False, text = "Air Heat Power (%)", background='ivory2')
chamber24_air.place(x=170, y = 330)

chamber24_pan_bool = BooleanVar()
chamber24_pan = Checkbutton(root, variable=chamber24_pan_bool, onvalue=True, offvalue=False, text = "Pan/Water Heat Power (%)", background='ivory2')
chamber24_pan.place(x=170, y = 350)


# In[15]:


def graph():     

    start_time = StringVar() 
    start_time = ' 01:00:00'
    end_time = StringVar() 
    end_time = ' 01:00:00'
    #timeFormat = StringVar() 
    #timeFormat = '%y-%m-%d %H:%M:%S'
   
    start_datetime = start_date.get() + start_time    
    end_datetime = end_date.get() + end_time        
       
    dry_dfs = {}
    drys_dfs_count = 0
    humid_dfs = {}
    humids_dfs_count = 0
    dry = pd.DataFrame()
    humid = pd.DataFrame()

    
    for i in drys_dict:                
    	dry_dfs['dry_%s' % str(drys_dfs_count)] = pd.read_parquet(drys_dict[i])
    	drys_dfs_count += 1
    	for i in dry_dfs:
    		dry = dry.append(dry_dfs[i], sort = False)
    		dry_hourly = dry.resample('H').mean()
    		dry_date = dry_hourly.loc[start_datetime:end_datetime]


    for i in humids_dict:
    	humid_dfs['humid_%s' % str(humids_dfs_count)] = pd.read_parquet(humids_dict[i])          
    	humids_dfs_count += 1
    	for i in humid_dfs: 
    		humid = humid.append(humid_dfs[i], sort = False)

        #HARDCODED PARQUET FILES    
        #dry = pd.read_parquet(DRY_PARQUET_1)
        #humid = pd.read_parquet(HUMID_PARQUET_1)

        #dry2 = pd.read_parquet(DRY_PARQUET_2)
        #humid2 = pd.read_parquet(HUMID_PARQUET_2)     

        #dry = dry.append(dry2)
        #humid = humid.append(humid2)

    #     #Aggregate Hourly
	dry_hourly = dry.resample('H').mean()
	humid_hourly = humid.resample('H').mean()    

    #     #creates a new data frame depending on the date range 
    dry_date = dry_hourly.loc[start_datetime:end_datetime]
   	humid_date = humid_hourly.loc[start_datetime:end_datetime]
   #print(dry_date)

   if(start_datetime < end_datetime):       
        
        


        try:
            #CHAMBER 4 AND 2 TEMPERATURES GRAPHING 
            if((chamber4_bool.get() and chamber2_bool.get() and humid_air_bool.get() and humid_water_bool.get() and humid_pan_bool.get()) == True):
                get_ipython().run_line_magic('matplotlib', 'tk')
                humid_date.loc[:,('2_Air_Temperature (Deg C)', '2_Water_Level (Deg C)', '2_Pan_Temperature (Deg C)', '4_Air_Temperature (Deg C)', '4_Water_Level (Deg C)', '4_Pan_Temperature (Deg C)')].plot()
                plt.legend()
                plt.show() 
            elif((chamber4_bool.get() and chamber2_bool.get() and humid_pan_bool.get() and humid_water_bool.get()) == True): 
                get_ipython().run_line_magic('matplotlib', 'tk')
                humid_date.loc[:,('2_Water_Level (Deg C)', '2_Pan_Temperature (Deg C)','4_Water_Level (Deg C)', '4_Pan_Temperature (Deg C)')].plot()
                plt.legend()
                plt.show()
            elif((chamber4_bool.get() and chamber2_bool.get() and humid_water_bool.get() and humid_air_bool.get()) == True):
                get_ipython().run_line_magic('matplotlib', 'tk')
                humid_date.loc[:, ('2_Water_Level (Deg C)','2_Air_Temperature (Deg C)','4_Water_Level (Deg C)','4_Air_Temperature (Deg C)')].plot()
                plt.legend()
                plt.show()
            elif((chamber4_bool.get() and chamber2_bool.get() and humid_pan_bool.get() and humid_air_bool.get()) == True):
                get_ipython().run_line_magic('matplotlib', 'tk')
                humid_date.loc[:,('2_Pan_Temperature (Deg C)', '2_Air_Temperature (Deg C)','4_Pan_Temperature (Deg C)', '4_Air_Temperature (Deg C)')].plot()
                plt.legend()
                plt.show()        
            elif((chamber4_bool.get() and chamber2_bool.get() and humid_pan_bool.get()) == True):
                get_ipython().run_line_magic('matplotlib', 'tk')
                humid_date.loc[:,('2_Pan_Temperature (Deg C)', '4_Pan_Temperature (Deg C)')].plot()
                plt.legend()
                plt.show()
            elif((chamber4_bool.get() and chamber2_bool.get() and humid_air_bool.get()) == True):
                get_ipython().run_line_magic('matplotlib', 'tk')
                humid_date.loc[:,('2_Air_Temperature (Deg C)', '4_Air_Temperature (Deg C)')].plot()
                plt.legend()
                plt.show()
            elif((chamber4_bool.get() and chamber2_bool.get() and humid_water_bool.get()) == True):
                get_ipython().run_line_magic('matplotlib', 'tk')
                humid_date.loc[:,('2_Water_Level (Deg C)', '4_Water_Level (Deg C)')].plot()
                plt.legend()
                plt.show()
            elif(chamber2_bool.get() == True): 
                if((chamber2_bool.get() and humid_air_bool.get() and humid_water_bool.get() and humid_pan_bool.get()) == True):
                    get_ipython().run_line_magic('matplotlib', 'tk')
                    humid_date.loc[:,('2_Air_Temperature (Deg C)', '2_Water_Level (Deg C)', '2_Pan_Temperature (Deg C)')].plot()
                    plt.legend()
                    plt.show() 
                elif((chamber2_bool.get() and humid_pan_bool.get() and humid_water_bool.get()) == True): 
                    get_ipython().run_line_magic('matplotlib', 'tk')
                    humid_date.loc[:,('2_Water_Level (Deg C)', '2_Pan_Temperature (Deg C)')].plot()
                    plt.legend()
                    plt.show()
                elif((chamber2_bool.get() and humid_water_bool.get() and humid_air_bool.get()) == True):
                    get_ipython().run_line_magic('matplotlib', 'tk')
                    humid_date.loc[:, ('2_Water_Level (Deg C)','2_Air_Temperature (Deg C)')].plot()
                    plt.legend()
                    plt.show()
                elif((chamber2_bool.get() and humid_pan_bool.get() and humid_air_bool.get()) == True):
                    get_ipython().run_line_magic('matplotlib', 'tk')
                    humid_date.loc[:,('2_Pan_Temperature (Deg C)', '2_Air_Temperature (Deg C)')].plot()
                    plt.legend()
                    plt.show()        
                elif((chamber2_bool.get() and humid_pan_bool.get()) == True):
                    get_ipython().run_line_magic('matplotlib', 'tk')
                    humid_date.loc[:,('2_Pan_Temperature (Deg C)')].plot()
                    plt.legend()
                    plt.show()
                elif((chamber2_bool.get() and humid_air_bool.get()) == True):
                    get_ipython().run_line_magic('matplotlib', 'tk')
                    humid_date.loc[:,('2_Air_Temperature (Deg C)')].plot()
                    plt.legend()
                    plt.show()
                elif((chamber2_bool.get() and humid_water_bool.get()) == True):
                    get_ipython().run_line_magic('matplotlib', 'tk')
                    humid_date.loc[:,('2_Water_Level (Deg C)')].plot()
                    plt.legend()      
                    plt.show()             
            elif(chamber4_bool.get() == True):
                if((chamber4_bool.get() and humid_air_bool.get() and humid_water_bool.get() and humid_pan_bool.get()) == True):
                    get_ipython().run_line_magic('matplotlib', 'tk')
                    humid_date.loc[:,('4_Air_Temperature (Deg C)', '4_Water_Level (Deg C)', '4_Pan_Temperature (Deg C)')].plot()
                    plt.legend()
                    plt.show() 
                elif((chamber4_bool.get() and humid_pan_bool.get() and humid_water_bool.get()) == True): 
                    get_ipython().run_line_magic('matplotlib', 'tk')
                    humid_date.loc[:,('4_Water_Level (Deg C)', '4_Pan_Temperature (Deg C)')].plot()
                    plt.legend()
                    plt.show()
                elif((chamber4_bool.get() and humid_water_bool.get() and humid_air_bool.get()) == True):
                    get_ipython().run_line_magic('matplotlib', 'tk')
                    humid_date.loc[:, ('4_Water_Level (Deg C)','4_Air_Temperature (Deg C)')].plot()
                    plt.legend()
                    plt.show()
                elif((chamber4_bool.get() and humid_pan_bool.get() and humid_air_bool.get()) == True):
                    get_ipython().run_line_magic('matplotlib', 'tk')
                    humid_date.loc[:,('4_Pan_Temperature (Deg C)', '4_Air_Temperature (Deg C)')].plot()
                    plt.legend()
                    plt.show()        
                elif((chamber4_bool.get() and humid_pan_bool.get()) == True):
                    get_ipython().run_line_magic('matplotlib', 'tk')
                    humid_date.loc[:,('4_Pan_Temperature (Deg C)')].plot()
                    plt.legend()
                    plt.show()
                elif((chamber4_bool.get() and humid_air_bool.get()) == True):
                    get_ipython().run_line_magic('matplotlib', 'tk')
                    humid_date.loc[:,('4_Air_Temperature (Deg C)')].plot()
                    plt.legend()
                    plt.show()
                elif((chamber4_bool.get() and humid_water_bool.get()) == True):
                    get_ipython().run_line_magic('matplotlib', 'tk')
                    humid_date.loc[:,('4_Water_Level (Deg C)')].plot()
                    plt.legend()
                    plt.show()
            #else: 
                #messagebox.showerror("ERROR #5", "Incorrect Humid/Temperature selection. Please try again by pressing the clear button.\nReminder: You cannot graph Humid Temperatures and Power at the same time.\nIf it does not work, please contact the developer (Manika Sachdeva)") 


            #CHAMBERS 2 AND 4 Power Graphing 
            if((chamber4_bool.get() and chamber2_bool.get() and chamber24_air_bool.get() and chamber24_pan_bool.get()) == True):
                get_ipython().run_line_magic('matplotlib', 'tk')
                humid_date.loc[:,('Chamber_2_Air Heat Power (%)',  'Chamber_2_Pan/Water Heat Power (%)', 'Chamber_4_Air Heat Power (%)', 'Chamber_4_Pan/Water Power (%)')].plot()
                plt.legend()
                plt.show()      
            elif((chamber4_bool.get() and chamber2_bool.get() and chamber24_air_bool.get()) == True):
                get_ipython().run_line_magic('matplotlib', 'tk')
                humid_date.loc[:,('Chamber_2_Air Heat Power (%)', 'Chamber_4_Air Heat Power (%)')].plot()
                plt.legend()
                plt.show()    
            elif((chamber4_bool.get() and chamber2_bool.get() and chamber24_pan_bool.get()) == True):
                get_ipython().run_line_magic('matplotlib', 'tk')
                humid_date.loc[:,('Chamber_2_Pan/Water Heat Power (%)', 'Chamber_4_Pan/Water Power (%)')].plot()
                plt.legend()
                plt.show()
            elif(chamber2_bool.get() == True): 
                if((chamber2_bool.get() and chamber24_air_bool.get() and chamber24_pan_bool.get()) == True):
                    get_ipython().run_line_magic('matplotlib', 'tk')
                    humid_date.loc[:,('Chamber_2_Air Heat Power (%)', 'Chamber_2_Pan/Water Heat Power (%)')].plot()
                    plt.legend()
                    plt.show() 
                elif((chamber2_bool.get() and chamber24_pan_bool.get()) == True): 
                    get_ipython().run_line_magic('matplotlib', 'tk')
                    humid_date.loc[:,('Chamber_2_Pan/Water Heat Power (%)')].plot()
                    plt.legend()
                    plt.show()        
                elif((chamber2_bool.get() and chamber24_air_bool.get()) == True):
                    get_ipython().run_line_magic('matplotlib', 'tk')
                    humid_date.loc[:,('Chamber_2_Air Heat Power (%)')].plot()
                    plt.legend()
                    plt.show()    
            elif(chamber4_bool.get() == True):
                if((chamber4_bool.get() and chamber24_air_bool.get() and chamber24_pan_bool.get()) == True):
                    get_ipython().run_line_magic('matplotlib', 'tk')
                    humid_date.loc[:,('Chamber_4_Air Heat Power (%)', 'Chamber_4_Pan/Water Power (%)')].plot()
                    plt.legend()
                    plt.show()             
                elif((chamber4_bool.get() and chamber24_air_bool.get()) == True):
                    get_ipython().run_line_magic('matplotlib', 'tk')
                    humid_date.loc[:,('Chamber_4_Air Heat Power (%)')].plot()
                    plt.legend()
                    plt.show()
                elif((chamber4_bool.get() and chamber24_pan_bool.get()) == True):
                    get_ipython().run_line_magic('matplotlib', 'tk')
                    humid_date.loc[:,('Chamber_4_Pan/Water Power (%)')].plot()
                    plt.legend()
                    plt.show()            
            #else: 
                #messagebox.showerror("ERROR #6", "Incorrect Humid/Power selection. Please try again by pressing the clear button.\nReminder: You cannot graph Humid Temperatures and Power at the same time.\nIf it does not work, please contact the developer (Manika Sachdeva)") 

            #CHAMBER 1 3 5 for TEMPERATURE
            if((chamber1_bool.get() and chamber3_bool.get() and chamber5_bool.get() and dry_air_bool.get()) == True):
                get_ipython().run_line_magic('matplotlib', 'tk')
                dry_date.loc[:,('1-Air_Temperature (Deg C)', '3-Air_Temperature (Deg C)','5-AirTemperature (Deg C)')].plot()
                plt.legend()
                plt.show()
            elif((chamber1_bool.get() and chamber3_bool.get()) == True): 
                if((chamber1_bool.get() and chamber3_bool.get() and dry_air_bool.get()) == True):
                    get_ipython().run_line_magic('matplotlib', 'tk')
                    dry_date.loc[:,('1-Air_Temperature (Deg C)', '3-Air_Temperature (Deg C)')].plot()
                    plt.legend()
                    plt.show()
            elif((chamber1_bool.get() and chamber5_bool.get()) == True): 
                if((chamber1_bool.get() and chamber5_bool.get() and dry_air_bool.get()) == True):
                    get_ipython().run_line_magic('matplotlib', 'tk')
                    dry_date.loc[:,('1-Air_Temperature (Deg C)', '5-AirTemperature (Deg C)')].plot()
                    plt.legend()
                    plt.show()
            elif((chamber3_bool.get() and chamber5_bool.get()) == True): 
                if((chamber3_bool.get() and chamber5_bool.get() and dry_air_bool.get()) == True):
                    get_ipython().run_line_magic('matplotlib', 'tk')
                    dry_date.loc[:,('3-Air_Temperature (Deg C)', '5-AirTemperature (Deg C)')].plot()
                    plt.legend()
                    plt.show()  
            elif(chamber1_bool.get() == True): 
                get_ipython().run_line_magic('matplotlib', 'tk')
                dry_date.loc[:,('1-Air_Temperature (Deg C)')].plot()
                plt.legend()
                plt.show()  
            elif(chamber3_bool.get() == True):
                get_ipython().run_line_magic('matplotlib', 'tk')
                dry_date.loc[:,('3-Air_Temperature (Deg C)')].plot()
                plt.legend()
                plt.show()  
            elif(chamber5_bool.get() == True):
                get_ipython().run_line_magic('matplotlib', 'tk')
                dry_date.loc[:,('5-AirTemperature (Deg C)')].plot()
                plt.legend()
                plt.show()  

            #CHAMBER 1 3 5 for POWER
            if((chamber1_bool.get() and chamber3_bool.get() and chamber5_bool.get() and chamber1_55_bool.get() and chamber35_81_bool.get()) == True):
                get_ipython().run_line_magic('matplotlib', 'tk')
                dry_date.loc[:,('Chamber_1_-_55C Heat Power (%)', 'Chamber_3_-_81C Heat Power (%)','Chamber_5_-_81C Heat Power (%)')].plot()
                plt.legend()
                plt.show()
            elif((chamber1_bool.get() and chamber3_bool.get()) == True): 
                if((chamber1_bool.get() and chamber3_bool.get() and chamber1_55_bool.get() and chamber35_81_bool.get()) == True):
                    get_ipython().run_line_magic('matplotlib', 'tk')
                    dry_date.loc[:,('Chamber_1_-_55C Heat Power (%)', 'Chamber_3_-_81C Heat Power (%)')].plot()
                    plt.legend()
                    plt.show()
            elif((chamber1_bool.get() and chamber5_bool.get()) == True): 
                if((chamber1_bool.get() and chamber5_bool.get() and chamber1_55_bool.get() and chamber35_81_bool.get()) == True):
                    get_ipython().run_line_magic('matplotlib', 'tk')
                    dry_date.loc[:,('Chamber_1_-_55C Heat Power (%)', 'Chamber_5_-_81C Heat Power (%)')].plot()
                    plt.legend()
                    plt.show()
            elif((chamber3_bool.get() and chamber5_bool.get()) == True): 
                if((chamber3_bool.get() and chamber5_bool.get() and chamber35_81_bool.get()) == True):
                    get_ipython().run_line_magic('matplotlib', 'tk')
                    dry_date.loc[:,('Chamber_3_-_81C Heat Power (%)','Chamber_5_-_81C Heat Power (%)')].plot()
                    plt.legend()
                    plt.show()
            elif(chamber1_bool.get() == True):
                if((chamber1_bool.get() and chamber1_55_bool.get() ) == True):
                    get_ipython().run_line_magic('matplotlib', 'tk')
                    dry_date.loc[:,('Chamber_1_-_55C Heat Power (%)')].plot()
                    plt.legend()
                    plt.show()
            elif(chamber3_bool.get() == True):
                if((chamber3_bool.get() and chamber35_81_bool.get()) == True):
                    get_ipython().run_line_magic('matplotlib', 'tk')
                    dry_date.loc[:,('Chamber_3_-_81C Heat Power (%)')].plot()
                    plt.legend()
                    plt.show()
            elif(chamber5_bool.get() == True):
                if((chamber5_bool.get() and chamber35_81_bool.get()) == True):
                    get_ipython().run_line_magic('matplotlib', 'tk')
                    dry_date.loc[:,('Chamber_5_-_81C Heat Power (%)')].plot()
                    plt.legend()
                    plt.show()
        except: 
            messagebox.showerror("ERROR #5", "Incorrect selections.\nPlease press the clear button to try again.\n\nReminder: You cannot graph Humid and Dry Temperatures/Powers together.\nPlease contact the developer (Manika Sachdeva) for questions or errors.")    
    else: 
        print("error")
    


# In[16]:


def file(): 
    #for i in dry_paths:
        #for j in humid_paths: 
    messagebox.showinfo("File Names", "Dry Files\n" + str(dry_paths) + "\n\n"+ "Humid Files\n"+ str(humid_paths) + "\n\n")

    


# In[17]:


def reset():
    chamber1.deselect()
    chamber2.deselect()
    chamber3.deselect()
    chamber4.deselect()
    chamber5.deselect()
    humid_air.deselect()
    dry_air.deselect()
    humid_water.deselect()
    humid_pan.deselect()
    chamber1_55.deselect()
    chamber35_81.deselect()
    chamber24_air.deselect()
    chamber24_pan.deselect()
    entry_box1.delete(0, END)
    entry_box2.delete(0, END)


# In[18]:


fileButton = Button(root, text = "VIEW FILE NAMES", bg ='lightpink', font = ("calibri", 12, "bold"), fg="blue", width=35, command=file)
fileButton.place(x = 30, y = 385)

graphButton = Button(root, text="GRAPH", bg="lightblue", font = ("calibri", 12, "bold"),fg="blue", width=35, command=graph)
graphButton.place(x = 30, y = 430)

resetButton = Button(root, text="CLEAR", bg="lightgreen", font = ("calibri", 12, "bold"), fg="blue", width=35, command=reset)
resetButton.place(x = 30, y = 475)


# In[ ]:


root.mainloop()

