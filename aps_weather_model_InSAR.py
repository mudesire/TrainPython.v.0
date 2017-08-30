# Autogenerated with SMOP 
from smop.core import *
# matlab/aps_weather_model_InSAR.m

    
@function
def aps_weather_model_InSAR(model_type=None,*args,**kwargs):
    varargin = aps_weather_model_InSAR.varargin
    nargin = aps_weather_model_InSAR.nargin

    # [] = aps_weather_model_InSAR(model_type)
# Goes to the InSAR data path and interpolates the weathermodel data to the InSAR
# grid. The tropospheric correction results are stored in the "tca2.mat" or 
# "tca_sb2.mat" file as the ph_tropo_era for ERA, and ph_tropo_merra for MERRA.
# The sign convention is defined such ph_after_corection = ph - ph_tropo_* is the phase corrected 
# the tropospheric signal. 
# 
#     Copyright (C) 2015  Bekaert David - University of Leeds
#     Email: eedpsb@leeds.ac.uk or davidbekaert.com
    
    #     This program is free software; you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation; either version 2 of the License, or
#     (at your option) any later version.
    
    #     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
    
    #     You should have received a copy of the GNU General Public License along
#     with this program; if not, write to the Free Software Foundation, Inc.,
#     51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
    
    # By David Bekaert -- University of Leeds
    
    # Modifications
# 10/2013   DB      Include conversion from zenith to slant delay 
# 10/2013   DB      Include processing structure different from stamps
# 11/2013   DB      Change the name to Hydrostratic as dry is incorrect
#                   naming
# 01/2014   DB      Fix in the saving of the tca filename.
# 05/2014   DB      Adding compatibility with non-stamps processing
#                   structures
# 06/2014   DB      Add check to make sure both master and slave have data.
# 02/2015   DB      Fix for the look angle in case its a single value
# 04/2016   DB      Convert code to be weather model independent and use
#                   modular approach
# 04/2016   DB      Forgot to remove call to old script
# 05/2016   DB      Include merra2
    
    # Filename suffix of the output files
    wetoutfile='_ZWD.xyz'
# matlab/aps_weather_model_InSAR.m:45
    hydroutfile='_ZHD.xyz'
# matlab/aps_weather_model_InSAR.m:46
    # error calling if needed
    if nargin < 1:
        error('Give at least the model_type: era or merra')
    
    # getting the variables from the parms_aps file
    stamps_processed=getparm_aps('stamps_processed',1)
# matlab/aps_weather_model_InSAR.m:53
    ll_matfile=getparm_aps('ll_matfile',1)
# matlab/aps_weather_model_InSAR.m:54
    ifgday_matfile=getparm_aps('ifgday_matfile')
# matlab/aps_weather_model_InSAR.m:55
    model_type=lower(model_type)
# matlab/aps_weather_model_InSAR.m:57
    if strcmpi(model_type,'era'):
        weather_model_datapath=getparm_aps('era_datapath',1)
# matlab/aps_weather_model_InSAR.m:59
    else:
        if strcmpi(model_type,'merra') or strcmpi(model_type,'merra2'):
            weather_model_datapath=getparm_aps('merra_datapath',1)
# matlab/aps_weather_model_InSAR.m:61
    
    lambda_=dot(getparm_aps('lambda',1),100)
# matlab/aps_weather_model_InSAR.m:63
    
    datestructure='yyyymmdd'
# matlab/aps_weather_model_InSAR.m:64
    
    look_angle=getparm_aps('look_angle',1)
# matlab/aps_weather_model_InSAR.m:65
    # loading the data
    if strcmp(stamps_processed,'y'):
        fprintf('Stamps processed structure \\n')
        ps=load(ll_matfile)
# matlab/aps_weather_model_InSAR.m:71
        load('psver')
        dates=ps.day
# matlab/aps_weather_model_InSAR.m:73
        lonlat=ps.lonlat
# matlab/aps_weather_model_InSAR.m:74
        if ischar(look_angle) == 1:
            look_angle=load(look_angle)
# matlab/aps_weather_model_InSAR.m:76
            look_angle=look_angle.la
# matlab/aps_weather_model_InSAR.m:77
        # getting the dropped ifgs
        drop_ifg_index=getparm('drop_ifg_index')
# matlab/aps_weather_model_InSAR.m:81
        if strcmp(getparm('small_baseline_flag'),'y'):
            sb_flag=1
# matlab/aps_weather_model_InSAR.m:84
        else:
            sb_flag=0
# matlab/aps_weather_model_InSAR.m:86
        n_ifg=ps.n_ifg
