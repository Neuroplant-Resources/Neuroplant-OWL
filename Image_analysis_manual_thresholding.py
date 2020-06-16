#!/usr/bin/env python
# coding: utf-8

# ## Load Libraries

# In[1]:


import pandas as pd
import time
import skimage
from skimage import io
from skimage import feature
from skimage import morphology
from skimage import measure
from skimage import exposure
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy import ndimage as ndi
import numpy as np
import pathlib as plb
import csv 



def load_image_data(data_location, prefix, plate_id):

    
    fin_file = data_location.joinpath(prefix + '_fin' + plate_id + '.tif' )
    fin_image = skimage.io.imread(fin_file)

    return fin_image


# In[3]:


def get_plate_id(slot, image_pointer, img_metdat):
    file_name = image_pointer.resolve().stem[:] + '.tif'

    if slot == 1:
        data_list = img_metdat.loc[img_metdat['filename'] == file_name, ['slot1_plate', 'slot1_compound' ]].values.flatten().tolist()
        plate = data_list[0]
        compound = data_list[1]
    elif slot == 2:
        data_list = img_metdat.loc[img_metdat['filename'] == file_name, ['slot2_plate', 'slot2_compound' ]].values.flatten().tolist()
        plate = data_list[0]
        compound = data_list[1]
    elif slot == 3:
        data_list = img_metdat.loc[img_metdat['filename'] == file_name, ['slot3_plate', 'slot3_compound' ]].values.flatten().tolist()
        plate = data_list[0]
        compound = data_list[1]
    elif slot == 4:
        data_list = img_metdat.loc[img_metdat['filename'] == file_name, ['slot4_plate', 'slot4_compound' ]].values.flatten().tolist()
        plate = data_list[0]
        compound = data_list[1]
        
    return plate, compound


# In[4]:


def get_strain(prefix, well_id, batch_dat):
    if well_id == 'P':
        strain_l = batch_dat.loc[batch_dat['dates_modified'] == prefix, ['strain_wellP']].values.flatten().tolist()
        strain = strain_l[0]
    elif well_id == 'Q':
        strain_l = batch_dat.loc[batch_dat['dates_modified'] == prefix, ['strain_wellQ']].values.flatten().tolist()
        strain = strain_l[0]
    elif well_id == 'R':
        strain_l = batch_dat.loc[batch_dat['dates_modified'] == prefix, ['strain_wellR']].values.flatten().tolist()
        strain = strain_l[0]
    elif well_id == 'S':
        strain_l = batch_dat.loc[batch_dat['dates_modified'] == prefix, ['strain_wellS']].values.flatten().tolist()
        strain = strain_l[0]
        
    return strain


# ## Cropping images
# 1. Cropping to individual plates
# 2. Cropping to individual wells.
# 3. The location of the plates on the scanner has important implications to how the wells are cropped. The outer edges of the plates have more 'dead' space in the images and need to be cropped to avoid bias relative to the center of the plate.

# In[5]:


def crop_to_one_plate(fin_image, slot_id):
    # select bounds of the slot we're working on now
    if slot_id == 1:
        upper_boundary = 220
        lower_boundary = 6246
        left_boundary = 6140
        right_boundary = 10144
    elif slot_id == 2:
        upper_boundary = 220
        lower_boundary = 6246
        left_boundary = 1484 
        right_boundary = 5488
    elif slot_id == 3:
        upper_boundary = 6940
        lower_boundary = 12966
        left_boundary = 1484
        right_boundary = 5488
    elif slot_id == 4:
        upper_boundary = 6940
        lower_boundary = 12966
        left_boundary = 6140
        right_boundary = 10144
    else:
        raise ValueError('Lane label not recognized.')

    fin_image = fin_image[upper_boundary:lower_boundary, left_boundary:right_boundary]
    
    return fin_image


# In[6]:


def left_crop_to_one_well(fin_image, well_id):
    # select bounds of the lane we're working on now
    Left_boundary = 300
    Right_boundary = 3724
    if well_id == 'P':
        Upper_boundary = 265
        Lower_boundary = 1415
    elif well_id == 'Q':
        Upper_boundary = 1725
        Lower_boundary = 2875
    elif well_id == 'R':
        Upper_boundary = 3165
        Lower_boundary = 4315
    elif well_id == 'S':
        Upper_boundary = 4615
        Lower_boundary = 5765
    fin_image = fin_image[ Upper_boundary:Lower_boundary ,Left_boundary:Right_boundary ]

    
    # Crop larger image to make before and after images the same size
    #x_min = 0
    #x_max = fin_image.shape[1]
    
    #y_min = 100
    #y_max = 3790 # min(pre_image.shape[0], fin_image.shape[0])
    
    #fin_image = fin_image[y_min:y_max, x_min:x_max]
    
    return fin_image

