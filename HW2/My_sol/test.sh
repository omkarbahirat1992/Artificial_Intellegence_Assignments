#!/bin/sh

#exe_file="Final/hw2cs561s16.py"
exe_file="/media/sf_Desktop/hw2cs561s16.py"
md5sum $exe_file

echo $exe_file
echo "__________________sample01_______________"
python $exe_file -i ../samples_v4/sample01.txt && diff output.txt ../samples_v4/sample01.output.txt
echo " "

echo "__________________sample02_______________"
python $exe_file -i ../samples_v4/sample02.txt && diff output.txt ../samples_v4/sample02.output.txt
echo " "

echo "__________________sample03_______________"
python $exe_file -i ../samples_v4/sample03.txt && diff output.txt ../samples_v4/sample03.output.txt -w
echo " "

echo "__________________sample04_______________"
python $exe_file -i ../samples_v4/sample04.txt && diff output.txt ../samples_v4/sample04.output.txt -w
echo " "

echo "__________________sample05_______________"
python $exe_file -i ../samples_v4/sample05.txt && diff output.txt ../samples_v4/sample05.output.txt
echo " "
