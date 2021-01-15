#!/bin/sh

# Install CI dependencies

# required for wheel packages
pip install wheel

# required for tests
pip install pytest pytest-cov

pip install flake8

# iterate over optional dependencies
for par in "$@"; do
  case $par in
    amici)
      # for amici
      sudo apt-get install \
        swig3.0 libatlas-base-dev libhdf5-serial-dev

      # install latest amici release
      pip install amici
    ;;

    *)
      echo "Unknown argument: $par" >&2
      exit 1
    ;;
  esac
done
