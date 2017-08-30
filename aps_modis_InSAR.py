# Autogenerated with SMOP 
from smop.core import *
# matlab/aps_modis_InSAR.m

    
@function
def aps_modis_InSAR(*args,**kwargs):
    varargin = aps_modis_InSAR.varargin
    nargin = aps_modis_InSAR.nargin

    # [] = aps_modis_InSAR()
# Goes to the InSAR data path and interpolate the modis result to the InSAR
# grid. Skip those images that do not have modis data to correct for.
# Also only keep those modis tracks that cover a percentage of the InSAR
# track. The tropospheric correction results are stored in the "tca2.mat" or "tca_sb2.mat" file as the ph_tropo_modis variable.
# The sign convention is defined such ph_after_corection = ph - ph_tropo_modis is the phase corrected 
# the tropospheric signal.
    
    # OPTIONAL INPUTS
# meris_perc_coverage 	Minimum percentage of PS locations that should have no cloud coverage.
#                       By default this value is set to 80#.
# lambda                Radar wavelength [cm], by default c-band (5.6)
# datestructure         Modis date structure, by default this is assumed 'yyyymmdd'.
    
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
    
    # By David Bekaert - May 2014
# University of Leeds
    
    # modifications
# DB    08/2014     Output the parameters that are being lated from parms aps
# DB    08/2014     Include support for calibrated MODIS data
# DB    02/2016     Fix for the incidence angle in case a singel value is given
    
    # getting the variables from the parms_aps file
    stamps_processed=getparm_aps('stamps_processed',1)
# matlab/aps_modis_InSAR.m:44
    ll_matfile=getparm_aps('ll_matfile',1)
# matlab/aps_modis_InSAR.m:45
    modis_datapath=getparm_aps('modis_datapath',1)
# matlab/aps_modis_InSAR.m:46
    modis_perc_coverage=getparm_aps('meris_perc_coverage',1)
# matlab/aps_modis_InSAR.m:47
    
    #                                                           have meris coverage. In case this is less
#                                                           the meris data is rejected.
    lambda_=dot(getparm_aps('lambda',1),100)
# matlab/aps_modis_InSAR.m:50
    
    look_angle=getparm_aps('look_angle',1)
# matlab/aps_modis_InSAR.m:51
    ifgday_matfile=getparm_aps('ifgday_matfile',1)
# matlab/aps_modis_InSAR.m:52
    modis_recalibrated=getparm_aps('modis_recalibrated',1)
# matlab/aps_modis_InSAR.m:53
    # checking if its recalibrated modis data or not
    if strcmpi(modis_recalibrated,'y'):
        recal_str='recal_'
# matlab/aps_modis_InSAR.m:57
    else:
        recal_str=''
# matlab/aps_modis_InSAR.m:59
    
    # The modis files used for the estimation. 
# The no interp file is used to check the cloud coverage.
# the interpolated file is used as correction result.
    modis_file_suffix_nointerp=matlabarray(cat(recal_str,'ZWD_nointerp.xyz'))
# matlab/aps_modis_InSAR.m:64
    modis_file_suffix_interp=matlabarray(cat(recal_str,'ZWD_surf.xyz'))
# matlab/aps_modis_InSAR.m:65
    datestructure='yyyymmdd'
# matlab/aps_modis_InSAR.m:67
    
    # getting the dropped ifgs
    
    # loading the data
    if strcmp(stamps_processed,'y'):
        fprintf('Stamps processed structure \\n')
        drop_ifg_index=getparm('drop_ifg_index')
# matlab/aps_modis_InSAR.m:74
        if ischar(look_angle) == 1:
            look_angle=load(look_angle)
# matlab/aps_modis_InSAR.m:78
            look_angle=look_angle.la
# matlab/aps_modis_InSAR.m:79
        # longitude, latitude and time information
        ps=load(ll_matfile)
# matlab/aps_modis_InSAR.m:83
        load('psver')
        dates=ps.day
# matlab/aps_modis_InSAR.m:85
        lonlat=ps.lonlat
# matlab/aps_modis_InSAR.m:86
        if strcmp(getparm('small_baseline_flag'),'y'):
            sb_flag=1
