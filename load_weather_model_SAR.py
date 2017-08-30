# Autogenerated with SMOP 
from smop.core import *
# matlab/load_weather_model_SAR.m

    
@function
def load_weather_model_SAR(filename=None,xy_out_grid=None,overwrite_flag=None,*args,**kwargs):
    varargin = load_weather_model_SAR.varargin
    nargin = load_weather_model_SAR.nargin

    # [xyz] = load_weather_model_SAR(filename,crop_filename,geocoord_flag) 
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
#                       assumed. if xyz_output is inf, then the data has
#                       been stored and not given as output. This is
#                       default option for grd files, as they can become
#                       large.
    
    # By David Bekaert - University of Leeds
    
    # Modifications:
# DB    10/06/2015      Fix in case the lonlat observations are a rectangle
# DB    24/11/2015      Include chunking of the data for large datasets
# DB    24/11/2015      Add support for grd files
# DB    30/11/2015      Remove the polygon cropping option, introduce
#                       overwrite flag overwrite_flag instead. Include the
#                       option to use MEX file to write out the data. This
#                       is much faster than standard matlab, but requires
#                       correct compiling of the mex code.
# DB    10/04/2016      Generalize for weather models
# DB    29/04/2016      Include a fix in case the coordiantes are way off during geocooding.
    
    plot_flag=0
# matlab/load_weather_model_SAR.m:35
    # options of handling larger data.
# 1) use of .grd files and gmt. In future the .grd approach will become the
# default processing in aps_era_SAR and aps_wrf_SAR.
# this however requires the data grid to be written once to a txt file,
# which with regular matlab can take long time. Therefore there is the
# option to use a mex variant that is much faster, but needs to be compiled
# first. By default this will be tried, and reversed to conventional
# data writing if it fails.
    
    # 2) use of .xyz datafiles and matlab. This is backward compatible with old
# TRAIN processed data. For large datasets this will becomes challenging,
# instead you can chunk you data to make it less memory intensive. By
# default this option is turned on. If set to 'n' matlab will interpolate
# all data at once.
    chunk_flag='y'
# matlab/load_weather_model_SAR.m:51
    
    chunk_bin_size=0.5
# matlab/load_weather_model_SAR.m:52
    
    if nargin < 1:
        error('myApp:argChk',cat('Not enough input arguments...\\n'))
    
    if nargin < 2 or isempty(xy_out_grid):
        interpolate_flag=0
# matlab/load_weather_model_SAR.m:58
    else:
        interpolate_flag=1
# matlab/load_weather_model_SAR.m:60
    
    if nargin < 3 or isempty(overwrite_flag):
        overwrite_flag=1
# matlab/load_weather_model_SAR.m:63
    
    
    ## checking the file type if its grd or not
    file_type_grd='n'
# matlab/load_weather_model_SAR.m:70
    file_path,temp,file_ext=fileparts(filename,nargout=3)
# matlab/load_weather_model_SAR.m:71
    # check if this is a grd file already
    if strcmpi(file_ext,'.grd'):
        fprintf(cat('Specified aps correction is a .grd file\\n'))
        file_type_grd='y'
# matlab/load_weather_model_SAR.m:75
        xyz_input=copy(inf)
# matlab/load_weather_model_SAR.m:76
        gmt5_above,gmt_version=get_gmt_version(nargout=2)
# matlab/load_weather_model_SAR.m:78
        error('This is currently under development')
    else:
        ## Loading of processed data files
        fid=fopen(filename,'r')
# matlab/load_weather_model_SAR.m:83
        data_vector=fread(fid,'double')
# matlab/load_weather_model_SAR.m:84
        fclose(fid)
        xyz_input=reshape(data_vector,3,[]).T
# matlab/load_weather_model_SAR.m:88
        clear('data_vector')
    
    ## Crop the dataset when usign a scatter approach in matlab