def right_crop_to_one_well(fin_image, well_id):
    # select bounds of the lane we're working on now
    Left_boundary = 190
    Right_boundary = 3614
    if well_id == 'P':
        Upper_boundary = 265
        Lower_boundary = 1415
    elif well_id == 'Q':
        Upper_boundary = 1725
        Lower_boundary = 2875
    elif well_id == 'R':
        Upper_boundary = 3165
        Lower_boundary = 4315
    elif well_id == 'S':
        Upper_boundary = 4615
        Lower_boundary = 5765
    fin_image = fin_image[ Upper_boundary:Lower_boundary , Left_boundary:Right_boundary ]
    
    return fin_image


# ### Find worms

# In[7]:


def find_worms(fin_image):
    feature_find_start = time.time()
    
    mask = fin_image > 55
    masked_image = fin_image  * mask
    
    ## Subtract background
    #bkg_subtract = np.subtract(pre_image.astype('int16'),
    #                           fin_image.astype('int16'))
    
    bkg_subtract = masked_image - fin_image
    bkg_subtract[bkg_subtract < 0] = 0
    #bkg_subtract = bkg_subtract.astype('uint8')
 
    
    ## Threshold to get binary image
    thresh = skimage.filters.threshold_otsu(fin_image)
    binarized = bkg_subtract < thresh
    #print('Binarization threshold is', str(thresh))

    ## Find features in binary image
    labeled_array, num_features = ndi.label(binarized)
    all_regions = measure.regionprops(label_image=labeled_array, intensity_image=fin_image,
                                      coordinates='rc')

    filtered_regions = []
    for region in all_regions:
        area = region.area

        if area >= 100 and area <=1000 and region.major_axis_length < 120:
            filtered_regions.append(region)
            
#     print('Worm finding and filtering took', str(int(time.time() - feature_find_start)), 'seconds.')
    return filtered_regions


# ### Save worm locations

# In[8]:


def save_worm_locations(filename, worms):
    with open(filename, 'w', newline='') as csvfile:
        worm_writer = csv.writer(csvfile, delimiter=',')
        worm_writer.writerow([' ','X','Y']) # header row

        worm_num = 1
        for worm in worms:
            worm_writer.writerow([worm_num, worm.centroid[1], worm.centroid[0]])
            worm_num += 1


# ### Calculate Chemotaxis Index

# In[9]:


def calc_chemotaxis_index(worm_regions):
   
    ## Assign features to zones of the plate
    left_area_boundary = int(3424*4/9) #8000
    right_area_boundary = int(3424*5/9)

    left_side_worms = [worm for worm in worm_regions if worm.centroid[1] <= left_area_boundary]
    middle_worms = [worm for worm in worm_regions 
                    if worm.centroid[1] > left_area_boundary and worm.centroid[1] < right_area_boundary]
    right_side_worms = [worm for worm in worm_regions if worm.centroid[1] >= right_area_boundary]

    ## Calculate chemotaxis index
    worms_in_left_region = len(left_side_worms)
    worms_in_middle_region = len(middle_worms)
    worms_in_right_region = len(right_side_worms)
    total_worms_found = len(worm_regions)
    #print('Left; ' + str(worms_in_left_region) + '   Right: ' + str(worms_in_right_region))
    
    chemotaxis_index = ((worms_in_left_region - worms_in_right_region) 
                        / (worms_in_left_region + worms_in_right_region))
  
    x_coords = []
    y_coords = []
    for worm in worm_regions:
        x_coords.append(worm.centroid[0])
        y_coords.append(worm.centroid[1])

    centroid = (sum(x_coords)/len(x_coords), sum(y_coords)/len(y_coords))

    return chemotaxis_index, centroid


# In[10]:


def plot_worms(df, fin_image):

    fig, ax = plt.subplots(figsize=(5, 10))

    ax.imshow(fin_image)#[y_min:y_max, x_min:x_max])
    ax.set_title('Worm Locations' +prefix + '_' + plate_id + '_'+ well_id)
    for index, row in df.iterrows():
        minr, minc, maxr, maxc = row['bbox']

        rect = mpl.patches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                                  fill=False, edgecolor='red', linewidth=.5)
        ax.add_patch(rect)
        

