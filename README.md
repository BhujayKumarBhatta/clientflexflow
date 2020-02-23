# micros1-client 

python and cli client for accessing the api routes from micros1  micro service 

installation 
=====================================
    
    virtualenv -p python3 venv
    source venv/bin/activate
    pip install -r requirement.txt
    pip install invstore_client


  
alternate to run from source 

    git clone https://github.com/microservice-tsp-billing/micros1-client.git
    cd micros-client1
    virtualenv -p python3 venv
    source venv/bin/activate
	pip install -r requirements.txt

config
===============================================================
Follow readme for configuring the tokenleaderclient first - https://github.com/microservice-tsp-billing/tokenleaderclient
apart from the tokenleaderclient configuration  the following sections should be present in the /etc/tokenleader/client_configs.yml


	invstore_client:
	  url_type: endpoint_url_external
	  ssl_enabled: no
	  ssl_verify: no
  
  
hence the complete configuraion will look as:  


    user_auth_info_from: file # OSENV or file
	user_auth_info_file_location: /home/bhujay/tlclient/user_settings.ini
	fernet_key_file: /home/bhujay/tlclient/prod_farnetkeys	
	tl_public_key: ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCYV9y94je6Z9N0iarh0xNrE3IFGrdktV2TLfI5h60hfd9yO7L9BZtd94/r2L6VGFSwT/dhBR//CwkIuue3RW23nbm2OIYsmsijBSHtm1/2tw/0g0UbbneM9vFt9ciCjdq3W4VY8I6iQ7s7v98qrtRxhqLc/rH2MmfERhQaMQPaSnMaB59R46xCtCnsJ+OoZs5XhGOJXJz8YKuCw4gUs4soRMb7+k7F4wADseoYuwtVLoEmSC+ikbmPZNWOY18HxNrSVJOvMH2sCoewY6/GgS/5s1zlWBwV/F0UvmKoCTf0KcNHcdzXbeDU9/PkGU/uItRYVfXIWYJVQZBveu7BYJDR bhujay@DESKTOP-DTA1VEB
	tl_user: user1
	tl_url: http://localhost:5001
	ssl_verify: False	
	invstore_client:
	  url_type: endpoint_url_external
	  ssl_enabled: no
	  ssl_verify: no
 
consult with the tokenleader administrator  to replace the values in the above values :  

1. get the correct public key 
2. To register your username 
3. To assign a role
4. In the  micros1 server the role name to be mapped with the api route permission for the following 
  - tokenleader.adminops.adminops_restapi.list_users  
  - linkInventory.restapi.routes.get_links_rest
  - linkInventory.restapi.routes.get_link_by_slno
  - micros1.ms2app.restapi.firstapi.ep3
  - micros1.create_invoice
  - micros1.upload_excel
  - micros1.list_all
  - micros1.delete_all
  - micros1.update_invoice
  - micros1.recommend_change
  - micros1.accept_recom
  - micros1.approve_invoice
  - micros1.reject_invoice

5. user tokneleader get token to see the  service catalog and identify the correct url_type for micros1 which is reachable from your client 
 

PYTHON client
===================================

   flexflow
    ####################
    from tokenleaderclient.configs.config_handler import Configs
    from tokenleaderclient.client.client import Client
    cfg = Configs(tlusr='itssuser1', tlpwd='Itssuser1@123', domain='ITC')
    from clientflexflow.client import clientflexflow
    t = Client(cfg)
    t.get_token()
    c = clientflexflow(t)
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


    
output of list 
==========================

    [{'status': 'InfobahnRecommendedtoTSP', 'autochk': {'bom_comp_result': [], 'autocheck_status': 'Failed', 'lnet_status': 'No link in lnet by the infoops id S0000000001', 'inventory_status': 'No link in inventory by the infoops id S0000000001'}, 'xldata': {'premiseno': '52454', 'accountno': 'XDN038414', 'fullsiteaddress': 'This looks like a good address', 'remarks': 'OK', 'invoiceno': '1', 'gstno': 'None', 'circuitid': 'UploadCircuit', 'slno': 1, 'city': 'Gujrat', 'invoicedate': '15-03-2019', 'customername': 'ABC Limited', 'speed': 'INFOB recommending to tsp - 1st', 'action': 'InfobahnRecommendedtoTSP', 'premisename': '52454', 'servicetype': 'GXDN', 'billingdateto': '01-03-2019', 'arc': '2400', 'pin': 52454, 'infoid': 'S0000000001', 'division': 'POPCompany', 'billingdatefrom': '02-12-2018', 'customerid': 'XI000555', 'state': 'GG', 'taxname': 'USA SGST@9%+CGST@9%', 'tsp': 'TATA', 'total': 234455, 'siteid': '52454'}, 'invoiceno': '1'}]

listing single by invoice number 
============================================

    c.list_invoices('1')

    [{'status': 'InfobahnRecommendedtoTSP', 'autochk': {'bom_comp_result': [], 'autocheck_status': 'Failed', 'lnet_status': 'No link in lnet by the infoops id S0000000001', 'inventory_status': 'No link in inventory by the infoops id S0000000001'}, 'xldata': {'premiseno': '52454', 'accountno': 'XDN038414', 'fullsiteaddress': 'This looks like a good address', 'remarks': 'OK', 'invoiceno': '1', 'gstno': 'None', 'circuitid': 'UploadCircuit', 'slno': 1, 'city': 'Gujrat', 'invoicedate': '15-03-2019', 'customername': 'ABC Limited', 'speed': 'INFOB recommending to tsp - 1st', 'action': 'InfobahnRecommendedtoTSP', 'premisename': '52454', 'servicetype': 'GXDN', 'billingdateto': '01-03-2019', 'arc': '2400', 'pin': 52454, 'infoid': 'S0000000001', 'division': 'POPCompany', 'billingdatefrom': '02-12-2018', 'customerid': 'XI000555', 'state': 'GG', 'taxname': 'USA SGST@9%+CGST@9%', 'tsp': 'TATA', 'total': 234455, 'siteid': '52454'}, 'invoiceno': '1'}]

delete invoices
===================================================
>>> c.delete_invoices('1')

{'Failure': None}

>>> c.list_invoices('1')

[]







	