#!/bin/sh

# Install tox
pip install tox

# Update apt package lists
sudo apt-get update

# iterate over optional dependencies
for par in "$@"; do
  case $par in
    amici)
      # for amici
      sudo apt-get install \
        swig libatlas-base-dev libhdf5-serial-dev
    ;;

    doc)
      # documentation
      sudo apt-get install pandoc
    ;;

    *)
      echo "Unknown argument: $par" >&2
      exit 1
    ;;
  esac
done