# matlab/aps_modis_InSAR.m:90
        else:
            sb_flag=0
# matlab/aps_modis_InSAR.m:92
        n_ifg=ps.n_ifg
# matlab/aps_modis_InSAR.m:95
        if sb_flag == 1:
            # for SB
            ifg_number=cat(arange(1,n_ifg)).T
# matlab/aps_modis_InSAR.m:99
            ifgday_ix=ps.ifgday_ix
# matlab/aps_modis_InSAR.m:100
            ifgday_ix[drop_ifg_index,:]=[]
# matlab/aps_modis_InSAR.m:102
            ifg_number[drop_ifg_index]=[]
# matlab/aps_modis_InSAR.m:103
            ifgs_ix=matlabarray(cat(ifgday_ix,ifg_number))
# matlab/aps_modis_InSAR.m:106
            ifgs_ix_no_interp=copy(ifgs_ix)
# matlab/aps_modis_InSAR.m:107
        else:
            # slightly different for PS.
            date_slave_ix=cat(arange(1,n_ifg)).T
# matlab/aps_modis_InSAR.m:111
            ifg_number=cat(arange(1,n_ifg)).T
# matlab/aps_modis_InSAR.m:112
            date_slave_ix[drop_ifg_index]=[]
# matlab/aps_modis_InSAR.m:115
            ifg_number[drop_ifg_index]=[]
# matlab/aps_modis_InSAR.m:116
            date_master_ix=repmat(ps.master_ix,size(date_slave_ix,1),1)
# matlab/aps_modis_InSAR.m:119
            ifgs_ix=matlabarray(cat(date_master_ix,date_slave_ix,ifg_number))
# matlab/aps_modis_InSAR.m:122
            ifgs_ix_no_interp=copy(ifgs_ix)
# matlab/aps_modis_InSAR.m:123
    else:
        sb_flag=0
# matlab/aps_modis_InSAR.m:128
        psver=2
# matlab/aps_modis_InSAR.m:129
        lonlat=load(ll_matfile)
# matlab/aps_modis_InSAR.m:131
        lonlat=lonlat.lonlat
# matlab/aps_modis_InSAR.m:132
        if ischar(look_angle) == 1:
            look_angle=load(look_angle)
# matlab/aps_modis_InSAR.m:136
            look_angle=look_angle.la
# matlab/aps_modis_InSAR.m:137
        # getting the dates in jullian format
        ifgs_dates=load(ifgday_matfile)
# matlab/aps_modis_InSAR.m:143
        ifgs_dates=ifgs_dates.ifgday
# matlab/aps_modis_InSAR.m:144
        dates=reshape(ifgs_dates,[],1)
# matlab/aps_modis_InSAR.m:145
        dates=unique(dates)
# matlab/aps_modis_InSAR.m:146
        dates=datenum(num2str(dates),'yyyymmdd')
# matlab/aps_modis_InSAR.m:147
        dates=sort(dates)
# matlab/aps_modis_InSAR.m:148
        # getting the ix position for the master and slave dates with respect
    # to the times
        date_master=datenum(num2str(ifgs_dates[:,1]),'yyyymmdd')
# matlab/aps_modis_InSAR.m:152
        date_slave=datenum(num2str(ifgs_dates[:,2]),'yyyymmdd')
# matlab/aps_modis_InSAR.m:153
        ifg_number=cat(arange(1,size(date_master,1))).T
# matlab/aps_modis_InSAR.m:154
        for k in arange(1,size(date_master,1)).reshape(-1):
            date_master_ix[k,1]=find(date_master[k,1] == dates)
# matlab/aps_modis_InSAR.m:158
            date_slave_ix[k,1]=find(date_slave[k,1] == dates)
# matlab/aps_modis_InSAR.m:159
        # ix interferograms
        ifgs_ix=matlabarray(cat(date_master_ix,date_slave_ix,ifg_number))
# matlab/aps_modis_InSAR.m:163
        n_ifg=size(ifgs_dates,1)
