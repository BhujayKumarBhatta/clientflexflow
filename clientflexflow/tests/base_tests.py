import os
import json
import unittest

from tokenleaderclient.configs.config_handler import Configs    
from  tokenleaderclient.client.client import Client 
from micros2client.client   import MSClient
auth_config = Configs()
tlclient = Client(auth_config)
c = MSClient(tlclient)

class TestMclient(unittest.TestCase): 
        
    def test_save_tsprec(self):        
        with open('../invstore_client/invstore_client/tests/testdata/list_datarec.json') as f:
            l = json.load(f)
            r = c.save_tesprec(l)
            print(r)
            
            

    
