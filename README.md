## StDb: Station Database Module and associated Tools

![](./stdb/examples/figures/StDb_logo.png)

StDb is a package containing tools for building a database of station information
from geophysical observatories. The code is used through command-line scripts 
and include several options for querying an online fdsn archive, list 
the content of an existing station database, merge existing databases, and 
manually append new station information (e.g., for stations not hosted on
any fdsn archive). 

The resulting station dictionary is used in various seismic applications, 
such as [`SplitPy`](https://github.com/paudetseis/SplitPy) and `RfPy`.


## Installation

### Dependencies

You will need **Python 3.7+**.
Also, the following packages are required:

- [`obspy`](https://github.com/obspy/obspy/wiki)

other required packages (e.g., `numpy` and `matplotlib`) are installed as 
dependencies of `obspy`. 

### Conda environment

You can create a custom [conda environment](https://conda.io/docs/user-guide/tasks/manage-environments.html)
where `StDb` can be installed along with its dependencies.

Create the environment and install the dependencies:
```bash
conda create -n stdb python=3.7 obspy
```

Activate the newly created environment:
```bash
conda activate stdb
```

### Installing from Pypi

```bash
pip install stdb
```

### Installing from source

- Clone the repository:

```bash
git clone https://gitlab.com/uottawa-geophysics/SeismoPy/StDb.git
cd StDb
```

- Install using pip

```bash
pip install .
```