# matlab/aps_modis_InSAR.m:166
        fprintf('Check the InSAR dates, this has not been tested \\n')
    
    InSAR_datapath=matlabarray(cat('.',filesep))
# matlab/aps_modis_InSAR.m:172
    apsname=matlabarray(cat(InSAR_datapath,'tca',num2str(psver),'.mat'))
# matlab/aps_modis_InSAR.m:173
    apssbname=matlabarray(cat(InSAR_datapath,'tca_sb',num2str(psver),'.mat'))
# matlab/aps_modis_InSAR.m:174
    n_dates=length(dates)
# matlab/aps_modis_InSAR.m:178
    n_points=size(lonlat,1)
# matlab/aps_modis_InSAR.m:179
    ## loading the meris data
# initialisation
    d_modis=NaN(cat(n_points,n_dates))
# matlab/aps_modis_InSAR.m:183
    
    d_modis_no_interp=NaN(cat(n_points,n_dates))
# matlab/aps_modis_InSAR.m:184
    
    SAR_modis_perc=NaN(cat(n_dates,1))
# matlab/aps_modis_InSAR.m:187
    
    counter=0
# matlab/aps_modis_InSAR.m:188
    counter_threshold=0
# matlab/aps_modis_InSAR.m:189
    ix_no_modis=matlabarray([])
# matlab/aps_modis_InSAR.m:190
    ix_no_modis_coverage=matlabarray([])
# matlab/aps_modis_InSAR.m:191
    ix_no_modis_no_interp_file=matlabarray([])
# matlab/aps_modis_InSAR.m:192
    for k in arange(1,n_dates).reshape(-1):
        # getting the SAR data and convert it to a string
        modis_date_str=datestr(dates[k,1],datestructure)
# matlab/aps_modis_InSAR.m:196
        modis_filename_interp=matlabarray(cat(modis_datapath,filesep,modis_date_str,filesep,modis_date_str,'_',modis_file_suffix_interp))
# matlab/aps_modis_InSAR.m:199
        modis_filename_nointerp=matlabarray(cat(modis_datapath,filesep,modis_date_str,filesep,modis_date_str,'_',modis_file_suffix_nointerp))
# matlab/aps_modis_InSAR.m:200
        # leave NaN's in the matrix.
        if exist(modis_filename_interp,'file') == 2:
            # computing the percentage of pixels that do not have data coverage
            if exist(modis_filename_nointerp,'file') == 2:
                xyz_input_nointerp,xyz_output_nointerp=load_meris_SAR(modis_filename_nointerp,lonlat,nargout=2)
# matlab/aps_modis_InSAR.m:207
                d_modis_no_interp[:,k]=xyz_output_nointerp[:,3]
# matlab/aps_modis_InSAR.m:210
                SAR_modis_perc[k,1]=dot((1 - sum(isnan(xyz_output_nointerp[:,3])) / n_points),100)
# matlab/aps_modis_InSAR.m:212
                if dot((1 - sum(isnan(xyz_output_nointerp[:,3])) / n_points),100) < modis_perc_coverage:
                    # reject the modis acquisition as to much of it is covered
                # by clouds.
                    keep_modis=0
# matlab/aps_modis_InSAR.m:216
                    counter_threshold=counter_threshold + 1
# matlab/aps_modis_InSAR.m:217
                else:
                    # good modis acquisition
                    keep_modis=1
# matlab/aps_modis_InSAR.m:220
                clear('xyz_input_nointerp','xyz_output_nointerp')
            else:
                # no way to test if its a good modis track, keep it.
            # best is to keep all the outputs from the modis computation
                keep_modis=1
# matlab/aps_modis_InSAR.m:226
            if keep_modis == 1:
                # load the interpolated modis data
                xyz_input_interp,xyz_output_interp=load_meris_SAR(modis_filename_interp,lonlat,nargout=2)
# matlab/aps_modis_InSAR.m:231
                clear('xyz_input_interp')
                # saving the output data
                d_modis[:,k]=xyz_output_interp[:,3]
# matlab/aps_modis_InSAR.m:235
                clear('xyz_output_interp')
                # counting the number of SAR dates with modis data that have
            # enough coverage
                counter=counter + 1
