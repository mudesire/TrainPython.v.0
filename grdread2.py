# Autogenerated with SMOP 
from smop.core import *
# Trainmatlab.v.0/grdread2.m

    
@function
def grdread2(file=None,*args,**kwargs):
    varargin = grdread2.varargin
    nargin = grdread2.nargin

    #GRDREAD2  Load a GMT grdfile (netcdf format)
    
    # Uses NetCDF libraries to load a GMT grid file.
# Duplicates (some) functionality of the program grdread (which requires
# compilation as a mexfile-based function on each architecture) using
# Matlab 2008b (and later) built-in NetCDF functionality
# instead of GMT libraries.
    
    # Z=GRDREAD2('filename.grd') will return the data as a matrix in Z
    
    # [X,Y,Z]=GRDREAD2('filename.grd') will also return X and Y vectors
# suitable for use in Matlab commands such as IMAGE or CONTOUR.
# e.g., imagesc(X,Y,Z); axis xy
    
    # Although both gridline and pixel registered grids can be read,
# pixel registration will be converted to gridline registration
# for the x- and y-vectors.
    
    # See also GRDWRITE2, GRDINFO2
    
    # CAUTION: This program currently does little error checking and makes
# some assumptions about the content and structure of NetCDF files that
# may not always be valid.  It is tested with COARDS-compliant NetCDF
# grdfiles, the standard format in GMT 4 and later, as well as GMT v3
# NetCDF formats.  It will not work with any binary grid file formats.
# It is the responsibility of the user to determine whether this
# program is appropriate for any given task.
    
    # For more information on GMT grid file formats, see:
# http://www.soest.hawaii.edu/gmt/gmt/doc/gmt/html/GMT_Docs/node70.html
# Details on Matlab's native netCDF capabilities are at:
# http://www.mathworks.com/access/helpdesk/help/techdoc/ref/netcdf.html
    
    # GMT (Generic Mapping Tools, <http://gmt.soest.hawaii.edu>)
# was developed by Paul Wessel and Walter H. F. Smith
    
    # Kelsey Jordahl
# Marymount Manhattan College
# Time-stamp: <Wed Jan  6 16:37:45 EST 2010>
    
    # Version 1.1.1, 6-Jan-2010
# released with minor changes in documentation along with grdwrite2 and grdinfo2
# Version 1.1, 3-Dec-2009
# support for GMT v3 grids added
# Version 1.0, 29-Oct-2009
# first posted on MATLAB Central
    
    if nargin < 1:
        help(mfilename)
        return x,y,z
    
    # check for appropriate Matlab version (>=7.7)
    V=regexp(version,'[ \\.]','split')
# Trainmatlab.v.0/grdread2.m:55
    if logical_or((str2num(V[1]) < 7),(str2num(V[1]) == logical_and(7,str2num(V[2])) < 7)):
        ver
        error('grdread2: Requires Matlab R2008b or later!')
    
    ncid=netcdf.open(file,'NC_NOWRITE')
# Trainmatlab.v.0/grdread2.m:61
    if isempty(ncid):
        return x,y,z
    
    ndims,nvars,ngatts,unlimdimid=netcdf.inq(ncid,nargout=4)
# Trainmatlab.v.0/grdread2.m:66
    if (nvars == 3):
        x=netcdf.getVar(ncid,0).T
# Trainmatlab.v.0/grdread2.m:69
        y=netcdf.getVar(ncid,1).T
# Trainmatlab.v.0/grdread2.m:70
        z=netcdf.getVar(ncid,2).T
# Trainmatlab.v.0/grdread2.m:71
    else:
        if (nvars == 6):
            dimname,dimlen=netcdf.inqDim(ncid,1,nargout=2)
# Trainmatlab.v.0/grdread2.m:74
            if (dimname == 'xysize'):
                xrange=netcdf.getVar(ncid,0).T
# Trainmatlab.v.0/grdread2.m:76
                yrange=netcdf.getVar(ncid,1).T
# Trainmatlab.v.0/grdread2.m:77
                z=netcdf.getVar(ncid,5)
# Trainmatlab.v.0/grdread2.m:78
                dim=netcdf.getVar(ncid,4).T
# Trainmatlab.v.0/grdread2.m:79
                pixel=netcdf.getAtt(ncid,5,'node_offset')
# Trainmatlab.v.0/grdread2.m:80
                if pixel:
                    dx=diff(xrange) / double(dim[1])
# Trainmatlab.v.0/grdread2.m:82
                    dy=diff(yrange) / double(dim[2])
# Trainmatlab.v.0/grdread2.m:83
                    x=arange(xrange[1] + dx / 2,xrange[2] - dx / 2,dx)
# Trainmatlab.v.0/grdread2.m:84
                    y=arange(yrange[1] + dy / 2,yrange[2] - dy / 2,dy)
# Trainmatlab.v.0/grdread2.m:85
                else:
                    dx=diff(xrange) / double(dim[1] - 1)
# Trainmatlab.v.0/grdread2.m:87
                    dy=diff(yrange) / double(dim[2] - 1)
# Trainmatlab.v.0/grdread2.m:88
                    x=arange(xrange[1],xrange[2],dx)
# Trainmatlab.v.0/grdread2.m:89
                    y=arange(yrange[1],yrange[2],dy)
# Trainmatlab.v.0/grdread2.m:90
                z=flipud(reshape(z,dim[1],dim[2]).T)
# Trainmatlab.v.0/grdread2.m:92
            else:
                error('Apparently not a GMT netCDF grid')
        else:
            error('Wrong number of variables in netCDF file!')
    
    netcdf.close(ncid)
    if 1 == nargout:
        double
        varargout[1]=z
# Trainmatlab.v.0/grdread2.m:105
    else:
        if 3 == nargout:
            varargout[1]=x
# Trainmatlab.v.0/grdread2.m:107
            varargout[2]=y
# Trainmatlab.v.0/grdread2.m:108
            varargout[3]=z
# Trainmatlab.v.0/grdread2.m:109
        else:
            error('grdread2: Incorrect # of output arguments!')
    