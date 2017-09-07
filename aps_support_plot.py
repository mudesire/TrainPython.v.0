# Autogenerated with SMOP 
from smop.core import *
# Trainmatlab.v.0/aps_support_plot.m

    
@function
def aps_support_plot(technique=None,*args,**kwargs):
    varargin = aps_support_plot.varargin
    nargin = aps_support_plot.nargin

    # plotting the support information used for the APS correction methods
# technique flag
# when:
# 1 powerlaw
# 2 ERA-I
# 3 Meris
    
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
    
    # By Bekaert David
    
    fontsize=15
# Trainmatlab.v.0/aps_support_plot.m:29
    load('tca_support')
    ## power- law
    if technique == 1:
        if exist('aps_p','dir') != 7:
            mkdir('aps_p')
        if strcmpi(getparm_aps('powerlaw_ridge_constraint'),'y'):
            deminfo=powerlaw_ridges.deminfo
# Trainmatlab.v.0/aps_support_plot.m:40
            InSAR_convexhull=powerlaw_ridges.InSAR_convexhull
# Trainmatlab.v.0/aps_support_plot.m:41
            mountain_ridge=powerlaw_ridges.mountain_ridge
# Trainmatlab.v.0/aps_support_plot.m:42
            hard_ridge_flag=powerlaw_ridges.hard_ridge_flag
# Trainmatlab.v.0/aps_support_plot.m:43
            fprintf('Plotting power-law ridges \\n')
            h1=figure('name','Power-law ridges','position',cat(200,243,610,603))
# Trainmatlab.v.0/aps_support_plot.m:49
            plot(mean(cat(deminfo.xmin,deminfo.xmax)),mean(cat(deminfo.ymax,deminfo.ymin)),'g-','linewidth',2)
            hold('on')
            plot(mean(cat(deminfo.xmin,deminfo.xmax)),mean(cat(deminfo.ymax,deminfo.ymin)),'r-','linewidth',2)
            hold('on')
            plot(mean(cat(deminfo.xmin,deminfo.xmax)),mean(cat(deminfo.ymax,deminfo.ymin)),'r--','linewidth',2)
            imagesc(cat(deminfo.xmin,deminfo.xmax),cat(deminfo.ymax,deminfo.ymin),deminfo.dem_smooth)
            cc=copy(colorbar)
# Trainmatlab.v.0/aps_support_plot.m:58
            view(0,90)
            axis('equal')
            axis('tight')
            colormap(flipud(gray))
            axis('xy')
            box('on')
            hold('on')
            plot(InSAR_convexhull[:,1],InSAR_convexhull[:,2],'g-','linewidth',2)
            # plotting the line on the figure
            for counter in arange(1,length(mountain_ridge)).reshape(-1):
                if hard_ridge_flag[counter] == 1:
                    plot(mountain_ridge[counter](arange(),1),mountain_ridge[counter](arange(),2),'r-','linewidth',2)
                else:
                    plot(mountain_ridge[counter](arange(),1),mountain_ridge[counter](arange(),2),'r--','linewidth',2)
            box('on')
            xlabel(cc,'[m]','fontsize',fontsize)
            ylabel(cc,'Topography','fontsize',fontsize)
            legend('Location','NorthOutside','InSAR region','Hard ridge','Subregion boundary')
            title('Ridge definition','fontsize',fontsize)
            set(gca,'fontsize',fontsize)
            print_(h1,'-dpng',cat('aps_p/mountain_ridges.png'))
            print_(h1,'-depsc',cat('aps_p/mountain_ridges.eps'))
        else:
            # plotting the power-law windows
            fprintf('Plotting power-law windows \\n')
            # see if the real dem is available otherzie use the poitn heights
            dem_flag=1
# Trainmatlab.v.0/aps_support_plot.m:91
            if exist('powerlaw_ridges','var') == 1:
                deminfo=powerlaw_ridges.deminfo
# Trainmatlab.v.0/aps_support_plot.m:93
            else:
                if exist('era','var') == 1:
                    deminfo=era.deminfo
