CFLAGS=-Wall -Wextra -std=c11 -pedantic -ggdb

SRCS = external/flag.c
LIB_DIR = flag/lib
LIBNAME = libflag.so


define REMOVE_DIRECTORY
  	 @find $(1) -type d -name $(2) -exec sh -c 'echo "removing directory: {}"' \;
	-@find $(1) -type d -name $(2) -exec rm -r {} +
endef


.PHONY: all
all: shared

shared: $(SRCS)
	@mkdir -p $(LIB_DIR)
	$(CC) $(CFLAGS) -shared -o $(LIB_DIR)/$(LIBNAME) -fPIC $(SRCS)

submodule:
	git submodule update --init --recursive

whl:
	python -m build

clean:
# clean up any pycache and egg-info files
	$(call REMOVE_DIRECTORY, "flag", "__pycache__")
	$(call REMOVE_DIRECTORY, "flag", "flag.egg-info")
	 @echo "removing dist/"
	-@rm -rf dist/
	 @echo "removing build/"
	-@rm -rf build/
	 @echo "removing $(LIB_DIR)/$(LIBNAME)"
	-@rm $(LIB_DIR)/$(LIBNAME)