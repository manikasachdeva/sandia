#!/usr/bin/env python
# coding: utf-8
 
import os 
import traceback
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tkinter import *
from tkinter import messagebox
from tkinter import Canvas
from pathlib import Path


PARQUET_FOLDER = Path(os.getenv("PARQUET_FOLDER", '//cfs2e.nist.gov/73_EL/731/internal/CONFOCAL/FS2/Data4/Sandia/Parquet Files'))
#Initializing Dictionaries to hold the Parquet File Name: Path
try: 
    #Adds all the dry and humid parquet files in a dictionary with variable names and their file paths
    dry_paths = list(PARQUET_FOLDER.glob("dry-*.parquet"))
    humid_paths = list(PARQUET_FOLDER.glob("humid-*.parquet"))
    dry = pd.concat((pd.read_parquet(path, engine='fastparquet') for path in dry_paths), axis=0)
    humid = pd.concat((pd.read_parquet(path, engine='fastparquet') for path in humid_paths), axis=0)

    #Aggregate Hourly
    dry_hourly = dry.resample('H').mean() 
    humid_hourly = humid.resample('H').mean()    
except: 
    print(traceback.format_exc())
    messagebox.showerror("ERROR #1", "Unable to read files. Please contact the application developer (Manika Sachdeva) for details.")


#Interface Coding 
root=Tk()
root.title("Sandia Graphs Generator (2018)")
#setting the size of the window so it doesn't change
root.minsize(width=350, height=475)
root.maxsize(width=350, height=475)
#root.configure(background='ivory2')

line = Canvas(root)
line.place(width=520, height=520)

line.create_rectangle(9,124,167, 380)
line.create_rectangle(167,124,343, 380)

header = Label(root, text="Sandia Graphs Generator", font=("calibri", 23, "bold"), fg="blue").place(x=10, y =0)

#Menu Bar Functions
def info(): 
    try: 
        messagebox.showinfo("Info", "This program was developed for the NRC Cables Project.\n\nPurpose: Display graphs of the different chambers with different conditions based on a specific time range\n\nHow to Use:\n-Input date ranges in the format (YYYY-MM-DD) (You can check the dates from the Files menu.)\n-Select the Chamber and the corresponding temperature and power options (You cannot graph Dry and Humid selections together)\n-Click the Graph button, and a figure should pop up. If not that means you have chosen incorrectly.\n-Press Clear to clear all selections.\n\nIf there are any questions please contact the developer.")
    except:
        print(traceback.format_exc())
        messagebox.showerror("ERROR #2", "Not displaying Information Window. Please contact the application developer (Manika Sachdeva) for details.")

def error(): 
    try:
        messagebox.showinfo("Error Codes", "ERROR #1\nUnable to read files.\n\nERROR #2\nNot Displaying Information Window.\n\nERROR #3\nNot Displaying Error Codes.\n\nERROR #4\nNot Displaying Developer Information.\n\nERROR #5\nNot Displaying Files\n\nERROR #6\nIncorrect Selection.\n\nERROR #7\nIncorrect Date Ranges.")
    except: 
        print(traceback.format_exc())
        messagebox.showerror("ERROR #3", "Not displaying Error Codes. Please contact the application developer (Manika Sachdeva) for details.")

def developer(): 
    try: 
        messagebox.showinfo("Developer Details", "National Institute of Standards and Technology\nEngineering Laboratory\nDivision 731.04\nManika Sachdeva\nmanika.sachdeva@nist.gov\nSupervisor: Dr. Stephanie Watson\n\nLast Update: 10/3/2018")
    except:
        print(traceback.format_exc())
        messagebox.showerror("ERROR #4", "Not displaying Developer Information. Please contact the application developer (Manika Sachdeva) for details.")

def paths(): 
    try:
        messagebox.showinfo("Files", "Data Set Folder: //cfs2e.nist.gov/73_EL/731/internal/CONFOCAL/FS2/Data4/Sandia/Sandia Data\n\nParquet Folder: //cfs2e.nist.gov/73_EL/731/internal/CONFOCAL/FS2/Data4/Sandia/Parquet Files\n\nDry Files:\n"+ str([p.name for p in dry_paths])+ "\n"+
        "\nHumid Files:\n " + str([p.name for p in humid_paths]))
    except: 
        print(traceback.format_exc())
        messagebox.showerror("ERROR #5", "Not displaying Files. Please contact the application developer (Manika Sachdeva) for details.")

