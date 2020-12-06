import pandas as pd
import time
from skimage.io import imread, imshow
from skimage import feature
from skimage import measure
from skimage import exposure
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy import ndimage as ndi
import numpy as np
import pathlib as plb 
import csv

#import seaborn as sns
import matplotlib.patches as mpatches
import numpy as np
from skimage.io import imread
from skimage.util import crop
from skimage import data
from skimage.filters import threshold_otsu, threshold_li
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops, regionprops_table
from skimage.morphology import closing, square, remove_small_objects



def calc_chemotaxis_index(filtered_worm, dims):
    
    ## Assign features to zones of the plate
    left_area_boundary = int(4/9*dims[1])#int(3424*4/9) #8000
    #print(left_area_boundary)
    right_area_boundary = int(5/9*dims[1])#int(3424*5/9)
    #print(right_area_boundary)

    left_side_worms = filtered_worm[filtered_worm['centroid-1'] <= left_area_boundary]
    middle_w = filtered_worm[filtered_worm['centroid-1'] < right_area_boundary]
    middle_worms = middle_w[middle_w['centroid-1'] >left_area_boundary]
    right_side_worms = filtered_worm[filtered_worm['centroid-1'] >= right_area_boundary]

    ## Calculate chemotaxis index
    worms_in_left_region = len(left_side_worms)
    worms_in_middle_region = len(middle_worms)
    worms_in_right_region = len(right_side_worms)
    total_worms_found = len(filtered_worm)
    #print('Left; ' + str(worms_in_left_region) + '   Right: ' + str(worms_in_right_region))

    

    try:
        chemotaxis_index = ((worms_in_left_region - worms_in_right_region) 
                        / (worms_in_left_region + worms_in_right_region))
        return chemotaxis_index

    except ZeroDivisionError:
        return 0
    
def slots_wells(row):
    row['Slot'] = row['WellNo'][0]
    row['Well'] = row['WellNo'][1]
    return row

def loopWell(df_f,image,path_rslt, vals):

    for index, row in df_f.iterrows():

#     fin_image = image[ df_f[][]:Lower_boundary , Left_boundary:Right_boundary ]
        
        fin_image = image[ df_f['bbox-0'][index]:df_f['bbox-2'][index], df_f['bbox-1'][index]:df_f['bbox-3'][index]]
        wellno = df_f['WellNo'][index]
        image_dims = fin_image.shape
        compound_key = '-Compound' + wellno[0] + '-'
        pid_key = '-PID' + wellno[0] + '-'
        plate_id = vals.get(pid_key)
        compound = vals.get(compound_key)
        df_f['Compound'] = compound_key
        print(compound)
        
        thresh = threshold_otsu(fin_image)
        binarized = closing(fin_image > thresh, square(10))
        #imshow(binarized)
        
        ## Find features in binary image
        labeled_array, num_features = ndi.label(binarized)
        props_worm = regionprops_table(label_image=labeled_array, properties=('label','centroid', 'area'))
        worms=pd.DataFrame(props_worm)
        
        # label image regions
        #label_image = label(cleare)
        #image_label_overlayy = label2rgb(label_image, image=fin_image, bg_label=0)
        filt_worm=worms[worms['area']<2000]
        filtered_worm=filt_worm[filt_worm['area']>50]


        print(len(filtered_worm))
        
        #fig, axes = plt.subplots(figsize=(8, 16), constrained_layout=True)
        #axes.imshow(binarized)
        #axes.set_title(wellno)
        #sns.scatterplot(x='centroid-1', y='centroid-0', ax=axes, data=filtered_worm, s=10,color='red',edgecolor='none', legend=False )
        #fig.savefig(fig_path.joinpath(wellno + ".tif"), orientation='landscape')
        
        tw = len(filtered_worm)
        CI = calc_chemotaxis_index(filtered_worm,image_dims)
        df_f['Chemotaxis']=CI
        #df_f.loc[df_f['WellNo'] == wellno, 'Chemotaxis'] = CI
        df_f.loc[df_f['WellNo'] == wellno, 'Total Worms'] = tw
    df_f.to_csv(path_or_buf= path_rslt.joinpath('test_summary.csv'))
        #save_worm_locations(df_f,filtered_worm,path_rslt,label)


def crop_image(flpath, rslt_path, vals):
    label_begin = time.time()
    #os.chdir(path_img)

    image_path = plb.Path(flpath)
    path_rslt = plb.Path(rslt_path)
    image = imread(image_path)
    image_nvrt = np.invert(image)
    # apply threshold
    print('At threshold')
    thresh = threshold_otsu(image_nvrt)
    print('Threshold: ' + str(thresh))
    bw = closing(image_nvrt > thresh, square(10))

    # remove artifacts connected to image border
    cleared = remove_small_objects(clear_border(bw), 1000000)
    print('Clearing small objects took ', str(int(time.time() - label_begin)), 'seconds.')
    #print('Image Cleared')
    # label image regions
    label_image = label(bw)
    print('Feature finding and labeling took ', str(int(time.time() - label_begin)), 'seconds.')
    #image_label_overlay = label2rgb(label_image, image=image, bg_label=0)

    props = regionprops_table(label_image, properties=('label','centroid', 'bbox', 'area'))
    dff=pd.DataFrame(props)

    df_area = dff.sort_values(by=['area'], ascending=False)
    image_center = (int(label_image.shape[1]/2),int(label_image.shape[0]/2))
    print('Center of image = ' + str(image_center))
    df_area.to_csv(path_or_buf=path_rslt.joinpath('df_area.csv'))

    wells = df_area[(df_area.area>= 2000000) & (df_area.area<=2500000)]
    wells=wells.sort_values(by=['bbox-1'])
    print('Number of wells: ' + str(len(wells)))

    wells.reset_index(drop=True, inplace=True)

    #df.to_csv(path_or_buf=path_rslt.joinpath('df.csv'))
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

    loopWell(df_f, image, path_rslt,vals)
