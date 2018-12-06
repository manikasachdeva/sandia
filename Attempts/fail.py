import csv 
import sys 
import time 
from datetime import datetime, time
import os 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk
from tkinter import *
from pathlib import Path
from itertools import chain

#Colors: https://wiki.tcl.tk/37701 



def sandia2parquet(csvPaths, outputPath):
    """Combine Sandia raw files and save DataFrame in Parquet."""
    df = pd.concat(pd.read_csv(p, parse_dates=[[0, 1]], index_col=0) for p in csvPaths)
    df.drop_duplicates(inplace=True)
    df.sort_index(inplace=True) # ensure datetime is increasing
    df.to_parquet(outputPath)
    return outputPath

def main():

	
	#Interface Coding 
	root=Tk()
	root.title("Sandia Graphs Generator (2018)")
	#setting the size of the window so it doesn't change
	root.minsize(width=350, height=450)
	root.maxsize(width=350, height=450)
	root.configure(background='ivory2')

	header = Label(root, text="Sandia Graphs Generator", font=("calibri", 23, "bold"), fg="blue", background='ivory2').place(x=10, y =0)

	#User Input for dates
	#DOES NOT WORK YET
	startLabel = Label(root, text="Please enter the start date: ", font=("calibri", 12), fg="blue", background='ivory2').place(x=10, y = 50)
	startDate = StringVar()
	entry_box1 = Entry(root, textvariable = startDate, width = 17, bg = "lightblue").place(x=200, y = 55)

	endLabel = Label(root, text="Please enter the end date: ", font=("calibri", 12), fg="blue", background='ivory2').place(x=10, y = 90)
	endDate = StringVar()
	entry_box2 = Entry(root, textvariable = endDate, width = 17, bg = "lightblue", ).place(x=200, y = 95)
	
	
	
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
	
	
	#Humid Chambers Check Boxes 
	humidChamber = Label(root, text="Humid", font=("calibri", 12), fg="blue", background='ivory2').place(x=170, y = 125)

	chamber2bool = BooleanVar()
	chamber4bool= BooleanVar()

	chamber2 = Checkbutton(root, variable = chamber2bool, onvalue=True, offvalue=False, text = "Chamber 2", background='ivory2')
	chamber2.place(x =170, y = 150)
	
	chamber4 = Checkbutton(root, variable = chamber4bool, onvalue=True, offvalue=False, text = "Chamber 4", background='ivory2')
	chamber4.place(x =170, y = 170)	


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

	
	def process(): 

		#progressBarBool = True;

		#while progressBarBool == True:
			#print("IN THE WHILE LOOP")
			#File Paths 
		SANDIA = Path("//cfs2e.nist.gov/73_EL/731/internal/CONFOCAL/FS2/Data4/Sandia/Sandia Data")
		DATA1 = SANDIA / "613_625"
		DATA2 = SANDIA / "626_710"
		DATA3 = SANDIA / "711_725"

		print(DATA3)

			# List Dry files
			# Parent folder name irregular, sort each list separately then combine
		PATTERN = "Dry_*.csv"
		DRY_FILES = list(chain.from_iterable([
		 sorted(DATA1.glob(PATTERN)),
		sorted(DATA2.glob(PATTERN)),
		sorted(DATA3.glob(PATTERN)),
		]))	

			# List of Humid files
		PATTERN = "Humid_*.csv"
		HUMID_FILES = list(chain.from_iterable([
		sorted(DATA1.glob(PATTERN)),
		sorted(DATA2.glob(PATTERN)),
		sorted(DATA3.glob(PATTERN)),
		]))

		DRY_PARQUET = Path("../data/dry-0613-0724-2018.parquet")
		HUMID_PARQUET = Path("../data/humid-0613-0724-2018.parquet")
			# Process raw files if parquet files don't exist
		if not DRY_PARQUET.exists():
			sandia2parquet(DRY_FILES, DRY_PARQUET)

		dry = pd.read_parquet(DRY_PARQUET)

		if not HUMID_PARQUET.exists():

	   		sandia2parquet(HUMID_FILES, HUMID_PARQUET)

		humid = pd.read_parquet(HUMID_PARQUET)
		#progressBarBool = False;

		#if progressBarBool == True:
		#	progressWindow=Tk()
			#root.title("Sandia Graphs Generator (2018)")


		#	progressWindow.geometry('450x450')
		#	progressWindow.title('Data Chunking..')

		#	progressBar = Progressbar(progressWindow,orient ="horizontal",length = 200, mode ="determinate")
		#	progressBar.pack()





		#userStart = startDate.get()
		#userEnd = endDate.get()


			
	def graph(): 
			print("graph")


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

	processButton = Button(root, text="PROCESS", bg="lightpink", font = ("calibri", 12, "bold"),fg="blue", width=20, command=process)
	processButton.place(x = 90, y = 310)

	graphButton = Button(root, text="GRAPH", bg="lightblue", font = ("calibri", 12, "bold"),fg="blue", width=20, command=graph)
	graphButton.place(x = 90, y = 350)

	resetButton = Button(root, text="CLEAR", bg="lightgreen", font = ("calibri", 12, "bold"), fg="blue", width=20, command=reset)
	resetButton.place(x = 90, y = 390)


	root.mainloop()	


main() 