# matlab/aps_modis_InSAR.m:240
            else:
                # rejected list of modis images
                ix_no_modis=matlabarray(cat(ix_no_modis,k))
# matlab/aps_modis_InSAR.m:243
        else:
            # rejected list of modis images
            ix_no_modis_no_interp_file=matlabarray(cat(ix_no_modis_no_interp_file,k))
# matlab/aps_modis_InSAR.m:247
            ix_no_modis=matlabarray(cat(ix_no_modis,k))
# matlab/aps_modis_InSAR.m:248
            ix_no_modis_coverage=matlabarray(cat(ix_no_modis_coverage,k))
# matlab/aps_modis_InSAR.m:249
        clear('modis_filename','modis_date_str')
    
    fprintf(cat('\\n-----------------------------------------------------\\n',num2str(counter),' out of ',num2str(n_dates),' SAR images have a tropospheric delay estimated \\n'))
    fprintf(cat(num2str(counter_threshold),' images did not meet the ',num2str(modis_perc_coverage),' procent threshold. \\n'))
    # outputting a summary of the modis data:
    no_modis_data=repmat(' ',n_dates,13)
# matlab/aps_modis_InSAR.m:258
    no_modis_data[ix_no_modis_coverage,:]=repmat('no modis data',length(ix_no_modis_coverage),1)
# matlab/aps_modis_InSAR.m:259
    output_str=matlabarray(cat(datestr(dates,datestructure),repmat(':  ',n_dates,1),num2str(round(dot(SAR_modis_perc,10)) / 10),repmat(' procent     ',n_dates,1),no_modis_data,repmat('\\n',n_dates,1)))
# matlab/aps_modis_InSAR.m:260
    for k in arange(1,n_dates).reshape(-1):
        fprintf(cat(output_str[k,:]))
    
    fprintf(cat('\\n-----------------------------------------------------\\n'))
    ## Converting the Zenith delays to a slant delay
    if size(look_angle,2) > 1 and size(look_angle,1) == 1:
        look_angle=look_angle.T
# matlab/aps_modis_InSAR.m:269
    
    if size(look_angle,2) == 1 and size(look_angle,2) != 1:
        look_angle=repmat(look_angle,1,size(d_modis,2))
# matlab/aps_modis_InSAR.m:272
    
    d_modis=d_modis / cos(look_angle)
# matlab/aps_modis_InSAR.m:274
    d_modis_no_interp=d_modis_no_interp / cos(look_angle)
# matlab/aps_modis_InSAR.m:275
    ## Converting the modis delays to a phase delay
# converting to phase delay. 
# The sign convention is such that ph_corrected = ph_original - ph_modis
    ph_SAR_modis=multiply(dot(- 4,pi) / lambda_,d_modis)
# matlab/aps_modis_InSAR.m:281
    ph_SAR_modis_no_interp=multiply(dot(- 4,pi) / lambda_,d_modis_no_interp)
# matlab/aps_modis_InSAR.m:282
    clear('d_modis','d_modis_no_interp')
    ## Computing the interferometric tropopsheric delays
# removing the dates for which there is no data.
    if isempty(ix_no_modis) != 1:
        for k in arange(1,length(ix_no_modis)).reshape(-1):
            # reject based on slave dates
            ix_ifg_reject=find(ix_no_modis[k] == ifgs_ix[:,2])
# matlab/aps_modis_InSAR.m:291
            ifgs_ix[ix_ifg_reject,:]=[]
# matlab/aps_modis_InSAR.m:292
            ix_ifg_reject=find(ix_no_modis[k] == ifgs_ix[:,1])
# matlab/aps_modis_InSAR.m:294
            ifgs_ix[ix_ifg_reject,:]=[]
# matlab/aps_modis_InSAR.m:295
            clear('ix_ifg_reject')
    
    # removing the dates for which there is no data.
    if isempty(ix_no_modis_no_interp_file) != 1:
        for k in arange(1,length(ix_no_modis_no_interp_file)).reshape(-1):
            # reject based on slave dates
            ix_ifg_reject_no_interp=find(ix_no_modis_no_interp_file[k] == ifgs_ix_no_interp[:,2])