# ## Loop through all of the images in the 'Images' folder

def run_loop(img_loc, batch_loc, img_metdat, batch_dat, auto_loc):
    loop_start = time.time()
    results = []
    for image in img_loc.glob('*fin*.tif'): #image_location.glob('scan*Fin.tif'): #
        plate_start = time.time()
        path = image.resolve()
        image_id = image.stem
        prefix = image.stem[0:8]
        suffix = image.stem[12:]
        bins = 9
    #    if image.parent.joinpath(prefix + '_' + plate_id + '_pre.tif').exists is False:
    #        raise NameError('No matching pre-image found.')
        
        # Load the entire image
        fin_image = load_image_data(img_loc, prefix, suffix)
        print('Image load took', str(int(time.time()-plate_start)), 'seconds.')
        
        
        for i in range(1,5):
            slot_id = i
            fin_cropped_2plate = crop_to_one_plate(fin_image, slot_id) 
            plate_id, compound = get_plate_id(slot_id, path, img_metdat)
            if plate_id == '0':
                break
            else:
                results_list = []
                for well_id in ['P', 'Q', 'R', 'S']:
                    # Process one well at a time
                    if slot_id == 1 or slot_id == 4:
                        cropped_fin_image = right_crop_to_one_well(fin_cropped_2plate, well_id)
                    elif slot_id == 2 or slot_id == 3:
                        cropped_fin_image = left_crop_to_one_well(fin_cropped_2plate, well_id)

                    worms = find_worms(cropped_fin_image)
                    total_worms = len(worms)
                    strain = get_strain(prefix, well_id, batch_dat)
                    # Save the results
                    filename = auto_loc.joinpath(prefix + '_' + plate_id + '_' + well_id + '_automatedCounts' + '.csv')
                    save_worm_locations(filename, worms)

                    # Calculate chemotaxis index and gather into a dataframe
                    if total_worms == 0:
                        chemotaxis_index = 'NA'
                        results_dict = {'Date' : prefix,
                                    'Filename': image_id,
                                    'Well_id': well_id,
                                    'Plate_id': plate_id,
                                    'Strain_id' : strain,
                                    'Compound_id' : compound,
                                    'Total_Worms' : total_worms,
                                    'Bin#' : bins,
                                    'chemotaxis_index': chemotaxis_index,
                                    'centroid_x': centroid[1],
                                    'centroid_y': centroid[0]}
                        results_list.append(results_dict)
                        results.append(results_dict)

                        props = ['area', 'convex_area', 'bbox', 'centroid']
                        worm_df = pd.DataFrame([{prop: getattr(reg, prop) for prop in props} for reg in worms])
                    
                    else:

                        chemotaxis_index, centroid = calc_chemotaxis_index(worms)
                        results_dict = {'Date' : prefix,
                                        'Filename': image_id,
                                        'Well_id': well_id,
                                        'Plate_id': plate_id,
                                        'Strain_id' : strain,
                                        'Compound_id' : compound,
                                        'Total_Worms' : total_worms,
                                        'Bin#' : bins,
                                        'chemotaxis_index': chemotaxis_index,
                                        'centroid_x': centroid[1],
                                        'centroid_y': centroid[0]}
                        results_list.append(results_dict)
                        results.append(results_dict)

                        props = ['area', 'convex_area', 'bbox', 'centroid']
                        worm_df = pd.DataFrame([{prop: getattr(reg, prop) for prop in props} for reg in worms])

                    #plot_worms(worm_df, cropped_fin_image)

                #results_df = pd.DataFrame(results_list)
                #results_df.to_csv(path_or_buf=results_location.joinpath(prefix + '_' + plate_id + '_chemotaxis_summary.csv'))


                print('Finished', plate_id,'in', str(int(time.time()-plate_start)), 'seconds.')
        all_results_df = pd.DataFrame(results)
        all_results_df.to_csv(path_or_buf=auto_loc.joinpath('analysis_summary.csv'))
            # results_df = pd.DataFrame(results_list)
            # results_df.to_csv(path_or_buf=base_folder.joinpath('chemotaxis_summary.csv'))
    print('Finished everything in', str(int(time.time()-loop_start)), 'seconds.')




