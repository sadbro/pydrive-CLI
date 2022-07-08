
global COL

import os
from termcolor import colored, cprint

## THE STANDARD DISPLAY DRIVER IN COMMAND-LINE

def R(text):

    return colored(text, "red")

def G(text):

    return colored(text, "green")

def B(text):

    return colored(text, "blue")

def Y(text):

    return colored(text, "yellow")

def W(text):

    return colored(text, "white")

def out(ITEMS):

    global COL

    COL= os.get_terminal_size()[0]
    TAB= round((0.6*COL))

    print(colored("\nGOOGLE DRIVE MANAGEMENT\n", "red", attrs=['underline', 'bold']))
    gi= G(" | ")
    print(colored("Directory", "yellow") + gi + colored("File", "white") + gi + colored("Error", "red"))
    print(G("="*COL))
    counter = 0
    total_size = 0
    for ITEM in ITEMS:
        gin= G("[{}] ".format(counter))
        counter += 1
        FI_FO = ITEM["NAME"]
        if ITEM["TYPE"] == "FILE":
            name_length= len(str(counter))+ 3+ len(FI_FO)
            GAP= TAB-name_length
            file_size= ITEM["SIZE"]
            print(gin + colored("{}".format(str(FI_FO)), "white") + colored("-"*GAP +"{}".format(file_size), "blue"))

        elif ITEM["TYPE"] == "DRIVE":
            print(gin + colored("{}/".format(str(FI_FO)), "yellow"))

        else:
            print(gin + colored("{}".format(str(FI_FO)), "red"))

    print(G("="*COL))

def fout(*args, **kwargs):

    content = args[0]
    delimiter = kwargs["sep"]
    has_index = kwargs["index"]

    if isinstance(content, list):

        if has_index:

            start = 1
            for item in content:
                print("[{}] {}".format(start, item))
                start += 1

        else:

            print(*content, sep=delimiter)

    else:

        print(content)
