#!/bin/sh

#exe_file="Final_with_deadcode/hw2cs561s16.py"
exe_file="hw2cs561s16.py"
#exe_file="/media/sf_Desktop/hw2cs561s16.py"
md5sum $exe_file
echo $exe_file

#for i in $(seq 1 33)
#for i in 8 10 14 16 20 29 33
for i in 33
do
    echo "__________________input_$i.txt_______________"
    python $exe_file -i ../testCases/input_$i.txt && diff output.txt ../testCases/output_$i.txt -w
echo " "
done
