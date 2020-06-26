from brute import brute
from unrar import rarfile
import os
import pandas as pd


def fromdictionary(dicname):
    f = pd.read_table(dicname, encoding='utf-8', header=None, names=['wordlist'], dtype={'wordlist': str})
    for i in range(0, len(f)):
        yield f['wordlist'].values[i]


def crackrar(rarfilename, pwdgenerator):
    found = False
    foldernum = len(next(os.walk('.'))[1])
    for pwd in pwdgenerator:
        try:
            rar = rarfile.RarFile(rarfilename, pwd=pwd)
            rar.extractall(pwd=pwd)
            if foldernum < len(next(os.walk('.'))[1]):
                print("file extracted")
                print("the password is %s" % pwd)
                found = True
                break
        except rarfile.BadRarFile:
            pass
    if not found:
        print("Sorry, cannot find the password")


while __name__ == '__main__':
    print('----------------------------------------------------')
    print('    RAR Cracker')
    print('----------------------------------------------------')
    filename = input('Please enter the filename: ')
    while not os.path.isfile(filename):
        filename = input('no such file, please enter a valid filename: ')

    mode = ''
    while mode != 'dictionary' and mode != 'brute':
        mode = input("Please select a working mode [dictionary/brute]: ")

    pwdGen = None
    if mode == 'dictionary':
        dic_name = input("Please enter the filename of the dictionary: ")
        while not os.path.isfile(dic_name):
            dic_name = input("no such file, please enter a valid filename: ")
        pwdGen = fromdictionary(dic_name)

    if mode == 'brute':
        letters = input("Include letters? [yes/no] (default yes) ") != 'no'
        symbols = input("Include symbols? [yes/no] (default yes) ") != 'no'
        numbers = input("Include numbers? [yes/no] (default yes) ") != 'no'
        spaces = input("Include spaces? [yes/no] (default no) ") == 'yes'
        start_length = int(input("min length: "))
        length = int(input("max length: "))
        pwdGen = brute(start_length=start_length, length=length, letters=letters, numbers=numbers, symbols=symbols,
                       spaces=spaces)

    print('Start cracking')
    print('This may take some time, please wait...')
    crackrar(filename, pwdGen)
