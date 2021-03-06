# Autogenerated with SMOP 
from smop.core import *
# Trainmatlab.v.0/aps_meris_SAR.m

    
@function
def aps_meris_SAR(batchfile=None,*args,**kwargs):
    varargin = aps_meris_SAR.varargin
    nargin = aps_meris_SAR.nargin

    # aps_meris_SAR(datelist)
# Scipt to load meris data, mask out clouds, interpolate over gaps and cut 
# the data to the right size for which the tropospheric delay is being computed. 
# The DEM file inputed should have an asociated
# ".rsc" file, with the same filename as the DEM. The ".rsc" files should
# contain a WIDTH, LENGTH, X_FIRST, Y_FIRST, X_STEP, Y_STEP and optional a 
# FORMAT string. The meris data is assumed to be structured in date folders. 
# The batchfile contains the full path to the meris files in these folders. 
# Note that the first line of the batchfile should read "files".
    
    
    # INPUTS:
# batchfile             A txt file containing the full path and file names of the
#                       meris data that needs to be processed. The first
#                       line of this file should read "files". The data
#                       should be structured in date folders.
# demfile               Full path to the DEM file. The DEM needs to me in meters.
# xlims                 Limits in the x-direction, either in degrees
# ylims                 Limits in the y-direction, either in degrees
# wetdry                1=calc wet only, 2=calc dry only, 3=calc both (default).
# demnull               The value for no DEM data, default is -32768.
# smpres                The output resolution, either in degrees
#                       Units needs to be consistend with xlims and ylims.
    
    # OPTIONAL INPUTS:
# conversion            Conversion factor, default 6.2 .
# scaleheight           Scale height, default 8340 m.
    
    # OUTPUTS:
# Depending on your selected option it will give computed dry, wet, or
# combined delay maps in cm. By default the wet delay is
# computed as the dry delay is not recomended to be used for meris, use era
# or weather model instead
    
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
    
    # Modified from Richard Walters - Oxford / Leeds University 2012-2013
# Modifications:
# DB 	02/2013		Convert script to a function and add syntax
# DB    02/2013		Allow for a more flexible input file name
# DB    02/2013     Make the output files independant of grd files.
# DB    02/2013     Allow the precision of the DEM to be specified in the
#                   dem input file (.rsc file).
# DB    02/2013     Adding extra syntax to the code
# DB    04/2013     Adding extra check for input arguments
# DB    04/2013     Incorporate getparm_aps from the aps_toolbox.
# DB    10/2013     Changed filename to be more consistent with toolbox
# DB    03/2014     Suppress command line output
# DB    03/2014     Include an extra check for the DEM grd file and the
#                   selected crop
# DB    07/2014     Include user interaction message for DEM check
# DB    07/2014     Redefine meris_lat(lon)_range to region_lat(lon)_range
# DB    08/2014     Include option to have factors varying for each SAR date
# DB    02/2015     Remove the hydrostatic component and only keep wet delay.
# DB    03/2015     Remove scale height paramter
    
    
    if nargin < 1:
        fprintf('load_meris(batchfile) \\n')
        error('myApp:argChk',cat('Not enough input arguments...\\n'))
    
    conversion_vector=getparm_aps('spectrometer_PIconversion')
# Trainmatlab.v.0/aps_meris_SAR.m:80
    smpres=getparm_aps('region_res')
# Trainmatlab.v.0/aps_meris_SAR.m:81
    
    xlims=getparm_aps('region_lon_range')
# Trainmatlab.v.0/aps_meris_SAR.m:83
    ylims=getparm_aps('region_lat_range')
# Trainmatlab.v.0/aps_meris_SAR.m:84
    dryconversion=0.23
# Trainmatlab.v.0/aps_meris_SAR.m:85
    wetdry=1
# Trainmatlab.v.0/aps_meris_SAR.m:86
    
    ## the actual scripting
#bounds for all ifgms in degrees or in meters
    xmin=xlims[1]
# Trainmatlab.v.0/aps_meris_SAR.m:92
    xmax=xlims[2]
# Trainmatlab.v.0/aps_meris_SAR.m:93
    ymin=ylims[1]
# Trainmatlab.v.0/aps_meris_SAR.m:94
    ymax=ylims[2]
