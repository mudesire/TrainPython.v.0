# Autogenerated with SMOP 
from smop.core import *
# Trainmatlab.v.0/aps_linear.m

    
@function
def aps_linear(save_path=None,*args,**kwargs):
    varargin = aps_linear.varargin
    nargin = aps_linear.nargin

    # [ph_tropo_linear] = aps_linear(save_path)
# Scipt to compute the tropospheric delay map from a linear relation
# between phase and topography, optional a non-deforming polygon can be 
# specified by setting crop_flag to 'y' in the parms_aps list.
# The computed tropospheric delay is in the same units as the
# inputed interferogram phases.
    
    # All required inputs will be read from the aps_parm list. This includes:
# non_defo_flag 'y' or 'n' to use a non-deformaing region.
#               Polygon of the non-deforming area. By default 'n' the whole
#               interferogram is used. Change to 'y' by using setparm_aps. 
#               Note that this variable is a matrix with in its columns the 
#               longitude and latitude of the non-deforming area.
# hgt_matfile   Path to the interferograms 
#               Interferogram phases, given as a column vector or matrix
#               with in its columens the different interferograms.
#               Stamps structure will automatically be recognised. Use
#               setparm_aps so change the data path pointing to the .mat
#               file.
# hgt_matfile   Path to the heights file.
#               Colum vector of the topography. 
#               Stamps structure will automatically be recognised. Use
#               setparm_aps so change the data path pointing to the .mat
#               file.
# ll_matfile    Path to the longitude and latitude file
#               Matrix with in its columns the longitude and latitude. 
#               Stamps structure will automatically be recognised. Use
#               setparm_aps so change the data path pointing to the .mat
#               file. In case the poly argument is specified, both need to 
#               have the same units.
    
    # OUTPUTS:
# ph_tropo_linear   The topography correlated delays either estimated from a
#                   linear relationship over the whole interferogram of using 
#                   a non-deforming region. By default the output of this
#                   function is stored in the 'tca2.mat' or 'tca_sb2.mat'
#                   for StaMPS SM and SB option. In case no StaMPs
#                   structure is used the data is saved in 'tca2.mat'.
    
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
    
    # Bekaert David - Leeds University 2013
# Modifcations:
# DB:   04/2013     Include SB functionality for stamps
# DB:   04/2013     Uset setparm_aps and getparm_aps to get the processign
#                   parameters
# DB:   06/2015     Suppress the output, as its saved anyway.
# DB:   01/2016     Include non-Stamps support
# DB:   02/2016     Remove inlfuence of NaN's
    
    test_fig=0
# Trainmatlab.v.0/aps_linear.m:68
    
    # estimated line
    n_fig_line=7
# Trainmatlab.v.0/aps_linear.m:70
    
    fontsize=10
# Trainmatlab.v.0/aps_linear.m:71
    
    if nargin < 1 or isempty(save_path):
        save_path=matlabarray(cat('.'))
# Trainmatlab.v.0/aps_linear.m:75
    
    stamps_processed=getparm_aps('stamps_processed',1)
# Trainmatlab.v.0/aps_linear.m:79
    hgt_matfile=getparm_aps('hgt_matfile',1)
# Trainmatlab.v.0/aps_linear.m:80
    ll_matfile=getparm_aps('ll_matfile',1)
# Trainmatlab.v.0/aps_linear.m:81
    phuw_matfile=getparm_aps('phuw_matfile',1)
# Trainmatlab.v.0/aps_linear.m:82
    if strcmp(getparm_aps('non_defo_flag',1),'n'):
        non_defo_flag=0
# Trainmatlab.v.0/aps_linear.m:85
    else:
        non_defo_flag=1
# Trainmatlab.v.0/aps_linear.m:87
    
    # loading the data
    phuw=load(phuw_matfile)
# Trainmatlab.v.0/aps_linear.m:91
    lonlat=load(ll_matfile)
# Trainmatlab.v.0/aps_linear.m:92
    hgt=load(hgt_matfile)
# Trainmatlab.v.0/aps_linear.m:93
    if strcmp(stamps_processed,'y'):
        load('psver')
    else:
        psver=2
