######################################################################
# Compiler definitions for jaguar.ccs.ornl.gov (compute nodes) 
#  all compiler specific information should be declared here
CXX:=CC

CXXFLAGS:= -fastsse -tp k8-64 -DMPICH_IGNORE_CXX_SEEK  

CXXFLAGS += -DUSE_MPI -DUSE_STDARG -DHAVE_STDLIB_H=1 -DHAVE_STRING_H=1 \
            -DHAVE_UNISTD_H=1 -DHAVE_STDARG_H=1 -DUSE_STDARG=1 \
            -DMALLOC_RET_VOID=1 -I$(MPIDIRECTORY)/include $(INCLUDEPATH)

#CXXFLAGS+= -DUSE_LAPACK -DUSE_BLAS

#LAPACK_LIBS := -L/usr/lib -llapack -lf77blas -lcblas -latlas 

#BLAS_LIBS := $(LAPACK_LIBS)

#DEBUG := -Wall  -DRANGE_CHECKING -DDEBUG_WRITE
DEBUG := -DNO_RANGE_CHECKING -DNDEBUG -DDEBUG_WRITE
#LDFLAGS := -static
LDFLAGS :=


######################################################################
# This is the invokation to generate dependencies
DEPENDMAKER:=CC -MM  $(INCLUDEPATH)

