import os
import requests
import json
import jwt

# from tokenleaderclient.client.client import Client as tlClient
from clientflexflow.configs.config_handler import Configs as MSConfig

# must_have_keys_in_yml_for_ms1c = {
#                                   'url_type',
#                                   'ssl_enabled',
#                                   'ssl_verify'                            
#                                  }   

service_name = 'flexflow'
conf_file='/etc/tokenleader/client_configs.yml'

must_have_keys_in_yml = {}   

conf = MSConfig(service_name, conf_file=conf_file, must_have_keys_in_yml= must_have_keys_in_yml)

clientflexflow_yml = conf.yml.get(service_name)
   

class clientflexflow():   
    '''
    First initialize an instance of tokenleader client and  pass it to clientpaperhouse 
    as its parameter
    
    flexflow
    ####################
    from tokenleaderclient.configs.config_handler import Configs
    from tokenleaderclient.client.client import Client
    cfg = Configs(tlusr='itssuser1', tlpwd='Itssuser1@123', domain='ITC')
    from clientflexflow.client import clientflexflow
    t = Client(cfg)
    t.get_token()
    c = clientflexflow(t)
    c.get_wfmobj_keys('Wfstats')
    #['name']
    data= [{"name": "ABC"}]
    c.add_wfmasterObj('Wfstatus', data)
    #{'message': 'has been registered', 'status': 'success'}
    c.list_wfmasterObj('Wfstatus')
    #[{'name': 'ABC'}]
    c.list_wfmasterObj('Wfstatus', {"name": 'ABC'})
    #[{'name': 'ABC'}]
    data_dict = {"update_data_dict": {"name": "DEF"},
                         "search_filter": {"name": "ABC"}
                         }
                         
    
    c.update_wfmasterObj('Wfstatus', data_dict) 
    #{'message': "updated the follwoing ['name attribute from current value ABC to  DEF']", 'status': 'success'}
    filter_data = {"name": "DEF"}
    c.delete_wfmasterObj('Wfstatus', filter_data)
    #"{'name': 'DEF'} has been  deleted successfully"
    '''
    
    def __init__(self, tlClient ):       
        
        self.tlClient = tlClient
        self.url_type = clientflexflow_yml.get('url_type')
        self.ssl_enabled = clientflexflow_yml.get('ssl_verify')
        self.ssl_verify = clientflexflow_yml.get('ssl_verify')
#         self.url_to_connect = self.get_url_to_connect()
#         
    
    ################# clientpaperhouse routes   ##############################################
    
    def get_wfmobj_keys(self, objname):
        api_route = '/get_wfmobj_keys/{}'.format(objname)
        return self.get_request(api_route)
    
    def add_wfmasterObj(self, objname, data:dict):
        api_route = '/add/{}'.format(objname)
        result = self.post_request(api_route, data)
        return result
       
    def list_wfmasterObj(self, objname, filter={}):
        '''instead of GET it is a POST request because with post we can send multiple keys as filter, whereas with get we can pass only a single key and value'''
        api_route = '/list/{}'.format(objname)
        result = self.post_request(api_route, filter)
        return result
    
    def list_wfmasterObj_by_key_val(self, objname, key, val):
        '''instead of GET it is a POST request because with post we can send multiple keys as filter, whereas with get we can pass only a single key and value'''
        api_route = '/list/{}/{}/{}'.format(objname, key,val)
        result_lst = self.get_request(api_route)
        return result_lst[0]
    
    def update_wfmasterObj(self, objname, data:dict):
        ''' data_dict = {"update_data_dict": {"name": "DEF"},
                     "search_filter": {"name": "ABC"}
                     }
        c.update_wfmasterObj('Wfstatus', data_dict) 
        #{'message': "updated the follwoing ['name attribute from current value ABC to  DEF']", 'status': 'success'}

        SAFE : if no search_filter is provided first records found is only updated '''
        api_route = '/update/{}'.format(objname)
        result = self.put_request(api_route, data)
        return result
    
    def delete_wfmasterObj(self, objname, filter):
        '''
        filter_data = {"name": "DEF"}
        c.delete_wfmasterObj('Wfstatus', filter_data)
        #"{'name': 'DEF'} has been  deleted successfully"

        filter must be provided to avoid accidental delete all'''
        api_route = '/delete/{}'.format(objname)
        result = self.post_request(api_route, filter)
        return result
    
    def delete_wfmasterObj_by_name(self, objname, filter):
        '''
        filter_data = {"name": "DEF"}
        c.delete_wfmasterObj('Wfstatus', filter_data)
        #"{'name': 'DEF'} has been  deleted successfully"

        filter must be provided to avoid accidental delete all'''
        api_route = '/delete_by_name/{}/{}'.format(objname, filter)
        result = self.delete_request(api_route)
        return result

   
        
    ################# clientpaperhouse routes   ##############################################
    
           
    def get_service_ep_n_auth_header(self, api_route, service_name=service_name):
        ''' url to connect method was not caturing the exception when service enfpoint
        construction fails for non availability of tokenleader. Also there  call to 
        tokenleader used to be  twice. This code will correct the above issues but need to 
        be tested'''       
        url_to_connect = None
        try:
            all_data_token = self.tlClient.get_token()
            auth_token = all_data_token.get('auth_token')
            headers_v={'X-Auth-Token': auth_token}
            catalogue = all_data_token.get('service_catalog')            
            api_route = api_route            
        #print(catalogue)
            if catalogue.get(service_name):
                #print(catalogue.get(service_name))
                url_to_connect = catalogue[service_name][self.url_type]
                service_endpoint_v = url_to_connect + api_route
            else:
                msg = ("{} is not found in the service catalogue, ask the administrator"
                       " to register it in tokenleader".format(service_name))
                print(msg)
        except:
            print("could not retrieve service_catalog from token leader," 
                  " is token leaader service running ?"
                  " is tokenleader reachable from this server/container ??")
        return service_endpoint_v,  headers_v
    
    
    def handle_response(self, return_response):
        try:
            r_dict = json.loads(return_response.content.decode())
        except Exception as e:
            r_dict = {"Content returned by the server is not json serializable"
                    " checking the server log  might  help. "
                    " the text returned by the server is {}".format(
                        return_response.text)}
        return r_dict
        
        
    def post_request(self , api_route, data):        
        service_ep, headers = self.get_service_ep_n_auth_header(api_route)
        headers.update({'content-type':'application/json'})
        try:  
            r = requests.post(service_ep, 
                             headers=headers, 
                             data = json.dumps(data),                             
                            verify=self.ssl_verify)
            r_dict = self.handle_response(r)               
        except Exception as e:
            r_dict = {'error': 'could not connect to server , the error is {}'.format(e)}    #     
            print(r_dict)
