#!/bin/bash
.SILENT:
.DEFAULT_GOAL := all
HOME_DIR?=${shell pwd}
GIT_DIR=~/Git/
PETSC_DIR=${GIT_DIR}/petsc/
PETSC_ARCH=arch-linux-c-opt

all: createfolder dependencies clonepetsc instpestc

createfolder:
	if [ ! -d ${GIT_DIR} ]; then mkdir -p ${GIT_DIR}; fi

dependencies: 
	sudo apt-get install git
	sudo apt-get install gcc
	sudo apt-get install make

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