#!/usr/bin/env bash
current_date=`date +"%d-%m-%Y-%H-%M-%S"`;
folder_name=$(basename `pwd`);
cd ..;
tar -cvzf "stego_$current_date.tgz" $folder_name;
ls *.tgz;
cd -;
echo "done"