# matlab/aps_weather_model_InSAR.m:89
        if sb_flag == 1:
            # for SB
            ifg_number=cat(arange(1,n_ifg)).T
# matlab/aps_weather_model_InSAR.m:93
            ifgday_ix=ps.ifgday_ix
# matlab/aps_weather_model_InSAR.m:94
            ifgday_ix[drop_ifg_index,:]=[]
# matlab/aps_weather_model_InSAR.m:96
            ifg_number[drop_ifg_index]=[]
# matlab/aps_weather_model_InSAR.m:97
            ifgs_ix=matlabarray(cat(ifgday_ix,ifg_number))
# matlab/aps_weather_model_InSAR.m:100
        else:
            # slightly different for PS.
            date_slave_ix=cat(arange(1,n_ifg)).T
# matlab/aps_weather_model_InSAR.m:103
            ifg_number=cat(arange(1,n_ifg)).T
# matlab/aps_weather_model_InSAR.m:104
            date_slave_ix[drop_ifg_index]=[]
# matlab/aps_weather_model_InSAR.m:107
            ifg_number[drop_ifg_index]=[]
# matlab/aps_weather_model_InSAR.m:108
            date_master_ix=repmat(ps.master_ix,size(date_slave_ix,1),1)
# matlab/aps_weather_model_InSAR.m:111
            ifgs_ix=matlabarray(cat(date_master_ix,date_slave_ix,ifg_number))
# matlab/aps_weather_model_InSAR.m:114
    else:
        psver=2
# matlab/aps_weather_model_InSAR.m:117
        sb_flag=0
# matlab/aps_weather_model_InSAR.m:120
        lonlat=load(ll_matfile)
# matlab/aps_weather_model_InSAR.m:123
        lonlat=lonlat.lonlat
# matlab/aps_weather_model_InSAR.m:124
        if ischar(look_angle) == 1:
            look_angle=load(look_angle)
# matlab/aps_weather_model_InSAR.m:128
            look_angle=look_angle.la
# matlab/aps_weather_model_InSAR.m:129
        # getting the dates in jullian format
        ifgs_dates=load(ifgday_matfile)
# matlab/aps_weather_model_InSAR.m:133
        ifgs_dates=ifgs_dates.ifgday
# matlab/aps_weather_model_InSAR.m:134
        dates=reshape(ifgs_dates,[],1)
# matlab/aps_weather_model_InSAR.m:135
        dates=unique(dates)
# matlab/aps_weather_model_InSAR.m:136
        dates=datenum(num2str(dates),'yyyymmdd')
# matlab/aps_weather_model_InSAR.m:137
        dates=sort(dates)
# matlab/aps_weather_model_InSAR.m:138
        # getting the ix position for the master and slave dates with respect
    # to the times
        date_master=datenum(num2str(ifgs_dates[:,1]),'yyyymmdd')
# matlab/aps_weather_model_InSAR.m:142
        date_slave=datenum(num2str(ifgs_dates[:,2]),'yyyymmdd')
# matlab/aps_weather_model_InSAR.m:143
        ifg_number=cat(arange(1,size(date_master,1))).T
# matlab/aps_weather_model_InSAR.m:144
        drop_ifg_index=matlabarray([])
# matlab/aps_weather_model_InSAR.m:146
        date_slave[drop_ifg_index]=[]
# matlab/aps_weather_model_InSAR.m:149
        date_master[drop_ifg_index]=[]
# matlab/aps_weather_model_InSAR.m:150
        ifg_number[drop_ifg_index]=[]
# matlab/aps_weather_model_InSAR.m:151
        for k in arange(1,size(date_master,1)).reshape(-1):
            date_master_ix[k,1]=find(date_master[k,1] == dates)
# matlab/aps_weather_model_InSAR.m:153
            date_slave_ix[k,1]=find(date_slave[k,1] == dates)
# matlab/aps_weather_model_InSAR.m:154
        # ix interferograms
        ifgs_ix=matlabarray(cat(date_master_ix,date_slave_ix,ifg_number))
# matlab/aps_weather_model_InSAR.m:158
        n_ifg=size(ifgs_dates,1)
# matlab/aps_weather_model_InSAR.m:161
        ps.day = copy(dates)
# matlab/aps_weather_model_InSAR.m:164
    
    n_dates=length(dates)
# matlab/aps_weather_model_InSAR.m:166
    InSAR_datapath=matlabarray(cat('.'))
# matlab/aps_weather_model_InSAR.m:167
    apsname=matlabarray(cat(InSAR_datapath,filesep,'tca',num2str(psver),'.mat'))
# matlab/aps_weather_model_InSAR.m:168
    apssbname=matlabarray(cat(InSAR_datapath,filesep,'tca_sb',num2str(psver),'.mat'))
