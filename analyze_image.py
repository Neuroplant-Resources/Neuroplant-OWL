import pandas as pd
import time
import scipy.stats as stats
from scipy import ndimage as ndi
import numpy as np
import pathlib as plb
from os import path
import csv
import numpy as np
from skimage import feature
from skimage import exposure
from skimage.io import imread
from skimage.util import crop
from skimage import data
from skimage.filters import threshold_otsu, threshold_li
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops, regionprops_table
from skimage.morphology import closing, square, remove_small_objects
import connect_metadata
import tkinter as tk
import tkinter.ttk as ttk
import time
import glob
from PySimpleGUI import popup
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

def dpi2mm(dpi):
# 1 inch = 25.4mm
    px_mm = 1200/25.4
# 1200 pixels per 25.4mm
    mm = (-(dpi/px_mm)+32.5)
#mm_df = ref_df.apply(lambda x: -(x/px_mm)+32.5)
    return mm


def calc_chemotaxis_index(filtered_worm, dims):
    
    ## Assign features to zones of the plate
    left_area_boundary = int(4/9*dims[1])#int(3424*4/9) #8000
    #print(left_area_boundary)
    right_area_boundary = int(5/9*dims[1])#int(3424*5/9)
    #print(right_area_boundary)

    left_side_worms = filtered_worm[filtered_worm['X'] <= left_area_boundary]
    middle_w = filtered_worm[filtered_worm['X'] < right_area_boundary]
    middle_worms = middle_w[middle_w['X'] >left_area_boundary]
    right_side_worms = filtered_worm[filtered_worm['X'] >= right_area_boundary]

    ## Calculate chemotaxis index
    worms_in_left_region = len(left_side_worms)
    worms_in_middle_region = len(middle_worms)
    worms_in_right_region = len(right_side_worms)
    total_worms_found = len(filtered_worm)


    try:
        chemotaxis_index = ((worms_in_left_region - worms_in_right_region)
                        / (worms_in_left_region + worms_in_right_region))
        return chemotaxis_index

    except ZeroDivisionError:
        return 0

def assay_qc(total_worms):
    if total_worms < 150:
        return 'N'
    else:
        return 'Y'
    
def slots_wells(row):
    row['Slot'] = row['WellNo'][0]
    row['Well'] = row['WellNo'][1]
    return row

### This function is called when the user clicks the "Analyze" button on the Single Image GUI window
def single_process(image_fpath, rslt_path, vals, event):
    image_folder = plb.Path(image_fpath)
    results_folder = plb.Path(rslt_path)
    fname = image_folder.stem
    results = crop_image(image_folder, results_folder, vals, event)
    if results.empty:
        results.to_csv(path_or_buf= results_folder.joinpath(fname + '.csv'))
    else:
        results.drop(['centroid-0', 'centroid-1', 'bbox-0', 'bbox-1', 'bbox-2', 'bbox-3', 'area'], axis=1, inplace=True)
        results.to_csv(path_or_buf= results_folder.joinpath(fname + '.csv'))
        



        

### This function is called when the user clicks the "Submit" button in the Batch Process window
def batch_process(image_fpath, rslt_path, mdpath, vals, event, results_name):


    results_df = pd.DataFrame()

    for image in image_fpath.glob('[!._]*.tif*'):

        fname = image.stem
        print('Processing image ID ' + fname)
        pattern = '^[a-zA-Z]'
        image_data = crop_image(image, rslt_path, vals, event)

        results_df = results_df.append(image_data)
        print(fname + ' processed')


    if path.exists(mdpath):
        connected = connect_metadata.connect(mdpath, results_df)
    elif (path.exists(mdpath) == False) and (len(mdpath) > 0):
        popup('File path to metadata invalid. Metadata will not be connected.')
        connected = results_df
    else:
        connected = results_df
 
    
    ### Ensuring that the file is named correctly
    substring = '.csv'
    if substring in results_name:
        results_file = results_name
    else:
        results_file  = results_name + substring

    if connected.empty:
        connected.to_csv(path_or_buf= results_folder.joinpath(results_file))
    else:
        connected.drop(['centroid-0', 'centroid-1', 'bbox-0', 'bbox-1', 'bbox-2', 'bbox-3'], axis=1, inplace=True)
        connected.to_csv(path_or_buf= rslt_path.joinpath(results_file))




   


