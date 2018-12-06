
# coding: utf-8

# In[ ]:


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
import fastparquet
import threading


# In[ ]:



print("in process function")

def sandia2parquet(csvPaths, outputPath):
    """Combine Sandia raw files and save DataFrame in Parquet."""
    print("in sandia2parquet function")
    df = pd.concat(pd.read_csv(p, parse_dates=[[0, 1]], index_col=0) for p in csvPaths)
    print("after data frame")
    df.drop_duplicates(inplace=True)
    print("drop duplicates")
    df.sort_index(inplace=True) # ensure datetime is increasing
    print("sort index")
    df.to_parquet(outputPath)
    print("parquet made")
    return outputPath


# In[ ]:


SANDIA = Path("//cfs2e.nist.gov/73_EL/731/internal/CONFOCAL/FS2/Data4/Sandia/Sandia Data")
DATA1 = SANDIA / "613_625"
DATA2 = SANDIA / "626_710"
DATA3 = SANDIA / "711_725"

print(SANDIA)


# In[ ]:


# List Dry files
# Parent folder name irregular, sort each list separately then combine
PATTERN = "Dry_*.csv"
DRY_FILES = list(chain.from_iterable([
    sorted(DATA1.glob(PATTERN)),
    sorted(DATA2.glob(PATTERN)),
    sorted(DATA3.glob(PATTERN)),
]))
print("dry files list")


# In[ ]:


# List of Humid files
PATTERN = "Humid_*.csv"
HUMID_FILES = list(chain.from_iterable([
    sorted(DATA1.glob(PATTERN)),
    sorted(DATA2.glob(PATTERN)),
    sorted(DATA3.glob(PATTERN)),
]))


# In[ ]:


# Output files
DRY_PARQUET = Path("//cfs2e.nist.gov/73_EL/731/internal/CONFOCAL/FS2/Data4/Sandia/Parquet Files/dry-0613-0724-2018.parquet")
HUMID_PARQUET = Path("//cfs2e.nist.gov/73_EL/731/internal/CONFOCAL/FS2/Data4/Sandia/Parquet Files/humid-0613-0724-2018.parquet")


# In[ ]:


print(DRY_PARQUET)
#%%time
# Process raw files if parquet files don't exist
if not DRY_PARQUET.exists():

    sandia2parquet(DRY_FILES, DRY_PARQUET)
    print("processing dry")
dry = pd.read_parquet(DRY_PARQUET)


# In[ ]:


get_ipython().run_cell_magic('time', '', 'if not HUMID_PARQUET.exists():\n    sandia2parquet(HUMID_FILES, HUMID_PARQUET)\nhumid = pd.read_parquet(HUMID_PARQUET)')

