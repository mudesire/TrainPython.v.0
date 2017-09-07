# Autogenerated with SMOP 
from smop.core import *
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m

    
@function
def aps_spectrometer_PWV_meris(batchfile=None,*args,**kwargs):
    varargin = aps_spectrometer_PWV_meris.varargin
    nargin = aps_spectrometer_PWV_meris.nargin

    # aps_spectrometer_PWV_comparison(datelist)
# Scipt to load meris data, mask out clouds. The meris data is assumed to 
# be structured in date folders. The batchfile contains the full path to the
# meris files in these folders. Note that the first line of the batchfile should read "files".
    
    
    # INPUTS:
# batchfile             A txt file containing the full path and file names of the
#                       meris data that needs to be processed. The first
#                       line of this file should read "files". The data
#                       should be structured in date folders.
# xlims                 Limits in the x-direction, either in degrees
# ylims                 Limits in the y-direction, either in degrees
# smpres                The output resolution, either in degrees
#                       Units needs to be consistend with xlims and ylims.
    
    
    # By David Bekaert - University of Leeds
# August 2014
    
    fig_test=1
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:22
    
    if nargin < 1:
        fprintf('aps_spectrometer_PWV_meris(batchfile) \\n')
        error('myApp:argChk',cat('Not enough input arguments...\\n'))
    
    smpres=getparm_aps('region_res',1)
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:32
    
    xlims=getparm_aps('region_lon_range',1)
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:33
    ylims=getparm_aps('region_lat_range',1)
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:34
    stamps_processed=getparm_aps('stamps_processed',1)
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:35
    ## the actual scripting
