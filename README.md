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



## Unblinding your Metadata Sheet
The Worm Counter GUI allows users to unblind their metadata sheets. Rather than manually unblinding the metadata sheet, users can record their blinding information that consists of the blinded names and actual names into the 'blinding key' sheet that is provided below, enter the blinding key and the metadata sheet into the unblinding page of the GUI, and obtain the unblinded verison of their metadata. Depending on the users needs, the GUI gives the options to unblind the compound names, the strain names, or both. 
The following link is the google sheet of the blinding key template. Users should make a copy of this template to make edits on their local device, enter the blinded names and actual names of the compounds and/or strains, and download it as csv file.
The blinding key template: (https://docs.google.com/spreadsheets/d/1XUiqgqrw89kvR9hmZIWSK4jBfCoYfG0F9WB4e3YIkN0/edit?usp=sharing)
The unblinding page is designed to have both the metadata sheet and the blinding key in csv format. Users should ensure that the type of their documents are csv files.

## Adding Time Points to your Batch Results File
If you have done time lapse analysis and would like to do data visualisations with the time points, you may add a time points collumn to your batch results file (the file that gets produced from the image analysis). To do so, please insert your batch results file, the time points key file, which matches the filename with the time point, and the name you would like the new batch results file which has a time points collumn to have. Users should make a copy of the time points key template to make edits on their local device, and enter the filename and the corresponding time point. 
The time points key template: (https://docs.google.com/spreadsheets/d/1TMy_FJ-7xEaRHS1HiiJfOHE9yI8LHBTdbuKqjPxzTB8/edit?usp=sharing)

## Data Visualisation

The Worm Counter GUI allows users to do data visualisations using the location files and the batch results file that gets generated from the image analysis. Estimation plots gets generated and 3 options are offered for the user: shared control estimation plot, 2 group estimation plot, and multi 2 group plots. After choosing which plot the user would like to plot, a new window is created to select the files.

### 1. shared control estimation plot:

    - 3 options as an independent variable are offered for the user: compound, strain, timelapse. 
    - Select your batch results file (the summary file that gets generated from image analysis)
    - Select the folder that contains the corresponding location files (the location files get generated from image analysis)
    - Input the name of your control variable (the rest of the variables in the batch results file are plotted as test variables in comparison with the control variable)
    - If the variable that is not being plotted is also tested with different kinds, you may restrict this variable under one of its conditions. Otherwise please click 'None', if this variable is the same across all rows. For example, if compound is your independent variable where DMSO is tested with different compounds, and the only strain that is used is N2, you should click 'None'. However, if different strains are also used while testing the different compounds, and if you would like to restrict the visualisation under one type of strain, please click strain, and input the name of the strain variable. There are 4 options to restrict under: None, Compound, Strain, Both. A user must click an option to continue. 
    - If you prefer to select the colors of your estimation plot, you may use the color key. Please click 'Yes' and input a colors key. The color key matches the name of the variable with the color you select for it from the pull down bar. Please input all the variables that are in the batch results file that will be plotted into the color key (for example, if your independent variable is compound, please input all the compound types on your batch results file into the color key and select a color). If you would prefer not to select your colors, you may click 'No'. If your visualisation labels include both strain and compound, please name your variables in the format: compound_strain in the colors key. compound_strain names appear when restircting a variable. please make sure that the inpendent variable is written in lowercase in the colors key and the restricted variable in the way it appears in the batch results file. For example, if compound is the independent variable, and the strain is restricted under Tax-4 strain, please input the compound names as lowercase and Tax-4 as it appears in the file while inputting the names into the colors key in compound_strain format.
    - If you would like to save your plot as a pdf file, you may click 'Yes' and make the selections for which file to save the plot and the name of the plot. 
    - the number of wells that didnt pass quality control and the number of wells that pass quality control that are used in data visualisation get printed in the terminal.
    
The color key template: (https://docs.google.com/spreadsheets/d/1xdAJYOK26fsM8uFkZXIBNLxrziE9vB7q0AoK1pYCyWI/edit?usp=sharing)
Color options on matplotlib: (https://matplotlib.org/2.0.2/mpl_examples/color/named_colors.pdf)
    - Click 'Do Data Viz' to see your plot generated.
    
2. 2 group estimation plot:

    - 3 options as an independent variable are offered for the user: compound, strain, timelapse. 
    - Select your batch results file (the summary file that gets generated from image analysis)
    - Select the folder that contains the corresponding location files (the location files get generated from image analysis)
    - Input the name of your control variable 
    - Input the name of your test variable 
    - Click 'Do Data Viz' to see your plot generated.
    
3. Multi 2 group plots:

- If you have a reference condition that has 2 changing variables, and a comparison factor that is the indepdendent variable, you may use this option. This option generates 2 plots: 2 shared control plots next to each other, where the comparison factor (the indepdent variable) is restricted under each reference condition, and a multi-2 group plot that compares each of the comparison factor under the 2 reference conditions. If you have compound as your indepdent variable, and you have used 2 kinds of strains, if you would like to see how the compounds behave under each strain and if you would like to compare a compound under the 2 strain conditions, you can use this option. 
- IMPORTANT NOTE FOR MULTI-2 GROUP PLOTS: please input the names of the variables into the GUI as they appear in the batch results file. Please input the names into the colors key as compound_strain format and keep the names as they are in the batch results file. If dmso and N2 appear as DMSO and N2 in the batch results file, you should input the name as DMSO_N2 into the colors key. 

    


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
