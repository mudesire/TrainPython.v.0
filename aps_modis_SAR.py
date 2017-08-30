# Autogenerated with SMOP 
from smop.core import *
# matlab/aps_modis_SAR.m

    
@function
def aps_modis_SAR(batchfile=None,*args,**kwargs):
    varargin = aps_modis_SAR.varargin
    nargin = aps_modis_SAR.nargin

    # aps_modis_SAR(datelist)
# Scipt to load modis data, mask out clouds, interpolate over gaps and cut 
# the data to the right size for which the tropospheric delay is being computed. 
# The modis data is assumed to be structured in date folders. 
# The batchfile contains the full path to the modis files in these folders. 
# Note that the first line of the batchfile should read "files".
    
    # modis calibration factor from:
# Li, Z., Fielding, E. J., Cross, P., & Preusker, R. (2009). 
# Advanced InSAR atmospheric correction: MERIS/MODIS combination and 
# stacked water vapour models. International Journal of Remote Sensing, 30(13), 
# 3343-3363. doi: 10.1080/01431160802562172
    
    
    # INPUTS used:
# batchfile             A txt file containing the full path and file names of the
#                       meris data that needs to be processed. The first
#                       line of this file should read "files". The data
#                       should be structured in date folders.
# xlims                 Limits in the x-direction, either in degrees
# ylims                 Limits in the y-direction, either in degrees
# smpres                The output resolution, either in degrees
#                       Units needs to be consistend with xlims and ylims.
    
    # OPTIONAL INPUTS:
# conversion            PI conversion factor, default 6.2, or sounding data .
    
    # OUTPUTS:
# It will give wet delay maps in cm.
    
    # By David Bekaert - University of Leeds
    
    # modifications:
# DB    07/2014     Include calibration factor for modis, dem check
# DB    07/2014     Make more explicit that its only wet delays
# DB    07/2014     Redefine meris_lon(lat)_range to region_lon(lat)_range
# DB    08/2014     Include option to have factors varying for each SAR date
# DB    03/2015     Fix in case file names have varying length
# DB    02/2016     Update an error message
    
    # setting the defaults and checking the input arguments
    if nargin < 1:
        fprintf('aps_modis_SAR(batchfile) \\n')
        error('myApp:argChk',cat('Not enough input arguments...\\n'))
    
    conversion_vector=getparm_aps('spectrometer_PIconversion',1)
# matlab/aps_modis_SAR.m:52
    smpres=getparm_aps('region_res',1)
# matlab/aps_modis_SAR.m:53
    
    xlims=getparm_aps('region_lon_range',1)
# matlab/aps_modis_SAR.m:54
    ylims=getparm_aps('region_lat_range',1)
# matlab/aps_modis_SAR.m:55
    modis_recalibrated=getparm_aps('modis_recalibrated',1)
# matlab/aps_modis_SAR.m:56
    stamps_processed=getparm_aps('stamps_processed',1)
# matlab/aps_modis_SAR.m:57
    # check if the modis data is already calibrated
    if strcmpi(modis_recalibrated,'y'):
        modis_calibration=1
# matlab/aps_modis_SAR.m:61
    else:
        modis_calibration=getparm_aps('modis_calibration',1)
# matlab/aps_modis_SAR.m:63
    
    ## the actual scripting
#bounds for all ifgms in degrees or in meters
    if isempty(xlims) or isempty(ylims):
        error('myApp:argChk',cat('Please specify a region_lon_range and region_lat_range\\n'))
    
    xmin=xlims[1]
# matlab/aps_modis_SAR.m:72
    xmax=xlims[2]
# matlab/aps_modis_SAR.m:73
    ymin=ylims[1]
# matlab/aps_modis_SAR.m:74
    ymax=ylims[2]
# matlab/aps_modis_SAR.m:75
    fprintf(cat('Lon range: ',num2str(xmin),' -- ',num2str(xmax),' degrees\\n'))
    fprintf(cat('Lat range: ',num2str(ymin),' -- ',num2str(ymax),' degrees\\n'))
    fprintf(cat('Output resolution is assumed to be ',num2str(smpres),' degrees \\n'))
    # getting the number of files to be processed
    files=char(textread(batchfile,'%s','headerlines',1))
# matlab/aps_modis_SAR.m:82
    ix_keep=matlabarray([])
# matlab/aps_modis_SAR.m:83
    for counter in arange(1,size(files,1)).reshape(-1):
        if strcmpi(modis_recalibrated,'y') == 1:
            if logical_not(isempty(strfind(files[counter,:],'recal'))):
                ix_keep=matlabarray(cat([ix_keep],[counter]))
# matlab/aps_modis_SAR.m:88
                recal_str='_recal'
# matlab/aps_modis_SAR.m:89
        else:
            if isempty(strfind(files[counter,:],'recal')):
                ix_keep=matlabarray(cat([ix_keep],[counter]))
# matlab/aps_modis_SAR.m:93
                recal_str=''