# Trainmatlab.v.0/aps_linear.m:97
    
    phuw=phuw.phuw
# Trainmatlab.v.0/aps_linear.m:99
    lonlat=lonlat.lonlat
# Trainmatlab.v.0/aps_linear.m:100
    hgt=hgt.hgt
# Trainmatlab.v.0/aps_linear.m:101
    ## Loading of the data
# file names of the output data
    apsname=matlabarray(cat(save_path,filesep,'tca',num2str(psver),'.mat'))
# Trainmatlab.v.0/aps_linear.m:106
    apssbname=matlabarray(cat(save_path,filesep,'tca_sb',num2str(psver),'.mat'))
# Trainmatlab.v.0/aps_linear.m:107
    # the number of interferograms
    n_dates=size(phuw,2)
# Trainmatlab.v.0/aps_linear.m:111
    ## use a non-deforming area
    if non_defo_flag == 1:
        non_defo=load('non_defo.mat')
# Trainmatlab.v.0/aps_linear.m:116
        poly=non_defo.poly
# Trainmatlab.v.0/aps_linear.m:117
        ix_points=cat(arange(1,size(hgt,1))).T
# Trainmatlab.v.0/aps_linear.m:120
        ix_temp=inpolygon(lonlat[:,1],lonlat[:,2],poly[:,1],poly[:,2])
# Trainmatlab.v.0/aps_linear.m:121
        ix_points=ix_points[ix_temp]
# Trainmatlab.v.0/aps_linear.m:122
        ixnon_points=cat(arange(1,size(hgt,1))).T
# Trainmatlab.v.0/aps_linear.m:123
        ixnon_points=ixnon_points[ix_points]
# Trainmatlab.v.0/aps_linear.m:124
        clear('ix_temp')
    else:
        # use all points
        ix_points=cat(arange(1,size(hgt,1))).T
# Trainmatlab.v.0/aps_linear.m:130
        ixnon_points=matlabarray([])
# Trainmatlab.v.0/aps_linear.m:131
    
    ## correct for DEM error
    DEM_corr=getparm_aps('powerlaw_DEM_corr',1)
# Trainmatlab.v.0/aps_linear.m:136
    # geting the number of interferograms and points from the phase matrix
    n_interferograms=size(phuw,2)
# Trainmatlab.v.0/aps_linear.m:138
    n_points=size(phuw,1)
# Trainmatlab.v.0/aps_linear.m:139
    if strcmp(DEM_corr,'y') and n_interferograms > 5:
        # loading the perpendicualr baseline information
        bperp_matfile=getparm_aps('bperp_matfile',1)
# Trainmatlab.v.0/aps_linear.m:143
        bperp=load(bperp_matfile)
# Trainmatlab.v.0/aps_linear.m:144
        if strcmp(stamps_processed,'y'):
            bperp=bperp.bperp
# Trainmatlab.v.0/aps_linear.m:146
        # checking the size of bperp
        if size(bperp,2) > 1:
            bperp=bperp.T
# Trainmatlab.v.0/aps_linear.m:150
            if size(bperp,2) > 1:
                error('myApp:argChk',cat('bperp is not a vector,... \\nAbort,... \\n'))
        # estimating the correlated errors
        DEM_corr_e=lscov(bperp,phuw.T).T
# Trainmatlab.v.0/aps_linear.m:156
        phuw=phuw - multiply(repmat(bperp.T,n_points,1),repmat(DEM_corr_e,1,n_interferograms))
# Trainmatlab.v.0/aps_linear.m:159
        clear('A')
    else:
        if strcmp(DEM_corr,'y') and n_interferograms <= 5:
            fprintf('Not enough interferograms to make a reliable estimate for the DEM error \\n')
            DEM_corr='n'
# Trainmatlab.v.0/aps_linear.m:164
        DEM_corr_e=zeros(cat(n_points,1))
# Trainmatlab.v.0/aps_linear.m:166
    
    ## Compute the linear relation between phase and topography for each interferogram
# and compute the tropospheric delay for the full interferogram from it.
# initialisation of the tropospheric delay matrix
    ph_tropo_linear=zeros(cat(size(hgt,1),n_dates))
