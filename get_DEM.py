# Autogenerated with SMOP 
from smop.core import *
# Trainmatlab.v.0/get_DEM.m

    
@function
def get_DEM(*args,**kwargs):
    varargin = get_DEM.varargin
    nargin = get_DEM.nargin

    # function to load the DEM, convert to a grid, resample to the user defined
# grid. Gives as output the DEM grid, the coordinates information, number
# of rows and columns of the grid.
    
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
    
    # By Bekaert David - Unversity of Leeds
# modifications:
# 10/2015   DB  Adding support for grd file DEM's
# 10/2015   DB  bug fix for grd file, when the longitude is defined +360degree
# 10/2015   DB  Checking for GMT5 compatibility. No issues found, but
#               information is passed on
# 11/2015   DB  Add system call check for errors
# 02/2016   DB  Add a fix in case format is not given
#               Attemt to autofix between int16 and short format
# 04/2016   DB  Check if the DEM exist
# 04/2016   DB  Add option to give DEM with .xml file too
    
    # retreiving which version of GMT this is
    gmt5_above,gmt_version=get_gmt_version
# Trainmatlab.v.0/get_DEM.m:38
    fig_test=1
# Trainmatlab.v.0/get_DEM.m:42
    
    smpdem='dem_smp.xyz'
# Trainmatlab.v.0/get_DEM.m:43
    
    # information read from teh paramter file
    demfile=getparm_aps('demfile')
# Trainmatlab.v.0/get_DEM.m:46
    pixelreg='node'
# Trainmatlab.v.0/get_DEM.m:47
    
    # outfmt = getparm_aps('outfmt');
    demnull=getparm_aps('dem_null')
# Trainmatlab.v.0/get_DEM.m:49
    xlims=getparm_aps('region_lon_range',1)
# Trainmatlab.v.0/get_DEM.m:50
    ylims=getparm_aps('region_lat_range',1)
# Trainmatlab.v.0/get_DEM.m:51
    smpres=getparm_aps('region_res',1)
# Trainmatlab.v.0/get_DEM.m:52
    ## no changes required below
# check if DEM exist
    if exist(demfile,'file') != 2:
        error(cat(demfile,' does not exist'))
    
    # check if the longitude and latitude are given correctly
    xlims_test=matlabarray(cat(min(xlims),max(xlims)))
# Trainmatlab.v.0/get_DEM.m:63
    ylims_test=matlabarray(cat(min(ylims),max(ylims)))
# Trainmatlab.v.0/get_DEM.m:64
    if (sum(cat(ylims_test - ylims)) + sum(cat(xlims_test - xlims))) > 0:
        error(cat('You region_lon_range and/or region_lat_range is not defined as [smallest largest], correct this.'))
    
    # the region the delay needs to cover.
# slightly larger than the InSAR region
    xmin=xlims[1]
# Trainmatlab.v.0/get_DEM.m:71
    xmax=xlims[2]
# Trainmatlab.v.0/get_DEM.m:72
    ymin=ylims[1]
# Trainmatlab.v.0/get_DEM.m:73
    ymax=ylims[2]
# Trainmatlab.v.0/get_DEM.m:74
    # getting the DEM path
    path_dem,filename_dem,ext_dem=fileparts(demfile,nargout=3)
# Trainmatlab.v.0/get_DEM.m:77
    # checking if file exists
    if exist(demfile,'file') != 2:
        error('dem file does not exist')
    
    # check if this is a grd file already
    if strcmpi(ext_dem,'.grd'):
        fprintf(cat('Specified DEM is a .grd file\\n'))
        if exist('tmp.grd','file') == 2:
            delete('tmp.grd')
        system_command=matlabarray(cat('ln -s ',demfile,' tmp.grd'))
# Trainmatlab.v.0/get_DEM.m:90
        aps_systemcall(system_command)
    else:
        clear('filename_dem','ext_dem')
        file_bad=2
# Trainmatlab.v.0/get_DEM.m:95
        dem_support=matlabarray([])
# Trainmatlab.v.0/get_DEM.m:96
        if exist(cat(demfile,'.rsc'),'file') == 2:
            file_bad=file_bad - 1
# Trainmatlab.v.0/get_DEM.m:98
            dem_support=matlabarray(cat('.rsc'))
# Trainmatlab.v.0/get_DEM.m:99
        if exist(cat(demfile,'.xml'),'file') == 2:
            file_bad=file_bad - 1
# Trainmatlab.v.0/get_DEM.m:102
            dem_support=matlabarray(cat('.xml'))