# Trainmatlab.v.0/aps_meris_SAR.m:95
    fprintf(cat('Lon range: ',num2str(xmin),' -- ',num2str(xmax),' degrees\\n'))
    fprintf(cat('Lat range: ',num2str(ymin),' -- ',num2str(ymax),' degrees\\n'))
    fprintf(cat('Output resolution is assumed to be ',num2str(smpres),' degrees \\n'))
    # getting the number of files to be processed
    files=char(textread(batchfile,'%s','headerlines',1))
# Trainmatlab.v.0/aps_meris_SAR.m:102
    ndates=size(files,1)
# Trainmatlab.v.0/aps_meris_SAR.m:103
    # loading the date information
    stamps_processed=getparm_aps('stamps_processed')
# Trainmatlab.v.0/aps_meris_SAR.m:106
    if strcmp(stamps_processed,'y'):
        ps=load(getparm_aps('ll_matfile'))
# Trainmatlab.v.0/aps_meris_SAR.m:108
        ifgs_dates=ps.day
# Trainmatlab.v.0/aps_meris_SAR.m:109
        fprintf('Stamps processed structure \\n')
    else:
        ifgday_matfile=getparm_aps('ifgday_matfile')
# Trainmatlab.v.0/aps_meris_SAR.m:112
        ifgs_dates=load(ifgday_matfile)
# Trainmatlab.v.0/aps_meris_SAR.m:113
        ifgs_dates=ifgs_dates.ifgday
# Trainmatlab.v.0/aps_meris_SAR.m:114
        ifgs_dates=reshape(ifgs_dates,[],1)
# Trainmatlab.v.0/aps_meris_SAR.m:115
        ifgs_dates=unique(ifgs_dates)
# Trainmatlab.v.0/aps_meris_SAR.m:116
    
    # extracting the dates from the filenames
    for k in arange(1,ndates).reshape(-1):
        path,filename_temp,ext_temp=fileparts(files[k,:],nargout=3)
# Trainmatlab.v.0/aps_meris_SAR.m:122
        clear('filename_temp','ext_temp')
        path_temp,date,ext_temp=fileparts(path,nargout=3)
# Trainmatlab.v.0/aps_meris_SAR.m:124
        clear('path_temp','ext_temp')
        # save the paths as structures to allow for variable path lengths
        pathlist[k]=path
# Trainmatlab.v.0/aps_meris_SAR.m:128
        clear('path')
        # saving the date information
        datelist[k,:]=date
# Trainmatlab.v.0/aps_meris_SAR.m:131
        clear('date')
    
    if length(conversion_vector) > 1:
        fprintf('Conversion factor varies for each SAR date.\\n')
    
    #start loop here to calculate atmos correction for each date
    fprintf('Starting the computation for each SAR date \\n')
    for n in arange(1,ndates).reshape(-1):
        if length(conversion_vector) > 1:
            ix_date_postion=find(ifgs_dates == datenum(datelist[n,:],'yyyymmdd'))
# Trainmatlab.v.0/aps_meris_SAR.m:145
            conversion=conversion_vector[ix_date_postion]
# Trainmatlab.v.0/aps_meris_SAR.m:146
        else:
            conversion=copy(conversion_vector)
# Trainmatlab.v.0/aps_meris_SAR.m:148
        file=matlabarray(cat(files[n,:]))
# Trainmatlab.v.0/aps_meris_SAR.m:151
        outfile=matlabarray(cat(pathlist[n],filesep,datelist[n,:],'_SWD_nointerp.xyz'))
# Trainmatlab.v.0/aps_meris_SAR.m:152
        outfile_gauss=matlabarray(cat(pathlist[n],filesep,datelist[n,:],'_SWD_gauss.xyz'))
# Trainmatlab.v.0/aps_meris_SAR.m:153
        outfile_surf=matlabarray(cat(pathlist[n],filesep,datelist[n,:],'_SWD_surf.xyz'))
# Trainmatlab.v.0/aps_meris_SAR.m:154
        dryoutfile=matlabarray(cat(pathlist[n],filesep,datelist[n,:],'_SHD.xyz'))
# Trainmatlab.v.0/aps_meris_SAR.m:155
        tifinfo=geotiffinfo(file)
# Trainmatlab.v.0/aps_meris_SAR.m:158
        mer_xmin=tifinfo.CornerCoords.X(1)
# Trainmatlab.v.0/aps_meris_SAR.m:159
        mer_xmax=tifinfo.CornerCoords.X(2)
# Trainmatlab.v.0/aps_meris_SAR.m:160
        mer_ymin=tifinfo.CornerCoords.Y(3)
# Trainmatlab.v.0/aps_meris_SAR.m:161
        mer_ymax=tifinfo.CornerCoords.Y(1)
