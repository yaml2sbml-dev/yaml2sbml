#!/bin/sh

# Install CI dependencies

# required for wheel packages
pip install wheel

# iterate over optional dependencies
for par in "$@"; do
  case $par in
    amici)
      # for amici
      sudo apt-get install \
        swig3.0 libatlas-base-dev libhdf5-serial-dev
      sudo ln -s /usr/bin/Swig3.0 /usr/bin/swig

      # amici dev
      pip install \
        git+https://github.com/amici-dev/amici.git@develop#egg=amici\&subdirectory=python/sdist
    ;;

    *)
      echo "Unknown argument" >&2
      exit 1
    ;;
  esac
done
