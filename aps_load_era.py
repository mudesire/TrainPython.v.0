# Autogenerated with SMOP 
from smop.core import *
# Trainmatlab.v.0/aps_load_era.m

    
@function
def aps_load_era(file=None,era_data_type=None,*args,**kwargs):
    varargin = aps_load_era.varargin
    nargin = aps_load_era.nargin

    # loading era-I data from ECMWF or BADC websites
# Bekaert David
# modifications
# DB    10/04/2016  extract code from aps_era_SAR.m to make code modular
    
    ### Example on how to load netcdf files 
# ncid = netcdf.open(file,'NC_NOWRITE');
# [numdims,numvars,numglobalatts,unlimdimid] = netcdf.inq(ncid);
# [dimname, dimlen] = netcdf.inqDim(ncid,0);
    
    #         for k=1:numvars
#             [dimname, dimlen] = netcdf.inqVar(ncid,k-1); 
#             fprintf([num2str(k-1) ' - ' dimname '\n'])
#         end
    
    # debug figure to test and validate dataloading.
    debug_fig=0
# Trainmatlab.v.0/aps_load_era.m:18
    # open the netcdf
    ncid=netcdf.open(file,'NC_NOWRITE')
# Trainmatlab.v.0/aps_load_era.m:21
    # read netcdf variables and get number of variables
    numdims,numvars,numglobalatts,unlimdimid=netcdf.inq(ncid,nargout=4)
# Trainmatlab.v.0/aps_load_era.m:24
    ## Swapping between BADC and ECMWF website data
    if strcmpi(era_data_type,'ECMWF'):
        # ECMWF data has field data and a scale plus offset.
    # Depending if this exist its added to the data
        for i in arange(0,numvars - 1).reshape(-1):
            varname,xtype,dimids,numatts=netcdf.inqVar(ncid,i,nargout=4)
# Trainmatlab.v.0/aps_load_era.m:32
            flag=0
# Trainmatlab.v.0/aps_load_era.m:33
            for j in arange(0,numatts - 1).reshape(-1):
                attname1=netcdf.inqAttName(ncid,i,j)
# Trainmatlab.v.0/aps_load_era.m:35
                attname2=netcdf.getAtt(ncid,i,attname1)
# Trainmatlab.v.0/aps_load_era.m:36
                if strcmp('add_offset',attname1):
                    offset=copy(attname2)
# Trainmatlab.v.0/aps_load_era.m:39
                if strcmp('scale_factor',attname1):
                    scale=copy(attname2)
# Trainmatlab.v.0/aps_load_era.m:43
                    flag=1
# Trainmatlab.v.0/aps_load_era.m:44
            if flag:
                eval(cat(varname,'= double(netcdf.getVar(ncid,i))*scale + offset;'))
            else:
                eval(cat(varname,'= double(netcdf.getVar(ncid,i));'))
            clear('varname')
            clear('xtype')
            clear('dimids')
            clear('numatts')
            clear('scale')
            clear('offset')
        # flip along third dimension, ECMWF format flipped compared to BADC
        Temp=t(arange(),arange(),arange(end(),1,- 1))
# Trainmatlab.v.0/aps_load_era.m:58
        Hum=r(arange(),arange(),arange(end(),1,- 1))
# Trainmatlab.v.0/aps_load_era.m:59
        Geopot=z(arange(),arange(),arange(end(),1,- 1))
# Trainmatlab.v.0/aps_load_era.m:60
        Plevs=flipud(level)
# Trainmatlab.v.0/aps_load_era.m:61
    else:
        if strcmpi(era_data_type,'BADC'):
            # This is for ERA-I from BADC
    # Datafield are structured differently with different names
    # than ECMWF website data.
            # variables at each node 20 (0-19)
            varname,vartype,dimids,natts=netcdf.inqVar(ncid,0,nargout=4)
# Trainmatlab.v.0/aps_load_era.m:70
            Temp=double(netcdf.getVar(ncid,5))
# Trainmatlab.v.0/aps_load_era.m:73
            Hum=double(netcdf.getVar(ncid,11))
# Trainmatlab.v.0/aps_load_era.m:74
            Geopot=double(netcdf.getVar(ncid,4))
# Trainmatlab.v.0/aps_load_era.m:75
            Plevs=double(netcdf.getVar(ncid,2))
# Trainmatlab.v.0/aps_load_era.m:76
    
    # Permute to a 3 D grid
    Temp=permute(Temp,cat(2,1,3))
# Trainmatlab.v.0/aps_load_era.m:80
    Hum=permute(Hum,cat(2,1,3))
# Trainmatlab.v.0/aps_load_era.m:81
    Geopot=permute(Geopot,cat(2,1,3))
# Trainmatlab.v.0/aps_load_era.m:82
    # Same for lats and lons
    lats=netcdf.getVar(ncid,1)
# Trainmatlab.v.0/aps_load_era.m:86
    n_latitude_points=size(lats,1)
# Trainmatlab.v.0/aps_load_era.m:87
    lons=netcdf.getVar(ncid,0)
# Trainmatlab.v.0/aps_load_era.m:88
    n_longitude_points=size(lons,1)