# Trainmatlab.v.0/aps_meris_SAR.m:162
        mer_cols=tifinfo.Width
# Trainmatlab.v.0/aps_meris_SAR.m:163
        mer_rows=tifinfo.Height
# Trainmatlab.v.0/aps_meris_SAR.m:164
        mer_x=(mer_xmax - mer_xmin) / mer_cols
# Trainmatlab.v.0/aps_meris_SAR.m:165
        mer_y=(mer_ymax - mer_ymin) / mer_rows
# Trainmatlab.v.0/aps_meris_SAR.m:166
        meris=imread(file,'tif')
# Trainmatlab.v.0/aps_meris_SAR.m:168
        #do masking, interpolating etc here.
    #convert flag matrix to long list of binary numbers e.g. 1000010000010000
        flagbin=dec2bin(meris[:,:,33])
# Trainmatlab.v.0/aps_meris_SAR.m:174
        #into matrix mask
        cloud=bin2dec(flagbin[:,2])
# Trainmatlab.v.0/aps_meris_SAR.m:178
        cloudmat=reshape(cloud,mer_rows,mer_cols)
# Trainmatlab.v.0/aps_meris_SAR.m:179
        cloudmat[cloudmat == 1]=NaN
# Trainmatlab.v.0/aps_meris_SAR.m:180
        # NaNs will penetrate through the stack
        pconf=bin2dec(flagbin[:,23])
# Trainmatlab.v.0/aps_meris_SAR.m:184
        pconfmat=reshape(pconf,mer_rows,mer_cols)
# Trainmatlab.v.0/aps_meris_SAR.m:185
        pconfmat[pconfmat == 1]=NaN
# Trainmatlab.v.0/aps_meris_SAR.m:186
        lowp=bin2dec(flagbin[:,24])
# Trainmatlab.v.0/aps_meris_SAR.m:188
        lowpmat=reshape(lowp,mer_rows,mer_cols)
# Trainmatlab.v.0/aps_meris_SAR.m:189
        lowpmat[lowpmat == 1]=NaN
# Trainmatlab.v.0/aps_meris_SAR.m:190
        maskmat=multiply(multiply(cloudmat,pconfmat),lowpmat)
# Trainmatlab.v.0/aps_meris_SAR.m:193
        maskmat[isnan(maskmat)]=1
# Trainmatlab.v.0/aps_meris_SAR.m:194
        se=strel('square',3)
# Trainmatlab.v.0/aps_meris_SAR.m:197
        maskmat=imdilate(maskmat,se)
# Trainmatlab.v.0/aps_meris_SAR.m:198
        maskmat[maskmat == 1]=NaN
# Trainmatlab.v.0/aps_meris_SAR.m:200
        maskmat[maskmat == 0]=1
# Trainmatlab.v.0/aps_meris_SAR.m:201
        watervap=meris[:,:,14]
# Trainmatlab.v.0/aps_meris_SAR.m:204
        watervap=watervap / cosd(meris[:,:,42])
# Trainmatlab.v.0/aps_meris_SAR.m:206
        watervap=multiply(watervap,conversion)
# Trainmatlab.v.0/aps_meris_SAR.m:208
        corwatervap=multiply(watervap,maskmat)
# Trainmatlab.v.0/aps_meris_SAR.m:210
        #         ### aditonal masking
#         # water mask
#         water = bin2dec(flagbin(:,3));
#         water=reshape(water,mer_rows,mer_cols);
#         
#         #decrease water mask edges, to make sure we do not remove land points
#         se = strel('square', 3);
#         water_new = imerode(water,se);
#         water_new(water_new==1)=NaN;
#         water_new(water_new==0)=1;
#         clear water
#         
#         corwatervap = corwatervap.*water_new; 
#         
#         
#         #### mask for outliers in the estimates
#         temp_data = (corwatervap - medfilt2(corwatervap, [3 3]));
#         temp  = reshape(temp_data,[],1);
#         temp(isnan(temp))=[];
#         outlier_mask = abs(temp_data)>4*std(temp);
#         outlier_mask = outlier_mask+1;
#         outlier_mask(outlier_mask==2)=NaN;
#         corwatervap = corwatervap.*outlier_mask; 
#         clear outlier_mask water maskmat
        fid=fopen('out.bin','w')
# Trainmatlab.v.0/aps_meris_SAR.m:239
        corwatervap=corwatervap.T
