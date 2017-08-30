# Autogenerated with SMOP 
from smop.core import *
# matlab/sounding_spectrometer_sens.m

    
@function
def sounding_spectrometer_sens(k1=None,k2=None,k3=None,h_max=None,*args,**kwargs):
    varargin = sounding_spectrometer_sens.varargin
    nargin = sounding_spectrometer_sens.nargin

    # Program which extract the surface temperature from the sounding list and 
# computes the PI conversion factor for spectrometer estimation of the tropopsheric delay.
    
    # OPTIONAL INPUTS
# k1            Optional argument to specify k1 of the soundign eq in [K/Pa]
# k2            Optional argument to specify k2 of the soundign eq in [K/Pa]
# k3            Optional argument to specify k3 of the soundign eq in [K^2/Pa]
# h_max         optional argument that gives they height for which below
#               the mean temperature is computed for the atmopshere, used  
#               in the computation of the scale height
    
    # INPUTS loaded from the parms_aps file
# start_date	Start date of the sounding period, by default [], full period
#               is considered.
# end_date      End date of the sounding period, by default [], full period 
#               is considered.
# time_stamp	Include a time stamp to it. This is a column vector with 
#               strings e.g. ['00';'12'] for 00Z and 12Z. Only those files 
#               ending with this are considered in the computation.
    
    # sounding_dir	Optional argument giving directly the full path to the soundings.
#               The files on this path should be the YYYYMMDD_HH.mat files. 
# error_promp_flag By default ([] or 1) this is turn on. Can be usefull to turn of
#               when running in a batch mode. Instead NaN values will be outputed.
    
    # Output:
# Creates a .mat files with the PI conversion factor and surface temperature associated
# with different dates.
    
    
    # NOTE on data format:
# sounding data needs to be stored in a folder called sounding_data, 
# within your processing directory. Within this folder, each sounding 
# aquisition needs to be stored in as 8 digit .mat files, e.g. YYYYMMDD_HH.mat 
# format, with the  pressure (hPa), temperature (degree), relative humidity (#)
# and heights (m) as matlab variables P, T, RH and h.
    
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
    
    # April 2013 --- Bekaert David 
# Modifications:
# 12/04/2013    Bekaert David   Include compuation for PI factor from
#                               Richard Walters shell script.
# 21/10/2013    Bekaert David   Include in APS toolbox, retrieve parms
#                               from parms_aps.
# 19/03/2014    Bekaert David   Suppress command line output, same setup of
#                               variable saving as for power-law
# 14/05/2014	Bekaert David	rename to spectrometer function name
    
    # --------- VARIABELS ---------- #
    fontsize=15
# matlab/sounding_spectrometer_sens.m:67
    
    save_fig=1
# matlab/sounding_spectrometer_sens.m:68
    ## Setting the defaults were needed
# setting the constants
    if nargin < 1 or isempty(k1):
        k1=0.776
# matlab/sounding_spectrometer_sens.m:73
    
    if nargin < 2 or isempty(k2):
        k2=0.704
# matlab/sounding_spectrometer_sens.m:76
    
    if nargin < 3 or isempty(k3):
        k3=3739
# matlab/sounding_spectrometer_sens.m:79
    
    if nargin < 4 or isempty(h_max):
        h_max=20000
# matlab/sounding_spectrometer_sens.m:82
        # height are used to compute the mean
                                    # temperature for the scale height
    
    curdir=copy(pwd)
# matlab/sounding_spectrometer_sens.m:87
    # getting parameters from parms_aps file
    sounding_dir=getparm_aps('sounding_dir')
# matlab/sounding_spectrometer_sens.m:90
    error_promp_flag=getparm_aps('sounding_error_promp')
# matlab/sounding_spectrometer_sens.m:91
    # getting teh time stamp needed
    time_stamp=getparm_aps('sounding_time_stamp')
# matlab/sounding_spectrometer_sens.m:94
    time_stamp_str=matlabarray([])
# matlab/sounding_spectrometer_sens.m:95
    for k in arange(1,size(time_stamp,1)).reshape(-1):
        if k > 1:
            time_stamp_str=matlabarray(cat(time_stamp_str,'_',time_stamp[k,:]))
# matlab/sounding_spectrometer_sens.m:98
        else:
            time_stamp_str=matlabarray(cat(time_stamp[k,:]))
# matlab/sounding_spectrometer_sens.m:100
    
    # check if it needs to be computed on SAR dates or not
    sounding_ifg_dates=getparm_aps('sounding_ifg_dates')
# matlab/sounding_spectrometer_sens.m:105
    if strcmp(sounding_ifg_dates,'y'):
        sar_date_sounding=1
