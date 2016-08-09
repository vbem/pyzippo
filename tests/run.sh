#!/usr/bin/env bash
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Introduction: run tests using Python unittest nodule
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# global configs
declare -i IS_DEBUG=1
declare PATH_THIS=$(realpath ${BASH_SOURCE[0]})
declare DIR_THIS=$(dirname $PATH_THIS)
declare BASE_THIS=$(basename $PATH_THIS)
declare DIR_TESTS=$DIR_THIS
declare DIR_PROJIECT=$(dirname $DIR_TESTS)

python -m unittest discover -cvb -s "$DIR_PROJIECT"