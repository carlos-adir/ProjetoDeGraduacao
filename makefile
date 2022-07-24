#!/bin/bash
.SILENT:
.DEFAULT_GOAL := all
HOME_DIR?=${shell cd ~ && pwd}
GIT_DIR=${HOME_DIR}/Git
PETSC_DIR=${GIT_DIR}/petsc/
PETSC_ARCH=arch-linux-c-opt

all: createfolder dependencies clonepetsc instpestc

createfolder:
	(cd ~; \
	echo HOME_DIR=${HOME_DIR}; \
	echo GIT_DIR=${GIT_DIR}; \
	echo PETSC_DIR=${PETSC_DIR}; \
	if [ ! -d ${GIT_DIR} ]; then mkdir -p ${GIT_DIR}; fi)

dependencies:
	sudo apt-get install git -y
	sudo apt-get install gcc -y
	sudo apt-get install make -y

clonepetsc: createfolder dependencies
	(cd ${GIT_DIR}; \
	if [ ! -d ${PETSC_DIR} ]; then \
		git clone -b release https://gitlab.com/petsc/petsc.git petsc --depth 1; \
	fi)

instpestc: clonepetsc
	(cd ${PETSC_DIR}; \
		./configure --download-mpich --with-debugging=no --download-f2cblaslapack=1; \
		make PETSC_DIR=${PETSC_DIR} PETSC_ARCH=${PETSC_ARCH} all; \
		make PETSC_DIR=${PETSC_DIR} PETSC_ARCH=${PETSC_ARCH} check)
