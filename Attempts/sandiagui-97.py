
# coding: utf-8

# In[1]:


import csv 
import sys 
import time 
from datetime import datetime, time
import os 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#import tkinter as tk
from tkinter import *
from pathlib import Path
from itertools import chain

#from ipywidgets import widgets
#from ipywidgets import interact, interactive, fixed, interact_manual


# In[2]:


# Output files
DRY_PARQUET = Path("//cfs2e.nist.gov/73_EL/731/internal/CONFOCAL/FS2/Data4/Sandia/Parquet Files/dry-0613-0724-2018.parquet")
HUMID_PARQUET = Path("//cfs2e.nist.gov/73_EL/731/internal/CONFOCAL/FS2/Data4/Sandia/Parquet Files/humid-0613-0724-2018.parquet")


# In[3]:


#Interface Coding 
root=Tk()
root.title("Sandia Graphs Generator (2018)")
#setting the size of the window so it doesn't change
root.minsize(width=350, height=470)
root.maxsize(width=350, height=470)
root.configure(background='ivory2')

header = Label(root, text="Sandia Graphs Generator", font=("calibri", 23, "bold"), fg="blue", background='ivory2').place(x=10, y =0)


# In[4]:


#User Input for dates
#DOES NOT WORK YET
startLabel = Label(root, text="Please enter the start date: ", font=("calibri", 12), fg="blue", background='ivory2').place(x=10, y = 50)
startDate = StringVar()
entry_box1 = Entry(root, textvariable = startDate, width = 17, bg = "lightblue")
entry_box1.place(x=200, y = 55)

endLabel = Label(root, text="Please enter the end date: ", font=("calibri", 12), fg="blue", background='ivory2').place(x=10, y = 90)
endDate = StringVar()
entry_box2 = Entry(root, textvariable = endDate, width = 17, bg = "lightblue", )
entry_box2.place(x=200, y = 95)


# In[5]:


#Dry Chambers Check Boxes
dryChamber = Label(root, text="Dry", font=("calibri", 12), fg="blue", background='ivory2').place(x=10, y = 125)

chamber1bool = BooleanVar()
chamber3bool = BooleanVar()
chamber5bool = BooleanVar()	

chamber1 = Checkbutton(root, variable = chamber1bool, onvalue=True, offvalue=False,text = "Chamber 1", background='ivory2')
chamber1.place(x =10, y = 150)
    
chamber3 = Checkbutton(root, variable = chamber3bool, onvalue=True, offvalue=False, text = "Chamber 3", background='ivory2')
chamber3.place(x =10, y = 170)

chamber5 = Checkbutton(root,variable = chamber5bool, onvalue=True, offvalue=False, text = "Chamber 5", background='ivory2')
chamber5.place(x =10, y = 190)


# In[6]:


#Humid Chambers Check Boxes 
humidChamber = Label(root, text="Humid", font=("calibri", 12), fg="blue", background='ivory2').place(x=170, y = 125)

chamber2bool = BooleanVar()
chamber4bool= BooleanVar()

chamber2 = Checkbutton(root, variable = chamber2bool, onvalue=True, offvalue=False, text = "Chamber 2", background='ivory2')
chamber2.place(x =170, y = 150)
    
chamber4 = Checkbutton(root, variable = chamber4bool, onvalue=True, offvalue=False, text = "Chamber 4", background='ivory2')
chamber4.place(x =170, y = 170)	


# In[7]:


#Temperature options 
temp = Label(root, text= "Dry Temps", font = ("calibri", 12), fg = "blue", background='ivory2').place(x=10, y = 210)
temp2 = Label(root, text= "Humid Temps", font = ("calibri", 12), fg = "blue", background='ivory2').place(x=170, y = 210)
            
airTempDbool = BooleanVar()
airTempD = Checkbutton(root, variable=airTempDbool, onvalue=True, offvalue=False, text = "Air Temperature (Deg C)", background='ivory2')
airTempD.place(x = 10, y=235)

airTempHbool = BooleanVar()
airTempH = Checkbutton(root, variable=airTempHbool, onvalue=True, offvalue=False, text = "Air Temperature (Deg C)", background='ivory2')
airTempH.place(x = 170, y = 235)