# matlab/sounding_spectrometer_sens.m:107
        # It used a window arounf the data, but it wil first check if the date
    # itself has data and use that value. Incase there is no data for the
    # SAR date it will use an average
        # loading the data
        stamps_processed=getparm_aps('stamps_processed')
# matlab/sounding_spectrometer_sens.m:115
        if strcmp(stamps_processed,'y'):
            ll_matfile=getparm_aps('ll_matfile',1)
# matlab/sounding_spectrometer_sens.m:117
            ps=load(ll_matfile)
# matlab/sounding_spectrometer_sens.m:118
            ifgs_dates=ps.day
# matlab/sounding_spectrometer_sens.m:119
            fprintf('Stamps processed structure \\n')
        else:
            ifgday_matfile=getparm_aps('ifgday_matfile',1)
# matlab/sounding_spectrometer_sens.m:122
            ifgs_dates=load(ifgday_matfile)
# matlab/sounding_spectrometer_sens.m:123
            ifgs_dates=ifgs_dates.ifgday
# matlab/sounding_spectrometer_sens.m:124
            ifgs_dates=reshape(ifgs_dates,[],1)
# matlab/sounding_spectrometer_sens.m:125
            ifgs_dates=unique(ifgs_dates)
# matlab/sounding_spectrometer_sens.m:126
        date_start_vector=datestr(ifgs_dates - 15,'yyyymmdd')
# matlab/sounding_spectrometer_sens.m:129
        date_end_vector=datestr(ifgs_dates + 15,'yyyymmdd')
# matlab/sounding_spectrometer_sens.m:130
        date_start_temp=getparm_aps('sounding_start_date')
# matlab/sounding_spectrometer_sens.m:133
        date_end_temp=getparm_aps('sounding_end_date')
# matlab/sounding_spectrometer_sens.m:134
        start_year_str=date_start_temp[1:4]
# matlab/sounding_spectrometer_sens.m:135
        end_year_str=date_end_temp[1:4]
# matlab/sounding_spectrometer_sens.m:136
        start_str=date_start_temp[5:6]
# matlab/sounding_spectrometer_sens.m:137
        end_str=date_end_temp[5:6]
# matlab/sounding_spectrometer_sens.m:138
        save_name_final=matlabarray(cat(sounding_dir,filesep,'Spectrometer',filesep,'Spectrometer_sensitivity_SAR_dates_1month_',time_stamp_str,'Hr_',num2str(start_year_str),start_str,'_',num2str(end_year_str),end_str,'.mat'))
# matlab/sounding_spectrometer_sens.m:140
        if exist(cat(sounding_dir,filesep,'Spectrometer'),'dir') != 7:
            mkdir(cat(sounding_dir,filesep,'Spectrometer'))
    else:
        # this is regular sensitivity on a wider range of data
        sar_date_sounding=0
# matlab/sounding_spectrometer_sens.m:150
        date_start_vector=getparm_aps('sounding_start_date')
# matlab/sounding_spectrometer_sens.m:151
        date_end_vector=getparm_aps('sounding_end_date')
# matlab/sounding_spectrometer_sens.m:152
        start_year_str=date_start_vector[1:4]
# matlab/sounding_spectrometer_sens.m:154
        end_year_str=date_end_vector[1:4]
# matlab/sounding_spectrometer_sens.m:155
        start_str=date_start_vector[5:6]
# matlab/sounding_spectrometer_sens.m:156
        end_str=date_end_vector[5:6]
# matlab/sounding_spectrometer_sens.m:157
        save_name_final=matlabarray(cat(sounding_dir,filesep,'Spectrometer',filesep,'Spectrometer_sensitivity_',time_stamp_str,'Hr_',num2str(start_year_str),start_str,'_',num2str(end_year_str),end_str,'.mat'))
# matlab/sounding_spectrometer_sens.m:159
    
    # Constants
    R=8.3144621
# matlab/sounding_spectrometer_sens.m:164
    
    Mw=0.01801528
# matlab/sounding_spectrometer_sens.m:165
    
    Md=0.02897
# matlab/sounding_spectrometer_sens.m:166
    
    pw=1000
# matlab/sounding_spectrometer_sens.m:167
    
    g=9.80666
# matlab/sounding_spectrometer_sens.m:168
    
    if save_fig == logical_and(1,exist(cat(sounding_dir,filesep,'Spectrometer',filesep,'figures'),'dir')) != 7:
        mkdir(cat(sounding_dir,filesep,'Spectrometer',filesep,'figures'))
    
    if save_fig == logical_and(1,exist(cat(sounding_dir,filesep,'Spectrometer',filesep,'figures',filesep,'PI_factor'),'dir')) != 7:
        mkdir(cat(sounding_dir,filesep,'Spectrometer',filesep,'figures',filesep,'PI_factor'))
    
    if save_fig == 1 and exist(cat(sounding_dir,filesep,'Spectrometer',filesep,'figures',filesep,'H_scaling_factor'),'dir') != 7:
        mkdir(cat(sounding_dir,filesep,'Spectrometer',filesep,'figures',filesep,'H_scaling_factor'))
    
    # looping over the data. In case SAR sensitivity is needed no average is