### loopwell() is called after the image has been cropped
### This is when the worms are identified, counted and when the CI is calculated
def loopWell(df_f,image, im_path, path_rslt, vals, event):

    for index, row in df_f.iterrows():

        
        fin_image = image[ df_f['bbox-0'][index]:df_f['bbox-2'][index], df_f['bbox-1'][index]:df_f['bbox-3'][index]]
        wellno = df_f['WellNo'][index]
        image_dims = fin_image.shape
        
        compound_key = '-Compound' + wellno[0] + '-'
        strain_key = '-Strain' + wellno[0] + '-'
        pid_key = '-PID' + wellno[0] + '-'
        plate_id = vals.get(pid_key)
        compound = vals.get(compound_key)
        strain = vals.get(strain_key)
        image_fname = im_path.stem
        rslts_fldr = plb.Path(path_rslt)
        
        thresh = threshold_otsu(fin_image)
        binarized = fin_image > thresh
        #imshow(binarized)
        
        ## Find features in binary image
        labeled_array, num_features = ndi.label(binarized)
        props_worm = regionprops_table(label_image=labeled_array, properties=('label','centroid', 'area'))
        worms=pd.DataFrame(props_worm)
        worms = worms.rename(columns= {'centroid-0': 'Y', 'centroid-1':'X'})
        
        # label image regions

        filt_worm=worms[worms['area']<2500]
        filtered_worm=filt_worm[filt_worm['area']>50]
        filtered_worm.to_csv(rslts_fldr.joinpath('loc_' + image_fname + '_' +  wellno + '.csv'))

        
        tw = len(filtered_worm)
        CI = calc_chemotaxis_index(filtered_worm,image_dims)
        qc = assay_qc(tw)
        mean = filtered_worm.X.mean()
        mean_mm = dpi2mm(mean)


        df_f.loc[index, 'File Name'] = image_fname
        df_f.loc[index, 'Well width'] = image_dims[1]
        df_f.loc[index, 'Plate ID'] = plate_id
        df_f.loc[index, 'Chemotaxis'] = CI
        df_f.loc[index, 'Total Worms'] = tw
        df_f.loc[index, 'Passes QC'] = qc
        df_f.loc[index, 'Compound'] = compound
        df_f.loc[index, 'Strain'] = strain
        df_f.loc[index, 'Mean Position'] = mean_mm


    return df_f




def crop_image(flpath, rslt_path, vals, event):

    label_begin = time.time()
    image = imread(flpath)
    image_nvrt = np.invert(image)
    
    # apply threshold
    thresh = threshold_otsu(image_nvrt)
    print('Threshold: ' + str(thresh))

    bw = closing(image_nvrt > thresh, square(3))
    
    # remove artifacts connected to image border
    cleared = clear_border(bw)
    #cleared = remove_small_objects(clear_border(bw))

  #  update_progressbar(self1)

    # label image regions
    label_image = label(bw)
    print('Feature finding and labeling took ', str(int(time.time() - label_begin)), 'seconds.')
    #image_label_overlay = label2rgb(label_image, image=image, bg_label=0)
  #  update_progressbar(self1)
    
    props = regionprops_table(label_image, properties=('label','centroid', 'bbox', 'area'))
    dff=pd.DataFrame(props)

    df_area = dff.sort_values(by=['area'], ascending=False)
    image_center = (int(label_image.shape[1]/2),int(label_image.shape[0]/2))


    wells = df_area[(df_area.area>= 2000000) & (df_area.area<=2500000)]
    wells=wells.sort_values(by=['bbox-1'])
    print('Number of wells: ' + str(len(wells)))
