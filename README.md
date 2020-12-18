# Neuroplant
Analysis code for the lab's neuroplant project. This code analyzes images of chemotaxis assays as part of the [Neuroplant project]{http://www.neuroplant.org/}. There are 2 python files and a .yml file:
* wormGUI.py: Generates the graphic user interface to analyze chemotaxis images
* analyze_image.py: This is the code that automatically crops the images, identifies and counts worms, and calculates the chemotaxis index.
* simplified_conda_env.yml: Creates the the virtual environment that contains all of the packages needed to run the image analysis code.

## Getting started
Installing and running the code requires some knowledge of using github, conda, jupyter notebook, and python.

1. Clone the github repo: Next, you need to download the code to your computer. If you do so by [cloning this github](https://help.github.com/en/articles/cloning-a-repository), you'll be able to keep your code updated with the latest edits using git.
1. Install conda environment: To use the code, you first need to install the software libraries it uses. To do so, you must [install conda](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html) first. Use the `NP_conda_env.yml` file to recreate the software libraries needed for running the code. To do so, open a terminal, navigate to the cloned git repo and run the command:
   ```
   conda env create -f NP_conda_env.yml
   ```
   This will create a conda environment called `neuroplant` that has all the packages for running the analysis code.

1. Run the wormGUI.py code: Navigate to the location of the github repo, activate the conda environment, and launch jupyter notebook. The following line of code will run each step. Be sure replace the text in the file path to match the location of the repo on your own device.
   ```
   cd /path/to/repo/Neuroplant
   conda activate neuroplant
   python wormGUI.py
   ```
1. The Worm Counter GUI window should appear

1. When finished with the Worm Counter, you should deactivate the virtual environmet. Just input:
	```
	conda deactivate
	```

## Using the Worm Counter GUI
The Worm Counter GUI allows users to automate the counting of C. elegans on a 4 well plate. The algorithm will detect any number of plates up to 4 in any configuration. To ensure that the algorithm provides accurate counts for your images, be sure to follow the instructuions in the [image capture workflow] ...link to workflow...

#### Welcom Window: This is where you will choose to process a single image or a batch of images. 
Just click on the radio button that matches your needs:
* Single Image 
* Batch

#### Single Image Processing
1. Metadata: There are text fields to enter some of metadata to be included in the results that are returned to the user. These text fields are ...not mandatory... 
1. Results Folder: The user is required to choose a folder to store the analysis results in. Click the 'Browse' button and navigate to the desired folder. ...The user should not store the results in the repository folder...
1. Image File: The user is required to choose an image file to analyze. Click 'Browse' and select the desired image file.
1. Click 'Analyze'

#### Batch Image Processing
1. Results Folder: The user is required to choose a folder to store the analysis results in. Click the 'Browse' button and navigate to the desired folder.
1. Image Folder: The user is required to choose a folder containing images to analyze. Click 'Browse' and select the desired folder. The code will detect and analyze all files ending in .tif
1. Click 'Analyze'

#### Analysis
You can monitor the progress of your analysis in the Terminal or PowerShell/Command Prompt window. Each image takes approximately 30 seconds to analyze. Once the analysis is complete, you will be returned to the 'Welcome Window.' Here you can choose to analyze more images or simply 'Exit' the programm. 

#### Compare the results with your images
It is always a good idea to check that the returned results are accurate. If the numbers don't appear to match the results see below for common problems and troubleshootin tips.

## Troubleshooting


<!---
Google drive API tutorial: https://codelabs.developers.google.com/codelabs/gsuite-apis-intro/
try pydrive instead?
 --->
