# Neuroplant
Analysis code for the lab's neuroplant project. This code analyzes images of chemotaxis assays as part of the [Neuroplant project]{http://www.neuroplant.org/}. There are three jupyter notebooks:
* Neuroplant image analysis: Finds worms and calculates the chemotaxis index. Saves a csv file with the locations of the worms and a csv file with a summary of the results for each plate.
* Manual analysis comparisons: Compares results from the automated analysis and manual analysis.
* Plot chemotaxis results: Plots the results of the automated analysis.

## Getting started
Installing and running the code requires some knowledge of using github, conda, jupyter notebook, and python.

1. Clone the github repo: Next, you need to download the code to your computer. If you do so by [cloning this github](https://help.github.com/en/articles/cloning-a-repository), you'll be able to keep your code updated with the latest edits using git.
1. Install conda environment: To use the code, you first need to install the software libraries it uses. To do so, you must [install conda](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html) first. Use the `neuroplant_conda_env.yml` file to recreate the software libraries needed for running the code. To do so, open a terminal, navigate to the cloned git repo and run the command:
   ```
   conda env create -f neuroplant_conda_env.yml
   ```
   This will create a conda environment called `neuroplant` that has all the packages for running the analysis code.

1. Launch juptyer notebook: Navigate to the location of the github repo, activate the conda environment, and launch jupyter notebook. This enables you to actually run the code.
   ```
   cd /path/to/repo/Neuroplant
   conda activate neuroplant
   jupyter notebook
   ```
1. Update file locations: The first step in actually using the code is to update the location where the image files are stored at the top of the notebook. This tells the code where to look for images. You also need to specify where you want results to be saved. These locations should be different from the location of the cloned git repository. Update these file paths in the cell near the top of the jupyter notebook where they are specified.

<!---
Google drive API tutorial: https://codelabs.developers.google.com/codelabs/gsuite-apis-intro/
try pydrive instead?
 --->