menu_bar = Menu(root)
menu_bar.add_cascade(label="Information", command = info)
menu_bar.add_cascade(label="Error Codes", command = error)
menu_bar.add_cascade(label="File Paths", command = paths)
menu_bar.add_cascade(label="Developer", command = developer)
root.config(menu=menu_bar)

#User Input for dates
start_label = Label(root, text="Please enter the start date: ", font=("calibri", 12), fg="blue").place(x=10, y = 50)
start_date = StringVar()
entry_box1 = Entry(root, textvariable = start_date, width = 22, bg = "lightblue")
entry_box1.place(x=200, y = 55)

end_label = Label(root, text="Please enter the end date: ", font=("calibri", 12), fg="blue").place(x=10, y = 90)
end_date = StringVar()
entry_box2 = Entry(root, textvariable = end_date, width = 22, bg = "lightblue", )
entry_box2.place(x=200, y = 95)


#Dry Chambers Check Boxes
dry_chamber_label = Label(root, text="Dry", font=("calibri", 12), fg="blue").place(x=10, y = 125)

chamber1_bool = BooleanVar()
chamber3_bool = BooleanVar()
chamber5_bool = BooleanVar()

chamber1 = Checkbutton(root, variable = chamber1_bool, onvalue=True, offvalue=False,text = "Chamber 1")
chamber1.place(x =10, y = 150)
    
chamber3 = Checkbutton(root, variable = chamber3_bool, onvalue=True, offvalue=False, text = "Chamber 3")
chamber3.place(x =10, y = 170)

chamber5 = Checkbutton(root,variable = chamber5_bool, onvalue=True, offvalue=False, text = "Chamber 5")
chamber5.place(x =10, y = 190)


#Humid Chambers Check Boxes 
humid_chamber_label = Label(root, text="Humid", font=("calibri", 12), fg="blue").place(x=170, y = 125)

chamber2_bool = BooleanVar()
chamber4_bool= BooleanVar()

chamber2 = Checkbutton(root, variable = chamber2_bool, onvalue=True, offvalue=False, text = "Chamber 2")
chamber2.place(x =170, y = 150)
    
chamber4 = Checkbutton(root, variable = chamber4_bool, onvalue=True, offvalue=False, text = "Chamber 4")
chamber4.place(x =170, y = 170)	


#Dry Temperature options 
dry_temp_label = Label(root, text= "Dry Temps", font = ("calibri", 12), fg = "blue").place(x=10, y = 215)
            
dry_air_bool = BooleanVar()
dry_air = Checkbutton(root, variable=dry_air_bool, onvalue=True, offvalue=False, text = "Air Temperature (Deg C)")
dry_air.place(x = 10, y=240)


#Humid Temperature Options
humid_temp_label = Label(root, text= "Humid Temps", font = ("calibri", 12), fg = "blue").place(x=170, y = 215)

humid_air_bool = BooleanVar()
humid_air = Checkbutton(root, variable=humid_air_bool, onvalue=True, offvalue=False, text = "Air Temperature (Deg C)")
humid_air.place(x = 170, y = 240)

humid_water_bool = BooleanVar()
humid_water = Checkbutton(root, variable=humid_water_bool, onvalue=True, offvalue=False, text = "Water Temperature (Deg C)")
humid_water.place(x=170, y = 260)

humid_pan_bool = BooleanVar()
humid_pan = Checkbutton(root,variable=humid_pan_bool, onvalue=True, offvalue=False,  text = "Pan Temperature (Deg C)")
humid_pan.place(x=170, y = 280)	


#Dry Power Options 
dry_power_label = Label(root, text= "Dry Heat Power ", font = ("calibri", 12), fg = "blue").place(x=10, y = 305)