# Trainmatlab.v.0/get_DEM.m:103
        if file_bad == 2:
            fprintf(cat('Your DEM is not .grd.\\n This is fine but you need a  .rsc or.xml file\\n'))
            error(cat(demfile,'.rsc or.xml not found'))
        else:
            if file_bad == 0:
                fprintf(cat('Found both ',demfile,'.xml and .rsc. Will use .rsc file by default \\n'))
                dem_support=matlabarray(cat('.rsc'))
# Trainmatlab.v.0/get_DEM.m:111
        # gettign the DEM specifics
        if strcmpi(dem_support,'.xml'):
            # get dem details from xml file
            keyboard
            infoLabel='Plot Tools'
# Trainmatlab.v.0/get_DEM.m:121
            infoCbk=''
# Trainmatlab.v.0/get_DEM.m:121
            itemFound=copy(false)
# Trainmatlab.v.0/get_DEM.m:121
            xDoc=xmlread(fullfile(matlabroot,'toolbox/matlab/general/info.xml'))
# Trainmatlab.v.0/get_DEM.m:122
            allListItems=xDoc.getElementsByTagName('listitem')
# Trainmatlab.v.0/get_DEM.m:125
            for i in arange(0,allListItems.getLength - 1).reshape(-1):
                thisListItem=allListItems.item(i)
# Trainmatlab.v.0/get_DEM.m:129
                childNode=thisListItem.getFirstChild
# Trainmatlab.v.0/get_DEM.m:130
                while logical_not(isempty(childNode)):

                    #Filter out text, comments, and processing instructions.
                    if childNode.getNodeType == childNode.ELEMENT_NODE:
                        #Assume that each element has a single org.w3c.dom.Text child
                        childText=char(childNode.getFirstChild.getData)
# Trainmatlab.v.0/get_DEM.m:136
                        if 'label' == char(childNode.getTagName):
                            itemFound=strcmp(childText,infoLabel)
# Trainmatlab.v.0/get_DEM.m:138
                        else:
                            if 'callback' == char(childNode.getTagName):
                                infoCbk=copy(childText)
# Trainmatlab.v.0/get_DEM.m:139
                    childNode=childNode.getNextSibling
# Trainmatlab.v.0/get_DEM.m:142

                if itemFound:
                    print_('itemFound-changed to comply with the smop python package-ask muhiredesire01@gmail.com')
                else:
                    infoCbk=''
# Trainmatlab.v.0/get_DEM.m:146
                #modified line was if itemFound return; else infoCbk = ''; end
            disp(sprintf('Item "%s" has a callback of "%s".',infoLabel,infoCbk))
            error('Work in progress')
        else:
            if strcmpi(dem_support,'.rsc'):
                # get dem details from rsc file
                ncols_cmd=matlabarray(cat('echo `grep WIDTH ',demfile,'.rsc | awk \'{print $2}\'`>',path_dem,filesep,'temp'))
# Trainmatlab.v.0/get_DEM.m:157
                aps_systemcall(ncols_cmd)
                nrows_cmd=matlabarray(cat('echo `grep LENGTH ',demfile,'.rsc | awk \'{print $2}\'`>>',path_dem,filesep,'temp'))
# Trainmatlab.v.0/get_DEM.m:159
                aps_systemcall(nrows_cmd)
                xfirst_cmd=matlabarray(cat('echo `grep X_FIRST ',demfile,'.rsc | awk \'{print $2}\'`>>',path_dem,filesep,'temp'))
# Trainmatlab.v.0/get_DEM.m:161
                aps_systemcall(xfirst_cmd)
                yfirst_cmd=matlabarray(cat('echo `grep Y_FIRST ',demfile,'.rsc | awk \'{print $2}\'`>>',path_dem,filesep,'temp'))
# Trainmatlab.v.0/get_DEM.m:163
                aps_systemcall(yfirst_cmd)
                xstep_cmd=matlabarray(cat('echo `grep X_STEP ',demfile,'.rsc | awk \'{print $2}\'`>>',path_dem,filesep,'temp'))
# Trainmatlab.v.0/get_DEM.m:165
                aps_systemcall(xstep_cmd)
                ystep_cmd=matlabarray(cat('echo `grep Y_STEP ',demfile,'.rsc | awk \'{print $2}\'`>>',path_dem,filesep,'temp'))
# Trainmatlab.v.0/get_DEM.m:167
                aps_systemcall(ystep_cmd)
                format_cmd=matlabarray(cat('echo `grep FORMAT ',demfile,'.rsc | awk \'{print $2}\'`>',path_dem,filesep,'temp2'))
