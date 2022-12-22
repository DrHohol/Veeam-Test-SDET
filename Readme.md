#  Folder sync

## What it is?
This is a program that periodically synchronizes the two folders and logs all actions.

## Usage
In command line you need to provide 4 arguments: Source path, replica path, path to log file and interval in seconds
#### Example 
`python3 script.py /home/user/my_folder /home/user/backup_folder log.txt 60`

In this example program will first copy all the data from my_folder to backup_folder, create log.txt file in directory with the script and then check my_folder for changes every 60 seconds.