#bounds for all ifgs in degrees or in meters
    xmin=xlims[1]
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:41
    xmax=xlims[2]
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:42
    ymin=ylims[1]
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:43
    ymax=ylims[2]
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:44
    # getting the number of files to be processed
    files=char(textread(batchfile,'%s','headerlines',1))
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:48
    ndates=size(files,1)
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:49
    # loading the date information
    if strcmp(stamps_processed,'y'):
        ps=load(getparm_aps('ll_matfile',1))
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:53
        ifgs_dates=ps.day
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:54
        fprintf('Stamps processed structure \\n')
    else:
        ifgday_matfile=getparm_aps('ifgday_matfile',1)
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:57
        ifgs_dates=load(ifgday_matfile)
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:58
        ifgs_dates=ifgs_dates.ifgday
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:59
        ifgs_dates=reshape(ifgs_dates,[],1)
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:60
        ifgs_dates=unique(ifgs_dates)
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:61
    
    fprintf(cat('Lon range: ',num2str(xmin),' -- ',num2str(xmax),' degrees\\n'))
    fprintf(cat('Lat range: ',num2str(ymin),' -- ',num2str(ymax),' degrees\\n'))
    fprintf(cat('Output resolution is assumed to be ',num2str(smpres),' degrees \\n'))
    # extracting the dates from the filenames
    for k in arange(1,ndates).reshape(-1):
        path,filename_temp,ext_temp=fileparts(files[k,:],nargout=3)
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:72
        clear('filename_temp','ext_temp')
        path_temp,date,ext_temp=fileparts(path,nargout=3)
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:74
        clear('path_temp','ext_temp')
        # save the paths as structures to allow for variable path lengths
        pathlist[k]=path
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:78
        clear('path')
        # saving the date information
        datelist[k,:]=date
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:81
        clear('date')
    
    #start loop here to calculate atmos correction for each date
    fprintf('Starting the masking and writing of the PWV for each SAR date \\n')
    for n in arange(1,ndates).reshape(-1):
        file=matlabarray(cat(files[n,:]))
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:91
        outfile_watervapor=matlabarray(cat(pathlist[n],filesep,datelist[n,:],'_ZPWV_nointerp.xyz'))
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:92
        tifinfo=geotiffinfo(file)
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:95
        mer_xmin=tifinfo.CornerCoords.X(1)
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:96
        mer_xmax=tifinfo.CornerCoords.X(2)
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:97
        mer_ymin=tifinfo.CornerCoords.Y(3)
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:98
        mer_ymax=tifinfo.CornerCoords.Y(1)
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:99
        mer_cols=tifinfo.Width
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:100
        mer_rows=tifinfo.Height
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:101
        mer_x=(mer_xmax - mer_xmin) / mer_cols
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:102
        mer_y=(mer_ymax - mer_ymin) / mer_rows
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:103
        meris=imread(file,'tif')
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:105
        #do masking, interpolating etc here.
    #convert flag matrix to long list of binary numbers e.g. 1000010000010000
        flagbin=dec2bin(meris[:,:,33])
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:112
        #take certain bits of binary numbers (e.g. second bit, 1=cloud), and reshape
    #into matrix mask
        cloud=bin2dec(flagbin[:,2])
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:118
        cloudmat=reshape(cloud,mer_rows,mer_cols)
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:119
        cloudmat[cloudmat == 1]=NaN
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:120
        # NaNs will penetrate through the stack
        pconf=bin2dec(flagbin[:,23])
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:124
        pconfmat=reshape(pconf,mer_rows,mer_cols)
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:125
        pconfmat[pconfmat == 1]=NaN
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:126
        lowp=bin2dec(flagbin[:,24])
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:127
        lowpmat=reshape(lowp,mer_rows,mer_cols)
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:128
        lowpmat[lowpmat == 1]=NaN
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:129
        maskmat=multiply(multiply(cloudmat,pconfmat),lowpmat)
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:130
        maskmat[isnan(maskmat)]=1
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:131
        se=strel('square',3)
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:134
        maskmat=imdilate(maskmat,se)
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:135
        maskmat[maskmat == 1]=NaN
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:136
        maskmat[maskmat == 0]=1
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:137
        #load water vapour
        watervap=meris[:,:,14]
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:141
        #mask out dodgy pixels
        corwatervap=multiply(watervap,maskmat)
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:143
        ### aditonal masking
    # water mask
        water=bin2dec(flagbin[:,3])
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:148
        water=reshape(water,mer_rows,mer_cols)
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:149
        se=strel('square',3)
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:152
        water_new=imerode(water,se)
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:153
        water_new[water_new == 1]=NaN
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:154
        water_new[water_new == 0]=1
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:155
        clear('water')
        corwatervap=multiply(corwatervap,water_new)
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:157
        fid=fopen('out.bin','w')
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:162
        corwatervap=corwatervap.T
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:163
        fwrite(fid,corwatervap,'real*4')
        fclose(fid)
        xyz2grd_cmd=matlabarray(cat('xyz2grd -R',num2str(mer_xmin),'/',num2str(mer_xmax),'/',num2str(mer_ymin),'/',num2str(mer_ymax),' -I',num2str(mer_cols),'+/',num2str(mer_rows),'+ out.bin -Gtmp.grd  -F -ZTLf'))
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:168
        a,b=system(xyz2grd_cmd,nargout=2)
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:169
        grdsmp_cmd=matlabarray(cat('grdsample -R',num2str(xmin),'/',num2str(xmax),'/',num2str(ymin),'/',num2str(ymax),' -I',num2str(smpres),' -F tmp.grd -Gtmp_smp.grd'))
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:172
        a,b=system(grdsmp_cmd,nargout=2)
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:173
        grd2xyz_cmd=matlabarray(cat('grd2xyz -R',num2str(xmin),'/',num2str(xmax),'/',num2str(ymin),'/',num2str(ymax),' tmp_smp.grd -bo >',outfile_watervapor))
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:174
        a,b=system(grd2xyz_cmd,nargout=2)
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:175
        # opening the data file (not-interpolated)
        nointfid=fopen(outfile_watervapor,'r')
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:182
        data_vector=fread(nointfid,'double')
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:183
        fclose(nointfid)
        data=reshape(data_vector,3,[]).T
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:186
        noint=data[:,3]
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:187
        xy=data[:,cat(arange(1,2))]
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:188
        clear('data','data_vector')
        #     figure; scatter3(xy(:,1),xy(:,2),noint,15,noint,'filled'); view(0,90); axis equal; axis tight
        # writing out the date again as a binary table
        data_write=cat(xy,noint).T
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:194
        clear('noint','xy')
        #output
        fid=fopen(outfile_watervapor,'w')
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:197
        fwrite(fid,data_write,'double')
        fclose(fid)
        clear('data_write')
        fprintf(cat(num2str(n),' completed out of ',num2str(ndates),'\\n'))
    
    a,b=system('!rm tmp.grd tmp.xyz out.bin tmp2.grd tmp_fil.grd tmp_smp.grd tmp_smp.xyz tmp_smp2.grd tmp_smp_fil.grd',nargout=2)
# Trainmatlab.v.0/aps_spectrometer_PWV_meris.m:206