# pased:
    for date_counter in arange(1,size(date_start_vector,1)).reshape(-1):
        start_date=date_start_vector[date_counter,:]
# matlab/sounding_spectrometer_sens.m:186
        end_date=date_end_vector[date_counter,:]
# matlab/sounding_spectrometer_sens.m:187
        start_year_str=start_date[1:4]
# matlab/sounding_spectrometer_sens.m:190
        end_year_str=end_date[1:4]
# matlab/sounding_spectrometer_sens.m:191
        start_str=start_date[5:6]
# matlab/sounding_spectrometer_sens.m:192
        end_str=end_date[5:6]
# matlab/sounding_spectrometer_sens.m:193
        # NaN values as output.
        continue_flag=1
# matlab/sounding_spectrometer_sens.m:197
        abord_flag=0
# matlab/sounding_spectrometer_sens.m:198
        while continue_flag:

            ## Getting the file list of the sounding data
            if isempty(sounding_dir) != 1:
                if exist(cat(sounding_dir,filesep),'dir') != 7:
                    error('myApp:argChk',cat('The specified filepath of the sounding data does not exist,...  \\nAbort,... \\n'))
                cd(sounding_dir)
            else:
                if exist('sounding_data/','dir') != 7:
                    error('myApp:argChk',cat('There is no sounding_data directory,...  \\nAbort,... \\n'))
                cd('sounding_data')
            if exist('sounding.list','file') != 2:
                # making a list of all the sounding files
                command_str=matlabarray(cat('echo sounding_list > sounding.list'))
# matlab/sounding_spectrometer_sens.m:215
                a,b=system(command_str,nargout=2)
# matlab/sounding_spectrometer_sens.m:216
                clear('command_str')
                for k in arange(1,size(time_stamp,1)).reshape(-1):
                    command_str=matlabarray(cat('ls [0-9]???????_',time_stamp[k,:],'.mat >> sounding.list'))
# matlab/sounding_spectrometer_sens.m:219
                    a,b=system(command_str,nargout=2)
# matlab/sounding_spectrometer_sens.m:220
            temp=tdfread('sounding.list')
# matlab/sounding_spectrometer_sens.m:223
            command_str=matlabarray(cat('rm sounding.list'))
# matlab/sounding_spectrometer_sens.m:224
            a,b=system(command_str,nargout=2)
# matlab/sounding_spectrometer_sens.m:225
            clear('command_str')
            date_list_temp=temp.sounding_list(arange(),cat(arange(1,8)))
# matlab/sounding_spectrometer_sens.m:228
            sounding_list=temp.sounding_list
# matlab/sounding_spectrometer_sens.m:229
            clear('ix')
            if isempty(start_date) != 1 and isempty(end_date) != 1:
                ix=find(datenum(date_list_temp,'yyyymmdd') >= logical_and(datenum(start_date,'yyyymmdd'),datenum(date_list_temp,'yyyymmdd')) <= datenum(end_date,'yyyymmdd'))
# matlab/sounding_spectrometer_sens.m:234
            else:
                if isempty(start_date) != 1 and isempty(end_date) == 1:
                    ix=find(datenum(date_list_temp,'yyyymmdd') >= datenum(start_date,'yyyymmdd'))
# matlab/sounding_spectrometer_sens.m:236
                else:
                    if isempty(start_date) == 1 and isempty(end_date) != 1:
                        ix=find(datenum(date_list_temp,'yyyymmdd') <= datenum(end_date,'yyyymmdd'))
# matlab/sounding_spectrometer_sens.m:238
            if isempty(start_date) != 1 or isempty(end_date) != 1:
                if isempty(ix) != 1:
                    date_list_temp=date_list_temp[ix,:]
# matlab/sounding_spectrometer_sens.m:245
                    sounding_list=sounding_list[ix,:]
# matlab/sounding_spectrometer_sens.m:246
                else:
                    fprintf('No sounding has been acquired in this period \\n')
                    continue_flag=0
# matlab/sounding_spectrometer_sens.m:249
                    abord_flag=1
# matlab/sounding_spectrometer_sens.m:250
                    break
                clear('temp','ix')
            ## Computing refractivity
            fprintf('Loading the data \\n')
            ix_skip_sounding=matlabarray([])
