# Autogenerated with SMOP 
from smop.core import *
# Trainmatlab.v.0/load_sounding_download.m

    
@function
def load_sounding_download(filename=None,*args,**kwargs):
    varargin = load_sounding_download.varargin
    nargin = load_sounding_download.nargin

    # [P,h,T,DWPT,RH] = load_sounding_profile_download(filename)
# Function to read and save the sounding data as donloaded by the sounding_profile_download function.
# Main program variables are saved as P [hPa], T [degrees], h [m] and  RH [#].
# The output file is saved under the same filename excluding the station number, i.e.
# it just contains the data YYYY_MM_DD_HH or acquisition.
    
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
    
    # Bekaert David generated using the auto load function in matlab
# University of Leeds
    
    # Modifications:
# DB 	03/2013 	Make comaptible with other sounding scripts
# DB	03/2013		Save the data automatically at the same path
# DB    10/2013   	Change filename
    
    startRow=5
# Trainmatlab.v.0/load_sounding_download.m:33
    ## Read columns of data as strings:
# For more information, see the TEXTSCAN documentation.
    formatSpec='%7s%7s%7s%7s%7s%7s%7s%7s%7s%7s%s%[^\\n\\r]'
# Trainmatlab.v.0/load_sounding_download.m:37
    ## Open the text file.
    fileID=fopen(filename,'r')
# Trainmatlab.v.0/load_sounding_download.m:40
    ## Read columns of data according to format string.
# This call is based on the structure of the file used to generate this
# code. If an error occurs for a different file, try regenerating the code
# from the Import Tool.
    dataArray=textscan(fileID,formatSpec,'Delimiter','','WhiteSpace','','HeaderLines',startRow - 1,'ReturnOnError',false)
# Trainmatlab.v.0/load_sounding_download.m:46
    ## Close the text file.
    fclose(fileID)
    ## Convert the contents of columns containing numeric strings to numbers.
# Replace non-numeric strings with NaN.
    raw=repmat(cellarray(['']),length(dataArray[1]),length(dataArray))
# Trainmatlab.v.0/load_sounding_download.m:53
    for col in arange(1,length(dataArray) - 1).reshape(-1):
        raw[1:length(dataArray[col]),col]=dataArray[col]
# Trainmatlab.v.0/load_sounding_download.m:55
    
    numericData=NaN(size(dataArray[1],1),size(dataArray,2))
# Trainmatlab.v.0/load_sounding_download.m:57
    for col in cat(1,2,3,4,5,6,7,8,9,10,11).reshape(-1):
        # Converts strings in the input cell array to numbers. Replaced non-numeric
    # strings with NaN.
        rawData=dataArray[col]
# Trainmatlab.v.0/load_sounding_download.m:62
        for row in arange(1,size(rawData,1)).reshape(-1):
            # suffixes.
            regexstr='(?<prefix>.*?)(?<numbers>([-]*(\\d+[\\,]*)+[\\.]{0,1}\\d*[eEdD]{0,1}[-+]*\\d*[i]{0,1})|([-]*(\\d+[\\,]*)*[\\.]{1,1}\\d+[eEdD]{0,1}[-+]*\\d*[i]{0,1}))(?<suffix>.*)'
# Trainmatlab.v.0/load_sounding_download.m:66
            try:
                result=regexp(rawData[row],regexstr,'names')
# Trainmatlab.v.0/load_sounding_download.m:68
                numbers=result.numbers
# Trainmatlab.v.0/load_sounding_download.m:69
                invalidThousandsSeparator=copy(false)
# Trainmatlab.v.0/load_sounding_download.m:72
                if any(numbers == ','):
                    thousandsRegExp='^\\d+?(\\,\\d{3})*\\.{0,1}\\d*$'
# Trainmatlab.v.0/load_sounding_download.m:74
                    if isempty(regexp(thousandsRegExp,',','once')):
                        numbers=copy(NaN)
# Trainmatlab.v.0/load_sounding_download.m:76
                        invalidThousandsSeparator=copy(true)
# Trainmatlab.v.0/load_sounding_download.m:77
                # Convert numeric strings to numbers.
                if logical_not(invalidThousandsSeparator):
                    numbers=textscan(strrep(numbers,',',''),'%f')
# Trainmatlab.v.0/load_sounding_download.m:82
                    numericData[row,col]=numbers[1]
# Trainmatlab.v.0/load_sounding_download.m:83
                    raw[row,col]=numbers[1]
# Trainmatlab.v.0/load_sounding_download.m:84
            finally:
                pass
    
    ## Replace non-numeric cells with NaN
    R=cellfun(lambda x=None: logical_not(isnumeric(x)) and logical_not(islogical(x)),raw)
# Trainmatlab.v.0/load_sounding_download.m:93
    
    raw[R]=cellarray([NaN])
# Trainmatlab.v.0/load_sounding_download.m:94
    
    ## Allocate imported array to column variable names
    P=cell2mat(raw[:,1])
# Trainmatlab.v.0/load_sounding_download.m:97
    h=cell2mat(raw[:,2])
# Trainmatlab.v.0/load_sounding_download.m:98
    T=cell2mat(raw[:,3])
# Trainmatlab.v.0/load_sounding_download.m:99
    DWPT=cell2mat(raw[:,4])
# Trainmatlab.v.0/load_sounding_download.m:100
    RH=cell2mat(raw[:,5])
# Trainmatlab.v.0/load_sounding_download.m:101
    MIXR=cell2mat(raw[:,6])
# Trainmatlab.v.0/load_sounding_download.m:102
    DRCT=cell2mat(raw[:,7])
# Trainmatlab.v.0/load_sounding_download.m:103
    SKNT=cell2mat(raw[:,8])
# Trainmatlab.v.0/load_sounding_download.m:104
    THTA=cell2mat(raw[:,9])
# Trainmatlab.v.0/load_sounding_download.m:105
    THTE=cell2mat(raw[:,10])
# Trainmatlab.v.0/load_sounding_download.m:106
    THTV=cell2mat(raw[:,11])
# Trainmatlab.v.0/load_sounding_download.m:107
    # saving the data in a mat variable. Omit the station number
    pathname,filename_temp,ext=fileparts(filename,nargout=3)
# Trainmatlab.v.0/load_sounding_download.m:111
    pathname=matlabarray(cat(pathname,filesep))
# Trainmatlab.v.0/load_sounding_download.m:112
    clear('ext')
    ix=find('_' == filename_temp)
# Trainmatlab.v.0/load_sounding_download.m:114
    if isempty(ix) == 1:
        fprintf('This is not the stationnumber_YYYYMMDD_HH.txt filename convention')
    
    save_filename=matlabarray(cat(pathname,filename_temp[ix[1] + 1:end()],'.mat'))
# Trainmatlab.v.0/load_sounding_download.m:118
    save(save_filename,'P','T','h','RH','MIXR','DRCT','SKNT','THTA','THTE','THTV')
    ## Clear temporary variables
    clear('filename')
    clear('startRow')
    clear('formatSpec')
    clear('fileID')
    clear('dataArray')
    clear('ans')
    clear('raw')
    clear('col')
    clear('numericData')
    clear('rawData')
    clear('row')
    clear('regexstr')
    clear('result')
    clear('numbers')
    clear('invalidThousandsSeparator')
    clear('thousandsRegExp')
    clear('me')
    clear('R')