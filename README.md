## UCOPY : A universal command line path copier

Universal Path Copier copies file/directory paths from the command line for further usage. It also offers a few basic conversion methods for the obtained filepaths

Command Line:
```
usage: Ucopy [-h] [-g | -R | -w | -l | -G] [-# | -a | -r] [--no-copy]
             [--no-print] [-u] [-/]
             [filepath ...]

Universal Path Copier. Copies file paths in a variety of different ways

optional arguments:
  -h, --help            show this help message and exit

Filepath Options: :
  [Positional Argument] How to choose the filepath to process

  filepath              Path to file. Can be empty(cwd), or more than one(only
                        first will be chosen)

Conversion Options: :
  Various types of conversions available in program

  -g, --gitbash         Convert windows path into gitbash path
  -R, --rc-trans, --reverse-chaeyoung
                        Get reverse chaeyoung translated path
  -w, --wsl             Get WSL equivalent(Windows only)
  -l, --lsw             Convert WSL path to Windows equivalent.
  -G, --reverse-gitbash
                        Reverse Gitbash path to windows path

Pre-processing Options: :
  Pre processing the path to the realpath/abspath before proceeding

  -#, --NONE            Take the input path as is. Useful for conversion of
                        WSL paths on Windows and such
  -a, --abs, --abspath  Get the absolute path. (DEFAULT)
  -r, --realpath, --real-path
                        Get realpath(traverse symlinks)

Final Driver Options: :
  Final options for the obtained path

  --no-copy             Does not copy final path to clipboard
  --no-print            Does not print final path to stdout
  -u, --url             Final path is made into URL instead of regular system
                        path
  -/, --/, --unix-slash
                        If switched, outputs all windows \ as unix /

```