# matlab/aps_modis_SAR.m:94
    
    files=files[ix_keep,:]
# matlab/aps_modis_SAR.m:99
    ndates=size(files,1)
# matlab/aps_modis_SAR.m:100
    # loading the date information
    if strcmp(stamps_processed,'y'):
        ps=load(getparm_aps('ll_matfile'))
# matlab/aps_modis_SAR.m:104
        ifgs_dates=ps.day
# matlab/aps_modis_SAR.m:105
        fprintf('Stamps processed structure \\n')
    else:
        ifgday_matfile=getparm_aps('ifgday_matfile',1)
# matlab/aps_modis_SAR.m:108
        ifgs_dates=load(ifgday_matfile)
# matlab/aps_modis_SAR.m:109
        ifgs_dates=ifgs_dates.ifgday
# matlab/aps_modis_SAR.m:110
        ifgs_dates=reshape(ifgs_dates,[],1)
# matlab/aps_modis_SAR.m:111
        ifgs_dates=unique(ifgs_dates)
# matlab/aps_modis_SAR.m:112
    
    # extracting the dates from the filenames
    for k in arange(1,ndates).reshape(-1):
        path,filename_temp,ext_temp=fileparts(files[k,:],nargout=3)
# matlab/aps_modis_SAR.m:117
        clear('filename_temp','ext_temp')
        path_temp,date,ext_temp=fileparts(path,nargout=3)
# matlab/aps_modis_SAR.m:119
        clear('path_temp','ext_temp')
        # save the paths as structures to allow for variable path lengths
        pathlist[k]=path
# matlab/aps_modis_SAR.m:123
        clear('path')
        # saving the date information
        datelist[k,:]=date
# matlab/aps_modis_SAR.m:126
        clear('date')
    
    if length(conversion_vector) > 1:
        fprintf('Conversion factor varies for each SAR date.\\n')
    
    #start loop here to calculate atmos correction for each date
    fprintf('Starting the computation for each SAR date \\n')
    for n in arange(1,ndates).reshape(-1):
        if length(conversion_vector) > 1:
            ix_date_postion=find(ifgs_dates == datenum(datelist[n,:],'yyyymmdd'))
# matlab/aps_modis_SAR.m:138
            conversion=conversion_vector[ix_date_postion]
# matlab/aps_modis_SAR.m:139
        else:
            conversion=copy(conversion_vector)
# matlab/aps_modis_SAR.m:141
        file=strtrim(cat(files[n,:]))
# matlab/aps_modis_SAR.m:144
        outfile=matlabarray(cat(pathlist[n],filesep,datelist[n,:],recal_str,'_ZWD_nointerp.xyz'))
# matlab/aps_modis_SAR.m:145
        outfile_gauss=matlabarray(cat(pathlist[n],filesep,datelist[n,:],recal_str,'_ZWD_gauss.xyz'))
# matlab/aps_modis_SAR.m:146
        outfile_surf=matlabarray(cat(pathlist[n],filesep,datelist[n,:],recal_str,'_ZWD_surf.xyz'))
# matlab/aps_modis_SAR.m:147
        lon_grid,lat_grid,watervap=grdread2(file,nargout=3)
# matlab/aps_modis_SAR.m:148
        D=grdinfo2(file)
# matlab/aps_modis_SAR.m:150
        mod_xmin=D[1]
# matlab/aps_modis_SAR.m:151
        mod_xmax=D[2]
# matlab/aps_modis_SAR.m:152
        mod_ymin=D[3]
# matlab/aps_modis_SAR.m:153
        mod_ymax=D[4]
# matlab/aps_modis_SAR.m:154
        mod_cols=length(lon_grid)
# matlab/aps_modis_SAR.m:155
        mod_rows=length(lat_grid)
# matlab/aps_modis_SAR.m:156
        clear('D')
        ## Calculate wet delay
    #convert from g/cm^2 slant water vapour to cm phase delay
        watervap=multiply(multiply(watervap,conversion),modis_calibration)
# matlab/aps_modis_SAR.m:161
        grdwrite2(lon_grid,lat_grid,watervap,'tmp.grd')
        # gaussian filter tmp.grd to get tmp2.grd
        grdfil1_cmd='grdfilter tmp.grd -Gtmp2.grd -Ni -D2 -Fg50'
# matlab/aps_modis_SAR.m:166
        a,b=system(grdfil1_cmd,nargout=2)
# matlab/aps_modis_SAR.m:167
        grd2xyz_cmd=matlabarray(cat('grd2xyz -R',num2str(mod_xmin),'/',num2str(mod_xmax),'/',num2str(mod_ymin),'/',num2str(mod_ymax),' tmp.grd -bo > tmp.xyz'))
# matlab/aps_modis_SAR.m:170
        a,b=system(grd2xyz_cmd,nargout=2)