# Trainmatlab.v.0/aps_support_plot.m:95
                else:
                    hgt_file=getparm_aps('hgt_matfile')
# Trainmatlab.v.0/aps_support_plot.m:97
                    ll_matfile=getparm_aps('ll_matfile')
# Trainmatlab.v.0/aps_support_plot.m:98
                    hgt=load(hgt_file)
# Trainmatlab.v.0/aps_support_plot.m:100
                    ll=load(ll_matfile)
# Trainmatlab.v.0/aps_support_plot.m:101
                    if strcmpi(getparm_aps('stamps_processed'),'y'):
                        hgt=hgt.hgt
# Trainmatlab.v.0/aps_support_plot.m:103
                        ll=ll.lonlat
# Trainmatlab.v.0/aps_support_plot.m:104
                        dem_flag=0
# Trainmatlab.v.0/aps_support_plot.m:105
            # making sure the dem and the other data have the same origin in
        # longitude
            if dem_flag == 1:
                if deminfo.xmax - max(InSAR_convexhull(arange(),1)) > 100:
                    deminfo.xmax = copy(deminfo.xmax - 360)
# Trainmatlab.v.0/aps_support_plot.m:112
                    deminfo.xmin = copy(deminfo.xmin - 360)
# Trainmatlab.v.0/aps_support_plot.m:113
            # laoding of the data
            window_box_ll=powerlaw_windows.window_box_ll
# Trainmatlab.v.0/aps_support_plot.m:118
            window_box_center_ll=powerlaw_windows.window_box_center_ll
# Trainmatlab.v.0/aps_support_plot.m:119
            h1=figure('name','Power-law windows','position',cat(200,243,610,603))
# Trainmatlab.v.0/aps_support_plot.m:123
            plot(window_box_ll[round(dot(0.5,(length(window_box_ll))))](arange(),1),window_box_ll[round(dot(0.5,(length(window_box_ll))))](arange(),2),'r-','linewidth',2)
            hold('on')
            plot(window_box_center_ll[1,1],window_box_center_ll[1,2],'wo','markeredgecolor','k','markerfacecolor','w','markersize',15)
            hold('on')
            plot(InSAR_convexhull(arange(),1),InSAR_convexhull(arange(),2),'g-','linewidth',2)
            hold('on')
            if dem_flag == 1:
                # plot the topogrpahy
                imagesc(cat(deminfo.xmin,deminfo.xmax),cat(deminfo.ymax,deminfo.ymin),deminfo.dem)
                view(0,90)
                axis('xy')
            else:
                scatter3(ll[:,1],ll[:,2],hgt,3,hgt,'filled')
                view(0,90)
            cc=copy(colorbar)
# Trainmatlab.v.0/aps_support_plot.m:141
            colormap(flipud(gray))
            xlabel(cc,'[m]','fontsize',fontsize)
            ylabel(cc,'Topography','fontsize',fontsize)
            axis('equal')
            axis('tight')
            hold('on')
            plot3(window_box_ll[round(dot(0.5,(length(window_box_ll))))](arange(),1),window_box_ll[round(dot(0.5,(length(window_box_ll))))](arange(),2),dot(99999.0,ones(size(window_box_ll[1](arange(),2)))),'r-','linewidth',2)
            hold('on')
            plot3(window_box_center_ll[:,1],window_box_center_ll[:,2],dot(10000000.0,ones(size(window_box_center_ll[:,2]))),'wo','markeredgecolor','k','markerfacecolor','w','markersize',15)
            hold('on')
            plot3(InSAR_convexhull(arange(),1),InSAR_convexhull(arange(),2),dot(99999.0,ones(size(InSAR_convexhull(arange(),2)))),'g-','linewidth',2)
            legend('Location','NorthOutside','Window example','Window centers','InSAR region')
            title('Window definition','fontsize',fontsize)
            set(gca,'fontsize',fontsize)
            grid('off')
            box('on')
            print_(h1,'-dpng',cat('aps_p/window_locations.png'))
            print_(h1,'-depsc',cat('aps_p/window_locations.eps'))
        ## ERA interim
    else:
        if technique == 2:
            if exist('aps_e','dir') != 7:
                mkdir('aps_e')
            # loading the ERA data
            deminfo=era.deminfo