waterTempbool = BooleanVar()
waterTemp = Checkbutton(root, variable=waterTempbool, onvalue=True, offvalue=False, text = "Water Temperature (Deg C)", background='ivory2')
waterTemp.place(x=170, y = 275)

panTempbool = BooleanVar()
panTemp = Checkbutton(root,variable=panTempbool, onvalue=True, offvalue=False,  text = "Pan Temperature (Deg C)", background='ivory2')
panTemp.place(x=170, y = 255)	


# In[8]:


#Power Options 
power = Label(root, text= "Dry Heat Power ", font = ("calibri", 12), fg = "blue", background='ivory2').place(x=10, y = 295)
power2 = Label(root, text= "Humid Heat Power ", font = ("calibri", 12), fg = "blue", background='ivory2').place(x=170, y = 295)

chamber1HeatBool = BooleanVar()
chamber1Heat55 = Checkbutton(root, variable=chamber1HeatBool, onvalue=True, offvalue=False, text = "55 C Heat Power (%)", background='ivory2')
chamber1Heat55.place(x=10, y = 320)

chamber35HeatBool = BooleanVar()
chamber35Heat81 = Checkbutton(root, variable=chamber35HeatBool, onvalue=True, offvalue=False, text = "81 C Heat Power (%)", background='ivory2')
chamber35Heat81.place(x=10, y = 340)

chamber24HeatAirBool = BooleanVar()
chamber24HeatAir = Checkbutton(root, variable=chamber24HeatAirBool, onvalue=True, offvalue=False, text = "Air Heat Power (%)", background='ivory2')
chamber24HeatAir.place(x=170, y = 320)

chamber24HeatPanBool = BooleanVar()
chamber24HeatPan = Checkbutton(root, variable=chamber24HeatPanBool, onvalue=True, offvalue=False, text = "Pan/Water Heat Power (%)", background='ivory2')
chamber24HeatPan.place(x=170, y = 340)


# In[9]:


def graph(): 
    
  #need to figure out issue of reading in multiple parquet files and how to do that to recognize the time range
  #dates are being inputted as 2018-06-13 so what file name system should I use to find out which files to read into
    
    
    dry = pd.read_parquet(DRY_PARQUET)
    humid = pd.read_parquet(HUMID_PARQUET)
    
    # Aggregate Hourly
    dry_hourly = dry.resample('H').mean() 
    humid_hourly = humid.resample('H').mean()
    
    #startRange = startDate.get() + "01:00:00"    
    #endRange = endDate.get() + "01:00:00"
    
    dry_date = humid_hourly.loc[startDate.get():endDate.get()]
    humid_date = humid_hourly.loc[startDate.get():endDate.get()] 
    
    if((chamber2bool.get() and airTempHbool.get() and waterTempbool.get() and panTempbool.get()) == True):
        get_ipython().run_line_magic('matplotlib', 'tk')
        humid_date.loc[:,('2_Air_Temperature (Deg C)', '2_Water_Level (Deg C)', '2_Pan_Temperature (Deg C)')].plot()
        plt.legend()
        plt.show() 
        
  
    
    
    
    

    
      


# In[10]:


def reset():
    chamber1.deselect()
    chamber2.deselect()
    chamber3.deselect()
    chamber4.deselect()
    chamber5.deselect()
    airTempH.deselect()
    airTempD.deselect()
    waterTemp.deselect()
    panTemp.deselect()
    chamber1Heat55.deselect()
    chamber35Heat81.deselect()
    chamber24HeatAir.deselect()
    chamber24HeatPan.deselect()
    entry_box1.delete(0, END)
    entry_box2.delete(0, END)


# In[11]:


graphButton = Button(root, text="GRAPH", bg="lightblue", font = ("calibri", 12, "bold"),fg="blue", width=35, command=graph)
graphButton.place(x = 30, y = 375)

resetButton = Button(root, text="CLEAR", bg="lightgreen", font = ("calibri", 12, "bold"), fg="blue", width=35, command=reset)
resetButton.place(x = 30, y = 420)


# In[12]:


root.mainloop()

