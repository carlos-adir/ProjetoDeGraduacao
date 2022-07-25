import sys
from os import system
from read_data_from_files import get_problem_files


def delete_command(filename: str):
    return "rm " + filename


def main():
    mainfolder = (sys.argv[0]).replace("removenonusefulfiles.py", "")
    folder = mainfolder + "results_googlecloud8-2022-07-24"
    filenames = get_problem_files(folder)
    for filename in filenames:
        command = delete_command(folder + "/" + filename)
        print(f"Removing file {filename}")
        system(command)

if __name__ == "__main__":
    main()
    
