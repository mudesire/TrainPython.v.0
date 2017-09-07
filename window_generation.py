# Autogenerated with SMOP 
from smop.core import *
# Trainmatlab.v.0/window_generation.m

    
@function
def window_generation(xy_local=None,n_patches=None,*args,**kwargs):
    varargin = window_generation.varargin
    nargin = window_generation.nargin

    # 
#  Windows are increasing bottom up and start in the lower left corner.
    
    # Inputs:
# xy_local      Local grid, recomended to be rotated to reduce number of windows
#               outside the dataset, specified as a 2 column matrix in km.
# Optional inputs:
# iterate           A struct containign vairables that are computed for the
#                   first run and whicha re not recompeted for the other runs.
#                   This includes:
#                   window_ix: a variable struct containing which points 
#                               are in wich window.
#                   window_xy: the window positions that cover the data
#                   window_xy_extra: the window positions of the bounding box 
#                               around the data.
# crop_flag     	Set to 'y' to crop out an area. By default this is not done.
#               	When 'y': Filename = "area_ex.mat", with variable called lonlat.
#               	Use: lonlat=ginput; to select polygon around the to be cropped (out) area.
#               	Save as: save('area_ex.mat','lonlat');
    
    #     window_generation.m
#     Copyright (C) 2015  Bekaert David - University of Leeds
#     Email: eedpsb@leeds.ac.uk or davidbekaert.com
# 
#     This program is free software; you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation; either version 2 of the License, or
#     (at your option) any later version.
# 
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
# 
#     You should have received a copy of the GNU General Public License along
#     with this program; if not, write to the Free Software Foundation, Inc.,
#     51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
    
    
    # September 2010 --- Bekaert David --- Initial codings
    
    # modifications:
# 07/2014   DB:     Fix the cropping out of a region
    
    ## defaults
# Defining input variables
    if nargin < 1:
        error('myApp:argChk',cat('Too few input arguments...\\nAbort... \\n'))
    
    
    flag_figure_checks=0
# Trainmatlab.v.0/window_generation.m:55
    n_points_min=1
# Trainmatlab.v.0/window_generation.m:56
    
    patch_overlap=50
# Trainmatlab.v.0/window_generation.m:58
    # getting the parameters from the parm list
    
    crop_flag=getparm_aps('crop_flag')
# Trainmatlab.v.0/window_generation.m:65
    stamps_processed=getparm_aps('stamps_processed')
# Trainmatlab.v.0/window_generation.m:66
    ## Redefine the grid wrt lower left corner.
    xy_local[:,2]=xy_local[:,2] - min(xy_local[:,2])
# Trainmatlab.v.0/window_generation.m:71
    xy_local[:,1]=xy_local[:,1] - min(xy_local[:,1])
# Trainmatlab.v.0/window_generation.m:72
    ## Computing the patch edges
# only perform operation this when it has not been done before
# size of the image in km
    width_x=(max(xy_local[:,1]) - min(xy_local[:,1]))
# Trainmatlab.v.0/window_generation.m:78
    width_y=(max(xy_local[:,2]) - min(xy_local[:,2]))
# Trainmatlab.v.0/window_generation.m:79
    # Assuming the patches to be approximately square to find number of 
# patches in x and y direction.
    patch_width=sqrt(dot(width_x,width_y) / n_patches)
# Trainmatlab.v.0/window_generation.m:83
    n_patches_x=ceil(width_x / patch_width)
# Trainmatlab.v.0/window_generation.m:84
    n_patches_y=ceil(width_y / patch_width)
# Trainmatlab.v.0/window_generation.m:85
    fprintf(cat(num2str(n_patches_x),' patches (+2 for the edges) in x-dir \\n'))
    fprintf(cat(num2str(n_patches_y),' patches (+2 for the edges) in y-dir \\n'))
    # Assume same patch overlap
# But allow in futuer for a different one in x and y direction.
    patch_overlap_x=copy(patch_overlap)
# Trainmatlab.v.0/window_generation.m:91
    patch_overlap_y=copy(patch_overlap)
