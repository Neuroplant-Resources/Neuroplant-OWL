# Neuroplant - Our Worm Locator (OWL)
A graphic user interface for analyzing images and generating confidence interval plots associated with the neuroplant project. [Neuroplant project](http://www.neuroplant.org/). 
[![DOI](https://zenodo.org/badge/203633591.svg)](https://zenodo.org/badge/latestdoi/203633591)

## Getting started
Installing and running the code requires some knowledge of using github, virtual environments, and python.

1. Clone the github repo:  [Cloning this github repository](https://help.github.com/en/articles/cloning-a-repository)
1. Create the working environment: To use the code, you first need to install the software libraries it uses. The easiest way to ensure that you have all the required packages is to work with a package manager. 
We recommend using [MiniForge]('https://github.com/conda-forge/miniforge')
[MambaForge]('https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html'), or [MiniConda]('https://docs.conda.io/en/main/miniconda.html'). Anaconda will work too, but it can be slow and it takes up a lot disk space. To create create the environment, open the terminal associated with your package manaager (miniforge prompt, anaconda prompt, etc), navigate to the cloned repository and run the command:
   ```
   cd /path/to/repo/Neuroplant
   conda env create -f NP_conda_env.yml
   ```
You will only need to create the environment once.

## Opening and running the OWL

1. To run the wormGUI.py code: Navigate to the location of the repository, activate the conda environment and run the OWL python file. The following lines of code will run each step. Be sure replace the text in the file path to match the location of the repo on your own device.
   ```
   cd /path/to/repo/Neuroplant
   conda activate neuroplant
   python wormGUI.py
   ```
1. The Worm Counter GUI window should appear

1. When finished with the Worm Counter, simply click the exit button in the GUI. You should also deactivate the virtual environment when you are finished with the GUI. To do so, input the following code into your terminal/prompt:
	```
	conda deactivate
	```

## Using the OWL
The OWL allows users to automate the counting of C. elegans on a 4 well NUNC plate. In addition to counting and locating the worms in an image, the GUI provides data visualization tools for the Neuroplant project.

The algorithm will detect up to 4 assay plates. To ensure that the algorithm provides accurate counts for your images, be sure to follow the instructuions in the [image capture workflow](https://docs.google.com/document/d/1WqvyStj1oJBW2A7Xqlo0mq0W0xOidGS7VAgk4tvFv_Y/edit?usp=sharing). 


### Welcome Window: This is where you will choose to analyze images, unblind your data or generate data visualizations
Select the tool you would like to use from the dropdown menu
* Image analysis
* Unblinding data
* Data visualization


#### Image analysis

1. Image Folder: The user is required to choose a folder containing the images they want to analyze. Click 'Browse' and select the desired folder. The code will detect and analyze all files ending in .tif or .tiff that are contained in the choosen folder.
1. Metadata file: the user is able to connect an assay's metadata to the images being analyzed. Connecting the metadata will populate the summary of the results with the conditions for each of the wells of each assay plate. *The user is required to use the [metadata template](https://docs.google.com/spreadsheets/d/1u8PN5a5s7SFurxspXNJSq5FKKNKTdzFmCgwjjsEf4XE/edit?usp=sharing) to ensure that the accurate transfer of data.*
1. Results Folder: The user is required to choose a folder to store the analysis results in. Click the 'Browse' button and navigate to the desired folder.
1. Click 'Analyze'
1. You can monitor the progress of your analysis in the Terminal or PowerShell/Command Prompt window. Each image takes approximately 30 seconds to analyze. Once the analysis is complete, you will be returned to the 'Welcome Window.' Here you can choose to analyze more images or 'Exit' the program. 
1. Compare the results with your images. It is always a good idea to check that the returned results are accurate. If the images don't appear to match the results, see below for common problems and troubleshooting tips.



## Unblinding your Metadata Sheet
The Worm Counter GUI allows users to unblind their metadata sheets. It is often the case that experimenters blind their data to avoid any bias in obtaining their results. When the experimenter is recording the conditions of each experiment within the metadata, those conditions remain blinded. Thus when the experimenter wants to perform the data analysis it is impossible to determine what the control and test conditions are. Unblinding each row of the metadata sheet is time consuming and inefficient. Rather than manually unblinding the metadata sheet, users can record their blinded data into the 'blinding key'. The blinding key maps the data back to the metadata sheet and an unblinded verison of their metadata is returned. The GUI gives the options to unblind the compound names, the strain names, or both to meet the needs of the screen. 

You can follow [this link to the blinding key template](https://docs.google.com/spreadsheets/d/1XUiqgqrw89kvR9hmZIWSK4jBfCoYfG0F9WB4e3YIkN0/edit?usp=sharing). 
- Users should make a copy of this template to make edits on their local device, enter the blinded names and actual names of the compounds and/or strains, and download it as csv file.

#### Steps for unblinding your data:
1. Choose what type of file to unblind:
    1. Metadata sheet
    1. Image analysis summary file - this is the summary file that is returned in addition to the location files during image analysis. 
1. Choose what condition you would like to unblind:
    1. Strain
    1. Compound
1. Input the location of the file that needs to be unblinded by clicking browse.
1. Input the location of your blinding key.
1. Choose where to store your unblinded file.
1. Name your unblinded file. It is a good idea to give this file a new name to avoid overwriting the original data. 

## Data Visualisation

The OWL allows users to analyze the results of their experiments by generating 95% bootstrapped mean difference confidence intervals. The OWL aggregates all of the worm locations for a given condition. Then, these data are bootstrapped (5000 resamples, seeded for reproducability) to determine the mean difference between the test and the control conditions, in addition to the lower and upper bounds of the confidence interval. Other data returned include the Mann-Whitney U test score. Details for the plots that are generated are below:

#### Shared control estimation plot:

1. Are you performing a between strains or a between compounds analysis? Select the independent variable: Compound or strain. 
1. Select your batch results file (the summary file that gets generated from image analysis). This file is used to link and aggregate the worm positions for each condition.
1. Select the folder that contains the corresponding location files (the location files are generated during image analysis)
1. Input the name of your control condition (Examples: DMSO, Water, N2)
  1. The rest of the conditions in the batch results file will be analyzed against the control.
1. If would like to select the colors for your plots, you have the option to input color values that correspond to your conditions.
  1. Click the "Select Data and Colors" button
  1. A new window will pop up that has a table
  1. Input the condition and the HEX code for the color you would like to use.
  1. Once you have entered all of your conditions and colors, click "Submit." 
1. Choose the type of file you want to save you plot as: PNG, PDF or SVG
1. Choose a location to save your file.
1. Name the file that contains your plot.
1. You can choose to exclude data that does not pass quality control (fewer than 150 worms) by checking the box
1. Click 'Do Data Viz' 
    
#### 2 group estimation plot:
<p> Sometimes we want to quickly check to see how single particular condition compares to the control. To do this we can generate a quick 2 group estimation plot.</p>

1. Select your independent variable : compound or strain
1. Select your summar results file that gets generated during image analysis
1. Select the folder that contains the files of the worm positions the conditions you would like to analyze
1. Input the name of your control variable 
1. Input the name of your test variable 
1. Click 'Do Data Viz' to see your plot generated.
    

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

 

