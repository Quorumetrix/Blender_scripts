# User’s guide for installing new Python modules in Blender. 

**Tldr:** *The Python data-science ecosystem of packages can be very beneficial for data processing and visualization in Blender, but using additional libraries can be a headache.  Until this is made easier in future versions of Blender (PLEASE), there are two main methods of installing new Python modules: either the pip-alone method in Blender’s pre-bundled Python, or replacing Blender’s pre-bundled Python with your own virtual environment.* 

Blender comes with it’s own Python version that makes getting up and running with scripting relatively painless. Hop over to the scripting tab, do a few operations in the Blender GUI, and it the ‘info’ window provides you with the Python API commands for the operations you did. It’s a very user-friendly and low barrier of entry to automating parts of your workflow. 
Combine this with some basic programming operations like looping and boolean logic, and you can accomplish a great deal. 

Blender’s Python distribution even comes with NumPy, the famed numerical processing library for Python that allows fast vectorized computations,  linear algebra, a variety or random distributions, interpolation, and tons of features above my pay grade. Most users won’t  need to go beyond NumPy for your data-processing needs. However, if you’re like me, you’ve grown accustomed to being able to import new modules as needed, or have grown dependent on certain data processing libraries that make your data-science workflow possible. This guide is for those who want to use Blender with additional libraries that don’t come pre-packed with Blender’s Python installation. 

I’ve struggled with this quirk of the Blender-Python situation for a few years. I currently have multiple Blender installations with different Python environments. (2.8, 2,93, 3.0.0, 3.30). Some of my scripts only run in certain versions because of the Python environments, so I’m putting together this guide to help others avoid this situation. My reasons are twofold: first to help others navigate this confusing space, and second: bringing this issue to more developers attention so that eventually this guide will be rendered obsolete. One option may be to release a branch of Blender that has many additional packages pre-packaged with the distribution.

Here are a few example packages that would improve data-science related functionality in Blender. 

**Pandas**: Easily save and load tabular data, apply data filtering,sorting processing operations using column headers. Pickle large datasets to store pre-processed files locally. Pandas read_csv() is, to my knowledge, the best and easiest way to bring a csv, tsv dataset into Python and interact with it intuitively.

**Datetime**: easily handle calendar dates and times for timeseries data. Calculate time deltas between measurements.

**H5py**: Load and parse data from the *.h5 file format. Very useful for storing big data, in a domain-neutral format 

**VTK**: (visualization Toolkit). Implementations of many advanced mesh-generating functions, such as marching cubes. Also includes especially functions for loading common scientific images like Tiffs. 
SciKit-learn: Apply machine learning algorithms, dimensionality reduction, feature standardization, and other useful data-science techniques.

**SciKit image:** Brilliant computer-vision toolkit for image analysis and processing. Particularly useful for processing 3D image volumes into volumetric renders using make_montage().

SO MANY OTHERS! While this is a list of packages I must use regularly, I have become increasingly dependent on invoking new models on the fly, as needed. For example, I wanted to draw arcs between two locations on the globe, but wanted to ensure they followed the shortest path (geodesic distance). I could have spend a few hours coding a custom implementation of the great circle calculations, but instead I find a user-friendly package that had already done the hard work. 


# Procedure:

### PIP-alone method:

- Find the blender Python installation in the Blender Directory.
- Open Blender’s Python in a terminal
- Ensure that PIP is installed (Python’s package manager)
- Pip install your needed packages. 

This is fairly straightforward, and seems to work well for most people. If you’re only using Python through Blender, then this is probably going to be the easiest and most stable route. As you install new versions of Blender, it should be possible to continue to use your older Python environment, until Blender changes which Python version it uses. 

In my case, since I have several local Python installations, and many Anaconda environments, eventually pip became confused when trying to install new packages. It would check my site packages, see that a module was already installed, and not install it. Then the package would not be importable in Blender. This method may break if your Python hygiene is like mine.


### Virtual environment method (Anaconda): 


Special thanks to Forrest Colman at the Allen Institute for pushing me in this direction. It is more complicated to get up and running initially, but for the moment, it seems to be more stable and easier to add new packages as needed. 

- Download a recent version of Blender - one that you’ll be okay with using for a while. It should be feasible to carry forward your Python environment with future Blender releases, until Blender changes the Python version used in the API. At the time of writing, Blender 3.3.0 comes with Python 3.10.10.
- Download and install Anaconda if not already installed. Open the anaconda prompt, and create a new environment, specifying the version of Python to use as identical to the one of your selected Blender version. 
Conda …. Blender330 python=3.10.10
This tells anaconda to create a new virtual environment, named blender330 and install Python version 3.10.10
[ Activate your conda environment:
Conda activate bender330
Either:
- Install packages one by one as needed:
Conda install pandas
OR
Pip install pandas
OR:
- Install an entire environment at once:
Pip install -r requirements.txt
OR:
Conda install environment.yml
Find your blender Python folder, delete it.
Find your anaconda site packages folder for this specific environment
Create a symbolic link to the environment folder in the Blender python folder. When Blender loads, it will search for Python and be redirected to the virtual environment. 

##### To import a new package
If ever you need to import a new package, you do this through the anaconda console, activate your environment, and use pip or conda to install the package of interest. 


##### Benefits for Devs.
While the added up-front steps make this method more cumbersome to set up, it makes it easier to install new packages in the long run. For my use however, the major benefit comes from being able to use the environment outside of Blender for development. I’ve installed jupyter notebook in my blender330 environment, so I can use a notebook to rapidly develop and test new functions, without running within Blender. Since I use the same environment as Blender, I know that whatever works in my development notebook, will also work once inside Blender.




 


