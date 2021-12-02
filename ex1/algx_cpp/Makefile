
HOSTNAME = $(shell hostname)
USERNAME = $(shell whoami)

EXEC = ./test_algx

DEBUG = 0

ARCH = x86-64
# Setup for MACOSX
# OS = osx
# Setup for Linux (might also depend on linux distro)
ifndef OS
    # default value
    OS = linux
endif

CPP = clang++
# CPP = g++



SRCDIR = .
OBJDIR = obj

CXXFLAGS = -Wall -Wno-non-virtual-dtor -pipe

LDFLAGS = -lpthread -ldl

ifeq ($(DEBUG), 1)
    CXXFLAGS += -g -p -std=c++17
else
    CXXFLAGS += -O3 -std=c++17
endif

STARTUP_SOURCE = main.cpp

# $< the name of the related file that caused the action.
# $* the prefix shared by target and dependent files.
# $? is the names of the changed dependents.
# $@ is the name of the file to be made.
# $^ dependencies above


# ----- object files ---------------------------------------------------------------

STARTUP_OBJ = $(addprefix $(OBJDIR)/, $(patsubst %.cpp,%.o, \
	$(patsubst src/%, %,$(STARTUP_SOURCE) ) ) )


all: test_algx

depend:
	@echo 
	@echo "creating dependencies ..."
	$(CPP) -MM $(CPPFLAGS) $(CPP_SOURCES) $(SINGLE_FILE_SOURCES) \
	$(STARTUP_SOURCE) $(LD_FLAGS) \
	| sed -e "s/.*:/$(OBJDIR)\/&/" > depend.in

# $(OBJDIR)/%.o: $(SRCDIR)/%.cpp $(SRCDIR)/%.h
# 	@echo
# 	@echo "compiling $<"
# 	$(CPP) $(CPPFLAGS) $(CXXFLAGS) -o $@ -c $< 

# for startup (no header file available)
$(OBJDIR)/main.o: $(STARTUP_SOURCE)
	@echo "compiling $<"
	$(CPP) $(CPPFLAGS) $(CXXFLAGS) -o $@ -c $< 

# ----- linking --------------------------------------------------------------------

test_algx: $(STARTUP_OBJ)
	@echo 
	@echo "linking ..."
	@echo
	$(CPP) $(CXXFLAGS) -o test_algx $(STARTUP_OBJ) $(LDFLAGS)

# ----- debugging and profiling ----------------------------------------------------

gdb: all
	gdb --args $(EXEC)

test: all
	$(EXEC)

clean:
	rm -rf obj/*.o test_algx

