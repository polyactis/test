export JULIA_DIR := $(HOME)/.julia/juliaup/julia-1.9.3+0.x64.linux.gnu


ExtraTargets = test
# include common after ExtraTargets so that ExtraTargets or other variables are initialized and could be expanded in dependency of all
# include common before other variables so that variables with += can build upon old values in common 
include ../../Makefile.common

JL_SHARE = $(shell julia -e 'print(joinpath(Sys.BINDIR, Base.DATAROOTDIR, "julia"))')
CFLAGS   += $(shell $(JL_SHARE)/julia-config.jl --cflags)
CXXFLAGS += $(shell $(JL_SHARE)/julia-config.jl --cflags)
LDFLAGS  += $(shell $(JL_SHARE)/julia-config.jl --ldflags)
LDLIBS   += $(shell $(JL_SHARE)/julia-config.jl --ldlibs)

test:	test.o
#	$(CCOMPILER) $< $(CFLAGS) $(IncludeDirs) -c -o $@
#	gcc -o test -fPIC -I$(JULIA_DIR)/include/julia -L$(JULIA_DIR)/lib -Wl,-rpath,$(JULIA_DIR)/lib test.c -ljulia




clean:	common_clean