chamber1_55_bool = BooleanVar()
chamber1_55 = Checkbutton(root, variable=chamber1_55_bool, onvalue=True, offvalue=False, text = "55 C Heat Power (%)")
chamber1_55.place(x=10, y = 330)

chamber35_81_bool = BooleanVar()
chamber35_81 = Checkbutton(root, variable=chamber35_81_bool, onvalue=True, offvalue=False, text = "81 C Heat Power (%)")
chamber35_81.place(x=10, y = 350)


#Humid Power Options
humid_power_label = Label(root, text= "Humid Heat Power ", font = ("calibri", 12), fg = "blue").place(x=170, y = 305)

chamber24_air_bool = BooleanVar()
chamber24_air = Checkbutton(root, variable=chamber24_air_bool, onvalue=True, offvalue=False, text = "Air Heat Power (%)")
chamber24_air.place(x=170, y = 330)

chamber24_pan_bool = BooleanVar()
chamber24_pan = Checkbutton(root, variable=chamber24_pan_bool, onvalue=True, offvalue=False, text = "Pan/Water Heat Power (%)")
chamber24_pan.place(x=170, y = 350)


#Graph Function
def graph():     

    start_time = StringVar() 
    start_time = ' 01:00:00'
    end_time = StringVar() 
    end_time = ' 01:00:00'
   
    start_datetime = start_date.get() + start_time    
    end_datetime = end_date.get() + end_time 
    
    if(start_datetime < end_datetime):       
        
 		#creates a new data frame depending on the date range 
        dry_date = dry_hourly.loc[start_datetime:end_datetime]
        humid_date = humid_hourly.loc[start_datetime:end_datetime] 

        try:
            #CHAMBER 4 AND 2 TEMPERATURES GRAPHING 
            if((chamber4_bool.get() and chamber2_bool.get() and humid_air_bool.get() and humid_water_bool.get() and humid_pan_bool.get()) == True):            
                humid_date.loc[:,('2_Air_Temperature (Deg C)', '2_Water_Level (Deg C)', '2_Pan_Temperature (Deg C)', '4_Air_Temperature (Deg C)', '4_Water_Level (Deg C)', '4_Pan_Temperature (Deg C)')].plot()
                plt.title("Humid Chamber 2 and 4") 
                plt.ylabel("Temperature (C)")
                plt.xlabel("Date (YYYY-MM-DD)")
                plt.tight_layout()
                plt.legend()
                plt.show() 
            elif((chamber4_bool.get() and chamber2_bool.get() and humid_pan_bool.get() and humid_water_bool.get()) == True):               
                humid_date.loc[:,('2_Water_Level (Deg C)', '2_Pan_Temperature (Deg C)','4_Water_Level (Deg C)', '4_Pan_Temperature (Deg C)')].plot()
                plt.title("Humid Chamber 2 and 4") 
                plt.ylabel("Temperature (C)")
                plt.xlabel("Date (YYYY-MM-DD)")
                plt.tight_layout()
                plt.legend()
                plt.show()
            elif((chamber4_bool.get() and chamber2_bool.get() and humid_water_bool.get() and humid_air_bool.get()) == True):       
                humid_date.loc[:, ('2_Water_Level (Deg C)','2_Air_Temperature (Deg C)','4_Water_Level (Deg C)','4_Air_Temperature (Deg C)')].plot()
                plt.title("Humid Chamber 2 and 4") 
                plt.ylabel("Temperature (C)")
                plt.xlabel("Date (YYYY-MM-DD)")
                plt.tight_layout()
                plt.legend()
                plt.show()
            elif((chamber4_bool.get() and chamber2_bool.get() and humid_pan_bool.get() and humid_air_bool.get()) == True):               
                humid_date.loc[:,('2_Pan_Temperature (Deg C)', '2_Air_Temperature (Deg C)','4_Pan_Temperature (Deg C)', '4_Air_Temperature (Deg C)')].plot()
                plt.title("Humid Chamber 2 and 4") 
                plt.ylabel("Temperature (C)")
                plt.xlabel("Date (YYYY-MM-DD)")
                plt.tight_layout()
                plt.legend()
                plt.show()        
            elif((chamber4_bool.get() and chamber2_bool.get() and humid_pan_bool.get()) == True):                
                humid_date.loc[:,('2_Pan_Temperature (Deg C)', '4_Pan_Temperature (Deg C)')].plot()
                plt.title("Humid Chamber 2 and 4") 
                plt.ylabel("Temperature (C)")
                plt.xlabel("Date (YYYY-MM-DD)")
                plt.tight_layout()
                plt.legend()
                plt.show()
            elif((chamber4_bool.get() and chamber2_bool.get() and humid_air_bool.get()) == True):                
                humid_date.loc[:,('2_Air_Temperature (Deg C)', '4_Air_Temperature (Deg C)')].plot()
                plt.title("Humid Chamber 2 and 4") 
                plt.ylabel("Temperature (C)")
                plt.xlabel("Date (YYYY-MM-DD)")
                plt.tight_layout()
                plt.legend()
                plt.show()
            elif((chamber4_bool.get() and chamber2_bool.get() and humid_water_bool.get()) == True):                
                humid_date.loc[:,('2_Water_Level (Deg C)', '4_Water_Level (Deg C)')].plot()
                plt.title("Humid Chamber 2 and 4") 
                plt.ylabel("Temperature (C)")
                plt.xlabel("Date (YYYY-MM-DD)")
                plt.tight_layout()
                plt.legend()
                plt.show()
            elif(chamber2_bool.get() == True): 
                if((chamber2_bool.get() and humid_air_bool.get() and humid_water_bool.get() and humid_pan_bool.get()) == True):                  
                    humid_date.loc[:,('2_Air_Temperature (Deg C)', '2_Water_Level (Deg C)', '2_Pan_Temperature (Deg C)')].plot()
                    plt.title("Humid Chamber 2") 
                    plt.ylabel("Temperature (C)")
                    plt.xlabel("Date (YYYY-MM-DD)")
                    plt.tight_layout()
                    plt.legend()
                    plt.show() 
                elif((chamber2_bool.get() and humid_pan_bool.get() and humid_water_bool.get()) == True):        
                    humid_date.loc[:,('2_Water_Level (Deg C)', '2_Pan_Temperature (Deg C)')].plot()
                    plt.title("Humid Chamber 2") 
                    plt.ylabel("Temperature (C)")
                    plt.xlabel("Date (YYYY-MM-DD)")
                    plt.tight_layout()
                    plt.legend()
                    plt.show()
                elif((chamber2_bool.get() and humid_water_bool.get() and humid_air_bool.get()) == True):                    
                    humid_date.loc[:, ('2_Water_Level (Deg C)','2_Air_Temperature (Deg C)')].plot()
                    plt.title("Humid Chamber 2") 
                    plt.ylabel("Temperature (C)")
                    plt.xlabel("Date (YYYY-MM-DD)")
                    plt.tight_layout()
                    plt.legend()
                    plt.show()
                elif((chamber2_bool.get() and humid_pan_bool.get() and humid_air_bool.get()) == True):             
                    humid_date.loc[:,('2_Pan_Temperature (Deg C)', '2_Air_Temperature (Deg C)')].plot()
                    plt.title("Humid Chamber 2") 
                    plt.ylabel("Temperature (C)")
                    plt.xlabel("Date (YYYY-MM-DD)")
                    plt.tight_layout()
                    plt.legend()
                    plt.show()        
                elif((chamber2_bool.get() and humid_pan_bool.get()) == True):                  
                    humid_date.loc[:,('2_Pan_Temperature (Deg C)')].plot()
                    plt.title("Humid Chamber 2") 
                    plt.ylabel("Temperature (C)")
                    plt.xlabel("Date (YYYY-MM-DD)")
                    plt.tight_layout()
                    plt.legend()
                    plt.show()
                elif((chamber2_bool.get() and humid_air_bool.get()) == True):
                    humid_date.loc[:,('2_Air_Temperature (Deg C)')].plot()
                    plt.title("Humid Chamber 2") 
                    plt.ylabel("Temperature (C)")
                    plt.xlabel("Date (YYYY-MM-DD)")
                    plt.tight_layout()
                    plt.legend()
                    plt.show()
                elif((chamber2_bool.get() and humid_water_bool.get()) == True):                   
                    humid_date.loc[:,('2_Water_Level (Deg C)')].plot()
                    plt.title("Humid Chamber 2") 
                    plt.ylabel("Temperature (C)")
                    plt.xlabel("Date (YYYY-MM-DD)")
                    plt.tight_layout()
                    plt.legend()      
                    plt.show()             
            elif(chamber4_bool.get() == True):
                if((chamber4_bool.get() and humid_air_bool.get() and humid_water_bool.get() and humid_pan_bool.get()) == True):            
                    humid_date.loc[:,('4_Air_Temperature (Deg C)', '4_Water_Level (Deg C)', '4_Pan_Temperature (Deg C)')].plot()
                    plt.title("Humid Chamber 4") 
                    plt.ylabel("Temperature (C)")
                    plt.xlabel("Date (YYYY-MM-DD)")
                    plt.tight_layout()
                    plt.legend()
                    plt.show() 
                elif((chamber4_bool.get() and humid_pan_bool.get() and humid_water_bool.get()) == True):                   
                    humid_date.loc[:,('4_Water_Level (Deg C)', '4_Pan_Temperature (Deg C)')].plot()
                    plt.title("Humid Chamber 4") 
                    plt.ylabel("Temperature (C)")
                    plt.xlabel("Date (YYYY-MM-DD)")
                    plt.tight_layout()
                    plt.legend()
                    plt.show()
                elif((chamber4_bool.get() and humid_water_bool.get() and humid_air_bool.get()) == True):                  
                    humid_date.loc[:, ('4_Water_Level (Deg C)','4_Air_Temperature (Deg C)')].plot()
                    plt.title("Humid Chamber 4") 
                    plt.ylabel("Temperature (C)")
                    plt.xlabel("Date (YYYY-MM-DD)")
                    plt.tight_layout()
                    plt.legend()
                    plt.show()
                elif((chamber4_bool.get() and humid_pan_bool.get() and humid_air_bool.get()) == True):  
                    humid_date.loc[:,('4_Pan_Temperature (Deg C)', '4_Air_Temperature (Deg C)')].plot()
                    plt.title("Humid Chamber 4") 
                    plt.ylabel("Temperature (C)")
                    plt.xlabel("Date (YYYY-MM-DD)")
                    plt.tight_layout()
                    plt.legend()
                    plt.show()        
                elif((chamber4_bool.get() and humid_pan_bool.get()) == True):                    
                    humid_date.loc[:,('4_Pan_Temperature (Deg C)')].plot()
                    plt.title("Humid Chamber 4") 
                    plt.ylabel("Temperature (C)")
                    plt.xlabel("Date (YYYY-MM-DD)")
                    plt.tight_layout()
                    plt.legend()
                    plt.show()
                elif((chamber4_bool.get() and humid_air_bool.get()) == True):                  
                    humid_date.loc[:,('4_Air_Temperature (Deg C)')].plot()
                    plt.title("Humid Chamber 4") 
                    plt.ylabel("Temperature (C)")
                    plt.xlabel("Date (YYYY-MM-DD)")
                    plt.tight_layout()
                    plt.legend()
                    plt.show()
                elif((chamber4_bool.get() and humid_water_bool.get()) == True):             
                    humid_date.loc[:,('4_Water_Level (Deg C)')].plot()
                    plt.title("Humid Chamber 4") 
                    plt.ylabel("Temperature (C)")
                    plt.xlabel("Date (YYYY-MM-DD)")
                    plt.tight_layout()
                    plt.legend()
                    plt.show()        


            #CHAMBERS 2 AND 4 Power Graphing 
            if((chamber4_bool.get() and chamber2_bool.get() and chamber24_air_bool.get() and chamber24_pan_bool.get()) == True):             
                humid_date.loc[:,('Chamber_2_Air Heat Power (%)',  'Chamber_2_Pan/Water Heat Power (%)', 'Chamber_4_Air Heat Power (%)', 'Chamber_4_Pan/Water Power (%)')].plot()
                plt.title("Humid Chamber 2 and 4") 
                plt.ylabel("Power (%)")
                plt.xlabel("Date (YYYY-MM-DD)")
                plt.tight_layout()
                plt.legend()
                plt.show()      
            elif((chamber4_bool.get() and chamber2_bool.get() and chamber24_air_bool.get()) == True):               
                humid_date.loc[:,('Chamber_2_Air Heat Power (%)', 'Chamber_4_Air Heat Power (%)')].plot()
                plt.title("Humid Chamber 2 and 4") 
                plt.ylabel("Power (%)")
                plt.xlabel("Date (YYYY-MM-DD)")
                plt.tight_layout()
                plt.legend()
                plt.show()    
            elif((chamber4_bool.get() and chamber2_bool.get() and chamber24_pan_bool.get()) == True):                
                humid_date.loc[:,('Chamber_2_Pan/Water Heat Power (%)', 'Chamber_4_Pan/Water Power (%)')].plot()
                plt.title("Humid Chamber 2 and 4") 
                plt.ylabel("Power (%)")
                plt.xlabel("Date (YYYY-MM-DD)")
                plt.tight_layout()
                plt.legend()
                plt.show()
            elif(chamber2_bool.get() == True): 
                if((chamber2_bool.get() and chamber24_air_bool.get() and chamber24_pan_bool.get()) == True):                    
                    humid_date.loc[:,('Chamber_2_Air Heat Power (%)', 'Chamber_2_Pan/Water Heat Power (%)')].plot()
                    plt.title("Humid Chamber 2") 
                    plt.ylabel("Power (%)")
                    plt.xlabel("Date (YYYY-MM-DD)")
                    plt.tight_layout()
                    plt.legend()
                    plt.show() 
                elif((chamber2_bool.get() and chamber24_pan_bool.get()) == True):                    
                    humid_date.loc[:,('Chamber_2_Pan/Water Heat Power (%)')].plot()
                    plt.title("Humid Chamber 2") 
                    plt.ylabel("Power (%)")
                    plt.xlabel("Date (YYYY-MM-DD)")
                    plt.tight_layout()
                    plt.legend()
                    plt.show()        
                elif((chamber2_bool.get() and chamber24_air_bool.get()) == True):                 
                    humid_date.loc[:,('Chamber_2_Air Heat Power (%)')].plot()
                    plt.title("Humid Chamber 2") 
                    plt.ylabel("Power (%)")
                    plt.xlabel("Date (YYYY-MM-DD)")
                    plt.tight_layout()
                    plt.legend()
                    plt.show()    
            elif(chamber4_bool.get() == True):
                if((chamber4_bool.get() and chamber24_air_bool.get() and chamber24_pan_bool.get()) == True):                  
                    humid_date.loc[:,('Chamber_4_Air Heat Power (%)', 'Chamber_4_Pan/Water Power (%)')].plot()
                    plt.title("Humid Chamber 4") 
                    plt.ylabel("Power (%)")
                    plt.xlabel("Date (YYYY-MM-DD)")
                    plt.tight_layout()
                    plt.legend()
                    plt.show()             
                elif((chamber4_bool.get() and chamber24_air_bool.get()) == True):                   
                    humid_date.loc[:,('Chamber_4_Air Heat Power (%)')].plot()
                    plt.title("Humid Chamber 4") 
                    plt.ylabel("Power (%)")
                    plt.xlabel("Date (YYYY-MM-DD)")
                    plt.tight_layout()
                    plt.legend()
                    plt.show()
                elif((chamber4_bool.get() and chamber24_pan_bool.get()) == True):                  
                    humid_date.loc[:,('Chamber_4_Pan/Water Power (%)')].plot()
                    plt.title("Humid Chamber 4") 
                    plt.ylabel("Power (%)")
                    plt.xlabel("Date (YYYY-MM-DD)")
                    plt.tight_layout()
                    plt.legend()
                    plt.show()            
            
            #CHAMBER 1 3 5 for TEMPERATURE
            if((chamber1_bool.get() and chamber3_bool.get() and chamber5_bool.get() and dry_air_bool.get()) == True):              
                dry_date.loc[:,('1-Air_Temperature (Deg C)', '3-Air_Temperature (Deg C)','5-AirTemperature (Deg C)')].plot()
                plt.title("Dry Chamber 1 and 3 and 5") 
                plt.ylabel("Temperature (C)")
                plt.xlabel("Date (YYYY-MM-DD)")
                plt.tight_layout()
                plt.legend()
                plt.show()
            elif((chamber1_bool.get() and chamber3_bool.get()) == True): 
                if((chamber1_bool.get() and chamber3_bool.get() and dry_air_bool.get()) == True):                 
                    dry_date.loc[:,('1-Air_Temperature (Deg C)', '3-Air_Temperature (Deg C)')].plot()
                    plt.title("Dry Chamber 1 and 3") 
                    plt.ylabel("Temperature (C)")
                    plt.xlabel("Date (YYYY-MM-DD)")
                    plt.tight_layout()
                    plt.legend()
                    plt.show()
            elif((chamber1_bool.get() and chamber5_bool.get()) == True): 
                if((chamber1_bool.get() and chamber5_bool.get() and dry_air_bool.get()) == True):                  
                    dry_date.loc[:,('1-Air_Temperature (Deg C)', '5-AirTemperature (Deg C)')].plot()
                    plt.title("Dry Chamber 1 and 5") 
                    plt.ylabel("Temperature (C)")
                    plt.xlabel("Date (YYYY-MM-DD)")
                    plt.tight_layout()
                    plt.legend()
                    plt.show()
            elif((chamber3_bool.get() and chamber5_bool.get()) == True): 
                if((chamber3_bool.get() and chamber5_bool.get() and dry_air_bool.get()) == True):                  
                    dry_date.loc[:,('3-Air_Temperature (Deg C)', '5-AirTemperature (Deg C)')].plot()
                    plt.title("Dry Chamber 3 and 5") 
                    plt.ylabel("Temperature (C)")
                    plt.xlabel("Date (YYYY-MM-DD)")
                    plt.tight_layout()
                    plt.legend()
                    plt.show()  
            elif(chamber1_bool.get() == True):      
            	if((chamber1_bool.get() and dry_air_bool.get()) == True):       
	                dry_date.loc[:,('1-Air_Temperature (Deg C)')].plot()
	                plt.title("Dry Chamber 1") 
	                plt.ylabel("Temperature (C)")
	                plt.xlabel("Date (YYYY-MM-DD)")
	                plt.tight_layout()
	                plt.legend()
	                plt.show()  
            elif(chamber3_bool.get() == True):
            	if((chamber3_bool.get() and dry_air_bool.get()) == True):              
	                dry_date.loc[:,('3-Air_Temperature (Deg C)')].plot()
	                plt.title("Dry Chamber 3") 
	                plt.ylabel("Temperature (C)")
	                plt.xlabel("Date (YYYY-MM-DD)")
	                plt.tight_layout()
	                plt.legend()
	                plt.show()  
            elif(chamber5_bool.get() == True):
            	if((chamber1_bool.get() and dry_air_bool.get()) == True):              
		            dry_date.loc[:,('5-AirTemperature (Deg C)')].plot()
		            plt.title("Dry Chamber 5") 
		            plt.ylabel("Temperature (C)")
		            plt.xlabel("Date (YYYY-MM-DD)")
		            plt.tight_layout()
		            plt.legend()
		            plt.show()  

            #CHAMBER 1 3 5 for POWER
            if((chamber1_bool.get() and chamber3_bool.get() and chamber5_bool.get() and chamber1_55_bool.get() and chamber35_81_bool.get()) == True):               
                dry_date.loc[:,('Chamber_1_-_55C Heat Power (%)', 'Chamber_3_-_81C Heat Power (%)','Chamber_5_-_81C Heat Power (%)')].plot()
                plt.title("Dry Chamber 1 and 3 and 5") 
                plt.ylabel("Power (%)")
                plt.xlabel("Date (YYYY-MM-DD)")
                plt.tight_layout()
                plt.legend()
                plt.show()
            elif((chamber1_bool.get() and chamber3_bool.get()) == True): 
                if((chamber1_bool.get() and chamber3_bool.get() and chamber1_55_bool.get() and chamber35_81_bool.get()) == True):                
                    dry_date.loc[:,('Chamber_1_-_55C Heat Power (%)', 'Chamber_3_-_81C Heat Power (%)')].plot()
                    plt.title("Dry Chamber 1 and 3") 
                    plt.ylabel("Power (%)")
                    plt.xlabel("Date (YYYY-MM-DD)")
                    plt.tight_layout()
                    plt.legend()
                    plt.show()
            elif((chamber1_bool.get() and chamber5_bool.get()) == True): 
                if((chamber1_bool.get() and chamber5_bool.get() and chamber1_55_bool.get() and chamber35_81_bool.get()) == True):                  
                    dry_date.loc[:,('Chamber_1_-_55C Heat Power (%)', 'Chamber_5_-_81C Heat Power (%)')].plot()
                    plt.title("Dry Chamber 1 and 5") 
                    plt.ylabel("Power (%)")
                    plt.xlabel("Date (YYYY-MM-DD)")
                    plt.tight_layout()
                    plt.legend()
                    plt.show()
            elif((chamber3_bool.get() and chamber5_bool.get()) == True): 
                if((chamber3_bool.get() and chamber5_bool.get() and chamber35_81_bool.get()) == True):                   
                    dry_date.loc[:,('Chamber_3_-_81C Heat Power (%)','Chamber_5_-_81C Heat Power (%)')].plot()
                    plt.title("Dry Chamber 3 and 5") 
                    plt.ylabel("Power (%)")
                    plt.xlabel("Date (YYYY-MM-DD)")
                    plt.tight_layout()
                    plt.legend()
                    plt.show()
            elif(chamber1_bool.get() == True):
                if((chamber1_bool.get() and chamber1_55_bool.get()) == True):                  
                    dry_date.loc[:,('Chamber_1_-_55C Heat Power (%)')].plot()
                    plt.title("Dry Chamber 1") 
                    plt.ylabel("Power (%)")
                    plt.xlabel("Date (YYYY-MM-DD)")
                    plt.tight_layout()
                    plt.legend()
                    plt.show()
            elif(chamber3_bool.get() == True):
                if((chamber3_bool.get() and chamber35_81_bool.get()) == True):                   
                    dry_date.loc[:,('Chamber_3_-_81C Heat Power (%)')].plot()
                    plt.title("Dry Chamber 3") 
                    plt.ylabel("Power (%)")
                    plt.xlabel("Date (YYYY-MM-DD)")
                    plt.tight_layout()
                    plt.legend()
                    plt.show()
            elif(chamber5_bool.get() == True):
                if((chamber5_bool.get() and chamber35_81_bool.get()) == True):
                    dry_date.loc[:,('Chamber_5_-_81C Heat Power (%)')].plot()
                    plt.title("Dry Chamber 5") 
                    plt.ylabel("Power (%)")
                    plt.xlabel("Date (YYYY-MM-DD)")
                    plt.tight_layout()
                    plt.legend()
                    plt.show()
        except: 
            messagebox.showerror("ERROR #6", "Cannot graph.\nMost likely an error in the selections.\nPlease press the clear button to try again.\n\nReminder: You cannot graph Humid and Dry Temperatures/Powers together.\nPlease contact the developer (Manika Sachdeva) for questions or errors.")    
    else: 
        messagebox.showerror("ERROR #7","Incorrect range of dates.\nPlease press the clear button to try again.\nPlease check the View Files button to see what files are in the system.\nPlease contact the developer (Manika Sachdeva) for questions or errors.")

#resets all inputs
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

#buttons
graphButton = Button(root, text="GRAPH", bg="lightblue", font = ("calibri", 12, "bold"),fg="blue", width=35, command=graph)
graphButton.place(x = 30, y = 390)

resetButton = Button(root, text="CLEAR", bg="lightgreen", font = ("calibri", 12, "bold"), fg="blue", width=35, command=reset)
resetButton.place(x = 30, y = 435)


root.mainloop()






