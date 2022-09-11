import sys
from os import remove
from read_data_from_files import all_results_folders, get_listfiles_in_folders, get_problem_files

def main():
    mainfolder = (sys.argv[0]).replace("removenonusefulfiles.py", "")
    allfolders = [mainfolder + folder for folder in all_results_folders()]
    listallfilenames = get_listfiles_in_folders(allfolders)
    problemfiles = get_problem_files(listallfilenames)
    print("Qtt problem files = ", len(problemfiles))
    for filename in problemfiles:
        remove(filename)

if __name__ == "__main__":
    main()
    