# Trainmatlab.v.0/window_generation.m:92
    fprintf(cat(num2str(patch_overlap_x),' procent patch overlap in x direction \\n'))
    fprintf(cat(num2str(patch_overlap_y),' procent patch overlap in y direction \\n'))
    # size of the patches including overlap
    patch_width_x=width_x / (patch_overlap_x / 100 + dot((1 - patch_overlap_x / 100),n_patches_x))
# Trainmatlab.v.0/window_generation.m:97
    patch_width_y=width_y / (patch_overlap_y / 100 + dot((1 - patch_overlap_y / 100),n_patches_y))
# Trainmatlab.v.0/window_generation.m:98
    fprintf(cat('Patch width with overlap in x-direction: ',num2str(patch_width_x),'\\n'))
    fprintf(cat('Patch width with overlap in y-direction: ',num2str(patch_width_y),'\\n'))
    # Patch size center to center
    patch_c2c_y=patch_width_y - dot(patch_width_y,patch_overlap_y) / 100
# Trainmatlab.v.0/window_generation.m:104
    patch_c2c_x=patch_width_x - dot(patch_width_x,patch_overlap_x) / 100
# Trainmatlab.v.0/window_generation.m:105
    patch_c2c=max(cat(patch_c2c_y,patch_c2c_x))
# Trainmatlab.v.0/window_generation.m:106
    
    ## determining the points in each window 
# Paches are increasing bottom up and start in the lower left corner.
# only perform the following operation when it has not been done before.
# doing onyl onces will save time for other interferograms
    n_points=size(xy_local,1)
# Trainmatlab.v.0/window_generation.m:114
    ix_window=matlabarray([])
# Trainmatlab.v.0/window_generation.m:115
    
    ixy_local=matlabarray(cat(cat(arange(1,n_points)).T,xy_local))
# Trainmatlab.v.0/window_generation.m:116
    counter=1
# Trainmatlab.v.0/window_generation.m:117
    
    counter_all=1
# Trainmatlab.v.0/window_generation.m:118
    
    for i in arange(1,n_patches_x + 2).reshape(-1):
        # search for the points in the window
        x_bounds=cat(dot(dot((i - 1),patch_width_x),(1 - patch_overlap_x / 100)),dot(dot((i - 1),patch_width_x),(1 - patch_overlap_x / 100)) + patch_width_x) - patch_width_x / 2
# Trainmatlab.v.0/window_generation.m:121
        ix_temp=find(x_bounds[1] <= logical_and(ixy_local[:,2],ixy_local[:,2]) < x_bounds[2])
# Trainmatlab.v.0/window_generation.m:122
        ixy_local_temp=ixy_local[ix_temp,:]
# Trainmatlab.v.0/window_generation.m:123
        clear('ix_temp')
        for k in arange(1,n_patches_y + 2).reshape(-1):
            # search for the points in the window
            y_bounds=cat(dot(dot((k - 1),patch_width_y),(1 - patch_overlap_y / 100)),dot(dot((k - 1),patch_width_y),(1 - patch_overlap_y / 100)) + patch_width_y) - patch_width_y / 2
# Trainmatlab.v.0/window_generation.m:127
            ix_temp=find(y_bounds[1] <= logical_and(ixy_local_temp[:,3],ixy_local_temp[:,3]) < y_bounds[2])
# Trainmatlab.v.0/window_generation.m:128
            ix=ixy_local_temp[ix_temp,1]
# Trainmatlab.v.0/window_generation.m:129
            clear('ix_temp')
            # keeping only those windows were there is actual data, and
        # were there are more than n_points_min
            if isempty(ix) != 1 and length(ix) >= n_points_min:
                # saving the data back into the struct
                window_ix[counter]=ix
# Trainmatlab.v.0/window_generation.m:136
                window_xy[counter,1]=x_bounds[1] + (x_bounds[2] - x_bounds[1]) / 2
# Trainmatlab.v.0/window_generation.m:139
                window_xy[counter,2]=y_bounds[1] + (y_bounds[2] - y_bounds[1]) / 2