# Trainmatlab.v.0/aps_support_plot.m:176
            era_lonlat=era.era_lonlat
# Trainmatlab.v.0/aps_support_plot.m:177
            if exist('InSAR_convexhull','var') == 1:
                insar_flag=1
# Trainmatlab.v.0/aps_support_plot.m:181
            else:
                insar_flag=0
# Trainmatlab.v.0/aps_support_plot.m:183
            if insar_flag == 1:
                if deminfo.xmax - max(InSAR_convexhull(arange(),1)) > 100:
                    InSAR_convexhull[:,1]=InSAR_convexhull(arange(),1) + 360
# Trainmatlab.v.0/aps_support_plot.m:187
            # plotting the figure
            hfig=figure('name','ERA points and InSAR region','position',cat(200,243,610,603))
# Trainmatlab.v.0/aps_support_plot.m:192
            plot(mean(cat(deminfo.xmin,deminfo.xmax)),mean(cat(deminfo.ymax,deminfo.ymin)),'wo','markeredgecolor','k','markerfacecolor','w','markersize',15)
            hold('on')
            # check if the insar convex hull can be plotted
            if insar_flag == 1:
                plot(mean(cat(deminfo.xmin,deminfo.xmax)),mean(cat(deminfo.ymax,deminfo.ymin)),'g-','linewidth',2)
            # plot the topogrpahy
            imagesc(cat(deminfo.xmin,deminfo.xmax),cat(deminfo.ymax,deminfo.ymin),deminfo.dem)
            cc=copy(colorbar)
# Trainmatlab.v.0/aps_support_plot.m:202
            view(0,90)
            colormap(flipud(gray))
            axis('xy')
            xlabel(cc,'[m]','fontsize',fontsize)
            ylabel(cc,'Topography','fontsize',fontsize)
            hold('on')
            plot(era_lonlat[:,1],era_lonlat[:,2],'wo','markeredgecolor','k','markerfacecolor','w','markersize',15)
            hold('on')
            if insar_flag == 1:
                plot(InSAR_convexhull[:,1],InSAR_convexhull[:,2],'g-','linewidth',2)
                legend('location','northoutside','Used ERA-I locations','InSAR region')
            else:
                legend('location','northoutside','Used ERA-I locations')
            title('ERA points distribution','fontsize',fontsize)
            set(gca,'fontsize',fontsize)
            axis('equal')
            axis('tight')
            print_(hfig,'-dpng',cat('aps_e/era_datapoints.png'))
            print_(hfig,'-depsc',cat('aps_e/era_datapoints.eps'))
        else:
            if technique == 3:
                load(psver)
                ps=load(cat('ps',num2str(psver),'.mat'))
# Trainmatlab.v.0/aps_support_plot.m:228
                stamps_processed=getparm_aps('stamps_processed')
# Trainmatlab.v.0/aps_support_plot.m:229
                small_baseline_flag=getparm('small_baseline_flag')
# Trainmatlab.v.0/aps_support_plot.m:230
                if strcmpi(small_baseline_flag,'y'):
                    load('tca_sb2.mat','ph_tropo_meris')
                    bperp=load(cat('..',filesep,'ps1.mat'),'bperp')
# Trainmatlab.v.0/aps_support_plot.m:234
                    bperp=bperp.bperp
# Trainmatlab.v.0/aps_support_plot.m:235
                    bperp=bperp[ps.ifgday_ix]
# Trainmatlab.v.0/aps_support_plot.m:236
                    dates=ps.ifgday
# Trainmatlab.v.0/aps_support_plot.m:237
                    ix_ifgs_keep=arange(1,ps.n_ifg)
# Trainmatlab.v.0/aps_support_plot.m:238
                else:
                    load('tca2.mat','ph_tropo_meris')
                    dates=matlabarray(cat(ps.day,repmat(ps.master_day,length(ps.day),1)))