# matlab/sounding_spectrometer_sens.m:259
            # initialisation of the variables
            hs_vector=NaN(cat(size(sounding_list,1),1))
# matlab/sounding_spectrometer_sens.m:262
            date_vector_J=NaN(cat(size(sounding_list,1),1))
# matlab/sounding_spectrometer_sens.m:263
            Ts_vector=NaN(cat(size(sounding_list,1),1))
# matlab/sounding_spectrometer_sens.m:264
            Tm_vector=NaN(cat(size(sounding_list,1),1))
# matlab/sounding_spectrometer_sens.m:265
            h_scaling_vector=NaN(cat(size(sounding_list,1),1))
# matlab/sounding_spectrometer_sens.m:266
            T_mean_vector=NaN(cat(size(sounding_list,1),1))
# matlab/sounding_spectrometer_sens.m:267
            Pi_factor_vector=NaN(cat(size(sounding_list,1),1))
# matlab/sounding_spectrometer_sens.m:268
            for i in arange(1,size(sounding_list,1)).reshape(-1):
                load(sounding_list[i,:])
                # - P (pressure in [hPa])
            # - T (temperature in [degrees])
            # - RH (relative humidity in [#]) 
            # - h (altitude in [m])
                # coping with NaN values in the RH data
                ix1=find(isnan(RH) == 1)
# matlab/sounding_spectrometer_sens.m:279
                ix2=find(isnan(h) == 1)
# matlab/sounding_spectrometer_sens.m:280
                ix=unique(cat([ix1],[ix2]))
# matlab/sounding_spectrometer_sens.m:281
                P[ix]=[]
# matlab/sounding_spectrometer_sens.m:282
                RH[ix]=[]
# matlab/sounding_spectrometer_sens.m:283
                T[ix]=[]
# matlab/sounding_spectrometer_sens.m:284
                h[ix]=[]
# matlab/sounding_spectrometer_sens.m:285
                clear('ix','ix1','ix2')
                # coping with errors in the data when a double recording was made
                ix_repeat=find(diff(sort(h)) == 0)
# matlab/sounding_spectrometer_sens.m:289
                h[ix_repeat]=[]
# matlab/sounding_spectrometer_sens.m:290
                P[ix_repeat]=[]
# matlab/sounding_spectrometer_sens.m:291
                RH[ix_repeat]=[]
# matlab/sounding_spectrometer_sens.m:292
                T[ix_repeat]=[]
# matlab/sounding_spectrometer_sens.m:293
                clear('ix_repeat')
                # Checking if there is still data left
                if isempty(h) == 1 and size(sounding_list,1) == 1 and error_promp_flag == 1:
                    error('myApp:argChk',cat('Datafile contains no numeric data. \\n'))
                else:
                    if isempty(h) == 1:
                        fprintf(cat(sounding_list[i,:],' sounding skipped as it containes no numeric data\\n'))
                        skip_sounding=1
# matlab/sounding_spectrometer_sens.m:302
                        ix_skip_sounding=matlabarray(cat([ix_skip_sounding],[i]))
# matlab/sounding_spectrometer_sens.m:303
                    else:
                        skip_sounding=0
# matlab/sounding_spectrometer_sens.m:305
                # when possible compute the PI factor
                if skip_sounding == 1:
                    # case of no data
                    hs=copy(NaN)
# matlab/sounding_spectrometer_sens.m:311
                    Ts=copy(NaN)
# matlab/sounding_spectrometer_sens.m:312
                    Tm=copy(NaN)
# matlab/sounding_spectrometer_sens.m:313
                    PI=copy(NaN)
# matlab/sounding_spectrometer_sens.m:314
                else:
                    # getting the surface elevation and surface temperature
                    hs=h[1]
# matlab/sounding_spectrometer_sens.m:318
                    Ts=T[1]
# matlab/sounding_spectrometer_sens.m:319
                    # computation of the PI factor
                    Tm=(70.2 + dot(0.72,(Ts + 273.15))) - 273.15
# matlab/sounding_spectrometer_sens.m:322
                    PI=dot(dot(dot(1e-06,pw),(R / Mw)),(k3 / (Tm + 273.15) + (k2 - (dot(k1,(Mw / Md))))))
# matlab/sounding_spectrometer_sens.m:323
                PI_factor.PI = copy(PI)
# matlab/sounding_spectrometer_sens.m:325
                PI_factor.Tm = copy(Tm)
# matlab/sounding_spectrometer_sens.m:326
                PI_factor.Ts = copy(Ts)
# matlab/sounding_spectrometer_sens.m:327
                PI_factor.hs = copy(hs)
# matlab/sounding_spectrometer_sens.m:328
                T_mean=mean(T[h <= h_max])
