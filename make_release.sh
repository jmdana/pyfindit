#!/bin/bash

function _trap_error () {
    _name="$0"
    _line="$1"
    _err="$2"

    echo
    echo "*********************************************"
    echo "${_name}: line ${_line}"
    echo "Exit status: ${_err}"
    echo "*********************************************"
    exit 1
}

trap '_trap_error ${LINENO} ${$?}' ERR

# Get both version number and package name from setup.py 
VER=`sed -n 's/\s*version\s*=\s*"\(.*\)\s*"\s*,/\1/p' setup.py`
NAME=`sed -n 's/\s*name\s*=\s*"\(.*\)\s*"\s*,/\1/p' setup.py`
PYPI_URL="https://pypi.python.org/packages/source/${NAME:0:1}/${NAME}/${NAME}-${VER}.tar.gz"
ARCH_PATH="./archlinux"

echo "PACKAGE: ${NAME}"
echo "VERSION: ${VER}"
echo "PYPI: ${PYPI_URL}"
read -p "Do you want to continue? [y/n]" -n 1 -r

if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo
    # Make the PyPI release
    python setup.py sdist upload
    
    FILE_SIZE=`wget --quiet -O - ${PYPI_URL}`
    # While until the file is available
    while [ ${#FILE_SIZE} == 0 ]; do
        echo "Package not available, retrying..."
        sleep 5
        FILE_SIZE=`wget --quiet -O - ${PYPI_URL}`
    done

    # Calculate MD5
    MD5=`wget --quiet -O - ${PYPI_URL} | md5sum | cut -f 1 -d " "`

    # Modify the PKGBUILD
    mv ${ARCH_PATH}/PKGBUILD ${ARCH_PATH}/PKGBUILD_old
    sed "s/\(\s*pkgver\s*=\s*\)\(.*\)\s*/\1${VER}/" ${ARCH_PATH}/PKGBUILD_old > ${ARCH_PATH}/PKGBUILD
    sed -i "s/\(\s*md5sums\s*=\s*(\s*\"\)\s*.*\s*\(\")\)\s*/\1${MD5}\2/" ${ARCH_PATH}/PKGBUILD

    # Make the Arch package
    pushd ${ARCH_PATH}
    makepkg
    popd
    
    # Make sure that the commit was made
    git commit -a

    # Make the tag
    git tag -a v${VER} -m "Version ${VER}"
fi




