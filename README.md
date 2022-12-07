# pydelft
Python tools for working with Delft3d FLOW.  
# Reading and writing the d3d oupput
## 1. Using the "requirments.txt" to install pacakages**
 ```
    py -m pip install -r requirements.txt 
```
[reference](https://packaging.python.org/en/latest/tutorials/installing-packages/)

## 2. 

 ```
    conda install pyqt=4
```
or
 ```
    conda install pyqt
```
[reference](https://anaconda.org/anaconda/pyqt)

## 3. How to install Matplotlib's basemap?
```
    pip install basemap-1.0.8-cp34-none-win_amd64.whl
```
[reference](https://stackoverflow.com/questions/33020202/how-to-install-matplotlibs-basemap)

or 
```
    pip install basemap
```

[reference](https://pypi.org/project/basemap/)

or 
```
    conda install -c conda-forge basemap
```
[reference](https://stackoverflow.com/questions/48388217/basemap-importerror-no-module-named-mpl-toolkits-basemap
)

or 
```
   conda install -c conda-forge basemap-data-hires 

```
After doing this, executing

```
from mpl_toolkits.basemap import Basemap

```
from python console should work normally.

## 4. Download the basemap
```
pip3 install basemap_data_hires-1.3.2-py3-none-any.whl
```
[reference](https://www.lfd.uci.edu/~gohlke/pythonlibs/)

## 5. How to add your Conda environment to your jupyter notebook in just 4 steps

Step 1: Create a Conda environment.
```
conda create --name firstEnv
```

Step 2: Activate the environment using the command as shown in the console. After you activate it, you can install any package you need in this environment.
```
conda install -c conda-forge tensorflow
```

Step 3: Now you have successfully installed Tensorflow.
```
conda install -c anaconda ipykernel
```

After installing this,
```
python -m ipykernel install --user --name=firstEnv
python -m ipykernel install --user --name=pydelft2
```

Step 4: Just check your Jupyter Notebook, to see the shining firstEnv.

## 6. 
```
pip3 install pyproj
```

## 7. UsageError: Line magic function `%` not found. Jupyter Notebook
Spell it as two words, rather than three:
```
%matplotlib inline
```

## 8. 'grd' no object has no attribute 'fileName' 

grd.py

__init__ function for your admin class needs a line
```
self.read_grd(fname)
```
[reference](https://stackoverflow.com/questions/39239665/admin-object-has-no-attribute-filename)

## 9. MITGCM
https://mitgcm.readthedocs.io/en/latest/utilities/utilities.html


## 10.linlk lpt
https://github.com/VeckoTheGecko/ocean-plastic-honours 

https://github.com/VeckoTheGecko/ocean-plastic-honours/blob/2825d9c75a75a893ada7fb37c5d30e0fd0da8fc6/my_modelling/delft_to_parcels_tooling.py 

https://tristansalles.github.io/EnviReef/6-addson/parcels.html#reading-velocities-into-parcels



