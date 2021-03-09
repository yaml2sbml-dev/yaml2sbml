#!/bin/sh

# iterate over optional dependencies
for par in "$@"; do
  case $par in
    amici)
      # for amici
      sudo apt-get install \
        swig3.0 libatlas-base-dev libhdf5-serial-dev libhdf5-cpp-100
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
