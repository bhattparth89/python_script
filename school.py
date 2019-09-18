# -*- codng: utf-8 -*-
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

class uploadtransport(object):
        
    url = 'http://localhost:8069'
    db = 'livedb'
    username = 'admin'
    password = '@123admin'
    
    description = ""
    client = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url));
    print(client.version())

    uid = client.authenticate(db, username, password, {})
    print(uid)

    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    
    @classmethod
    def createReg(self,stud_id,start_date,time,end_date,point_name,root_name,vehicle_name):
        trans_regis_object = self.models.execute_kw(self.db, self.uid, self.password,
            'transport.registration', 'create_bulk_reg',
            [stud_id,start_date,time,end_date,point_name,root_name,vehicle_name])
        if trans_regis_object > 0 :
            print(stud_id, 'created' )
        else:
            print(stud_id ,'not created' )


with open(r'C:\Users\user\Desktop\school transport\Transport_Details_CSV.csv ', newline='') as f:
    reader = csv.reader(f)
    duplicate_list = []
    i = 0
    for row in reader:
        if len(row[1]) > 0 :
            uploadtransport.createReg(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