# When doing the interpolation, crop the data first to the maximum required extend.
# overwrite any specific crop file then.
    if logical_not(strcmpi(file_ext,'.grd')):
        if interpolate_flag == 1:
            crop_flag=1
# matlab/load_weather_model_SAR.m:99
            xy_min=min(xy_out_grid)
# matlab/load_weather_model_SAR.m:100
            xy_max=max(xy_out_grid)
# matlab/load_weather_model_SAR.m:101
            xy_min=xy_min - 0.01
# matlab/load_weather_model_SAR.m:102
            xy_max=xy_max + 0.01
# matlab/load_weather_model_SAR.m:103
            poly.xy = copy(cat([xy_min[1],xy_min[2]],[xy_min[1],xy_max[2]],[xy_max[1],xy_max[2]],[xy_max[1],xy_min[2]]))
# matlab/load_weather_model_SAR.m:105
            if xy_min[1] < logical_and(0,min(xyz_input[:,1])) > 0:
                xyz_input[:,1]=xyz_input[:,1] - 360
# matlab/load_weather_model_SAR.m:111
            # do the actual cropping
            ix=inpolygon(xyz_input[:,1],xyz_input[:,2],poly.xy(arange(),1),poly.xy(arange(),2))
# matlab/load_weather_model_SAR.m:116
            ix[ix > 1]=1
# matlab/load_weather_model_SAR.m:118
            xyz_output=xyz_input[ix,:]
# matlab/load_weather_model_SAR.m:121
            clear('ix')
    
    ## When requested interpolate the data
    if interpolate_flag == 1:
        if strcmpi(file_ext,'.grd'):
            # writing out the lonlat coordiantes in an ASCI table for GMT to use latter on
            lonlat_file=matlabarray(cat(file_path,filesep,'..',filesep,'lonlat_temp.txt'))
# matlab/load_weather_model_SAR.m:134
            generate_file='n'
# matlab/load_weather_model_SAR.m:138
            if overwrite_flag == 0 and exist(lonlat_file,'file') != 2:
                generate_file='y'
# matlab/load_weather_model_SAR.m:140
            if overwrite_flag == 1:
                generate_file='y'
# matlab/load_weather_model_SAR.m:143
            # This file writign is intensive for high resolution data files.
        # The MEX file uses c-code and is much faster, but needs to be
        # compiled for your system. By default the slow matlab approach is
        # used. But once compiled you can change this flag to use the
        # faster code.
            if strcmpi(generate_file,'y'):
                try:
                    dumptofile(xy_out_grid,lonlat_file,' ')
                finally:
                    pass
            # generating the ifg filename
            SAR_path,SAR_filename,temp=fileparts(filename,nargout=3)
# matlab/load_weather_model_SAR.m:160
            save_name=matlabarray(cat(SAR_path,filesep,SAR_filename,'_SARll'))
# matlab/load_weather_model_SAR.m:161
            if strcmpi(gmt5_above,'y'):
                commandstr=matlabarray(cat('grdtrack ',lonlat_file,' -G',filename,'  -fg -N  -Z > ',save_name))
# matlab/load_weather_model_SAR.m:164
            else:
                commandstr=matlabarray(cat('grdtrack ',lonlat_file,' -G',filename,'  -fg -Qn  -Z > ',save_name))
# matlab/load_weather_model_SAR.m:166
            aps_systemcall(commandstr)
            plot_flag=0
# matlab/load_weather_model_SAR.m:172
            # that this is data saved.
            xyz_output=matlabarray(cat(save_name))
# matlab/load_weather_model_SAR.m:176
        else:
            if strcmpi(chunk_flag,'y'):
                # interpolate in chunks when requested
                xyz_output_temp=copy(xyz_output)
# matlab/load_weather_model_SAR.m:182
                clear('xyz_output')
                xyz_output=NaN(cat(size(xy_out_grid,1),3))
# matlab/load_weather_model_SAR.m:184
                xy_min=floor(min(xy_out_grid))
# matlab/load_weather_model_SAR.m:187
                xy_max=ceil(max(xy_out_grid))