# matlab/aps_weather_model_InSAR.m:169
    ## loading the ERA-I data
# initialisation
    d_wet=NaN(cat(size(lonlat,1),n_dates))
# matlab/aps_weather_model_InSAR.m:175
    
    d_hydro=NaN(cat(size(lonlat,1),n_dates))
# matlab/aps_weather_model_InSAR.m:176
    
    ix_no_weather_model_data=matlabarray([])
# matlab/aps_weather_model_InSAR.m:179
    counter=0
# matlab/aps_weather_model_InSAR.m:180
    # looping over the dates
    for k in arange(1,n_dates).reshape(-1):
        # getting the SAR data and convert it to a string
        date_str=datestr(ps.day(k,1),datestructure)
# matlab/aps_weather_model_InSAR.m:185
        model_filename_wet=matlabarray(cat(weather_model_datapath,filesep,date_str,filesep,date_str,wetoutfile))
# matlab/aps_weather_model_InSAR.m:188
        model_filename_hydro=matlabarray(cat(weather_model_datapath,filesep,date_str,filesep,date_str,hydroutfile))
# matlab/aps_weather_model_InSAR.m:189
        # leave NaN's in the matrix.
        if exist(model_filename_wet,'file') == 2:
            # computing the dry delay
            xyz_input,xyz_output=load_weather_model_SAR(model_filename_hydro,lonlat,nargout=2)
# matlab/aps_weather_model_InSAR.m:196
            d_hydro[:,k]=xyz_output[:,3]
# matlab/aps_weather_model_InSAR.m:198
            clear('xyz_input','xyz_output')
            # computing the wet delays
            xyz_input,xyz_output=load_weather_model_SAR(model_filename_wet,lonlat,nargout=2)
# matlab/aps_weather_model_InSAR.m:202
            d_wet[:,k]=xyz_output[:,3]
# matlab/aps_weather_model_InSAR.m:205
            clear('xyz_output')
            counter=counter + 1
# matlab/aps_weather_model_InSAR.m:207
        else:
            # rejected list of ERA-I images
            ix_no_weather_model_data=matlabarray(cat(ix_no_weather_model_data,k))
# matlab/aps_weather_model_InSAR.m:211
        clear('model_filename_hydro','model_filename_wet','date_str')
    
    fprintf(cat(num2str(counter),' out of ',num2str(n_dates),' SAR images have a tropospheric delay estimated \\n'))
    ## Computing the type of delay
    d_total=d_hydro + d_wet
# matlab/aps_weather_model_InSAR.m:219
    ## Converting the Zenith delays to a slant delay
    if size(look_angle,2) > 1 and size(look_angle,1) == 1:
        look_angle=look_angle.T
# matlab/aps_weather_model_InSAR.m:223
    
    if size(look_angle,2) == 1:
        look_angle=repmat(look_angle,1,size(d_total,2))
# matlab/aps_weather_model_InSAR.m:226
        if size(look_angle,1) == 1:
            look_angle=repmat(look_angle,size(d_total,1),1)
# matlab/aps_weather_model_InSAR.m:228
    
    
    d_total=d_total / cos(look_angle)
# matlab/aps_weather_model_InSAR.m:232
    d_hydro=d_hydro / cos(look_angle)
# matlab/aps_weather_model_InSAR.m:233
    d_wet=d_wet / cos(look_angle)
# matlab/aps_weather_model_InSAR.m:234
    ## Converting the range delay to a phase delay
# converting to phase delay. 
# The sign convention is such that ph_corrected = ph_original - ph_tropo*
    eval(cat('ph_SAR_',model_type,'= -4*pi./lambda.*d_total;'))
    
    eval(cat('ph_SAR_',model_type,'_hydro= -4*pi./lambda.*d_hydro;'))
    
    eval(cat('ph_SAR_',model_type,'_wet= -4*pi./lambda.*d_wet;'))
    
    ## Computing the interferometric tropopsheric delays
    
    # removing the dates for which there is no data.
    if isempty(ix_no_weather_model_data) != 1:
        for k in arange(1,length(ix_no_weather_model_data)).reshape(-1):
            # reject based on slave dates
            ix_ifg_reject=find(ix_no_weather_model_data[k] == ifgs_ix[:,2])
# matlab/aps_weather_model_InSAR.m:252
            ifgs_ix[ix_ifg_reject,:]=[]
# matlab/aps_weather_model_InSAR.m:253
            ix_ifg_reject=find(ix_no_weather_model_data[k] == ifgs_ix[:,1])