# Trainmatlab.v.0/get_DEM.m:169
                aps_systemcall(format_cmd)
                DEM_info=load(cat(path_dem,filesep,'temp'))
# Trainmatlab.v.0/get_DEM.m:173
                aps_systemcall(cat('rm ',path_dem,filesep,'temp'))
                ncols=DEM_info[1]
# Trainmatlab.v.0/get_DEM.m:175
                nrows=DEM_info[2]
# Trainmatlab.v.0/get_DEM.m:176
                xfirst=DEM_info[3]
# Trainmatlab.v.0/get_DEM.m:177
                yfirst=DEM_info[4]
# Trainmatlab.v.0/get_DEM.m:178
                xstep=DEM_info[5]
# Trainmatlab.v.0/get_DEM.m:179
                ystep=DEM_info[6]
# Trainmatlab.v.0/get_DEM.m:180
                clear('DEM_info')
        ## Getting the DEM precision
    #automatically checking dem format, by hua wang, 26 Feb 2015
        fid=fopen(demfile,'r')
# Trainmatlab.v.0/get_DEM.m:186
        fseek(fid,0,'eof')
        pos=ftell(fid)
# Trainmatlab.v.0/get_DEM.m:188
        byte=pos / ncols / nrows
# Trainmatlab.v.0/get_DEM.m:189
        fseek(fid,0,'bof')
        if 8 == byte:
            format_dem_str='d'
# Trainmatlab.v.0/get_DEM.m:193
        else:
            if 4 == byte:
                format_dem_str='f'
# Trainmatlab.v.0/get_DEM.m:195
            else:
                if 2 == byte:
                    format_dem_str='i'
# Trainmatlab.v.0/get_DEM.m:197
                else:
                    if 1 == byte:
                        format_dem_str='h'
# Trainmatlab.v.0/get_DEM.m:199
                    else:
                        error('no such dem format')
        # give warning as we cannot discriminate between int16 and short
        if strcmpi(format_dem_str,'i'):
            fprintf('Could be int16 or short format \\n')
        fclose(fid)
        fid=fopen(cat(path_dem,filesep,'temp2'))
# Trainmatlab.v.0/get_DEM.m:210
        DEM_info2=textscan(fid,'%s')
# Trainmatlab.v.0/get_DEM.m:211
        fclose(fid)
        aps_systemcall(cat('rm ',path_dem,filesep,'temp2'))
        format=DEM_info2[1]
# Trainmatlab.v.0/get_DEM.m:214
        clear('DEM_info2')
        format_dem_str_given=matlabarray([])
# Trainmatlab.v.0/get_DEM.m:217
        if logical_not(isempty(format)):
            if strcmpi(format,'r4') or strcmpi(format,'real4'):
                format_dem_str_given='f'
# Trainmatlab.v.0/get_DEM.m:220
            else:
                if strcmpi(format,'h'):
                    format_dem_str_given='h'
# Trainmatlab.v.0/get_DEM.m:222
        # checking if the specified precision is different, then that of the automated estimation
        if logical_not(isempty(format_dem_str_given)):
            if logical_not(strcmpi(format_dem_str_given,format_dem_str)):
                fprintf('The automated detected DEM precision is different then what you specified in dem.rsc file \\n:')
                fprintf(cat('Yours: ',format_dem_str_given,'\\n'))
                fprintf(cat('Auto: ',format_dem_str,'\\n'))
                repeat=1
# Trainmatlab.v.0/get_DEM.m:233
                while repeat == 1:

                    action_flag=str2num(input_('Keep yours (1), Keep auto (2), Different (3)? [1, 2, or 3] ','s'))
# Trainmatlab.v.0/get_DEM.m:235
                    if isnumeric(action_flag):
                        if action_flag == 1:
                            format_dem_str=copy(format_dem_str_given)
# Trainmatlab.v.0/get_DEM.m:238
                            repeat=0
# Trainmatlab.v.0/get_DEM.m:239
                        else:
                            if action_flag == 2:
                                format_dem_str=copy(format_dem_str)
# Trainmatlab.v.0/get_DEM.m:241
                                repeat=0
# Trainmatlab.v.0/get_DEM.m:242
                            else:
                                if action_flag == 3:
                                    action_flag=input_('To what do you want to update this? [give a format recognised by GMT]','s')
# Trainmatlab.v.0/get_DEM.m:244
                                    format_dem_str=copy(action_flag)
# Trainmatlab.v.0/get_DEM.m:245
                                    repeat=0