# matlab/load_weather_model_SAR.m:188
                lon_grid=matlabarray(cat(arange(xy_min[1],xy_max[1] - chunk_bin_size,chunk_bin_size)))
# matlab/load_weather_model_SAR.m:191
                lat_grid=matlabarray(cat(arange(xy_min[2],xy_max[2] - chunk_bin_size,chunk_bin_size)))
# matlab/load_weather_model_SAR.m:192
                lon_grid,lat_grid=meshgrid(lon_grid,lat_grid,nargout=2)
# matlab/load_weather_model_SAR.m:193
                lon_grid=reshape(lon_grid,[],1)
# matlab/load_weather_model_SAR.m:194
                lat_grid=reshape(lat_grid,[],1)
# matlab/load_weather_model_SAR.m:195
                tic
                fprintf(cat('Buffering in ',num2str(chunk_bin_size),' deg chunks... \\n'))
                for k in arange(1,length(lat_grid)).reshape(-1):
                    ix_temp=(xy_out_grid[:,1] >= logical_and(lon_grid[k],xy_out_grid[:,1]) <= logical_and(lon_grid[k] + chunk_bin_size,xy_out_grid[:,2]) >= logical_and(lat_grid[k],xy_out_grid[:,2]) <= lat_grid[k] + chunk_bin_size)
# matlab/load_weather_model_SAR.m:201
                    if sum(ix_temp) > 0:
                        ix_temp_full=(xyz_output_temp[:,1] >= logical_and(lon_grid[k] - chunk_bin_size / 2,xyz_output_temp[:,1]) <= logical_and(lon_grid[k] + chunk_bin_size + chunk_bin_size / 2,xyz_output_temp[:,2]) >= logical_and(lat_grid[k] - chunk_bin_size / 2,xyz_output_temp[:,2]) <= lat_grid[k] + chunk_bin_size + chunk_bin_size / 2)
# matlab/load_weather_model_SAR.m:203
                        z_output=griddata(xyz_output_temp[ix_temp_full,1],xyz_output_temp[ix_temp_full,2],xyz_output_temp[ix_temp_full,3],xy_out_grid[ix_temp,1],xy_out_grid[ix_temp,2],'linear')
# matlab/load_weather_model_SAR.m:204
                        if sum(ix_temp) == length(z_output):
                            xyz_output[ix_temp,:]=cat(xy_out_grid[ix_temp,:],z_output)
# matlab/load_weather_model_SAR.m:206
                    fprintf(cat(num2str(k),'/',num2str(length(lat_grid)),'\\n'))
                toc
            else:
                xyz_output_temp=copy(xyz_output)
# matlab/load_weather_model_SAR.m:215
                clear('xyz_output')
                z_output=griddata(xyz_output_temp[:,1],xyz_output_temp[:,2],xyz_output_temp[:,3],xy_out_grid[:,1],xy_out_grid[:,2],'linear')
# matlab/load_weather_model_SAR.m:217
                xyz_output=matlabarray(cat(xy_out_grid,z_output))
# matlab/load_weather_model_SAR.m:218
    
    ## Empty output variable in case no of the optional commands are selected
    if interpolate_flag == 0:
        xyz_output=matlabarray([])
# matlab/load_weather_model_SAR.m:225
    else:
        if plot_flag == 1:
            # plotting the cropped and or interpolated result
            figure('name','Cropped and or interpolated dataset')
            scatter3(xyz_output[:,1],xyz_output[:,2],xyz_output[:,3],30,xyz_output[:,3],'filled')
            view(0,90)
            axis('equal')
            axis('tight')
            colorbar
            box('on')
    
    if plot_flag == 1:
        # plotting the cropped and or interpolated result
        figure('name','Input dataset')
        scatter3(xyz_input[:,1],xyz_input[:,2],xyz_input[:,3],30,xyz_input[:,3],'filled')
        view(0,90)
        axis('equal')
        axis('tight')
        colorbar
        box('on')
    