# matlab/aps_modis_InSAR.m:304
            ifgs_ix_no_interp[ix_ifg_reject_no_interp,:]=[]
# matlab/aps_modis_InSAR.m:305
            ix_ifg_reject_no_interp=find(ix_no_modis_no_interp_file[k] == ifgs_ix_no_interp[:,1])
# matlab/aps_modis_InSAR.m:307
            ifgs_ix_no_interp[ix_ifg_reject_no_interp,:]=[]
# matlab/aps_modis_InSAR.m:308
            clear('ix_ifg_reject_no_interp')
    
    # computing the interferometric delay for each remaining interferogram
    n_ifg_modis=size(ifgs_ix,1)
# matlab/aps_modis_InSAR.m:314
    if isempty(ifgs_ix):
        fprintf('Not enough modis data to compute interferometric delays...\\n')
    
    # initialize the modis phase matrix for all interferograms, including those
# without correction.
    ph_tropo_modis=zeros(cat(n_points,n_ifg))
# matlab/aps_modis_InSAR.m:320
    ph_tropo_modis_no_interp=NaN(cat(n_points,n_ifg))
# matlab/aps_modis_InSAR.m:321
    for k in arange(1,n_ifg_modis).reshape(-1):
        ph_tropo_modis[:,ifgs_ix[k,3]]=ph_SAR_modis[:,ifgs_ix[k,1]] - ph_SAR_modis[:,ifgs_ix[k,2]]
# matlab/aps_modis_InSAR.m:323
    
    n_ifg_modis_no_interp=size(ifgs_ix_no_interp,1)
# matlab/aps_modis_InSAR.m:325
    for k in arange(1,n_ifg_modis_no_interp).reshape(-1):
        ph_tropo_modis_no_interp[:,ifgs_ix_no_interp[k,3]]=ph_SAR_modis_no_interp[:,ifgs_ix_no_interp[k,1]] - ph_SAR_modis_no_interp[:,ifgs_ix_no_interp[k,2]]
# matlab/aps_modis_InSAR.m:327
    
    # check if the data needs to be saved as recalibrated modis or not
    if strcmpi(modis_recalibrated,'y'):
        ph_tropo_modis_recal=copy(ph_tropo_modis)
# matlab/aps_modis_InSAR.m:334
        ph_tropo_modis_no_interp_recal=copy(ph_tropo_modis_no_interp)
# matlab/aps_modis_InSAR.m:335
        clear('ph_tropo_modis_no_interp','ph_tropo_modis')
        if sb_flag == 1:
            if exist(apssbname,'file') == 2:
                save(apssbname,'-append','ph_tropo_modis_recal','ph_tropo_modis_no_interp_recal')
            else:
                save(apssbname,'ph_tropo_modis_recal','ph_tropo_modis_no_interp_recal')
        else:
            if exist(apsname,'file') == 2:
                save(apsname,'-append','ph_tropo_modis_recal','ph_tropo_modis_no_interp_recal')
            else:
                save(apsname,'ph_tropo_modis_recal','ph_tropo_modis_no_interp_recal')
    else:
        if sb_flag == 1:
            if exist(apssbname,'file') == 2:
                save(apssbname,'-append','ph_tropo_modis','ph_tropo_modis_no_interp')
            else:
                save(apssbname,'ph_tropo_modis','ph_tropo_modis_no_interp')
        else:
            if exist(apsname,'file') == 2:
                save(apsname,'-append','ph_tropo_modis','ph_tropo_modis_no_interp')
            else:
                save(apsname,'ph_tropo_modis','ph_tropo_modis_no_interp')
    
    # output cloud information
    modis.SAR_no_cloud_perc = copy(SAR_modis_perc)
# matlab/aps_modis_InSAR.m:367
    modis.ix_no_data = copy(ix_no_modis_coverage)
# matlab/aps_modis_InSAR.m:368
    if exist('tca_support.mat','file') == 2:
        save('tca_support.mat','-append','modis')
    else:
        save('tca_support.mat','modis')
    