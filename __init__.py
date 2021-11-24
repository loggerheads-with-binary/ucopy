from argparse import ArgumentParser, Namespace
import os
import sys



def arguments(args : list = None ):

    parser = ArgumentParser(prog = "Ucopy" ,
                            description = "Universal Path Copier. Copies file paths in a variety of different ways" )


    fpath_parser = parser.add_argument_group(title = "Filepath Options: " , description = "[Positional Argument]\t\tHow to choose the filepath to process")
    fpath_parser.add_argument(dest = "filepath" , nargs = '*' , type = str ,
                        help = "Path to file. Can be empty(cwd), or more than one(only first will be chosen)")


    ##Type Conversion Flags
    types_parser = parser.add_argument_group(title = "Conversion Options: " , description = "Various types of conversions available in program")
    P2 = types_parser.add_mutually_exclusive_group()

    P2.add_argument('-g' , '--gitbash' , dest = 'type_' , action = 'store_const' , const = 'gitbash' , default = 'regular' ,
                    help = 'Convert windows path into gitbash path')

    P2.add_argument('-R' , '--rc-trans' , '--reverse-chaeyoung' , dest = 'type_' , default = 'regular' , action = 'store_const' , const = 'R_CHAE' ,
                    help = 'Get reverse chaeyoung translated path')

    P2.add_argument('-w' , '--wsl' , dest = 'type_' , action = 'store_const' , default = 'regular' , const = 'wsl' , help = "Get WSL equivalent(Windows only)" )
    P2.add_argument('-l' , '--lsw' , dest = 'type_' , action = 'store_const' , default = 'regular' , const = 'lsw' , help = "Convert WSL path to Windows equivalent.")

    P2.add_argument('-G' , '--reverse-gitbash' , dest = 'type_' , action = 'store_const' , default = 'regular' , const = 'rg' , help = "Reverse Gitbash path to windows path")



    ##Path type files

    pathtype_parser = parser.add_argument_group(title = "Pre-processing Options: " , description = "Pre processing the path to the realpath/abspath before proceeding")
    P3 = pathtype_parser.add_mutually_exclusive_group()


    P3.add_argument('-#' , '--NONE' , dest = 'driver' , action = 'store_const' , const = 'NONE' , default = 'ABS' ,
                    help = "Take the input path as is. Useful for conversion of WSL paths on Windows and such")

    P3.add_argument('-a' , '--abs' , '--abspath' , dest = 'driver' , action = 'store_const' , const = 'ABS' , default = 'ABS' ,
                    help = 'Get the absolute path. (DEFAULT)')


    P3.add_argument('-r' , '--realpath' , '--real-path' , dest = 'driver' , action = 'store_const' , const ='REAL' , default = 'ABS' ,
                    help = "Get realpath(traverse symlinks)")



    ##Output Type Flags
    final_parser = parser.add_argument_group(title = "Final Driver Options: " , description = "Final options for the obtained path")

    final_parser.add_argument('--no-copy' , action = 'store_false' , dest =  'copy_flag', help = "Does not copy final path to clipboard")
    final_parser.add_argument('--no-print' , action = 'store_false' , dest = 'print_flag' , help = "Does not print final path to stdout")

    final_parser.add_argument('-u' , '--url' , dest = 'url_flag' , action = 'store_true' , help = "Final path is made into URL instead of regular system path")
    final_parser.add_argument('-/' , '--/' , '--unix-slash' , dest = 'unix_slash' , action = 'store_true' ,
                        help = 'If switched, outputs all windows \\ as unix /')


    if args is None :
        return parser.parse_args()

    return parser.parse_args(args)

def reverse_chaeyoung(fpath):

    import Chaeyoung.Translation_Module as tm
    import Chaeyoung.chae_config as cfg

    tm.global_chaeyoung.load(cfg.DEFAULT_LINKER)
    header = tm.get_header()


    cfg.all_loaded_configs = [(name , alias , drive) for name , alias , drive in
                                                        zip(tm.global_chaeyoung.data['Name'], tm.global_chaeyoung.data['Alias'] , tm.global_chaeyoung.data[header])
                                                        if tm.isvalid(drive)    ]

    drive_vals = tm.get_drive(fpath)
    bs = '\\'

    return f"{{{drive_vals[0]}}}/{os.path.relpath(fpath , drive_vals[-1]).replace(bs , '/')}"

def rg_make(fpath):

    import ucopy.regex_content as ct

    path_dict = ct.converter(fpath , ct.GITBASH_SYNTAX)
    bs = '\\'

    return f'{path_dict["drive"].upper()}:\\{path_dict["relpath"].replace(bs , "/")}'

def gitbash_make(fpath):

    import ucopy.regex_content as ct

    path_dict = ct.converter(fpath , ct.WINDBLOWS_SYNTAX)
    bs = '\\'

    return f'/{path_dict["drive"].lower()}/{path_dict["relpath"].replace(bs , "/")}'

def wsl_make(fpath):

    import ucopy.regex_content as ct

    path_dict = ct.converter(fpath , ct.WINDBLOWS_SYNTAX)
    bs = '\\'

    return f'/mnt/{path_dict["drive"].lower()}/{path_dict["relpath"].replace(bs , "/")}'

def lsw_make(fpath):

    import ucopy.regex_content as ct

    path_dict = ct.converter(fpath , ct.WSL_SYNTAX)
    bs = '\\'

    return f'{path_dict["drive"].upper()}:\\{path_dict["relpath"].replace("/", bs )}'

def url_make(fpath):


    import urllib.parse

    fpath = fpath.lstrip('/').lstrip('\\')

    return 'file:///' + urllib.parse.quote(fpath)

def DriverMain(opts):

    if len(opts.filepath) == 0 :
        fpath = os.getcwd()
    else :
        fpath = opts.filepath[0]


    ##Get driver
    if opts.driver == 'NONE':
        pass
    elif opts.driver == 'REAL':
        fpath = os.path.realpath(fpath)
    elif opts.driver == 'ABS':
        fpath = os.path.abspath(fpath)

    ##Get Conversion
    if opts.type_ == 'regular':
        pass
    elif opts.type_ == 'gitbash':

        fpath = gitbash_make(fpath)
    elif opts.type_ == 'R_CHAE':

        fpath = reverse_chaeyoung(fpath)
    elif opts.type_ == 'wsl':
        #print("Got WSL" , end = '' , file = sys.stderr)
        fpath = wsl_make(fpath)

    elif opts.type_  == 'lsw':

        fpath = lsw_make(fpath)
    elif opts.type_ == 'rg':

        fpath = rg_make(fpath)

    if opts.unix_slash:
        fpath = fpath.replace('\\'  , '/')

    if opts.url_flag :

        if opts.type_ == "R_CHAE":

            import warnings
            warnings.warn("The URL conversion of Chaeyoung Header Paths is not an appropriate use case")


        fpath = url_make(fpath)

    if opts.copy_flag:

        import pyperclip
        pyperclip.copy(fpath)

    if opts.print_flag :

        print(fpath , end = '')

    return None


if __name__ == '__main__':

    import  pretty_traceback
    pretty_traceback.install()

    DriverMain(arguments())
