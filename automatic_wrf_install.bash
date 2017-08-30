#!/bin/tcsh -f
# On cygwin install gcc,g++,gfortan, tcsh and perl
#
#  Run cygwin then run this script
#    chmod +x automatic_wrf_install.sh
#      ./automatic_wrf_install.sh
#
# if using a Multiprocessor uncomment MPICH 
#
#     Copyright (C) 2016 MUHIRE Desire - University Chouaib Doukkali,Morocco 2017
#     Email: muhiredesire01@gmail.com
#     script generated from UCAR webpage 
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

echo "Installing WRF "
echo "Testing installation"

echo "changing temporaly to tcsh shell"
    exec /usr/bin/tcsh
echo "Shell changed to tcsh"

echo "test compilers"
which gfortran
which cpp
which gcc

mkdir Build_WRF TESTS
cd TESTS
wget http://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/Fortran_C_tests.tar
tar -xf Fortran_C_tests.tar

echo "Test #1: Fixed Format Fortran Test: TEST_1_fortran_only_fixed.f"
gfortran TEST_1_fortran_only_fixed.f
./a.out

echo "Test #2: Free Format Fortran: TEST_2_fortran_only_free.f90"
gfortran TEST_2_fortran_only_free.f90
./a.out

echo "Test #3: C: TEST_3_c_only.c"
gcc TEST_3_c_only.c
./a.out

echo "Test #4: Fortran Calling a C Function:TEST_4_fortran+c_c.c, and TEST_4_fortran+x_f.f90 "
gcc -c -m64 TEST_4_fortran+c_c.c
gfortran -c -m64 TEST_4_fortran+c_f.f90
gfortran -m64 TEST_4_fortran+c_f.o TEST_4_fortran+c_c.o
./a.out

echo "Testing the top level for the user interface:csh,perl,sh."
echo "Test #5:csh In the command line, type:"
./TEST_csh.csh

echo "Test #6:perl In the command line, type:"
./TEST_perl.pl

echo "Test #7:sh In the command line, type:"
./TEST_sh.sh

echo "Moving to build libraries"
cd ..
cd Build_WRF
mkdir LIBRARIES
cd LIBRARIES
wget http://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/mpich-3.0.4.tar.gz
wget http://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/netcdf-4.1.3.tar.gz
wget http://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/jasper-1.900.1.tar.gz
wget http://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/libpng-1.2.50.tar.gz
wget http://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/zlib-1.2.7.tar.gz

echo " These libraries must all be installed with the same compilers as will"
echo "be used to install WRFV3 and WPS."

echo "NetCDF: This library is always necessary!"

setenv DIR /cygwin64/home/toshiba/build_WRF/LIBRARIES
setenv CC gcc
setenv CXX g++
setenv FC gfortran
setenv FCFLAGS -m64
setenv F77 gfortran
setenv FFLAGS -m64

tar xzvf netcdf-4.1.3.tar.gz     #or just .tar if no .gz present
cd netcdf-4.1.3
./configure --prefix=$DIR/netcdf --disable-dap \
     --disable-netcdf-4 --disable-shared
make
make install
setenv PATH $DIR/netcdf/bin:$PATH
setenv NETCDF $DIR/netcdf
cd ..

#echo "MPICH: This library is necessary if you are planning to build WRF "
#"in parallel. If your machine does not have more than 1 processor "
#"if not, you can skip installing MPICH."
#tar xzvf mpich-3.0.4.tar.gz     #or just .tar if no .gz present
#cd mpich-3.0.4
#./configure --prefix=$DIR/mpich
#make
#make install
#setenv PATH $HOME/mpich/bin:$PATH
#cd ..

echo "zlib: This is a compression library necessary for compiling WPS "
echo "(specifically ungrib) with GRIB2 capability"
setenv LDFLAGS -L$DIR/grib2/lib 
setenv CPPFLAGS -I$DIR/grib2/include 

tar xzvf zlib-1.2.7.tar.gz     #or just .tar if no .gz present
cd zlib-1.2.7
./configure --prefix=$DIR/grib2
make
make install
cd ..

echo "libpng: This is a compression library necessary for compiling WPS "
"(specifically ungrib) with GRIB2 capability"
tar xzvf libpng-1.2.50.tar.gz     #or just .tar if no .gz present
cd libpng-1.2.50
./configure --prefix=$DIR/grib2
make
make install
cd ..