# Trainmatlab.v.0/window_generation.m:140
                if flag_figure_checks == 1:
                    patch_colors=jet(dot((n_patches_x + 2),(n_patches_y + 2)))
# Trainmatlab.v.0/window_generation.m:144
                    if counter == 1:
                        h1=figure('name','grid')
# Trainmatlab.v.0/window_generation.m:146
                    else:
                        figure(h1)
                        hold('on')
                    plot(window_xy[counter,1],window_xy[counter,2],'o','color',patch_colors[counter,:])
                    hold('on')
                    plot(cat(x_bounds[1],x_bounds[2],x_bounds[2],x_bounds[1],x_bounds[1]),cat(y_bounds[1],y_bounds[1],y_bounds[2],y_bounds[2],y_bounds[1]),'-','color',patch_colors[counter,:])
                    axis('equal')
                    axis('tight')
                    xlim(cat(0,width_x))
                    ylim(cat(0,width_y))
                # saving the orignal window number for the windows with points
                ix_window[counter]=counter_all
# Trainmatlab.v.0/window_generation.m:162
                counter=counter + 1
# Trainmatlab.v.0/window_generation.m:163
            counter_all=counter_all + 1
# Trainmatlab.v.0/window_generation.m:166
            clear('ix')
    
    clear('x_bounds','y_bounds','counter')
    # the windows that are edges:
    edges=matlabarray(cat(arange(1,dot((n_patches_x + 2),(n_patches_y + 2)),n_patches_y + dot(2(n_patches_y + 2),(n_patches_x + 2)) - (n_patches_y + 2) + 1),arange(1,dot((n_patches_y + 2),(n_patches_x + 2)) - n_patches_y + 1,n_patches_y + 2),arange(n_patches_y + 2,dot((n_patches_y + 2),(n_patches_x + 2)),n_patches_y + 2)))
# Trainmatlab.v.0/window_generation.m:174
    edges=unique(edges)
# Trainmatlab.v.0/window_generation.m:175
    # search those windows with points that are edge windows
    edges,temp,ix_edges_window=intersect(edges,ix_window,nargout=3)
# Trainmatlab.v.0/window_generation.m:177
    clear('counter_all','edges','temp')
    # getting the final number of windows
    n_windows=length(window_ix)
# Trainmatlab.v.0/window_generation.m:182
    # Computing weights based on distance from the points to the windows centers
    X_points=repmat(xy_local[:,1],1,n_windows)
# Trainmatlab.v.0/window_generation.m:185
    Y_points=repmat(xy_local[:,2],1,n_windows)
# Trainmatlab.v.0/window_generation.m:186
    X_windows=repmat(window_xy[:,1].T,n_points,1)
# Trainmatlab.v.0/window_generation.m:187
    Y_windows=repmat(window_xy[:,2].T,n_points,1)
# Trainmatlab.v.0/window_generation.m:188
    Distance=sqrt((X_points - X_windows) ** 2 + (Y_points - Y_windows) ** 2)
# Trainmatlab.v.0/window_generation.m:189
    clear('X_points')
    clear('Y_points')
    clear('X_windows')
    clear('Y_windows')
    # Compute the gaussian weight based on distance
    
    # 
# w_d = normpdf(Distance,0,patch_c2c);                               # [n_points x n_windows]
# if flag_figure_checks==1
#     figure('Name','Weighting based on Distance')
#     Distance_temp = [min(min(Distance)):(max(max(Distance))-min(min(Distance)))/100:max(max(Distance))]';
#     weights_temp = normpdf(Distance_temp,0,patch_c2c); 
#     plot(Distance_temp,weights_temp,'b.-')
# end
# clear Distance
    
    # getting the variables in a structure to load on the next run
    iterate.window_ix = copy(window_ix)
# Trainmatlab.v.0/window_generation.m:205
    iterate.window_xy = copy(window_xy)
# Trainmatlab.v.0/window_generation.m:206
    iterate.ix_edges_window = copy(ix_edges_window)
# Trainmatlab.v.0/window_generation.m:207
    # iterate.w_d = w_d;
    