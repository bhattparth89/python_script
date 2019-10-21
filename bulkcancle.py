 
 
 # cancle# -*- codng: utf-8 -*-
import logging
import csv
import re
import xmlrpc
_logger = logging.getLogger(__name__)
from xmlrpc import client
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xmlrpc.client
import sys

class CancleInvoice(object):
        
    url = 'http://localhost:8069'
    db = 'SHVOV-15-10-19'
    username = 'admin'
    password = '@123admin'
    
    description = ""
    client = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url));
    print(client.version())

    uid = client.authenticate(db, username, password, {})
    print(uid)
    
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
   
    #search in account invoice for partner
    invc_partner_list = models.execute_kw(db, uid, password, 'account.invoice','search',[[['standard_id', 'in', ['VI','VII','VIII','IX','X']],['is_fee','=',True],['state','=','open']]])
    invc_idarray = []
    invc_idarray.append(invc_partner_list)
    _logger.error("invc method called")
    
    #read invc partner data
    invc_partner_record = models.execute_kw(db, uid, password, 'account.invoice','read', invc_idarray)
    print("Partner")
    print(len(invc_partner_record))
    _logger.error("invc read method called")

    #add details in dict
    reco = {}
    ids = []
    nums = []
    #if len(invc_partner_record)>0:
    for reco in invc_partner_record:
        if reco.get("amount_total") == reco.get("residual"):
            state = models.exec_workflow(db, uid, password, 'account.invoice', 'invoice_cancel', reco.get("id"))
            if state == True:
                print("cancelled %s",reco.get("number"))
            else:
                print("not cancelled %s", state)
            ids.append(reco.get("id"))
            nums.append(reco.get("number"))
    print("inv numbers that are cancelled : %s",nums)
    