echo "JasPer: This is a compression library necessary for compiling WPS"
echo "(specifically ungrib) with GRIB2 capability"
tar xzvf jasper-1.900.1.tar.gz     #or just .tar if no .gz present
cd jasper-1.900.1
./configure --prefix=$DIR/grib2
make
make install
cd ..

echo "Library Compatibility Tests"
cd ..
cd TESTS
wget http://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/Fortran_C_NETCDF_MPI_tests.tar
tar -xf Fortran_C_NETCDF_MPI_tests.tar

echo "There are 2 tests of Library Compatibility Tests"
echo "Test #1: Fortran + C + NetCDF"
cp ${NETCDF}/include/netcdf.inc .

gfortran -c 01_fortran+c+netcdf_f.f
gcc -c 01_fortran+c+netcdf_c.c
gfortran 01_fortran+c+netcdf_f.o 01_fortran+c+netcdf_c.o \-L${NETCDF}/lib -lnetcdff -lnetcdf
./a.out
echo "The following should be displayed on your screen:
C function called by Fortran
Values are xx = 2.00 and ii = 1
SUCCESS test 1 fortran + c + netcdf
Test #2: Fortran + C + NetCDF + MPI"

echo "The NetCDF+MPI test requires include files from both of these packages be 
in this directory, but the MPI scripts automatically make the mpif.h file 
available without assistance, so no need to copy that one. Copy the NetCDF 
include file here:"
cp ${NETCDF}/include/netcdf.inc .
echo "Note that the MPI executables mpif90 and mpicc are used below when
compiling. Issue the following commands:"
mpif90 -c 02_fortran+c+netcdf+mpi_f.f
mpicc -c 02_fortran+c+netcdf+mpi_c.c
mpif90 02_fortran+c+netcdf+mpi_f.o \
02_fortran+c+netcdf+mpi_c.o \
     -L${NETCDF}/lib -lnetcdff -lnetcdf
mpirun ./a.out
echo "The following should be displayed on your screen:"
echo "C function called by Fortran
Values are xx = 2.00 and ii = 1
status = 2
SUCCESS test 2 fortran + c + netcdf + mpi"
cd ..

echo "Building WRFV3"
cd Build_WRF
wget http://www2.mmm.ucar.edu/wrf/src/WRFV3.8.1.TAR.gz
gunzip WRFV3.8.1.TAR.gz
tar -xf WRFV3.8.1.TAR
cd WRFV3
./configure
echo "Choose the option that lists the compiler you are using
and the way you wish to build WRFV3 (i.e., serially or in parallel). "
echo"choose number: 
1 for em_real (3d real case)
2 for em_quarter_ss (3d ideal case)
3 for em_b_wave (3d ideal case)
4 fro em_les (3d ideal case)
5 for em_heldsuarez (3d ideal case)
6 for em_tropical_cyclone (3d ideal case)
7 for em_hill2d_x (2d ideal case)
8 for em_squall2d_x (2d ideal case)
9 for em_squall2d_y (2d ideal case)
10 for em_grav2d_x (2d ideal case)
11 for em_seabreeze2d_x (2d ideal case)
12 em_scm_xy (1d ideal case)"
read n
if [ $n = "1" ]
then
        case_name= "em_real"; 
elif [ $n = "2" ]
then
        case_name= "em_quarter_ss"
elif [ $n = "3" ]
then
        case_name="em_b_wave"
elif [ $n = "4" ]
then
        case_name= "em_les"; 
elif [ $n = "5" ]
then
        case_name= "em_heldsuarez"
elif [ $n = "6" ]
then
        case_name="em_tropical_cyclone"	
	
else
        echo "Error compliler option not specified"
fi

case $n in
        1) 
        2) 
        3) 
        4) case_name="fro em_les"
        5) case_name="em_heldsuarez"
6 for em_tropical_cyclone (3d ideal case)
7 for em_hill2d_x (2d ideal case)
8 for em_squall2d_x (2d ideal case)
9 for em_squall2d_y (2d ideal case)
10 for em_grav2d_x (2d ideal case)
11 for em_seabreeze2d_x (2d ideal case)
12 em_scm_xy (1d ideal case)"
        *) echo "Error select compiler ";
   esac;

./compile case_name >& log.compile