# Trainmatlab.v.0/aps_load_era.m:89
    # close nedtcdf
    netcdf.close(ncid)
    # adapting to the right lon lat grid size
    Pressure=repmat(Plevs,cat(1,n_latitude_points,n_longitude_points))
# Trainmatlab.v.0/aps_load_era.m:97
    Pressure=permute(Pressure,cat(2,3,1))
# Trainmatlab.v.0/aps_load_era.m:98
    latgrid=repmat(lats,cat(1,37,n_longitude_points))
# Trainmatlab.v.0/aps_load_era.m:101
    latgrid=permute(latgrid,cat(1,3,2))
# Trainmatlab.v.0/aps_load_era.m:102
    longrid=repmat(lons,cat(1,37,n_latitude_points))
# Trainmatlab.v.0/aps_load_era.m:103
    longrid=permute(longrid,cat(3,1,2))
# Trainmatlab.v.0/aps_load_era.m:104
    # Get list of points to look at in analysis
    xx,yy=meshgrid(arange(1,n_longitude_points),arange(1,n_latitude_points),nargout=2)
# Trainmatlab.v.0/aps_load_era.m:107
    # (see IFS documentation part 2: Data assimilation (CY25R1)). 
# Calculate saturated water vapour pressure (svp) for water
# (svpw) using Buck 1881 and for ice (swpi) from Alduchow
# and Eskridge (1996) euation AERKi
    svpw=multiply(6.1121,exp((multiply(17.502,(Temp - 273.16))) / (240.97 + Temp - 273.16)))
# Trainmatlab.v.0/aps_load_era.m:114
    svpi=multiply(6.1121,exp((multiply(22.587,(Temp - 273.16))) / (273.86 + Temp - 273.16)))
# Trainmatlab.v.0/aps_load_era.m:115
    tempbound1=273.16
# Trainmatlab.v.0/aps_load_era.m:116
    
    tempbound2=250.16
# Trainmatlab.v.0/aps_load_era.m:117
    
    svp=copy(svpw)
# Trainmatlab.v.0/aps_load_era.m:118
    # Faster expression
    wgt=(Temp - tempbound2) / (tempbound1 - tempbound2)
# Trainmatlab.v.0/aps_load_era.m:121
    svp=svpi + multiply((svpw - svpi),wgt ** 2)
# Trainmatlab.v.0/aps_load_era.m:122
    ix_bound1=find(Temp > tempbound1)
# Trainmatlab.v.0/aps_load_era.m:123
    svp[ix_bound1]=svpw[ix_bound1]
# Trainmatlab.v.0/aps_load_era.m:124
    ix_bound2=find(Temp < tempbound2)
# Trainmatlab.v.0/aps_load_era.m:125
    svp[ix_bound2]=svpi[ix_bound2]
# Trainmatlab.v.0/aps_load_era.m:126
    WVapour=dot(Hum / 100.0,svp)
# Trainmatlab.v.0/aps_load_era.m:127
    clear('Hum')
    # inform about the organisation of the longitudes
    if sum(lons > 180) > 1:
        lon0360_flag='y'
# Trainmatlab.v.0/aps_load_era.m:132
    else:
        lon0360_flag='n'
# Trainmatlab.v.0/aps_load_era.m:134
    
    # validation plots
    if debug_fig == 1:
        figure('position',cat(3,628,1402,586))
        subplot(2,5,1)
        imagesc(Temp[:,:,end()])
        colorbar
        axis('xy')
        axis('equal')
        axis('tight')
        title('temp upper atmo')
        subplot(2,5,2)
        imagesc(Temp[:,:,1])
        colorbar
        axis('xy')
        axis('equal')
        axis('tight')
        title('temp lower atmo')
        subplot(2,5,3)
        imagesc(Pressure[:,:,end()])
        colorbar
        axis('xy')
        axis('equal')
        axis('tight')
        title('pressure upper atmo')
        subplot(2,5,4)
        imagesc(Pressure[:,:,1])
        colorbar
        axis('xy')
        axis('equal')
        axis('tight')
        title('pressure lower atmo')
        subplot(2,5,6)
        imagesc(WVapour[:,:,end()])
        colorbar
        axis('xy')
        axis('equal')
        axis('tight')
        title('Water vapour upper atmo')
        subplot(2,5,7)
        imagesc(WVapour[:,:,1])
        colorbar
        axis('xy')
        axis('equal')
        axis('tight')
        title('Water vapour lower atmo')
        subplot(2,5,8)
        imagesc(Geopot[:,:,end()])
        colorbar
        axis('xy')
        axis('equal')
        axis('tight')
        title('geopotential upper atmo')
        subplot(2,5,9)
        imagesc(Geopot[:,:,1])
        colorbar
        axis('xy')
        axis('equal')
        axis('tight')
        title('geopotential lower atmo')
        subplot(2,5,5)
        imagesc(latgrid[:,:,1])
        colorbar
        axis('xy')
        axis('equal')
        axis('tight')
        title('lat')
        subplot(2,5,10)
        imagesc(longrid[:,:,1])
        colorbar
        axis('xy')
        axis('equal')
        axis('tight')
        title('lon')
    