# matlab/sounding_spectrometer_sens.m:331
                H_scaling_factor=dot(R,(T_mean + 273.15)) / (dot(Md,g))
# matlab/sounding_spectrometer_sens.m:332
                H_scaling.H_scaling = copy(H_scaling_factor)
# matlab/sounding_spectrometer_sens.m:333
                H_scaling.T_mean = copy(T_mean)
# matlab/sounding_spectrometer_sens.m:334
                save(sounding_list[i,:],'-append','PI_factor','H_scaling')
                # Generating a vector for the output
                Pi_factor_vector[i]=PI
# matlab/sounding_spectrometer_sens.m:341
                date_vector_J[i]=datenum(date_list_temp[i,:],'yyyymmdd')
# matlab/sounding_spectrometer_sens.m:342
                hs_vector[i]=hs
# matlab/sounding_spectrometer_sens.m:343
                Ts_vector[i]=Ts
# matlab/sounding_spectrometer_sens.m:344
                Tm_vector[i]=Tm
# matlab/sounding_spectrometer_sens.m:345
                h_scaling_vector[i]=H_scaling_factor
# matlab/sounding_spectrometer_sens.m:346
                T_mean_vector[i]=T_mean
# matlab/sounding_spectrometer_sens.m:347
                clear('P','h','RH','T','PI','Tm','TS','hs','PI_factor','H_scaling_factor','T_mean')
                if floor(i / 10) == i / 10:
                    fprintf(cat(num2str(i),' out of ',num2str(size(sounding_list,1)),' done \\n'))
            clear('Rv','T0','L','e0','es','e','i','figure1')
            # remove those sounding acqusitions that have no data coverage
            if isempty(ix_skip_sounding) != 1:
                sounding_list[ix_skip_sounding,:]=[]
# matlab/sounding_spectrometer_sens.m:360
            continue_flag=0
# matlab/sounding_spectrometer_sens.m:363
            abord_flag=0
# matlab/sounding_spectrometer_sens.m:364

        # The while loop was existed because of an error statement.
        if abord_flag == 1 and sar_date_sounding == 0:
            Pi_factor_vector=copy(NaN)
# matlab/sounding_spectrometer_sens.m:369
            date_vector_J=copy(NaN)
# matlab/sounding_spectrometer_sens.m:370
            hs_vector=copy(NaN)
# matlab/sounding_spectrometer_sens.m:371
            Ts_vector=copy(NaN)
# matlab/sounding_spectrometer_sens.m:372
            Tm_vector=copy(NaN)
# matlab/sounding_spectrometer_sens.m:373
            h_scaling_vector=copy(NaN)
# matlab/sounding_spectrometer_sens.m:374
            T_mean_vector=copy(NaN)
# matlab/sounding_spectrometer_sens.m:375
            fprintf('Early termination \\n')
        else:
            if abord_flag == 1 and sar_date_sounding == 1:
                spectrometer_scaleheight[date_counter]=NaN
# matlab/sounding_spectrometer_sens.m:378
                spectrometer_PIconversion[date_counter]=NaN
# matlab/sounding_spectrometer_sens.m:379
            else:
                # checking for outliers
                ix_outlier=matlabarray([])
# matlab/sounding_spectrometer_sens.m:382
                # start acquiring at a latter stage
                ix_nan=isnan(hs_vector)
# matlab/sounding_spectrometer_sens.m:385
                hs_median=median(hs_vector[logical_not(ix_nan)])
# matlab/sounding_spectrometer_sens.m:386
                # the median elevation
                ix_hs=find(abs(hs_vector - hs_median) >= 20)
# matlab/sounding_spectrometer_sens.m:389
                fprintf('\\n Search for soundings that did not start acquiring at the surface \\n')
                if isempty(ix_hs):
                    fprintf('All soundings have their surface height within +-20m of the median elevation. \\n')
                else:
                    fprintf(cat(num2str(length(ix_hs)),' soundings were found to deviate more than +-20m of the median elevation.\\n'))
                    ix_outlier=matlabarray(cat([ix_outlier],[ix_hs]))
# matlab/sounding_spectrometer_sens.m:396
                # Mean temperatures. It might occur that the sounding ballon only
        # start acquiring at a latter stage
                Ts_mean=mean(Ts_vector[logical_not(ix_nan)])
# matlab/sounding_spectrometer_sens.m:400
                # the median elevation
                ix_Ts=find(abs(Ts_vector - Ts_mean) > 15)