# Trainmatlab.v.0/aps_linear.m:176
    hgt_range=cat(min(hgt),max(hgt)).T
# Trainmatlab.v.0/aps_linear.m:177
    if hgt_range[2] > 10:
        # height are in m
        hgt=hgt / 1000
# Trainmatlab.v.0/aps_linear.m:180
        hgt_range=hgt_range / 1000
# Trainmatlab.v.0/aps_linear.m:181
    
    xy=(llh2local(lonlat.T,mean(lonlat))).T
# Trainmatlab.v.0/aps_linear.m:184
    xy=matlabarray(cat(cat(arange(1,size(xy,1))).T,xy))
# Trainmatlab.v.0/aps_linear.m:185
    ps.xy = copy(xy)
# Trainmatlab.v.0/aps_linear.m:186
    ps.n_ifg = copy(size(phuw,2))
# Trainmatlab.v.0/aps_linear.m:187
    ps.n_ps = copy(size(phuw,1))
# Trainmatlab.v.0/aps_linear.m:188
    ix_points_or=copy(ix_points)
# Trainmatlab.v.0/aps_linear.m:191
    ixnon_points_or=copy(ixnon_points)
# Trainmatlab.v.0/aps_linear.m:192
    for k in arange(1,n_dates).reshape(-1):
        ixnon_points=copy(ixnon_points_or)
# Trainmatlab.v.0/aps_linear.m:194
        ix_points=copy(ix_points_or)
# Trainmatlab.v.0/aps_linear.m:195
        ixnon_points=unique(cat([ixnon_points],[find(isnan(phuw[:,k]) == 1)]))
# Trainmatlab.v.0/aps_linear.m:199
        ix_points=cat(arange(1,n_points)).T
# Trainmatlab.v.0/aps_linear.m:201
        ix_points[ixnon_points]=[]
# Trainmatlab.v.0/aps_linear.m:202
        A=matlabarray(cat(hgt[ix_points],ones(cat(length(ix_points),1))))
# Trainmatlab.v.0/aps_linear.m:206
        coeff=lscov(A,phuw[ix_points,k])
# Trainmatlab.v.0/aps_linear.m:210
        ph_tropo_linear[:,k]=dot(cat(hgt,ones(size(hgt))),coeff)
# Trainmatlab.v.0/aps_linear.m:212
        ph_tropo_linear[isnan(phuw[:,k]),k]=NaN
# Trainmatlab.v.0/aps_linear.m:215
        if test_fig == 1:
            if k == 1:
                figure('name','Linear relation between phase and topography')
                if n_dates / n_fig_line < 1:
                    n_rows=1
# Trainmatlab.v.0/aps_linear.m:221
                    n_columns=copy(n_dates)
# Trainmatlab.v.0/aps_linear.m:222
                else:
                    n_rows=ceil(n_dates / n_fig_line)
# Trainmatlab.v.0/aps_linear.m:224
                    n_columns=copy(n_fig_line)
# Trainmatlab.v.0/aps_linear.m:225
            subplot(n_rows,n_columns,k)
            plot(hgt[ix_points],phuw[ix_points,k],'g.')
            hold('on')
            plot(hgt[ixnon_points],phuw[ixnon_points,k],'k.')
            hold('on')
            plot(hgt,ph_tropo_linear[:,k],'r-','linewidth',2)
            xlim(hgt_range)
            xlabel('Height','fontsize',fontsize)
            ylabel('Phase','fontsize',fontsize)
            set(gca,'fontsize',fontsize)
    
    ## saving the data
# checking if this is StaMPS or not
    if strcmp(stamps_processed,'y'):
        # This is StaMPS
        if strcmp(getparm('small_baseline_flag'),'y'):
            if exist(apssbname,'file') == 2:
                save(apssbname,'-append','ph_tropo_linear')
            else:
                save(apssbname,'ph_tropo_linear')
        else:
            if exist(apsname,'file') == 2:
                save(apsname,'-append','ph_tropo_linear')
            else:
                save(apsname,'ph_tropo_linear')
    else:
        # This is not StaMPS
        if exist(apsname,'file') == 2:
            save(apsname,'-append','ph_tropo_linear')
        else:
            save(apsname,'ph_tropo_linear')
    