# Trainmatlab.v.0/aps_support_plot.m:241
                    bperp=matlabarray(cat(ps.bperp,zeros(cat(length(ps.day),1))))
# Trainmatlab.v.0/aps_support_plot.m:242
                    ix_ifgs_keep=arange(1,ps.n_ifg)
# Trainmatlab.v.0/aps_support_plot.m:243
                # plot the SB network and show for whcih connection there is meris data
                if strcmp(stamps_processed,'y'):
                    # remove that that have not been unwrapped before
                    ix_dropped=getparm('drop_ifg')
# Trainmatlab.v.0/aps_support_plot.m:251
                    temp=copy(ix_ifgs_keep)
# Trainmatlab.v.0/aps_support_plot.m:254
                    temp[ix_dropped]=[]
# Trainmatlab.v.0/aps_support_plot.m:255
                    ifgs_good=find(sum(ph_tropo_meris(arange(),temp) != 0,1) != 0)
# Trainmatlab.v.0/aps_support_plot.m:256
                    if strcmp(small_baseline_flag,'n'):
                        ix_dropped=unique(cat(ix_dropped,ps.master_ix))
# Trainmatlab.v.0/aps_support_plot.m:260
                    ix_ifgs_keep[ix_dropped]=[]
# Trainmatlab.v.0/aps_support_plot.m:262
                    bperp[ix_dropped,:]=[]
# Trainmatlab.v.0/aps_support_plot.m:263
                    dates[ix_dropped,:]=[]
# Trainmatlab.v.0/aps_support_plot.m:264
                    dates_all=copy(dates)
# Trainmatlab.v.0/aps_support_plot.m:267
                    bperp_all=copy(bperp)
# Trainmatlab.v.0/aps_support_plot.m:268
                    h_baselineplot=figure('name','Processed network')
# Trainmatlab.v.0/aps_support_plot.m:273
                    for ifgs_counter in arange(1,size(bperp_all,1)).reshape(-1):
                        hold('on')
                        plot(cat(dates_all[ifgs_counter,1],dates_all[ifgs_counter,2]),cat(bperp_all[ifgs_counter,1],bperp_all[ifgs_counter,2]),'k-','linewidth',1)
                    # plotting the network for which we have an APS correction
                    for ifgs_counter in arange(1,length(ifgs_good)).reshape(-1):
                        ifgs_counter
                        hold('on')
                        plot(cat(dates[ifgs_good[ifgs_counter],1],dates[ifgs_good[ifgs_counter],2]),cat(bperp[ifgs_good[ifgs_counter],1],bperp[ifgs_good[ifgs_counter],2]),'k-','linewidth',2)
                        text(mean(dates[ifgs_good[ifgs_counter],:]),mean(bperp[ifgs_good[ifgs_counter],:]) + 20,num2str(ifgs_good[ifgs_counter]),'fontsize',fontsize - 2,'backgroundColor',cat(1,1,1),'Margin',0.01)
                    hold('on')
                    # [dates_unique,ix_unique] = unique(dates(ifgs_good,:));
        # bperp_unique = bperp(ifgs_good,:);
        # bperp_unique = bperp_unique(ix_unique);
                    dates_unique,ix_unique=unique(dates_all,nargout=2)
# Trainmatlab.v.0/aps_support_plot.m:293
                    bperp_unique=copy(bperp_all)
# Trainmatlab.v.0/aps_support_plot.m:294
                    bperp_unique=bperp_unique[ix_unique]
# Trainmatlab.v.0/aps_support_plot.m:295
                    plot(dates_unique,bperp_unique,'ko','markerfacecolor','r','markersize',7)
                    clear('dates_unique','ix_unique','bperp_unique')
                    hold('on')
                    # set(gca,'XTick',dates_num)
                    datetick('x','mmm yy')
                    set(gca,'fontsize',fontsize)
                    box('on')
                    ylabel('Bperp [m]','fontsize',fontsize)
    