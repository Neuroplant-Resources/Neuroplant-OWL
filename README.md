# Neuroplant
Analysis code for the lab's neuroplant project.

## Getting started
Installing and running the code requires some knowledge of using github, conda, jupyter notebook, and python.

### Install conda environment
To use the code, you first need to install the software libraries it uses. To do so, you must [install conda](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html) first. Use the `neuroplant_conda_env.yml` file to recreate the software libraries needed for running the code. To do so, open a terminal and run the command 
```
conda env create -f neuroplant_conda_env.yml
```

### Clone the github repo
Next, you need to download the code to your computer. If you do so by [cloning this github](https://help.github.com/en/articles/cloning-a-repository), you'll be able to keep your code updated with the latest edits using git.

### Launch juptyer notebook
Navigate to the location of the github repo, activate the conda environment, and launch jupyter notebook. This enables you to actually run the code.

### Update file locations
The first step in actually using the code is to update the location where the image files are stored at the top of the notebook. This tells the code where to look for images. You also need to specify where you want results to be saved. These locations should be different from the location of the cloned git repository.

<!---
Google drive API tutorial: https://codelabs.developers.google.com/codelabs/gsuite-apis-intro/
try pydrive instead?
 --->