# Trainmatlab.v.0/aps_meris_SAR.m:240
        fwrite(fid,corwatervap,'real*4')
        fclose(fid)
        xyz2grd_cmd=matlabarray(cat('xyz2grd -R',num2str(mer_xmin),'/',num2str(mer_xmax),'/',num2str(mer_ymin),'/',num2str(mer_ymax),' -I',num2str(mer_cols),'+/',num2str(mer_rows),'+ out.bin -Gtmp.grd  -F -ZTLf'))
# Trainmatlab.v.0/aps_meris_SAR.m:246
        a,b=system(xyz2grd_cmd,nargout=2)
# Trainmatlab.v.0/aps_meris_SAR.m:247
        grd2xyz_cmd=matlabarray(cat('grd2xyz -R',num2str(mer_xmin),'/',num2str(mer_xmax),'/',num2str(mer_ymin),'/',num2str(mer_ymax),' tmp.grd -bo > tmp.xyz'))
# Trainmatlab.v.0/aps_meris_SAR.m:251
        a,b=system(grd2xyz_cmd,nargout=2)
# Trainmatlab.v.0/aps_meris_SAR.m:252
        grdfil1_cmd='grdfilter tmp.grd -Gtmp2.grd -Ni -D2 -Fg50'
# Trainmatlab.v.0/aps_meris_SAR.m:256
        a,b=system(grdfil1_cmd,nargout=2)
# Trainmatlab.v.0/aps_meris_SAR.m:257
        grdfil_cmd=matlabarray(cat('surface -R',num2str(mer_xmin),'/',num2str(mer_xmax),'/',num2str(mer_ymin),'/',num2str(mer_ymax),' tmp.xyz -I',num2str(mer_cols),'+/',num2str(mer_rows),'+ -bi -Gtmp_fil.grd -T0.5'))
# Trainmatlab.v.0/aps_meris_SAR.m:261
        a,b=system(grdfil_cmd,nargout=2)
# Trainmatlab.v.0/aps_meris_SAR.m:262
        #nointerp
        grdsmp_cmd=matlabarray(cat('grdsample -R',num2str(xmin),'/',num2str(xmax),'/',num2str(ymin),'/',num2str(ymax),' -I',num2str(smpres),' tmp.grd -Gtmp_smp.grd'))
# Trainmatlab.v.0/aps_meris_SAR.m:266
        a,b=system(grdsmp_cmd,nargout=2)
# Trainmatlab.v.0/aps_meris_SAR.m:267
        grd2xyz_cmd=matlabarray(cat('grd2xyz -R',num2str(xmin),'/',num2str(xmax),'/',num2str(ymin),'/',num2str(ymax),' tmp_smp.grd -bo >',outfile))
# Trainmatlab.v.0/aps_meris_SAR.m:268
        a,b=system(grd2xyz_cmd,nargout=2)
# Trainmatlab.v.0/aps_meris_SAR.m:269
        grdsmp_cmd=matlabarray(cat('grdsample -R',num2str(xmin),'/',num2str(xmax),'/',num2str(ymin),'/',num2str(ymax),' -I',num2str(smpres),' tmp2.grd -Gtmp_smp2.grd'))
# Trainmatlab.v.0/aps_meris_SAR.m:272
        a,b=system(grdsmp_cmd,nargout=2)
# Trainmatlab.v.0/aps_meris_SAR.m:273
        grd2xyz_cmd=matlabarray(cat('grd2xyz -R',num2str(xmin),'/',num2str(xmax),'/',num2str(ymin),'/',num2str(ymax),' tmp_smp2.grd -bo >',outfile_gauss))
# Trainmatlab.v.0/aps_meris_SAR.m:274
        a,b=system(grd2xyz_cmd,nargout=2)
# Trainmatlab.v.0/aps_meris_SAR.m:275
        grdsmp_cmd=matlabarray(cat('grdsample -R',num2str(xmin),'/',num2str(xmax),'/',num2str(ymin),'/',num2str(ymax),' -I',num2str(smpres),' tmp_fil.grd -Gtmp_smp_fil.grd'))
# Trainmatlab.v.0/aps_meris_SAR.m:277
        a,b=system(grdsmp_cmd,nargout=2)
# Trainmatlab.v.0/aps_meris_SAR.m:278
        grd2xyz_cmd=matlabarray(cat('grd2xyz -R',num2str(xmin),'/',num2str(xmax),'/',num2str(ymin),'/',num2str(ymax),' tmp_smp_fil.grd -bo >',outfile_surf))
