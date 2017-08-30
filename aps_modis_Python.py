# Autogenerated with SMOP 
from smop.core import *
# matlab/aps_modis_Python.m

    
@function
def aps_modis_Python(*args,**kwargs):
    varargin = aps_modis_Python.varargin
    nargin = aps_modis_Python.nargin

    # function that downloads the MOSID data from OSCAR and saves it in the
# correct data structure
    
    # A loop is included rather than a simultaneous call as this would kill the
# OSCAR server. To make sure the service was succesfull, a check is
# performed till all files are downloaded.
    
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
    
    # By David Bekaert - University of Leeds - May 2014
    
    # modifications
# DB    07/2014     Redefine meris_lat(lon)_range to region_lat(lon)_range
    
    # getting the variables from the parms_aps file
    workdir=copy(pwd)
# matlab/aps_modis_Python.m:34
    stamps_processed=getparm_aps('stamps_processed')
# matlab/aps_modis_Python.m:35
    UTC_sat=getparm_aps('UTC_sat')
# matlab/aps_modis_Python.m:36
    modis_datapath=getparm_aps('modis_datapath')
# matlab/aps_modis_Python.m:37
    datestructure='yyyymmdd'
# matlab/aps_modis_Python.m:38
    
    # loading the data
    if strcmp(stamps_processed,'y'):
        ll_matfile=getparm_aps('ll_matfile')
# matlab/aps_modis_Python.m:42
        ps=load(ll_matfile)
# matlab/aps_modis_Python.m:43
        dates=ps.day
# matlab/aps_modis_Python.m:44
        load('psver')
    else:
        ifgday_matfile=getparm_aps('ifgday_matfile')
# matlab/aps_modis_Python.m:47
        ifgs_dates=load(ifgday_matfile)
# matlab/aps_modis_Python.m:48
        ifgs_dates=ifgs_dates.ifgday
# matlab/aps_modis_Python.m:49
        dates=reshape(ifgs_dates,[],1)
# matlab/aps_modis_Python.m:50
        dates=unique(dates)
# matlab/aps_modis_Python.m:51
        dates=datenum(num2str(dates),'yyyymmdd')
# matlab/aps_modis_Python.m:52
    
    # the region the delay needs to cover.
# slightly larger than the InSAR region
    xlims=getparm_aps('region_lon_range')
# matlab/aps_modis_Python.m:57
    ylims=getparm_aps('region_lat_range')
# matlab/aps_modis_Python.m:58
    smpres=getparm_aps('region_res')
# matlab/aps_modis_Python.m:59
    xmin=xlims[1]
# matlab/aps_modis_Python.m:60
    xmax=xlims[2]
# matlab/aps_modis_Python.m:61
    ymin=ylims[1]
# matlab/aps_modis_Python.m:62
    ymax=ylims[2]
# matlab/aps_modis_Python.m:63
    # the region which is cropped from the ERA data and used to make the interpolation.
# Should be  larger than the region to which the delay is computed
    lonmin=floor(xmin) - 1
# matlab/aps_modis_Python.m:68
    lonmax=ceil(xmax) + 1
# matlab/aps_modis_Python.m:69
    latmin=floor(ymin) - 1
# matlab/aps_modis_Python.m:70
    latmax=ceil(ymax) + 1
# matlab/aps_modis_Python.m:71
    # getting the dates
    n_dates=length(dates)
# matlab/aps_modis_Python.m:76
    # downloading of the data
    counter=1
# matlab/aps_modis_Python.m:79
    continueflag=1
# matlab/aps_modis_Python.m:80
    count_exist=0
# matlab/aps_modis_Python.m:81
    while continueflag == 1:

        for k in arange(1,n_dates).reshape(-1):
            if exist(cat(modis_datapath,filesep,datestr(dates[k],datestructure)),'dir') != 7:
                mkdir(cat(modis_datapath,filesep,datestr(dates[k],datestructure)))
            if exist(cat(modis_datapath,filesep,datestr(dates[k],datestructure),filesep,'OSCAR_Modis_',datestr(dates[k],datestructure),'.grd'),'file') != 2:
                cd(cat(modis_datapath,filesep,datestr(dates[k],datestructure)))
                fprintf(cat('Downloading modis data for ',datestr(dates[k],datestructure),'\\n'))
                #  options for get_modis
            # -r (--region): lon in [-180,180], lat in [-90,90], mandatory'
            # -t (--time): time and date in ISO format, mandatory'
            # -p (--platform): terra (default), aqua, or any.'
            # -o (--outfile): output filename (default: mod_minlon_maxlon_minlat_maxlat_dateTtime.grd)'
            # -w (--timewindow): saerch time window size in second (default: 18000, i.e. time +/-5hrs)'
            # -g (--gridsize): grid spacing in degrees (default: 30./3600.=0.008333333...)'
            # -l (--localtime): if used, the given time is local time, otherwise UTC'
            # -f (--figurefile): downloads the png figure file (same fileroot but with .png)'
            # -v (--verbose)'
            # -s (--server): specify which server to use - oscar1 (default) or oscar2'
                commandstr=matlabarray(cat('python $get_modis_filepath -r ',num2str(lonmin),'/',num2str(lonmax),'/',num2str(latmin),'/',num2str(latmax),' -t ',datestr(dates[k],'yyyy-mm-dd'),'T',UTC_sat,':00 -p terra -v -o OSCAR_Modis_',datestr(dates[k],datestructure),'.grd -f -v > download.log'))
# matlab/aps_modis_Python.m:107
                a,b=system(commandstr,nargout=2)
# matlab/aps_modis_Python.m:108
                clear('commandstr','a','b')
            else:
                count_exist=count_exist + 1
# matlab/aps_modis_Python.m:111
        if count_exist == n_dates:
            fprintf('All files have been downloaded \\n')
            continueflag=0
# matlab/aps_modis_Python.m:117
        if counter == 10:
            fprintf('Stop iterating the download. Not all SAR dates where downloaded... \\n')
            continueflag=0
# matlab/aps_modis_Python.m:122
        counter=counter + 1
# matlab/aps_modis_Python.m:125

    
    cd(workdir)
    