#         print(r)  # for displaying from the cli  print in cli parser
        return r_dict
    
    
    def put_request(self , api_route, data):        
        service_ep, headers = self.get_service_ep_n_auth_header(api_route)
        headers.update({'content-type':'application/json'})
        try:  
            r = requests.put(service_ep, 
                             headers=headers, 
                             data = json.dumps(data),                             
                            verify=self.ssl_verify)
            r_dict = self.handle_response(r)                
        except Exception as e:
            r_dict = {'error': 'could not connect to server , the error is {}'.format(e)}    #     
            print(r_dict)
        return r_dict
    
    
    def delete_request_post(self, api_route, filter:dict ):
        service_ep, headers = self.get_service_ep_n_auth_header(api_route)
        try:  
            r = requests.delete(service_ep, 
                                headers=headers,
                                data = json.dumps(filter),
                                verify=self.ssl_verify,                                 
                                )           
        except Exception as e:
            r_dict = {'error': 'could not connect to server , the error is {}'.format(e)}
            print(r_dict)
        r_dict = self.handle_response(r)        
        return r_dict
    
    def delete_request(self, api_route):
        service_ep, headers = self.get_service_ep_n_auth_header(api_route)
        try:  
            r = requests.delete(service_ep, 
                                headers=headers,
                                verify=self.ssl_verify,                                 
                                )           
        except Exception as e:
            r_dict = {'error': 'could not connect to server , the error is {}'.format(e)}
            print(r_dict)
        r_dict = self.handle_response(r)        
        return r_dict
    
    
    def get_request(self, api_route):
        service_ep, headers = self.get_service_ep_n_auth_header(api_route)
        try:  
            r = requests.get(service_ep, headers=headers, verify=self.ssl_verify)            
        except Exception as e:
            r_dict = {'error': 'could not connect to server , the error is {}'.format(e)}
        r_dict = self.handle_response(r) 
        return r_dict
    
    
    def file_request_put(self, api_route, filepath):
            service_endpoint, headers = self.get_service_ep_n_auth_header(api_route)
            print(service_endpoint, headers)
            files = {'file': ( os.path.basename(filepath), 
                              open(filepath, 'rb'), 
                              'application/vnd.ms-excel', 
                              {'Expires': '0'})}
            try:              
                r = requests.put(service_endpoint, headers=headers, 
                                 files=files, verify=self.ssl_verify)
                r_dict = self.handle_response(r)               
            except Exception as e:
                r_dict = {'error': 'could not connect to server , the error is {}'.format(e)} 
            
            return r_dict
        
    def file_request_post(self, api_route, filepath):
            service_endpoint, headers = self.get_service_ep_n_auth_header(api_route)
            print(service_endpoint, headers)
            files = {'file': ( os.path.basename(filepath), 
                              open(filepath, 'rb'), 
                              'application/vnd.ms-excel', 
                              {'Expires': '0'})}
            try:              
                r = requests.post(service_endpoint, headers=headers, 
                                 files=files, verify=self.ssl_verify)
                r_dict = self.handle_response(r)               
            except Exception as e:
                r_dict = {'error': 'could not connect to server , the error is {}'.format(e)} 
            
            return r_dict
    
    
    
    
    