# Trainmatlab.v.0/aps_meris_SAR.m:279
        a,b=system(grd2xyz_cmd,nargout=2)
# Trainmatlab.v.0/aps_meris_SAR.m:280
        # opening the data file (not-interpolated)
        nointfid=fopen(outfile,'r')
# Trainmatlab.v.0/aps_meris_SAR.m:284
        data_vector=fread(nointfid,'double')
# Trainmatlab.v.0/aps_meris_SAR.m:285
        fclose(nointfid)
        data=reshape(data_vector,3,[]).T
# Trainmatlab.v.0/aps_meris_SAR.m:288
        noint=data[:,3]
# Trainmatlab.v.0/aps_meris_SAR.m:289
        clear('data','data_vector')
        # opening the gaussian interpolated file
        gaussfid=fopen(outfile_gauss,'r')
# Trainmatlab.v.0/aps_meris_SAR.m:294
        data_vector=fread(gaussfid,'double')
# Trainmatlab.v.0/aps_meris_SAR.m:295
        fclose(gaussfid)
        data=reshape(data_vector,3,[]).T
# Trainmatlab.v.0/aps_meris_SAR.m:298
        gauss=data[:,3]
# Trainmatlab.v.0/aps_meris_SAR.m:299
        xy=data[:,cat(arange(1,2))]
# Trainmatlab.v.0/aps_meris_SAR.m:300
        clear('data','data_vector')
        # (gaussian interpolated points only where no data available)
        noint[isnan(noint)]=0
# Trainmatlab.v.0/aps_meris_SAR.m:304
        gauss[noint != 0]=0
# Trainmatlab.v.0/aps_meris_SAR.m:305
        gauss_interp=gauss + noint
# Trainmatlab.v.0/aps_meris_SAR.m:306
        gauss_interp[gauss_interp == 0]=NaN
# Trainmatlab.v.0/aps_meris_SAR.m:307
        data_write=cat(xy,gauss_interp).T
# Trainmatlab.v.0/aps_meris_SAR.m:309
        clear('gauss_interp','noint','gauss')
        #output
        fid=fopen(outfile_gauss,'w')
# Trainmatlab.v.0/aps_meris_SAR.m:312
        fwrite(fid,data_write,'double')
        fclose(fid)
        clear('data_write')
        #output incidence.xyz one time only
        if n == 1:
            incidence=meris[:,:,42].T
# Trainmatlab.v.0/aps_meris_SAR.m:325
            fid=fopen('out.bin','w')
# Trainmatlab.v.0/aps_meris_SAR.m:326
            fwrite(fid,incidence,'real*4')
            fclose(fid)
            xyz2grd_cmd=matlabarray(cat('xyz2grd -R',num2str(mer_xmin),'/',num2str(mer_xmax),'/',num2str(mer_ymin),'/',num2str(mer_ymax),' -I',num2str(mer_cols),'+/',num2str(mer_rows),'+ out.bin -Gtmp.grd  -F -ZTLf'))
# Trainmatlab.v.0/aps_meris_SAR.m:330
            a,b=system(xyz2grd_cmd,nargout=2)
# Trainmatlab.v.0/aps_meris_SAR.m:331
            grdsmp_cmd=matlabarray(cat('grdsample -R',num2str(xmin),'/',num2str(xmax),'/',num2str(ymin),'/',num2str(ymax),' -I',num2str(smpres),' tmp.grd -Gtmp_smp.grd'))
# Trainmatlab.v.0/aps_meris_SAR.m:332
            a,b=system(grdsmp_cmd,nargout=2)
# Trainmatlab.v.0/aps_meris_SAR.m:333
            grd2xyz_cmd=matlabarray(cat('grd2xyz -R',num2str(xmin),'/',num2str(xmax),'/',num2str(ymin),'/',num2str(ymax),' tmp_smp.grd -bo > incidence.xyz'))
# Trainmatlab.v.0/aps_meris_SAR.m:334
            a,b=system(grd2xyz_cmd,nargout=2)
# Trainmatlab.v.0/aps_meris_SAR.m:335
        fprintf(cat(num2str(n),' completed out of ',num2str(ndates),'\\n'))
    
    a,b=system('!rm tmp.grd tmp.xyz out.bin tmp2.grd tmp_fil.grd tmp_smp.grd tmp_smp.xyz tmp_smp2.grd tmp_smp_fil.grd',nargout=2)
# Trainmatlab.v.0/aps_meris_SAR.m:342