# Trainmatlab.v.0/get_DEM.m:246

                fprintf(cat('Please verify, and re-run'))
        ## getting the DEM as a grid again
        #getting the extends of the DEM
    #revised by hua wang, 26, Feb
        if strcmp(pixelreg,'gridline') == 0:
            xlast=xfirst + dot(ncols,xstep)
# Trainmatlab.v.0/get_DEM.m:260
            ylast=yfirst + dot(nrows,ystep)
# Trainmatlab.v.0/get_DEM.m:261
        else:
            xlast=xfirst + dot((ncols - 1),xstep)
# Trainmatlab.v.0/get_DEM.m:263
            ylast=yfirst + dot((nrows - 1),ystep)
# Trainmatlab.v.0/get_DEM.m:264
        if strcmp(pixelreg,'gridline') == 0:
            xyz2grd_cmd=matlabarray(cat('xyz2grd -R',num2str(xfirst),'/',num2str(xlast),'/',num2str(ylast),'/',num2str(yfirst),' -I',num2str(ncols),'+/',num2str(nrows),'+ ',demfile,' -Gtmp.grd -N',num2str(demnull),' -F -ZTL',format_dem_str))
# Trainmatlab.v.0/get_DEM.m:268
        else:
            xyz2grd_cmd=matlabarray(cat('xyz2grd -R',num2str(xfirst),'/',num2str(xlast),'/',num2str(ylast),'/',num2str(yfirst),' -I',num2str(ncols),'+/',num2str(nrows),'+ ',demfile,' -Gtmp.grd -N',num2str(demnull),' -ZTL',format_dem_str))
# Trainmatlab.v.0/get_DEM.m:270
        # down-sample dem to the grid as secified by the user with the given resolution    
    # in case the format is int16 lets first try to see if its not short format
        if strcmpi(format_dem_str,'i'):
            try:
                aps_systemcall(xyz2grd_cmd)
            finally:
                pass
        else:
            aps_systemcall(xyz2grd_cmd)
    
    # getting the information about the grid dem file
    
    # getting a temp identified. 
# make it random such mutiple correction methods can be ran simultaneous
    temp_num=round(dot(rand(1),10000))
# Trainmatlab.v.0/get_DEM.m:297
    y_first_new_cmd=matlabarray(cat('echo `grdinfo tmp.grd | grep y_min`>','temp',num2str(temp_num)))
# Trainmatlab.v.0/get_DEM.m:299
    aps_systemcall(y_first_new_cmd)
    temp=fileread(cat('temp',num2str(temp_num)))
# Trainmatlab.v.0/get_DEM.m:301
    ix_y_min=findstr('y_min',temp)
# Trainmatlab.v.0/get_DEM.m:302
    ix_y_max=findstr('y_max',temp)
# Trainmatlab.v.0/get_DEM.m:303
    ix_y_end=findstr('y_inc',temp)
# Trainmatlab.v.0/get_DEM.m:304
    y_first_new=str2num(temp[ix_y_min + 7:ix_y_max - 2])
# Trainmatlab.v.0/get_DEM.m:305
    y_last_new=str2num(temp[ix_y_max + 7:ix_y_end - 2])
# Trainmatlab.v.0/get_DEM.m:306
    clear('y_first_new_cmd')
    clear('temp','ix_y_end')
    clear('ix_y_max')
    clear('ix_y_min')
    x_first_new_cmd=matlabarray(cat('echo `grdinfo tmp.grd | grep x_min`>','temp',num2str(temp_num)))
# Trainmatlab.v.0/get_DEM.m:308
    aps_systemcall(x_first_new_cmd)
    temp=fileread(cat('temp',num2str(temp_num)))
# Trainmatlab.v.0/get_DEM.m:310
    ix_x_min=findstr('x_min',temp)
# Trainmatlab.v.0/get_DEM.m:311
    ix_x_max=findstr('x_max',temp)
# Trainmatlab.v.0/get_DEM.m:312
    ix_x_end=findstr('x_inc',temp)
# Trainmatlab.v.0/get_DEM.m:313
    x_first_new=str2num(temp[ix_x_min + 7:ix_x_max - 2])
# Trainmatlab.v.0/get_DEM.m:314
    x_last_new=str2num(temp[ix_x_max + 7:ix_x_end - 2])
# Trainmatlab.v.0/get_DEM.m:315
    clear('x_first_new_cmd','temp','ix_x_end','ix_x_max','ix_x_min')
    delete(cat('temp',num2str(temp_num)))
    if ymin < y_first_new:
        fprintf('Your min latitude crop is outside the DEM extend, reset to the maximum \\n')
        ymin=copy(y_first_new)
