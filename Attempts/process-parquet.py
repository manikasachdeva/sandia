from pathlib import Path
from itertools import chain
import pandas as pd


def sandia2parquet(csvPaths, outputPath):
    """Combine Sandia raw files and save DataFrame in Parquet."""
    df = pd.concat(pd.read_csv(p, parse_dates=[[0, 1]], index_col=0) for p in csvPaths)
    df.sort_index(inplace=True) # ensure datetime is increasing
    df.drop_duplicates(inplace=True)
  
    df.to_parquet(outputPath)
    return outputPath

SANDIA = Path("//cfs2e.nist.gov/73_EL/731/internal/CONFOCAL/FS2/Data4/Sandia/Sandia Data")
DATA1 = SANDIA / "613_625"
DATA2 = SANDIA / "626_710"
DATA3 = SANDIA / "711_725"

        #print(DATA3)

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
DRY_PARQUET = Path("/sandia-graph/data/dry-0613-0724-2018.parquet")
HUMID_PARQUET = Path("/sandia-graph/data/humid-0613-0724-2018.parquet")
            # Process raw files if parquet files don't exist
if not DRY_PARQUET.exists():
    sandia2parquet(DRY_FILES, DRY_PARQUET)

dry = pd.read_parquet(DRY_PARQUET)

if not HUMID_PARQUET.exists():

    sandia2parquet(HUMID_FILES, HUMID_PARQUET)

humid = pd.read_parquet(HUMID_PARQUET)