# Autogenerated with SMOP 
from smop.core import *
# matlab/aps_powerlaw_bootstrap.m

    
@function
def aps_powerlaw_bootstrap(A=None,y=None,bood_num=None,*args,**kwargs):
    varargin = aps_powerlaw_bootstrap.varargin
    nargin = aps_powerlaw_bootstrap.nargin

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
    
    # iterations
    for k in arange(1,bood_num).reshape(-1):
        # bootstrapping positions
        ix=ceil(dot(rand(size(y,1),1),size(y,1)))
# matlab/aps_powerlaw_bootstrap.m:25
        A_new=copy(A)
# matlab/aps_powerlaw_bootstrap.m:26
        y_new=copy(y)
# matlab/aps_powerlaw_bootstrap.m:27
        A_new=A_new[ix,:]
# matlab/aps_powerlaw_bootstrap.m:28
        y_new=y_new[ix,:]
# matlab/aps_powerlaw_bootstrap.m:29
        coeff=lscov(A_new,y_new)
# matlab/aps_powerlaw_bootstrap.m:32
        coeff_vector[k,:]=coeff
# matlab/aps_powerlaw_bootstrap.m:34
    
    coeff_std=std(coeff_vector,0)
# matlab/aps_powerlaw_bootstrap.m:36