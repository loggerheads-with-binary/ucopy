import re

GITBASH_SYNTAX      =   {"reg_expression" : re.compile(r"^/(?P<drive>[A-Z|a-z])/(?P<relpath>.*)$" , re.UNICODE)  ,          "utility" : "GitBash for Windows"}
WSL_SYNTAX          =   {"reg_expression" : re.compile(r"^/mnt/(?P<drive>[A-Z|a-z])/(?P<relpath>.*)$" , re.UNICODE)  ,      "utility" : "Windows Subsystem for Linux"}
LOONIX_SYNTAX       =   {"reg_expression" : re.compile(r"^(?P<relpath>/.*)(?P<basename>[^/]*)/?$" , re.UNICODE)  ,          "utility" : "Unix based"}
WINDBLOWS_SYNTAX    =   {"reg_expression" : re.compile(r"^(?P<drive>[A-Z|a-z]):[\\|/]?(?P<relpath>.*)$" , re.UNICODE),       "utility" : "Windows NT"}


def converter(fpath , syntax):

    if syntax["reg_expression"].match(fpath) is None :

        raise ValueError(f"Given path `{fpath}` is not a valid `{syntax['utility']}` path")

    return syntax["reg_expression"].search(fpath).groupdict()