# matlab/sounding_spectrometer_sens.m:403
                if isempty(ix_Ts):
                    fprintf('All soundings have their mean temperatue within +-15deg of the mean temperature of all soundings. \\n')
                else:
                    fprintf(cat(num2str(length(ix_Ts)),' soundings were found to have their mean temperatue to deviate more than +-15deg of the mean temperature of all soundings.\\n'))
                    ix_outlier=matlabarray(cat([ix_outlier],[ix_Ts]))
# matlab/sounding_spectrometer_sens.m:408
                # remove potential duplicates
                ix_outlier=unique(ix_outlier)
# matlab/sounding_spectrometer_sens.m:411
                if save_fig == 1 and sar_date_sounding == 0:
                    if isempty(ix_outlier) != 1:
                        hfig=figure('name','Pi-factor variation with potential outliers')
# matlab/sounding_spectrometer_sens.m:415
                        plot(date_vector_J,Pi_factor_vector,'k.')
                        datetick('x','mmm/yyyy')
                        ylabel('PI Factor','fontsize',fontsize)
                        title(cat('PI-factor for surface temperature at ',num2str(mean(hs_vector[logical_not(ix_nan)])),' m elevation'),'fontsize',fontsize)
                        set(gca,'fontsize',fontsize)
                        hfig2=figure('name','Surface elevation variation with potential outliers')
# matlab/sounding_spectrometer_sens.m:422
                        plot(date_vector_J,hs_vector,'k.')
                        datetick('x','mmm/yyyy')
                        ylabel('Surface elevation [m]','fontsize',fontsize)
                        title(cat('Surface elevation variation'),'fontsize',fontsize)
                        set(gca,'fontsize',fontsize)
                        hfig3=figure('name','Surface temperature variation with potential outliers')
# matlab/sounding_spectrometer_sens.m:429
                        plot(date_vector_J,Ts_vector,'k.')
                        datetick('x','mmm/yyyy')
                        ylabel('Surface temperature [deg]','fontsize',fontsize)
                        title(cat('Surface Temperature variation'),'fontsize',fontsize)
                        set(gca,'fontsize',fontsize)
                        hfig4=figure('name','Scaling height with potential outliers')
# matlab/sounding_spectrometer_sens.m:436
                        plot(date_vector_J,h_scaling_vector / 1000,'k.')
                        datetick('x','mmm/yyyy')
                        ylabel('Scaling height [km]','fontsize',fontsize)
                        title(cat('Scaling height variation variation'),'fontsize',fontsize)
                        set(gca,'fontsize',fontsize)
                        hfig5=figure('name','Mean temperature with potential outliers')
# matlab/sounding_spectrometer_sens.m:443
                        plot(date_vector_J,T_mean_vector / 1000,'k.')
                        datetick('x','mmm/yyyy')
                        ylabel('Mean temperature [deg]','fontsize',fontsize)
                        title(cat('Mean temperature from elevations below ',num2str(h_max / 1000),' km'),'fontsize',fontsize)
                        set(gca,'fontsize',fontsize)
                        # saving of the figure when requested
                        if save_fig == 1:
                            fprintf(cat('Figure with _wpo refers to with potential outliers \\n'))
                            fig_save_name=matlabarray(cat(sounding_dir,filesep,'Spectrometer',filesep,'figures',filesep,'PI_factor',filesep,'PI_factor_wpo.eps'))
# matlab/sounding_spectrometer_sens.m:455
                            set(hfig,'PaperPositionMode','auto')
                            print_(hfig,'-depsc','-r150',fig_save_name)
                            clear('fig_save_name')
                            fig_save_name=matlabarray(cat(sounding_dir,filesep,'Spectrometer',filesep,'figures',filesep,'PI_factor',filesep,'surface_elevation_wpo.eps'))
# matlab/sounding_spectrometer_sens.m:460
                            set(hfig2,'PaperPositionMode','auto')
                            print_(hfig2,'-depsc','-r150',fig_save_name)
                            clear('fig_save_name')
                            fig_save_name=matlabarray(cat(sounding_dir,filesep,'Spectrometer',filesep,'figures',filesep,'PI_factor',filesep,'surface_temp_wpo.eps'))
# matlab/sounding_spectrometer_sens.m:465
                            set(hfig3,'PaperPositionMode','auto')
                            print_(hfig3,'-depsc','-r150',fig_save_name)
                            clear('fig_save_name')
                            fig_save_name=matlabarray(cat(sounding_dir,filesep,'Spectrometer',filesep,'figures',filesep,'H_scaling_factor',filesep,'H_scaling_wpo.eps'))
# matlab/sounding_spectrometer_sens.m:470
                            set(hfig4,'PaperPositionMode','auto')
                            print_(hfig4,'-depsc','-r150',fig_save_name)
                            clear('fig_save_name')
                            fig_save_name=matlabarray(cat(sounding_dir,filesep,'Spectrometer',filesep,'figures',filesep,'H_scaling_factor',filesep,'Mean_temp_wpo.eps'))
