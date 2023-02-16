.. geospatial-analysis documentation master file, created by
   sphinx-quickstart on Wed Feb 15 10:05:00 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the documentation for geospatial analysis!
*****************************************************

To get started with using Python to analyze geospatial data and plan the perfect route to your destination, this documentation provides a step-by-step guide to the process. With increasing traffic and environmental concerns, cycling and walking have become a popular mode of transportation, and finding the most efficient and enjoyable route can be a challenge. By using geospatial data and Python, you can easily find the best bike route to your office building or any other destination.

How to install required packages
================================
1. Either install a Python IDE or create a Python virtual environment with Conda to install the packages required
2. Install packages required, you can use the provided requirements.txt file
3. Use the different clases to calculate your prefered route

Installation
------------
Configure project environment (Either A. Install an IDE OR B. Create a Virtual Environment)
	A. Install an IDE such as Pycharm (www.jetbrains.com/pycharm/download/)
	
        - Open the script file folder
		
        - Configure the Base Project Interpreter (File -> Settings -> Project Interpreter) Base Project Interpreter: pyenv version 3.9.13 (pyenv was installed before creating the new project through 'pyenv install 3.7.0')
		
            .. note:: In my case, when I tried to install the requirements, my whole enviroment was messed up. 
			
        - Manually install packages to project interpreter (Pycharm -> Preferences -> Project -> Project Interpreter -> plus button on the lower left side of the package table) and apply changes OR type the command below on the activated virtual environment. 
		
		.. code-block:: console

			pycharm install -r requirements.txt
		
	B. Install Conda (https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
	
		1. Either create a new Conda environment or use an existing one
		
		.. code-block:: console

			conda create --name myenv python=3.9

		2. Activate the conda environment:
		
		.. code-block:: console

			conda activate myenv
		
		3. Install requirements using the provided requirements.txt file
		
		.. code-block:: console
		
			conda install --file requirements.txt			
		
Use the different classes to calculate your preferred route.

Documentation for the classes
=============================
.. toctree::
    :maxdepth: 2
    :caption: contents:

    loadWFS
    cityroute

loadWFS
=======
.. autoclass:: loadWFS.loadWFS
   :members:

cityroute
=========
.. autoclass:: cityroute.cityroute
   :members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Documentation
=============

    - Checkout`Spinx-doc <https://www.sphinx-doc.org/en/master/index.html>`_ to learn how to document this repo using Sphinx.