# Trainmatlab.v.0/get_DEM.m:321
    
    if ymax > y_last_new:
        fprintf('Your max latitude crop is outside the DEM extend, reset to the maximum \\n')
        ymax=copy(y_last_new)
# Trainmatlab.v.0/get_DEM.m:325
    
    # checking if both the region and grd are defined in the same quadrant
    if xmin / abs(xmin) != x_first_new / abs(x_first_new):
        x_first_new=x_first_new - 360
# Trainmatlab.v.0/get_DEM.m:329
    
    if xmax / abs(xmax) != x_last_new / abs(x_last_new):
        x_last_new=x_last_new - 360
# Trainmatlab.v.0/get_DEM.m:332
    
    if xmin < x_first_new:
        fprintf('Your min longitude crop is outside the DEM extend, reset to the maximum \\n')
        xmin=copy(x_first_new)
# Trainmatlab.v.0/get_DEM.m:336
    
    if xmax > x_last_new:
        fprintf('Your max longitude crop is outside the DEM extend, reset to the maximum \\n')
        xmax=copy(x_last_new)
# Trainmatlab.v.0/get_DEM.m:340
    
    if exist('tmp_smp.grd','file') == 2:
        delete('tmp_smp.grd')
    
    grdsmp_cmd=matlabarray(cat('grdsample -R',num2str(xmin),'/',num2str(xmax),'/',num2str(ymin),'/',num2str(ymax),' -I',num2str(smpres),' tmp.grd -Gtmp_smp.grd'))
# Trainmatlab.v.0/get_DEM.m:347
    aps_systemcall(grdsmp_cmd)
    grd2xyz_cmd=matlabarray(cat('grd2xyz -R',num2str(xmin),'/',num2str(xmax),'/',num2str(ymin),'/',num2str(ymax),' tmp_smp.grd -bo > ',smpdem))
# Trainmatlab.v.0/get_DEM.m:349
    aps_systemcall(grd2xyz_cmd)
    clear('a')
    clear('b')
    #reading the dem file again for latter processing
    demfid=fopen(smpdem,'r')
# Trainmatlab.v.0/get_DEM.m:354
    data_vector=fread(demfid,'double')
# Trainmatlab.v.0/get_DEM.m:355
    fclose(demfid)
    # reshaping into the right n column matrix
    data=reshape(data_vector,3,[]).T
# Trainmatlab.v.0/get_DEM.m:359
    dem=data[:,3]
# Trainmatlab.v.0/get_DEM.m:360
    clear('data')
    clear('data_vector')
    ## load the resampled DEM
    nncols_cmd=matlabarray(cat('echo `grdinfo tmp_smp.grd | grep nx | awk \'{print $NF}\'`>',path_dem,filesep,'temp3'))
# Trainmatlab.v.0/get_DEM.m:365
    aps_systemcall(nncols_cmd)
    nnrows_cmd=matlabarray(cat('echo `grdinfo tmp_smp.grd | grep ny | awk \'{print $NF}\'`>>',path_dem,filesep,'temp3'))
# Trainmatlab.v.0/get_DEM.m:367
    aps_systemcall(nnrows_cmd)
    DEM_info=load(cat(path_dem,filesep,'temp3'))
# Trainmatlab.v.0/get_DEM.m:369
    aps_systemcall(cat('rm ',path_dem,filesep,'temp3'))
    nncols=DEM_info[1]
# Trainmatlab.v.0/get_DEM.m:371
    nnrows=DEM_info[2]
# Trainmatlab.v.0/get_DEM.m:372
    clear('DEM_info')
    dem=reshape(dem,nncols,nnrows).T
# Trainmatlab.v.0/get_DEM.m:374
    if fig_test == 1:
        figure('name','DEM debug test')
        imagesc(cat(xmin,xmax),cat(ymax,ymin),dem)
        colorbar
        view(0,90)
        axis('equal')
        axis('tight')
        axis('xy')
        # check if this is correct
        str=''
# Trainmatlab.v.0/get_DEM.m:386
        while logical_not(strcmpi(str,'y')) and logical_not(strcmpi(str,'n')):

            fprintf(cat('Does the DEM look reasonable? \\n'))
            str=input_('Continue? [y: for yes, n: no] \\n','s')
# Trainmatlab.v.0/get_DEM.m:389

        if strcmpi(str,'n'):
            error('Check the dem input file.')
    