# matlab/sounding_spectrometer_sens.m:475
                            set(hfig5,'PaperPositionMode','auto')
                            print_(hfig5,'-depsc','-r150',fig_save_name)
                            clear('fig_save_name')
                        clear('figure2')
                    ix_no_outlier=cat(arange(1,length(Pi_factor_vector))).T
# matlab/sounding_spectrometer_sens.m:486
                    ix_no_outlier[ix_outlier]=[]
# matlab/sounding_spectrometer_sens.m:487
                    hfig=figure('name','Pi-factor variation')
# matlab/sounding_spectrometer_sens.m:489
                    plot(date_vector_J[ix_no_outlier],Pi_factor_vector[ix_no_outlier],'k.')
                    datetick('x','mmm/yyyy')
                    ylabel('PI Factor','fontsize',fontsize)
                    title(cat('PI-factor for surface temperature at ',num2str(mean(hs_vector[logical_not(ix_nan)])),' m elevation'),'fontsize',fontsize)
                    set(gca,'fontsize',fontsize)
                    hfig2=figure('name','Surface elevation variation')
# matlab/sounding_spectrometer_sens.m:496
                    plot(date_vector_J[ix_no_outlier],hs_vector[ix_no_outlier],'k.')
                    datetick('x','mmm/yyyy')
                    ylabel('Surface elevation [m]','fontsize',fontsize)
                    title(cat('Surface elevation variation'),'fontsize',fontsize)
                    set(gca,'fontsize',fontsize)
                    hfig3=figure('name','Surface temperature variation')
# matlab/sounding_spectrometer_sens.m:503
                    plot(date_vector_J[ix_no_outlier],Ts_vector[ix_no_outlier],'k.')
                    datetick('x','mmm/yyyy')
                    ylabel('Surface temperature [deg]','fontsize',fontsize)
                    title(cat('Surface Temperature variation'),'fontsize',fontsize)
                    set(gca,'fontsize',fontsize)
                    hfig4=figure('name','Scaling height')
# matlab/sounding_spectrometer_sens.m:510
                    plot(date_vector_J[ix_no_outlier],h_scaling_vector[ix_no_outlier] / 1000,'k.')
                    datetick('x','mmm/yyyy')
                    ylabel('Scaling height [km]','fontsize',fontsize)
                    title(cat('Scaling height variation variation'),'fontsize',fontsize)
                    set(gca,'fontsize',fontsize)
                    hfig5=figure('name','Mean temperature')
# matlab/sounding_spectrometer_sens.m:517
                    plot(date_vector_J[ix_no_outlier],T_mean_vector[ix_no_outlier] / 1000,'k.')
                    datetick('x','mmm/yyyy')
                    ylabel('Mean temperature [deg]','fontsize',fontsize)
                    title(cat('Mean temperature from elevations below ',num2str(h_max / 1000),' km'),'fontsize',fontsize)
                    set(gca,'fontsize',fontsize)
                    # saving of the figure when requested
                    if save_fig == 1:
                        fig_save_name=matlabarray(cat(sounding_dir,filesep,'Spectrometer',filesep,'figures',filesep,'PI_factor',filesep,'PI_factor.eps'))
# matlab/sounding_spectrometer_sens.m:527
                        set(hfig,'PaperPositionMode','auto')
                        print_(hfig,'-depsc','-r150',fig_save_name)
                        clear('fig_save_name')
                        fig_save_name=matlabarray(cat(sounding_dir,filesep,'Spectrometer',filesep,'figures',filesep,'PI_factor',filesep,'surface_elevation.eps'))
# matlab/sounding_spectrometer_sens.m:532
                        set(hfig2,'PaperPositionMode','auto')
                        print_(hfig2,'-depsc','-r150',fig_save_name)
                        clear('fig_save_name')
                        fig_save_name=matlabarray(cat(sounding_dir,filesep,'Spectrometer',filesep,'figures',filesep,'PI_factor',filesep,'surface_temp.eps'))
# matlab/sounding_spectrometer_sens.m:537
                        set(hfig3,'PaperPositionMode','auto')
                        print_(hfig3,'-depsc','-r150',fig_save_name)
                        clear('fig_save_name')
                        fig_save_name=matlabarray(cat(sounding_dir,filesep,'Spectrometer',filesep,'figures',filesep,'H_scaling_factor',filesep,'H_scaling.eps'))
