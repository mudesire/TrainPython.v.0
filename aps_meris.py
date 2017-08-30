# Autogenerated with SMOP 
from smop.core import *
# matlab/aps_meris.m

    
@function
def aps_meris(start_step=None,end_step=None,*args,**kwargs):
    varargin = aps_meris.varargin
    nargin = aps_meris.nargin

    # [] = aps_meris(start_step,end_step)
# 
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
# February 2013
    
    # Modifications:
# DB	03/2013 	Convert the program to a function
# DB 	03/2013 	Allow for PS and SB.
# DB    03/2013 	Output the percentage of all the SAR dates
# DB    03/2013		Fixing the sign convention. ph_tropo has the same sign like phase.
#                   A tropospheric correction ph_after_corection = ph - ph_tropo;
# DB    04/2013     Change to stamps aps filenaming convention.
# DB    04/2013     Incorporate getparm_aps as part of aps toolbox.
# DB    10/2013     Make aps_meris the main script for meris corrections
# DB    03/2014     Fixed typo in system function name
# DB    05/2014     Redefine spectrometer input variables
# DB    07/2014     Include revisualization for soundign data
# DB    08/2014     Include SAR varying conversion factors
    
    ## loading the StaMPS variables
    curdir=copy(pwd)
# matlab/aps_meris.m:46
    if start_step == 1:
        # Compute the MERIS conversion factors from the sounding data
        fprintf('Step 1: Compute the spectrometer conversion factors from the sounding data \\n')
        # getting parameters from parms_aps file
        sounding_dir=getparm_aps('sounding_dir',1)
# matlab/aps_meris.m:53
        start_date=getparm_aps('sounding_start_date',1)
# matlab/aps_meris.m:54
        end_date=getparm_aps('sounding_end_date',1)
# matlab/aps_meris.m:55
        time_stamp=getparm_aps('sounding_time_stamp',1)
# matlab/aps_meris.m:56
        sounding_ifg_dates=getparm_aps('sounding_ifg_dates',1)
# matlab/aps_meris.m:57
        start_year_str=start_date[1:4]
# matlab/aps_meris.m:58
        end_year_str=end_date[1:4]
# matlab/aps_meris.m:59
        start_str=start_date[5:6]
# matlab/aps_meris.m:60
        end_str=end_date[5:6]
# matlab/aps_meris.m:61
        time_stamp_str=matlabarray([])
# matlab/aps_meris.m:62
        for k in arange(1,size(time_stamp,1)).reshape(-1):
            if k > 1:
                time_stamp_str=matlabarray(cat(time_stamp_str,'_',time_stamp[k,:]))
# matlab/aps_meris.m:65
            else:
                time_stamp_str=matlabarray(cat(time_stamp[k,:]))
# matlab/aps_meris.m:67
        # see if the filename already exist
        if strcmp(sounding_ifg_dates,'y'):
            savename=matlabarray(cat(sounding_dir,filesep,'Spectrometer',filesep,'Spectrometer_sensitivity_SAR_dates_1month_',time_stamp_str,'Hr_',num2str(start_year_str),start_str,'_',num2str(end_year_str),end_str,'.mat'))
# matlab/aps_meris.m:73
        else:
            savename=matlabarray(cat(sounding_dir,filesep,'Spectrometer',filesep,'Spectrometer_sensitivity_',time_stamp_str,'Hr_',num2str(start_year_str),start_str,'_',num2str(end_year_str),end_str,'.mat'))
# matlab/aps_meris.m:75
        #     savename = [sounding_dir filesep 'Spectrometer' filesep 'Spectrometer_sensitivity_' time_stamp_str 'Hr_' num2str(start_year_str) start_str '_' num2str(end_year_str) end_str '.mat'];
        if exist(savename,'file') == 2:
            # check if user wants to visualize or re-run the data
            str=''
# matlab/aps_meris.m:80
            while strcmpi(str,'y') != 1 and strcmpi(str,'n') != 1:

                str=input_(cat('This file already exist, do you want to re-process the data? [y/n] \\n'),'s')
# matlab/aps_meris.m:82

            if strcmpi(str,'y'):
                rerun_flag=1
# matlab/aps_meris.m:86
            else:
                sounding_spectrometer_sens_display
                rerun_flag=0
# matlab/aps_meris.m:89
        else:
            rerun_flag=1
# matlab/aps_meris.m:92
        if rerun_flag == 1:
            sounding_spectrometer_sens
    
    if start_step <= 2 and end_step >= 2:
        # SAR delays using MERIS data
        fprintf('Step 2: Compute MERIS tropospheric delay for individual dates\\n')
        # generating a file list of the files to be processed:
        meris_datapath=getparm_aps('meris_datapath')
# matlab/aps_meris.m:105
        command_str='echo files > meris_batch_file.txt'
# matlab/aps_meris.m:106
        command_str2=matlabarray(cat('ls -d ',meris_datapath,filesep,'2*',filesep,'MER_RR_*reprojected.tif >> meris_batch_file.txt'))
# matlab/aps_meris.m:107
        temp,temp1=system(command_str,nargout=2)
# matlab/aps_meris.m:109
        temp,temp1=system(command_str2,nargout=2)
# matlab/aps_meris.m:110
        clear('temp','temp1')
        # running the MERIS computation on the file list
        aps_meris_SAR('meris_batch_file.txt')
    
    if start_step <= 3 and end_step >= 3:
        fprintf('Step 3: Computes MERIS tropospheric delay for inteferograms\\n')
        aps_meris_InSAR
    
    cd(curdir)