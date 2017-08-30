# Autogenerated with SMOP 
from smop.core import *
# matlab/aps_weather_model.m

    
@function
def aps_weather_model(model_type=None,start_step=None,end_step=None,save_path=None,*args,**kwargs):
    varargin = aps_weather_model.varargin
    nargin = aps_weather_model.nargin

    # [] = aps_weather_model(model_type,start_step,end_step)
# Function that computes the interferometric tropospheric delays from
# weather model including ERA-Interim and MERRA.
    
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
# November 2013
    
    # Modifications:
# 02/2014   DB  Include data from ECMWF and BADC as option
# 04/2014   DB  Include auto download for ECMWF website
# 04/2016   DB  Convert to a generic weather model correction using modular
#               approach. Include support for MERRA.
    
    # current processing directory
    curdir=copy(pwd)
# matlab/aps_weather_model.m:35
    # error catching
    if nargin < 3:
        error('Need to specify at least model_type, start_step, end_step')
    
    if logical_and(logical_and(logical_not(strcmpi(model_type,'era')),logical_not(strcmpi(model_type,'merra'))),logical_not(strcmpi(model_type,'merra2'))):
        error(cat('model_type needs to be era or merra'))
    
    # define save path if not given
    if nargin < 4:
        save_path=matlabarray(cat(curdir,filesep))
# matlab/aps_weather_model.m:46
    
    ## Defining the save path in case not given
# filenames
    curdir=copy(pwd)
# matlab/aps_weather_model.m:52
    model_type=lower(model_type)
# matlab/aps_weather_model.m:53
    # saving part of the data in a subfolder
    save_path=matlabarray(cat(save_path,filesep,'aps_',model_type))
# matlab/aps_weather_model.m:55
    if exist(save_path,'dir') != 7:
        mkdir(save_path)
    
    ## The different steps in the code
    if start_step == 0:
        if strcmpi(model_type,'era'):
            # Dummy run on the needed ERA-I files
            fprintf('Step 0: Dummy run on the needed ERA-I data files \\n')
            aps_era_files(0)
        else:
            if strcmpi(model_type,'merra') or strcmpi(model_type,'merra2'):
                # required MERRA files
                aps_merra_files(0,model_type)
    
    if start_step <= 1 and end_step >= 1:
        fprintf(cat('Step 1: Order and Download ',upper(model_type),' data files \\n'))
        if strcmpi(model_type,'era'):
            # order the ECMWF data ERA-I files
            era_data_type=getparm_aps('era_data_type',1)
# matlab/aps_weather_model.m:75
            if strcmpi(era_data_type,'ECMWF'):
                aps_era_files(1)
            else:
                fprintf('You need to download BADC data from command line')
        else:
            if strcmpi(model_type,'merra') or strcmpi(model_type,'merra2'):
                aps_merra_files(1,model_type)
    
    if start_step <= 2 and end_step >= 2:
        # SAR zenith delays
        fprintf(cat('Step 2: Compute the ',upper(model_type),' tropospheric (zenith) delay for individual dates\\n'))
        # running the SAR delay computation using the weather model observations
        aps_weather_model_SAR(model_type)
    
    if start_step <= 3 and end_step >= 3:
        # InSAR slant delays
        fprintf(cat('Step 3: Computes ',upper(model_type),' tropospheric (slant) delay for inteferograms\\n'))
        aps_weather_model_InSAR(model_type)
    
    cd(curdir)