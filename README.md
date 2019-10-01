## StDb: Station Database Module and associated Tools

This python module generates a class instance StDbElement which enables information
about particular stations to be stored in a format used by other tools in the SeismoPy
library. It also comes with several helper utilities to generate and view the station
database files.

Andrew Schaeffer, November 2016
v1.3.0


## Installation

### Dependencies

You will need **Python 3.7+**.
Also, the following packages are required:

- [`obspy`](https://github.com/obspy/obspy/wiki)

Note that `numpy` and `matplotlib` are installed as dependencies of `obspy`. See below for full installation details. 

### Conda environment

You can create a custom [conda environment](https://conda.io/docs/user-guide/tasks/manage-environments.html)
where `StDb` can be installed along with its dependencies.

Clone the repository:
```bash
git clone https://gitlab.com/uottawa-geophysics/SeismoPy/StDb.git
cd StDb
```

Create the environment from the `stdb_env.yml` file:
```bash
conda env create -f stdb_env.yml
```
Activate the newly created environment:
```bash
conda activate stdb
```

### 1) Installing using pip

Once the previous steps are performed, you can install `StDb` using pip:
```bash
pip install .
```

Installation after local or remote (gitlab/github) code updates:

```bash
pip install --upgrade .
```

### 2) Building and Installing

Alternatively, you can build and install the project (from the root of the source tree, e.g., inside the cloned `StDb` directory):

```bash
python setup.py build 
python setup.py install
```


Please note, if you are actively working on the code, or making frequent edits, it is advisable
to perform the pip installation with the -e flag. This enables an editable installation, where
symbolic links are used rather than straight copies. This means that any changes made in the
local folders will be reflected in the packages available on the system.


## Package Contents

### StDb Module 

*  Classes.py -> contains the Class definitions
*  convert.py -> subroutines for converting to/from csv types
*  io.py -> input and output routines for loading and writing the station databases.

### Scripts
Python scripts making use of the module for manipulation and creation of databases

* ls_stdb.py -> script for easily viewing the contents of a database
* gen_stdb.py -> script to create a databases from a text file (specific csv format)
* query_stdb.py -> script to create a new database based on a query to a network client
* dump_stdb.py -> script to export a database into csv format
* edit_stdb.py -> interactive entry-by-entry editing of a database file (not recommended if editing large numbers of entries)
* append_stdb.py -> add new entries to an existing database
* merge_stdb.py -> combine multiple station databases together
* update_stdb.py -> convert an old format station database to the new format (v1 to v2)


### Examples

1) Create a database of TA stations by searching IRIS only for those stations with data starting January 2017, within the geographic box defined by (-137,63),(-120,73):

```bash
andrew@Iridium:~$ query_fdsn_stdb.py -C BH? -N TA --minlat=63 --maxlat=73 --minlon=-137 --maxlon=-120  --start=2017-01-01 new_list
Performing Geographic Box Search:
    LL:   63.0000, -137.0000
    UR:   73.0000, -120.0000

Performing Fixed Time Range Search:
   Start: 2017-01-01 00:00:00
   End:   2599-12-31 23:59:59

Station/Channel Search Parameters:
   Network:  TA
   Stations: *
   Channels: BH?
   Channel Rank: LH,BH,HH

Output Files: new_list.csv and new_list.pkl

Initializing Client (IRIS)...Done

Querying client...Done

Search Complete:
  10 stations in 1 networks

Network: TA
   Station: A36M
     Lon, Lat, Elev: -125.2472,  71.9871,   0.03
     Start Date: 2013-09-02 00:00:00
     End Date:   2599-12-31 23:59:59
     Status:     open
     Selected Channel: BH
     Locations:        --
    Added as: TA.A36M
   Station: C36M
     Lon, Lat, Elev: -124.0703,  69.3475,   0.01
     Start Date: 2013-08-21 00:00:00
     End Date:   2599-12-31 23:59:59
     Status:     open
     Selected Channel: BH
     Locations:        --
    Added as: TA.C36M
   Station: EPYK
     Lon, Lat, Elev: -136.7191,  66.3701,   0.72
     Start Date: 2012-10-10 00:00:00
     End Date:   2599-12-31 23:59:59
     Status:     open
     Selected Channel: BH
     Locations:        --,01
    Added as: TA.EPYK
   Station: F30M
     Lon, Lat, Elev: -135.7863,  67.6106,   0.41
     Start Date: 2017-08-22 00:00:00
     End Date:   2599-12-31 23:59:59
     Status:     open
     Selected Channel: BH
     Locations:        --
    Added as: TA.F30M
   Station: F31M
     Lon, Lat, Elev: -133.7420,  67.4410,   0.06
     Start Date: 2016-08-22 00:00:00
     End Date:   2599-12-31 23:59:59
     Status:     open
     Selected Channel: BH
     Locations:        --
    Added as: TA.F31M
   Station: G30M
     Lon, Lat, Elev: -136.2216,  66.9808,   0.74
     Start Date: 2016-08-24 00:00:00
     End Date:   2599-12-31 23:59:59
     Status:     open
     Selected Channel: BH
     Locations:        --
    Added as: TA.G30M
   Station: G30M
     Lon, Lat, Elev: -136.2216,  66.9808,   0.74
     Start Date: 2016-08-24 00:00:00
     End Date:   2599-12-31 23:59:59
     Status:     open
     Selected Channel: BH
     Locations:        --
    Added as: TA.G30M
   Station: G31M
     Lon, Lat, Elev: -134.2708,  66.9227,   0.06
     Start Date: 2017-08-22 00:00:00
     End Date:   2599-12-31 23:59:59
     Status:     open
     Selected Channel: BH
     Locations:        --
    Added as: TA.G31M
   Station: H31M
     Lon, Lat, Elev: -134.3426,  65.8052,   0.64
     Start Date: 2017-07-15 00:00:00
     End Date:   2599-12-31 23:59:59
     Status:     open
     Selected Channel: BH
     Locations:        --
    Added as: TA.H31M
   Station: I30M
     Lon, Lat, Elev: -136.3767,  65.2225,   1.40
     Start Date: 2017-07-14 00:00:00
     End Date:   2599-12-31 23:59:59
     Status:     open
     Selected Channel: BH
     Locations:        --
    Added as: TA.I30M
   Station: J30M
     Lon, Lat, Elev: -136.3304,  64.5753,   1.42
     Start Date: 2017-07-13 00:00:00
     End Date:   2599-12-31 23:59:59
     Status:     open
     Selected Channel: BH
     Locations:        --
    Added as: TA.J30M

  Pickling (type 2) to new_list.pkl
  Saving csv to: new_list.csv
andrew@Iridium:~$
```

2) View a subset of stations within the database. Use a comma-separated list of keys to selec
which stations to include in the list.

