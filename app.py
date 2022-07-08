
from driver import *
from display import *
from parser import *

__all__ = {
                "i" : "CMD_INSPECT",
                "n" : "CMD_NEW_FILE",
                "c" : "CMD_CLEAR",
                "s" : "CMD_SHOW",
                "e" : "CMD_EXIT",
                "d" : "CMD_DL_FILE"
          }

ALL = []

def execute(arg):

    ctype = arg["CMD"]

    if ctype == "CMD_INSPECT":

        if len(arg["PARSED_ARGS"]) == 0:

            print(Y("[WARN] ") + "Please enter a index to inspect")
            return True

        return inspect(arg["PARSED_ARGS"], SERVICE)

    if ctype == "CMD_NEW_FILE":

        file_name = input("Enter file name: ")
        file_path = input("Enter file path: ")

        metadata = {"name":file_name, "FILE_PATH":file_path}

        return new_file(metadata, SERVICE)

    elif ctype == "CMD_EXIT":

        return False

    elif ctype == "CMD_SHOW":

        out(ALL)
        return True

    elif ctype == "CMD_CLEAR":

        return clear()

    elif ctype == "CMD_DL_FILE":

        return down(arg["PARSED_ARGS"], SERVICE)

status = True
while status:

    ALL = []
    fetch(ALL, SERVICE)

    rc = input(colored("pydrive> ", 'blue', attrs=['bold']))
    command = parse(rc, conversion=__all__, ctx=ALL)

    returned = execute(command)

    if returned and type(returned) == list:
        fout(returned, sep='\n', index=True)
    else:
        status = returned

