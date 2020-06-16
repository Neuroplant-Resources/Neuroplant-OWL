
import pandas as pd
import time
import pathlib as plb
import csv 
import Image_analysis_manual_thresholding as iam


def check_num_images(img_loc, batch_loc, img_metdat, batch_dat, auto_loc):
    all_or_none = input('Would you like to analyze all of the images in the Images folder? Y or N: ')
    all_or_none = all_or_none.lower()
    if all_or_none == 'y' or all_or_none == 'yes':
        print('Test')
        iam.run_loop(img_loc, batch_loc, img_metdat, batch_dat, auto_loc)
    elif all_or_none == 'n' or all_or_none == 'no':
        print('To be continued...')
    else:
        print('Please enter a valid response')
        check_num_images()

def main():
  # Create directory to store results to insure that naming conventions are consistent
  current_dir = plb.Path(input('Enter the file path to the folder containing the images and metadata to be analyzed: '))
  
  automated_results_location = current_dir.joinpath('automated_results')
  automated_results_location.mkdir(exist_ok=True, parents=True)


  # In[21]:


  image_location = current_dir.joinpath('Images')
  metadata_location = current_dir.joinpath('metadata')


  # In[22]:


  image_metadata_fname = input('Please enter the filename for the image metadata: ')


  # In[23]:


  batch_metdata_fname = input('Please enter the filename for the batch metadata: ')


  # In[25]:


  image_metadata_path = metadata_location.joinpath(image_metadata_fname)
  batch_metdata_path = metadata_location.joinpath(batch_metdata_fname)


  # In[26]:


  image_metadata = pd.read_csv(image_metadata_path)
  batch_metadata = pd.read_csv(batch_metdata_path)

  image_metadata.rename(columns={'Name of individual capturing image:': 'imager',
                       'Date:': 'date',
                       "Image file name:": 'filename',
                       'Is this the pre or post assay image?': 'pre_fin',
                      'Plate number in slot 1:': 'slot1_plate',
                       'Plate number in slot 2:': 'slot2_plate',
                       'Plate number in slot 3:': 'slot3_plate',
                       'Plate number in slot 4:': 'slot4_plate', 
                                 'Compound in slot 1:': 'slot1_compound', 
                                 'Compound in slot 2:': 'slot2_compound', 
                                 'Compound in slot 3:': 'slot3_compound', 
                                 'Compound in slot 4:': 'slot4_compound',}, inplace=True)

  batch_metadata.rename(columns={'Recorder\'s Name:': 'recorder',
                                'Date:': 'date',
                                 'Temperature:': 'temp',
                                'Humidity:': 'humidity',
                                'Date chemotaxis plates were poured:': 'plates_poured',
                                'Worm Strain in Well P:': 'strain_wellP',
                                'Worm Strain in Well Q:.1': 'strain_wellQ',
                                'Worm Strain in Well R:.1': 'strain_wellR',
                                'Worm Strain in Well S:.1': 'strain_wellS',
                                'dates' : 'dates_modified',}, inplace = True )
  batch_metadata['dates_modified'] = batch_metadata['dates_modified'].astype(str)





  check_num_images(image_location, metadata_location, image_metadata, batch_metadata, automated_results_location)

if __name__ == "__main__":
        main()


