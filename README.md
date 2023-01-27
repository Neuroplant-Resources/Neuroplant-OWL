# Neuroplant - Our Worm Locator (OWL)
A graphic user interface for analyzing images associated with the neuroplant project. This code analyzes images of chemotaxis assays as part of the [Neuroplant project](http://www.neuroplant.org/). 

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

## Using the OWL GUI
The Worm Counter GUI allows users to automate the counting of C. elegans on a 4 well plate. In addition to counting and locating the worms in an image, the GUI provides data visualization tools for the Neuroplant project.

 The algorithm will detect up to 4 assay plates. To ensure that the algorithm provides accurate counts for your images, be sure to follow the instructuions in the [image capture workflow](https://docs.google.com/document/d/1WqvyStj1oJBW2A7Xqlo0mq0W0xOidGS7VAgk4tvFv_Y/edit?usp=sharing). 


### Welcome Window: This is where you will choose to analyze images, unblind your data or generate data visualizations
Select the tool you would like to use from the dropdown menu
* Image analysis
* Unblinding data
* Data visualization


#### Image analysis

1. Image Folder: The user is required to choose a folder containing the images they want to analyze. Click 'Browse' and select the desired folder. The code will detect and analyze all files ending in .tif or .tiff that are contained in the choosen folder
1. Metadata file: the user is able to connect an assay's metadata to the images being analyzed. Connecting the metadata will populate the summary of the results with the conditions for each of the wells of each assay plate. *The user is required to use the metadata template to ensure that the accurate transfer of data.*
1. Results Folder: The user is required to choose a folder to store the analysis results in. Click the 'Browse' button and navigate to the desired folder.
1. Click 'Analyze'


#### Analysis
You can monitor the progress of your analysis in the Terminal or PowerShell/Command Prompt window. Each image takes approximately 30 seconds to analyze. Once the analysis is complete, you will be returned to the 'Welcome Window.' Here you can choose to analyze more image sor simply 'Exit' the program. 

#### Compare the results with your images
It is always a good idea to check that the returned results are accurate. If the images don't appear to match the results, see below for common problems and troubleshooting tips.



## Unblinding your Metadata Sheet
The Worm Counter GUI allows users to unblind their metadata sheets. It is often the case that experimenters blind their data to avoid any bias in obtaining the experimental data. When the experimenter is recording the conditions of each experiment within the metadata, those conditions remain blinded. Thus when the experimenter wants to perform the data analysis it is impossible to determine what the control and test conditions are. Unblinding each row of the metadata sheet is time consuming and inefficient. Rather than manually unblinding the metadata sheet, users can record their blinded data into the 'blinding key'. The blinding key maps the data back to the metadata sheet and users are returned an unblinded verison of their metadata. The GUI gives the options to unblind the compound names, the strain names, or both to meet the needs of the chemotaxis assay. 

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
1. Name your unblinded file. It is a good idea to give this file a new name if you do not want to overwrite the original data. 

## Data Visualisation

The OWL allows users to analyze the results of their experiments by generating 95% bootstrapped mean difference confidence intervals. The mean of the control condition is computed, then the OWL aggregates all of the worm locations for a given condition. These data are then bootstrapped (5000 resamples, seeded for reproducability) to determine mean difference between the test condition and the control, in addition to the lower and upper bounds of the confidence interval. Other data returned include the Mann-Whitney U test score. Details for the plots that are generated are below:

#### Shared control estimation plot:

1. Are you performing a between strains or a between compounds analysis? Select the independent variable: Compound or strain. 
1. Select your batch results file (the summary file that gets generated from image analysis). This file is used to link and aggregate the worm positions for each condition.
1. Select the folder that contains the corresponding location files (the location files are generated during image analysis)
1. Input the name of your control condition (Examples: DMSO, Water, N2)
  1. The rest of the conditions in the batch results file will be analyzed against the control.
1. If the that is not being plotted is also tested with different kinds, you may restrict this variable under one of its conditions. Otherwise please click 'None', if this variable is the same across all rows. For example, if compound is your independent variable where DMSO is tested with different compounds, and the only strain that is used is N2, you should click 'None'. However, if different strains are also used while testing the different compounds, and if you would like to restrict the visualisation under one type of strain, please click strain, and input the name of the strain variable. There are 4 options to restrict under: None, Compound, Strain, Both. A user must click an option to continue. 
1. If you prefer to select the colors of your estimation plot, you may use the color key. Please click 'Yes' and input a colors key. The color key matches the name of the variable with the color you select for it from the pull down bar. Please input all the variables that are in the batch results file that will be plotted into the color key (for example, if your independent variable is compound, please input all the compound types on your batch results file into the color key and select a color). If you would prefer not to select your colors, you may click 'No'. If your visualisation labels include both strain and compound, please name your variables in the format: compound_strain in the colors key. compound_strain names appear when restircting a variable. please make sure that the inpendent variable is written in lowercase in the colors key and the restricted variable in the way it appears in the batch results file. For example, if compound is the independent variable, and the strain is restricted under Tax-4 strain, please input the compound names as lowercase and Tax-4 as it appears in the file while inputting the names into the colors key in compound_strain format.
1. Choose what type of file you want to save you plot as: PNG, PDF or SVG

[The color key template](https://docs.google.com/spreadsheets/d/1xdAJYOK26fsM8uFkZXIBNLxrziE9vB7q0AoK1pYCyWI/edit?usp=sharing)
[Color options on matplotlib](https://matplotlib.org/2.0.2/mpl_examples/color/named_colors.pdf)
1. Click 'Do Data Viz' to see your plot generated.
    
#### 2 group estimation plot:

    - 3 options as an independent variable are offered for the user: compound, strain, timelapse. 
    - Select your batch results file (the summary file that gets generated from image analysis)
    - Select the folder that contains the corresponding location files (the location files get generated from image analysis)
    - Input the name of your control variable 
    - Input the name of your test variable 
    - Click 'Do Data Viz' to see your plot generated.
    



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
