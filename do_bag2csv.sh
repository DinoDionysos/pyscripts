#!/bin/bash
# $1: start index for the files (0)
# $2: end index (19)
# $3: file_prefix (c8_orb_mono)
# $4: folder (orb) 
# $5: how long to show the plot (2)
# $6: folder on SSD
folder_ssd=/mnt/d
file_prefix=$3 # c8_orb_mono
folder_orb=$4 # orb


for i in $(seq $1 1 $2)
do
    python3 bag2csv_2.py $file_prefix"_"$i gt $file_prefix $folder_ssd $folder_orb
    python3 bag2csv_2.py $file_prefix"_"$i orb $file_prefix $folder_ssd $folder_orb
done



for i in $(seq $1 1 $2)
do
    # here get length of smallest csv file and interpolate the others at the timestamps if it.
    python3 rotate_coor.py \
    orb $i $5 $file_prefix $folder_ssd $folder_orb
done

