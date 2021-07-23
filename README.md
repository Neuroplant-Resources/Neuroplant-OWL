# Neuroplant
Analysis code for the lab's neuroplant project. This code analyzes images of chemotaxis assays as part of the [Neuroplant project](http://www.neuroplant.org/). There are 2 python files and a .yml file:
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
The Worm Counter GUI allows users to automate the counting of C. elegans on a 4 well plate. The algorithm will detect up to 4 assay plates in any configuration. To ensure that the algorithm provides accurate counts for your images, be sure to follow the instructuions in the [image capture workflow](https://docs.google.com/document/d/1WqvyStj1oJBW2A7Xqlo0mq0W0xOidGS7VAgk4tvFv_Y/edit?usp=sharing). Additionally, be sure to set up a metadata sheet so that you can link the data (compound, strain, plate ID, etc.) that is respective to both the plate and the image. Most importantly, be sure to note the plate ID and it's location on the scanner. See the example below:

| Date   | Plate ID     | Compound Well A | Compound Well B | Compound Well C | Compound Well D | Strain | Scanner Location |
|------  |-------       |-----------------|-----------------|-----------------|-----------------|--------|------------------|
|07/21/21|NPP_202108_003| Diacetyl        | DMSO            | 2-nonanone      | Empty           | N2     | 1                  


#### Welcome Window: This is where you will choose to process a single image or a batch of images. 
Just click on the radio button that matches your needs:
* Single Image 
* Batch

#### Single Image Processing
1. Metadata: There are text fields to enter some of metadata to be included in the results that are returned to the user. These text fields are ...not mandatory... 
1. Results Folder: The user is required to choose a folder to store the analysis results in. Click the 'Browse' button and navigate to the desired folder. ...The user should not store the results in the repository folder...
1. Image File: The user is required to choose an image file to analyze. Click 'Browse' and select the desired image file.
1. Click 'Analyze'
1. The results will be stored as a .csv file in the folder chosen and will be named with the title of the image file selected: Choosen_image.csv

#### Batch Image Processing
1. Results Folder: The user is required to choose a folder to store the analysis results in. Click the 'Browse' button and navigate to the desired folder.
1. Image Folder: The user is required to choose a folder containing images to analyze. Click 'Browse' and select the desired folder. The code will detect and analyze all files ending in .tif
1. Click 'Analyze'


#### Analysis
You can monitor the progress of your analysis in the Terminal or PowerShell/Command Prompt window. Each image takes approximately 30 seconds to analyze. Once the analysis is complete, you will be returned to the 'Welcome Window.' Here you can choose to analyze more images or simply 'Exit' the program. 

#### Compare the results with your images
It is always a good idea to check that the returned results are accurate. If the images don't appear to match the results, see below for common problems and troubleshooting tips.

## Troubleshooting

#### The number of worms counted during the analysis is less than the number on the assay plate.
1. This problem often arises due to a low contrast image. To fix this, you can manually adjust the image contrast and/or brightness.
1. The assay plate may not have been placed properly on the scanner glass. Unfortunately there isn't anything that will fix this and the assay plate must be counted manually.
1. Clumping of worms. This can occur from adding too many worms to the assay plate or not drying the worms after dispensing them onto the plate. Sometimes the worms just aggregate. An update is coming shortly to handle the clumping phenomenon.

#### The Chemotaxis Index (CI) doesn't match the trend I see on the assay plate.
1. Check to see that the plate is oriented correctly in the image. It is easy to place the plate on the scanner incorrectly. If the orientation of the compound and solvent are not in the correct place (Compound/Left : Solvent/Right) then the sign of the CI will be flipped (+/-).
1. This may occur due to clumping or any of the common problems mentioned above.

#### The code was unable to identify my image file.
1. Check that you scanned and saved your image file in the .tif file format.
1. Check that you choose the correct folder.

 

<!---
Google drive API tutorial: https://codelabs.developers.google.com/codelabs/gsuite-apis-intro/
try pydrive instead?
 --->
