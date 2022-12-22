import os
from datetime import datetime
from hashlib import md5
from sys import argv
from time import sleep


def make_md5_list(path):
    # Creating dictonatry with
    # Hashsum and name of the file
    # For comparing existing files
    for filename in os.listdir(path):
        file = path + os.sep + filename
        if os.path.isdir(file):
            make_md5_list(file)
        else:
            with open(file, "rb") as f:
                hashed = md5(f.read()).hexdigest()
                if hashed not in md_dict:
                    md_dict[hashed] = file


def replication(s_path, r_path, l_file):

    make_md5_list(r_path)
    with open(l_file, "a") as log_file:
        # Open log file at start
        # To not open after every operation
        for filename in os.listdir(s_path):  # Get all filenames in directory
            # Generate path for file
            source_file = s_path + os.sep + filename
            replica = r_path + os.sep + filename

            if os.path.isdir(source_file):
                # If file is directory
                if not os.path.exists(replica):  # Check if exist
                    os.mkdir(replica)  # Create if not
                # And go to that dir with recursion
                replication(source_file, replica, l_file)
            else:
                try:
                    with open(source_file, "rb") as source:
                        # Get current time for log one time
                        # For reducing line size and not to get it every time
                        current_time = datetime.now().strftime('%H:%M:%S')
                        data = source.read()
                        # Get hash sum for comparing
                        md5_data = md5(data).hexdigest()
                        if md5_data not in md_dict and not os.path.exists(replica):
                            # Check if it full new file and copy
                            md_dict[md5_data] = replica
                            # Logging
                            print(
                                f"{current_time} | Copying {source_file} to {replica}")
                            log_file.write(
                                f"{current_time} | Copying {source_file} to {replica}\n")
                            with open(replica, "wb") as r_file:
                                r_file.write(data)
                        elif md5_data in md_dict and not os.path.exists(replica):
                            # Or if just renamed file
                            os.rename(md_dict[md5_data],
                                      r_path + os.sep + filename)
                            # Logging
                            log_file.write(
                                f"{current_time} | File {replica} was renamed\n")
                            print(
                                f"{current_time} | File {replica} was renamed")
                except PermissionError:
                    current_time = datetime.now().strftime('%H:%M:%S')
                    print(f"{current_time} | PermissionError with {source_file}")
                    log_file.write(
                        f"{current_time} | PermissionError with {source_file}")


def removing(s_path, r_path, l_file):
    for filename in os.listdir(r_path):
        # Get all files in replica folder and compare
        source_file = s_path + os.sep + filename
        replica = r_path + os.sep + filename
        current_time = datetime.now().strftime('%H:%M:%S')
        if os.path.isdir(replica):
            # if file is dir and was deleted
            if not os.path.exists(source_file):
                # Recursion for delete all the files
                removing(source_file, replica, l_file)
                os.rmdir(replica)
                with open(l_file, "a") as log_file:
                    log_file.write(
                        f"{current_time} | removing directory {replica}\n")
                print(
                    f"{current_time} | removing directory {replica}")
            else:
                removing(source_file, replica, l_file)
        else:
            if not os.path.exists(source_file):
                with open(l_file, "a") as log_file:
                    log_file.write(
                        f"{current_time} | removing {replica}\n")
                print(
                    f"{current_time} | removing {replica}")
                os.remove(replica)


if __name__ == "__main__":
    try:
        s_path = argv[1]
        r_path = argv[2]
        l_file = argv[3]
    except IndexError:
        print(
            "Some argument needed.\nUsage: python3 script.py /source/path /replica/path log.txt interval(in sec)"
        )
        exit()
    with open(l_file, "a") as log:
        log.write(
            f"{datetime.now().strftime('%H:%M:%S')} | Starting...\n")
    while True:
        try:
            # Cleaning dict for comparing
            md_dict = {}
            replication(s_path, r_path, l_file)
            removing(s_path, r_path, l_file)
            sleep(int(argv[4]))
        except KeyboardInterrupt:
            with open(l_file, "a") as log:
                log.write(
                    f"{datetime.now().strftime('%H:%M:%S')} | Exiting...\n")
            exit()
