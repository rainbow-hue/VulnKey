import xss_scanner
import keylogger
import sys
import getopt

argument_list = sys.argv[1:]
options = "hkxf:e:u:"
long_options = ["help","kelogger","xss-scanner","file","email","url"]

try:
    arguments, values = getopt.getopt(argument_list, options, long_options)

    for currentArgument, currentValue in arguments:
                if currentArgument in ("-h","--help"):
                    print("                  VulnKey         \n")
                    print("-k or --keylogger    -      for keylogger")
                    print("-x or --xss-scanner  -      for xss scanner")
                    print("\nFor the help menu of respective programs, add -h, Example: python vulnkey.py -k -h")
                    print("Example commands: python vulnkey.py -x -h")
                    print("Example commands: python vulnkey.py -xss-scanner -u [url]")
                    print("Example commands: python vulnkey.py -keylogger -e [email]")
                    exit()

                if currentArgument in ("-k", "--keylogger"):
                    keylogger = keylogger.Keylogger()
                    keylogger.start()

                if currentArgument in ("-x","--xss-scanner"):
                    scanner = xss_scanner.Scanner()
                    scanner.run()
except getopt.error as err:
    print(str(err))
    exit()

                    