# matlab/sounding_spectrometer_sens.m:542
                        set(hfig4,'PaperPositionMode','auto')
                        print_(hfig4,'-depsc','-r150',fig_save_name)
                        clear('fig_save_name')
                        fig_save_name=matlabarray(cat(sounding_dir,filesep,'Spectrometer',filesep,'figures',filesep,'H_scaling_factor',filesep,'Mean_temp.eps'))
# matlab/sounding_spectrometer_sens.m:547
                        set(hfig5,'PaperPositionMode','auto')
                        print_(hfig5,'-depsc','-r150',fig_save_name)
                        clear('fig_save_name')
                    clear('figure2')
                if sar_date_sounding == 1:
                    Pi_factor_vector[ix_outlier]=[]
# matlab/sounding_spectrometer_sens.m:562
                    date_vector_J[ix_outlier]=[]
# matlab/sounding_spectrometer_sens.m:563
                    h_scaling_vector[ix_outlier]=[]
# matlab/sounding_spectrometer_sens.m:564
                    ix_ourlier=find(sum(isnan(cat(Pi_factor_vector,h_scaling_vector)),2) >= 1)
# matlab/sounding_spectrometer_sens.m:566
                    Pi_factor_vector[ix_outlier]=[]
# matlab/sounding_spectrometer_sens.m:567
                    date_vector_J[ix_outlier]=[]
# matlab/sounding_spectrometer_sens.m:568
                    h_scaling_vector[ix_outlier]=[]
# matlab/sounding_spectrometer_sens.m:569
                    # stamp
                    ix_SAR_date=find(ifgs_dates[date_counter] == date_vector_J)
# matlab/sounding_spectrometer_sens.m:573
                    if logical_not(isempty(ix_SAR_date)):
                        spectrometer_scaleheight[date_counter]=nanmean(h_scaling_vector[ix_SAR_date])
# matlab/sounding_spectrometer_sens.m:576
                        spectrometer_PIconversion[date_counter]=nanmean(Pi_factor_vector[ix_SAR_date])
# matlab/sounding_spectrometer_sens.m:577
                    else:
                        if logical_not(isempty(Pi_factor_vector)):
                            spectrometer_scaleheight[date_counter]=nanmean(h_scaling_vector)
# matlab/sounding_spectrometer_sens.m:580
                            spectrometer_PIconversion[date_counter]=nanmean(Pi_factor_vector)
# matlab/sounding_spectrometer_sens.m:581
                        else:
                            spectrometer_scaleheight[date_counter]=NaN
# matlab/sounding_spectrometer_sens.m:583
                            spectrometer_PIconversion[date_counter]=NaN
# matlab/sounding_spectrometer_sens.m:584
                    if spectrometer_PIconversion[date_counter] == 0:
                        keyboard
                # saving of the data
                if date_counter == size(date_start_vector,1) and sar_date_sounding == 0:
                    fprintf('DONE \\n')
                    save(save_name_final,'date_vector_J','Pi_factor_vector','hs_vector','Ts_vector','Tm_vector','h_scaling_vector','T_mean_vector','ix_outlier','h_max')
                    spectrometer_scaleheight=nanmean(h_scaling_vector[ix_no_outlier])
# matlab/sounding_spectrometer_sens.m:599
                    spectrometer_PIconversion=nanmean(Pi_factor_vector[ix_no_outlier])
# matlab/sounding_spectrometer_sens.m:600
                    cd(curdir)
                    # updating of the parm_aps list
                    setparm_aps('spectrometer_scaleheight',spectrometer_scaleheight)
                    setparm_aps('spectrometer_PIconversion',spectrometer_PIconversion)
                else:
                    if date_counter == size(date_start_vector,1) and sar_date_sounding == 1:
                        cd(curdir)
                        # checking if some of the dates were not estimated.
            # take the mean of all existing to fill them in
                        ix_nan=find(isnan(spectrometer_PIconversion) == 1)
# matlab/sounding_spectrometer_sens.m:612
                        if logical_not(isempty(ix_nan)):
                            fprintf('Some dates did not have sounding data, fill the factors with the mean of the dates \\n')
                            datestr(ifgs_dates[ix_nan],'yyyymmdd')
                            spectrometer_scaleheight[ix_nan]=nanmean(spectrometer_scaleheight)
# matlab/sounding_spectrometer_sens.m:616
                            spectrometer_PIconversion[ix_nan]=nanmean(spectrometer_PIconversion)
# matlab/sounding_spectrometer_sens.m:617
                        # updating of the parm_aps list
                        setparm_aps('spectrometer_scaleheight',spectrometer_scaleheight)
                        setparm_aps('spectrometer_PIconversion',spectrometer_PIconversion)
                        save(save_name_final,'spectrometer_PIconversion','spectrometer_scaleheight','ix_nan','h_max','ifgs_dates')
    
    cd(curdir)