#    update_progressbar(self1)

    wells.reset_index(drop=True, inplace=True)

    # Sort the plates into the left and right
    mask1 = wells['bbox-1'] > image_center[0]
    df_r = wells[mask1]
    df_l = wells[~mask1]

    ## Split the right plates to upper (#1) and lower (#4)
    dffr=df_r.sort_values(by=['bbox-0'])
    dffr.reset_index(drop=True, inplace=True)


    mask2 = df_r['bbox-0'] > image_center[1]
    dff4 = df_r[mask2]
    dff1 = df_r[~mask2]

    ### Sort the wells on each plate
    df1=dff1.sort_values(by=['bbox-0'])
    df4=dff4.sort_values(by=['bbox-0'])
    df4.reset_index(drop=True, inplace=True)
    df1.reset_index(drop=True, inplace=True)

    ## Split the left plates to upper (#2) and lower (#3)
    dffl=df_l.sort_values(by=['bbox-0'])
    dffl.reset_index(drop=True, inplace=True)

    #MinCol2=1.05*list(dffl.items())[3][1][3]
    mask = df_l['bbox-0'] > image_center[1]
    dff3 = df_l[mask]
    dff2 = df_l[~mask]

    ### Sort the wells on each plate
    df2=dff2.sort_values(by=['bbox-0'])
    df3=dff3.sort_values(by=['bbox-0'])
    df3.reset_index(drop=True, inplace=True)
    df2.reset_index(drop=True, inplace=True)

    ## Update the label of each well
    new_label_1 = pd.Series(['1A', '1B','1C','1D'], name='label', index=[0,1,2,3])
    df1.update(new_label_1)

    new_label_2 = pd.Series(['2A', '2B','2C','2D'], name='label', index=[0,1,2,3])
    df2.update(new_label_2)

    new_label_3 = pd.Series(['3A', '3B','3C','3D'], name='label', index=[0,1,2,3])
    df3.update(new_label_3)

    new_label_4 = pd.Series(['4A', '4B','4C','4D'], name='label', index=[0,1,2,3])
    df4.update(new_label_4)


    ### Append the dataframes
    df_f=df1.append(df2, ignore_index=True).append(df3, ignore_index=True).append(df4, ignore_index=True)
    df_f["Total Worms"],df_f["Chemotaxis"], df_f["Compound"], df_f["Strain"] = [np.nan,np.nan,np.nan,np.nan]

    df_f = df_f.rename(columns={'label': 'WellNo'})
    df_f.apply(lambda row: slots_wells(row), axis=1)

    results_df = loopWell(df_f, image, flpath, rslt_path, vals, event)
    #results_df = loopWell(df_f, image, flpath, rslt_path, vals, event, self1)
    return results_df
    
        #save_worm_locations(df_f,filtered_worm,path_rslt,label)
        

    

#class App(tk.Tk):
#
#    def __init__(self):
#        tk.Tk.__init__(self)
#        self.title('Progress Bar')
#        self.label1 = tk.Label(self, text = 'Processing Image Files', width = 20, height = 1, fg = 'yellow', bg = 'purple').pack(padx=10, pady = 10)
#        self.progressbar1 = ttk.Progressbar(self, orient = 'horizontal', length = 400)
#        self.progressbar1.pack(padx=10, pady=10)
#        self.label2 = tk.Label(self, text = 'Analysing One Image', width = 20, height = 1, fg = 'yellow', bg = 'purple').pack(padx=10, pady = 10)
#        self.progressbar2 = ttk.Progressbar(self, orient = 'horizontal', length = 400)
#        self.progressbar2.pack(padx=10, pady=10)
#        self.button = tk.Button(self, text = 'OK', command = self.destroy)
#        self.button.pack(padx=10, pady=10)
#
#
#
#def update_progressbar(self):
#    #time.sleep(1) #delay
#    self.progressbar2['value'] += 20
#    self.update_idletasks() #updating the window each time to see the gradual progress
