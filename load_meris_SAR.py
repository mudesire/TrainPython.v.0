# Autogenerated with SMOP 
from smop.core import *
# matlab/load_meris_SAR.m

    
@function
def load_meris_SAR(filename=None,xy_out_grid=None,poly_crop_filename=None,*args,**kwargs):
    varargin = load_meris_SAR.varargin
    nargin = load_meris_SAR.nargin

    # [xyz] = load_meris_SAR(filename,crop_filename,geocoord_flag) 
# script to read and optional interpolate or crop the data. When
# interpolating, an initial crop is done based on the extend of the to be
# interpolated coordinated. It is assumed that locations are
# given in geo-coordinates (degrees).
    
    # INPUTS:
# filename              Filename with full path to the ".xyz" dataset to be read
# 
# OPTIONAL INPUTS
# xy_out_grid           Grid to which the input data should be interpolated
#                       to. This should have the same coordinates as the
#                       input dataset. A triangular interpolation is
#                       assumed.
# poly_crop_filename    Filename to the .mat crop file. The coordinates needs
#                       be the same as the xy coordinates of the datafile. The
#                       variable in the poly_crop_filename is needs to be called 
#                       "poly.xy".
    
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
    
    # By David Bekaert - University of Leeds
    
    # Modifications:
    
    plot_flag=0
# matlab/load_meris_SAR.m:43
    if nargin < 1:
        error('myApp:argChk',cat('Not enough input arguments...\\n'))
    
    if nargin < 2 or isempty(xy_out_grid):
        interpolate_flag=0
# matlab/load_meris_SAR.m:51
    else:
        interpolate_flag=1
# matlab/load_meris_SAR.m:53
    
    if nargin < 3 or isempty(poly_crop_filename):
        crop_flag=0
# matlab/load_meris_SAR.m:57
    else:
        crop_flag=1
# matlab/load_meris_SAR.m:59
    
    ## Loading of meris processed data files
    fid=fopen(filename,'r')
# matlab/load_meris_SAR.m:64
    data_vector=fread(fid,'double')
# matlab/load_meris_SAR.m:65
    fclose(fid)
    # reshaping into the right 3 column matrix
    xyz_input=reshape(data_vector,3,[]).T
# matlab/load_meris_SAR.m:69
    clear('data_vector')
    ## When requested crop the data
    if crop_flag == 1:
        load(poly_crop_filename)
    
    # When doing the interpolation, crop the data first to the maximum required extend.
# overwrite any specific crop file then.
    if interpolate_flag == 1:
        crop_flag=1
# matlab/load_meris_SAR.m:79
        xy_min=min(xy_out_grid)
# matlab/load_meris_SAR.m:80
        xy_max=max(xy_out_grid)
# matlab/load_meris_SAR.m:81
        poly.xy = copy(cat([xy_min[1],xy_min[2]],[xy_min[1],xy_max[2]],[xy_max[1],xy_max[2]],[xy_max[1],xy_min[2]]))
# matlab/load_meris_SAR.m:82
    
    # do the actual cropping
    if crop_flag == 1:
        ix=inpolygon(xyz_input[:,1],xyz_input[:,2],poly.xy(arange(),1),poly.xy(arange(),2))
# matlab/load_meris_SAR.m:89
        ix[ix > 1]=1
# matlab/load_meris_SAR.m:91
        xyz_output=xyz_input[ix,:]
# matlab/load_meris_SAR.m:94
        clear('ix')
    
    ## When requested interpolate the data
    if interpolate_flag == 1:
        xyz_output_temp=copy(xyz_output)
# matlab/load_meris_SAR.m:102
        clear('xyz_output')
        z_output=griddata(xyz_output_temp[:,1],xyz_output_temp[:,2],xyz_output_temp[:,3],xy_out_grid[:,1],xy_out_grid[:,2],'linear')
# matlab/load_meris_SAR.m:105
        xyz_output=matlabarray(cat(xy_out_grid,z_output))
# matlab/load_meris_SAR.m:106
    
    ## Empty output variable in case no of the optional commands are selected
    if interpolate_flag == 0 and crop_flag == 0:
        xyz_output=matlabarray([])
# matlab/load_meris_SAR.m:112
    else:
        if plot_flag == 1:
            # plotting the cropped and or interpolated result
            figure('name','Cropped and or interpolated dataset')
            scatter3(xyz_output[:,1],xyz_output[:,2],xyz_output[:,3],3,xyz_output[:,3],'filled')
            view(0,90)
            axis('equal')
            axis('tight')
            colorbar
            box('on')
    
    if plot_flag == 1:
        # plotting the cropped and or interpolated result
        figure('name','Input dataset')
        scatter3(xyz_input[:,1],xyz_input[:,2],xyz_input[:,3],3,xyz_input[:,3],'filled')
        view(0,90)
        axis('equal')
        axis('tight')
        colorbar
        box('on')
    