# matlab/aps_weather_model_InSAR.m:255
            ifgs_ix[ix_ifg_reject,:]=[]
# matlab/aps_weather_model_InSAR.m:256
            clear('ix_ifg_reject')
    
    # computing the interferometric delay for each remaining interferogram
    n_ifg=size(ifgs_ix,1)
# matlab/aps_weather_model_InSAR.m:262
    if isempty(ifgs_ix):
        fprintf(cat('Not enough ',upper(model_type),' data to compute interferometric delays...\\n'))
    
    # initialize the ERA phase matrix for all interferograms, including those without correction.
    eval(cat('ph_tropo_',model_type,'= zeros([size(lonlat,1) n_ifg]);'))
    
    eval(cat('ph_tropo_',model_type,'_hydro= zeros([size(lonlat,1) n_ifg]);'))
    
    eval(cat('ph_tropo_',model_type,'_wet= zeros([size(lonlat,1) n_ifg]);'))
    
    for k in arange(1,n_ifg).reshape(-1):
        # add extra flag that requires both master and slave SAR delay to be
    # present otherwize, its still a sar delay!
        good_ifg_data=1
# matlab/aps_weather_model_InSAR.m:275
        if eval(cat('sum(ph_SAR_',model_type,'(:,ifgs_ix(',num2str(k),',1)))==0 |  sum(ph_SAR_',model_type,'(:,ifgs_ix(',num2str(k),',2)))==0')):
            printf('Misses one of the SAR images for the interferometric delay \\n')
            good_ifg_data=0
# matlab/aps_weather_model_InSAR.m:279
        if good_ifg_data == 1:
            # ph_tropo_era(:,ifgs_ix(k,3)) = ph_SAR_era(:,ifgs_ix(k,1))-ph_SAR_era(:,ifgs_ix(k,2));
            eval(cat('ph_tropo_',model_type,'(:,ifgs_ix(',num2str(k),',3)) = ph_SAR_',model_type,'(:,ifgs_ix(',num2str(k),',1))-ph_SAR_',model_type,'(:,ifgs_ix(',num2str(k),',2));'))
            eval(cat('ph_tropo_',model_type,'_hydro(:,ifgs_ix(',num2str(k),',3)) = ph_SAR_',model_type,'_hydro(:,ifgs_ix(',num2str(k),',1))-ph_SAR_',model_type,'_hydro(:,ifgs_ix(',num2str(k),',2));'))
            eval(cat('ph_tropo_',model_type,'_wet(:,ifgs_ix(',num2str(k),',3)) = ph_SAR_',model_type,'_wet(:,ifgs_ix(',num2str(k),',1))-ph_SAR_',model_type,'_wet(:,ifgs_ix(',num2str(k),',2));'))
        else:
            # ph_tropo_era(:,ifgs_ix(k,3)) = NaN;
            eval(cat('ph_tropo_',model_type,'(:,ifgs_ix(',num2str(k),',3)) =NaN;'))
            eval(cat('ph_tropo_',model_type,'_hydro(:,ifgs_ix(',num2str(k),',3)) =NaN;'))
            eval(cat('ph_tropo_',model_type,'_wet(:,ifgs_ix(',num2str(k),',3)) =NaN;'))
    
    if sb_flag == 1:
        if exist(apssbname,'file') == 2:
            eval(cat('save(\'',apssbname,'\',\'-append\',\'ph_tropo_',model_type,'\',\'ph_tropo_',model_type,'_wet\',\'ph_tropo_',model_type,'_hydro\');'))
            # save(apssbname,'-append','ph_tropo_era','ph_tropo_era_wet','ph_tropo_era_hydro')
        else:
            eval(cat('save(\'',apssbname,'\',\'ph_tropo_',model_type,'\',\'ph_tropo_',model_type,'_wet\',\'ph_tropo_',model_type,'_hydro\');'))
            # save(apssbname,'ph_tropo_era','ph_tropo_era_wet','ph_tropo_era_hydro')
    else:
        if exist(apsname,'file') == 2:
            eval(cat('save(\'',apsname,'\',\'-append\',\'ph_tropo_',model_type,'\',\'ph_tropo_',model_type,'_wet\',\'ph_tropo_',model_type,'_hydro\');'))
            # save(apsname,'-append','ph_tropo_era','ph_tropo_era_wet','ph_tropo_era_hydro')
        else:
            eval(cat('save(\'',apsname,'\',\'ph_tropo_',model_type,'\',\'ph_tropo_',model_type,'_wet\',\'ph_tropo_',model_type,'_hydro\');'))
            # save(apsname,'ph_tropo_era','ph_tropo_era_wet','ph_tropo_era_hydro')
    