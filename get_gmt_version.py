# Autogenerated with SMOP 
from smop.core import *
# matlab/get_gmt_version.m

    
@function
def get_gmt_version(*args,**kwargs):
    varargin = get_gmt_version.varargin
    nargin = get_gmt_version.nargin

    # function that checks the GMT version and returns version number and if
# its GMT5 and above. This function also includes a fix for MAC OS.
    
    #     Copyright (C) 2016  Bekaert David 
#     davidbekaert.com
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
# modifications
# 02/2016   DB      Fix in case the dump of GMT --version does not work
# 03/2016   DB      Fix in case gmt is defined as GMT executable
# 03/2016   DB      Be more clear on the GMT and gmt definition
    
    # checking if GMT can be called
# this is a bugfix for the MAC OS systems
    command_str=matlabarray(cat('gmt --version > gmt_version'))
# matlab/get_gmt_version.m:31
    gmt_does_not_work,b=system(command_str,nargout=2)
# matlab/get_gmt_version.m:32
    # Leeds machines define gmt as GMT
    if gmt_does_not_work != 0:
        command_str=matlabarray(cat('GMT --version > gmt_version'))
# matlab/get_gmt_version.m:35
        gmt_does_not_work,b=system(command_str,nargout=2)
# matlab/get_gmt_version.m:36
    
    # GMT does not work well
    while gmt_does_not_work != 0:

        fprintf('GMT or gmt is not an executable, will try to fix \\n')
        # exporting the library path manual
        fprintf('Define the Library path manual in matlab: \'\' \\n')
        setenv('DYLD_LIBRARY_PATH','')
        command_str=matlabarray(cat('gmt --version > gmt_version'))
# matlab/get_gmt_version.m:47
        gmt_does_not_work,b=system(command_str,nargout=2)
# matlab/get_gmt_version.m:48
        if gmt_does_not_work != 0:
            command_str=matlabarray(cat('GMT --version > gmt_version'))
# matlab/get_gmt_version.m:51
            gmt_does_not_work,b=system(command_str,nargout=2)
# matlab/get_gmt_version.m:52
        if gmt_does_not_work == 0:
            break
        else:
            error('Could not fix it, try to fix youself such you can call GMT or gmt from matlab command line as e.g.: gmt --version or GMT --version')

    
    clear('command_str','gmt_does_not_work')
    # loading the version number
    fid=fopen('gmt_version')
# matlab/get_gmt_version.m:64
    gmt_version=textscan(fid,'%s')
# matlab/get_gmt_version.m:65
    gmt_version=gmt_version[1]
# matlab/get_gmt_version.m:66
    fclose(fid)
    # somtimes the machine does not want to dump the information lets try to
# retrieve different
    if isempty(gmt_version):
        if logical_not(isempty(b)):
            ix=findstr('GMT Version',b)
# matlab/get_gmt_version.m:73
            if logical_not(isempty(ix)):
                gmt_version=strtrim(b[ix + 12 - 1:ix + 12 - 1 + 2])
# matlab/get_gmt_version.m:75
            else:
                error('Could not retrieve your GMT version')
    else:
        gmt_version=gmt_version[:]
# matlab/get_gmt_version.m:81
    
    clear('b')
    delete('gmt_version')
    # trying to call a GMT function
    command_str=matlabarray(cat('man psxy > gmt_function_test'))
# matlab/get_gmt_version.m:87
    gmt_does_not_work,b=system(command_str,nargout=2)
# matlab/get_gmt_version.m:88
    if gmt_does_not_work != 0:
        command_str2=matlabarray(cat('psxy --help> gmt_function_test'))
# matlab/get_gmt_version.m:90
        gmt_does_not_work,b=system(command_str2,nargout=2)
# matlab/get_gmt_version.m:91
    
    # GMT does not work well
    while gmt_does_not_work != 0:

        fprintf('GMT not an executable, will try to fix \\n')
        # exporting the library path manual
        fprintf('Define the Library path manual in matlab: \'\' \\n')
        setenv('DYLD_LIBRARY_PATH','/usr/local/bin/')
        gmt_does_not_work,b=system(command_str,nargout=2)
# matlab/get_gmt_version.m:101
        if gmt_does_not_work == 0:
            break
        else:
            error('Could not fix it, try to fix youself such you can call GMT from matlab command line as e.g.: > gmt --version, and > xyz2grd')

    
    clear('b','command_str','gmt_does_not_work')
    delete('gmt_function_test')
    # check if its GMT 5 and above
    if str2num(gmt_version[1]) >= 5:
        gmt5_above='y'
# matlab/get_gmt_version.m:114
    else:
        gmt5_above='n'
# matlab/get_gmt_version.m:116
    
    # generate output for user
    fprintf(cat('You are using GMT version: ',gmt_version,'\\n'))
    # if strcmpi(gmt5_above,'y')
#     fprintf('Will need to use the GMT compatible codes for GMT5 and above... \n')
# else
#     fprintf('Will need to use the GMT compatible codes for version before GMT5... \n')    
# end