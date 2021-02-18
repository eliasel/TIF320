#!/bin/bash

for filename in ./gs_*tree*;
do
  echo $filename
  ase db $filename
done
