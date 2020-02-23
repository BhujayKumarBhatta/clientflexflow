#!./venv/bin/python

# -*- coding: utf-8 -*-

import os
import sys
import argparse


possible_topdir = os.path.normpath(os.path.join(os.path.abspath(sys.argv[0]),
                                                os.pardir,
                                                os.pardir))
                                                

# 
# if os.path.exists(os.path.join(possible_topdir,
#                                'app1',
#                                '__init__.py')):
apppath = (os.path.join(possible_topdir,
                               'clientpaperhouse',
                               'clientpaperhouse'))
#    sys.path.insert(0, apppath)

sys.path.insert(0, apppath)

#print(sys.path)

from tokenleaderclient.configs.config_handler import Configs    
from  tokenleaderclient.client.client import Client 
from micros2client.client   import MSClient

auth_config = Configs()
tlclient = Client(auth_config)
c = MSClient(tlclient)

parser = argparse.ArgumentParser(add_help=False)


subparser = parser.add_subparsers()

ep3_parser = subparser.add_parser('ep3', help="call the ep3 api route from microservice micros1")

upload_parser = subparser.add_parser('uploadxl', help='upload invoices from excel file')

upload_parser.add_argument('-f', '--file', action = "store", dest = "file",
                  required = True,
                  help = "full path of the excel file , the excel file must comply with the  "
                        " format as  described in the document of the microservice")

list_parser = subparser.add_parser('list', help='list previously uploaded  invoices from excel dump database')

list_parser.add_argument('-k', '--keyname', action = "store", dest = "keyname",
                  required = True,
                  help = "name of the excel column heading that will be used for querying the value, "
                  "type 'all' to  bypass this filter")

list_parser.add_argument('-v', '--value', action = "store", dest = "value",
                  required = True,
                  help = "some value ( text or number)  for the key choosen with -k option "
                          "  based on which the search can be filtered"
                          " type 'all' to  bypass this filter")

list_parser.add_argument('-l', '--level', action = "store", dest = "level",
                  required = False,
                  help = "some value ( text or number)  for the key choosen with -k option "
                          "  based on which the search can be filtered"
                          " type 'all' to  bypass this filter")

update_parser = subparser.add_parser('update', help='update invoices from excel file')

update_parser.add_argument('-f', '--file', action = "store", dest = "file",
                  required = True,
                  help = "full path of the excel file , the excel file must comply with the  "
                        " format as  described in the document of the microservice")


delete_parser = subparser.add_parser('delete', help='delete previously uploaded  invoices from excel dump database')

delete_parser.add_argument('-i', '--invoiceno', action = "store", dest = "invoiceno",
                  required = True,
                  help = "invoice number to delete , or type 'all' to delete all invoices")
                        

try:                    
    options = parser.parse_args()  
except:
    #print usage help when no argument is provided
    parser.print_help(sys.stderr)    
    sys.exit(1)

def main():
    if len(sys.argv)==1:
        # display help message when no args are passed.
        parser.print_help()
        sys.exit(1)   
   
    #print(sys.argv)
    
    if  sys.argv[1] == 'ep3':
        print(c.ep3()) 
        
    if sys.argv[1] == 'uploadxl':
        r = c.upload_xl(options.file)
        print(r)
        
    if sys.argv[1] == 'list':
        if options.level:
            r = c.list_invoices(options.keyname, options.value, options.level)
        else:
            r = c.list_invoices_clo(options.keyname, options.value)
        print(r)
        
    if sys.argv[1] == 'update':
        r = c.update_invoice(options.file)
        print(r)
        
    if sys.argv[1] == 'delete':
        r = c.delete_invoices(options.invoiceno)
        print(r)
            
                    
     
    
if __name__ == '__main__':
    main()
    

    
    