```bash
andrew@Iridium:~$ ls_stdb.py --keys=TA.E,TA.F new_list.pkl
Listing Station Pickle: new_list.pkl
--------------------------------------------------------------------------
1) TA.EPYK
     Station: TA EPYK
      Alternate Networks: None
      Channel: BH ;  Locations: --,01
      Lon, Lat, Elev:  66.37010, -136.71910,    0.7
      StartTime: 2012-10-10 00:00:00
      EndTime:   2599-12-31 23:59:59
      Status:    open
      Polarity: 1
      Azimuth Correction: 0.000000


--------------------------------------------------------------------------
2) TA.F30M
     Station: TA F30M
      Alternate Networks: None
      Channel: BH ;  Location: --
      Lon, Lat, Elev:  67.61060, -135.78630,    0.4
      StartTime: 2017-08-22 00:00:00
      EndTime:   2599-12-31 23:59:59
      Status:    open
      Polarity: 1
      Azimuth Correction: 0.000000


--------------------------------------------------------------------------
3) TA.F31M
     Station: TA F31M
      Alternate Networks: None
      Channel: BH ;  Location: --
      Lon, Lat, Elev:  67.44100, -133.74200,    0.1
      StartTime: 2016-08-22 00:00:00
      EndTime:   2599-12-31 23:59:59
      Status:    open
      Polarity: 1
      Azimuth Correction: 0.000000


andrew@Iridium:~$
```