# matlab/aps_modis_SAR.m:171
        grdfil_cmd=matlabarray(cat('surface -R',num2str(mod_xmin),'/',num2str(mod_xmax),'/',num2str(mod_ymin),'/',num2str(mod_ymax),' tmp.xyz -I',num2str(mod_cols),'+/',num2str(mod_rows),'+ -bi -Gtmp_fil.grd -T0.5'))
# matlab/aps_modis_SAR.m:174
        a,b=system(grdfil_cmd,nargout=2)
# matlab/aps_modis_SAR.m:175
        #nointerp
        grdsmp_cmd=matlabarray(cat('grdsample -R',num2str(xmin),'/',num2str(xmax),'/',num2str(ymin),'/',num2str(ymax),' -I',num2str(smpres),' tmp.grd -Gtmp_smp.grd'))
# matlab/aps_modis_SAR.m:179
        a,b=system(grdsmp_cmd,nargout=2)
# matlab/aps_modis_SAR.m:180
        grd2xyz_cmd=matlabarray(cat('grd2xyz -R',num2str(xmin),'/',num2str(xmax),'/',num2str(ymin),'/',num2str(ymax),' tmp_smp.grd -bo >',outfile))
# matlab/aps_modis_SAR.m:181
        a,b=system(grd2xyz_cmd,nargout=2)
# matlab/aps_modis_SAR.m:182
        grdsmp_cmd=matlabarray(cat('grdsample -R',num2str(xmin),'/',num2str(xmax),'/',num2str(ymin),'/',num2str(ymax),' -I',num2str(smpres),' tmp2.grd -Gtmp_smp2.grd'))
# matlab/aps_modis_SAR.m:185
        a,b=system(grdsmp_cmd,nargout=2)
# matlab/aps_modis_SAR.m:186
        grd2xyz_cmd=matlabarray(cat('grd2xyz -R',num2str(xmin),'/',num2str(xmax),'/',num2str(ymin),'/',num2str(ymax),' tmp_smp2.grd -bo >',outfile_gauss))
# matlab/aps_modis_SAR.m:187
        a,b=system(grd2xyz_cmd,nargout=2)
# matlab/aps_modis_SAR.m:188
        grdsmp_cmd=matlabarray(cat('grdsample -R',num2str(xmin),'/',num2str(xmax),'/',num2str(ymin),'/',num2str(ymax),' -I',num2str(smpres),' tmp_fil.grd -Gtmp_smp_fil.grd'))
# matlab/aps_modis_SAR.m:190
        a,b=system(grdsmp_cmd,nargout=2)
# matlab/aps_modis_SAR.m:191
        grd2xyz_cmd=matlabarray(cat('grd2xyz -R',num2str(xmin),'/',num2str(xmax),'/',num2str(ymin),'/',num2str(ymax),' tmp_smp_fil.grd -bo >',outfile_surf))
# matlab/aps_modis_SAR.m:192
        a,b=system(grd2xyz_cmd,nargout=2)
# matlab/aps_modis_SAR.m:193
        # opening the data file (not-interpolated)
        nointfid=fopen(outfile,'r')
# matlab/aps_modis_SAR.m:197
        data_vector=fread(nointfid,'double')
# matlab/aps_modis_SAR.m:198
        fclose(nointfid)
        data=reshape(data_vector,3,[]).T
# matlab/aps_modis_SAR.m:201
        noint=data[:,3]
# matlab/aps_modis_SAR.m:202
        clear('data','data_vector')
        # opening the gaussian interpolated file
        gaussfid=fopen(outfile_gauss,'r')
# matlab/aps_modis_SAR.m:207
        data_vector=fread(gaussfid,'double')
# matlab/aps_modis_SAR.m:208
        fclose(gaussfid)
        data=reshape(data_vector,3,[]).T
# matlab/aps_modis_SAR.m:211
        gauss=data[:,3]
# matlab/aps_modis_SAR.m:212
        xy=data[:,cat(arange(1,2))]
# matlab/aps_modis_SAR.m:213
        clear('data','data_vector')
        # (gaussian interpolated points only where no data available)
        noint[isnan(noint)]=0
# matlab/aps_modis_SAR.m:217
        gauss[noint != 0]=0
# matlab/aps_modis_SAR.m:218
        gauss_interp=gauss + noint
# matlab/aps_modis_SAR.m:219
        gauss_interp[gauss_interp == 0]=NaN
# matlab/aps_modis_SAR.m:220
        data_write=cat(xy,gauss_interp).T
# matlab/aps_modis_SAR.m:222
        clear('gauss_interp','noint','gauss')
        #output
        fid=fopen(outfile_gauss,'w')
# matlab/aps_modis_SAR.m:225
        fwrite(fid,data_write,'double')
        fclose(fid)
        clear('data_write')
        fprintf(cat(num2str(n),' completed out of ',num2str(ndates),'\\n'))
    
    a,b=system('rm tmp.grd tmp.xyz tmp2.grd tmp_fil.grd tmp_smp.grd tmp_smp2.grd tmp_smp_fil.grd',nargout=2)
# matlab/aps_modis_SAR.m:234