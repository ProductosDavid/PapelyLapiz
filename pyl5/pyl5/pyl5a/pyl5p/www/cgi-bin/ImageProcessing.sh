
#!/bin/bash

# Parameters:
#   Image Name
#   Work folder
#   Script XML name
#   Process log file
#   Executable location

{

echo Parameter 1: "$1"
echo Parameter 2: "$2"
echo Parameter 3: "$3"
echo Parameter 4: "$4"
echo Parameter 5: "$5"

date
echo

cd $5
./ImageProcessing "$1" "$2" "$3"

echo

date

} > "$2/$4" 2>&1

