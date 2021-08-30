#!/bin/bash

for i in {1,3,4,5}
do
#  mv generations/generation_"$i".txt generations/generations_$i.txt
  cat output/final/"$i".txt >> generations/generations_9.txt
done

