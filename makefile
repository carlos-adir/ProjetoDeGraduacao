#!/bin/bash
.SILENT:
.DEFAULT_GOAL := all
PETSC_DIR=~/Git/petsc/
PETSC_ARCH=arch-linux-c-opt

all: createfolder dependencies clonepetsc instpestc

createfolder:
	if [ ! -d ${PETSC_DIR} ]; then mkdir -p ${PETSC_DIR}; fi

dependencies: createfolder
	sudo apt-get install git
	sudo apt-get install gcc
	sudo apt-get install make

clonepetsc: dependencies
	~Git/ && git clone -b release https://gitlab.com/petsc/petsc.git petsc --depth 1 ${PETSC_DIR}

instpestc: clonepetsc
    (cd ${PETSC_DIR} && ./configure --download-mpich --with-debugging=no)
	