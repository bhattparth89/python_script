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
    db = '14th-SEPT-2019-Fresh-Master'
    username = 'admin'
    password = '@123admin'
    
    description = ""
    client = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url));
    print(client.version())

    uid = client.authenticate(db, username, password, {})
    print(uid)

    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    models.execute_kw(db, uid, password,
        'op.student', 'check_access_rights',
        ['read'], {'raise_exception': False})

    #transport root serch
    tran_root_ids = models.execute_kw(db, uid, password,
        'student.transport', 'search',[[]])
    tran_root_idarray = []
    tran_root_idarray.append(tran_root_ids)
    
    #transport point serch
    tran_point_ids = models.execute_kw(db, uid, password,
        'transport.point', 'search',[[]])
    tran_point_idarray = []
    tran_point_idarray.append(tran_point_ids)
    
    #transport student search
    op_stud_ids = models.execute_kw(db, uid, password,
        'op.student', 'search',[[]])
    op_stud_idarray = []
    op_stud_idarray.append(op_stud_ids)
    
      #transport vehicle search
    tran_vehi_ids = models.execute_kw(db, uid, password,
        'transport.vehicle', 'search',[[]])
    tran_vehi_idarray = []
    tran_vehi_idarray.append(tran_vehi_ids)
    
    
      
    #transport root read
    root_record = models.execute_kw(db, uid, password,
        'student.transport', 'read', tran_root_idarray)
    print("root_record")
    print(len(root_record))
    
    #transport point read
    point_record = models.execute_kw(db, uid, password,
        'transport.point', 'read', tran_point_idarray)
    print("point_record")
    print(len(point_record))
    
    #transport Student read
    student_record = models.execute_kw(db, uid, password,
        'op.student', 'read', op_stud_idarray)
    print("student_record")
    print(len(student_record))
    
    #transport vehicle read
    vehicle_record = models.execute_kw(db, uid, password,
        'transport.vehicle', 'read', tran_vehi_idarray)
    print("vehicle_record")
    print(len(vehicle_record))

   
    
    # -----------------add read list in dict-------------------------
    
    """# add attribute lines to dict
    dict_atttribute_lines = {}
    if len(attribute_lines_record)>0:
        for reco in attribute_lines_record:
            dict_atttribute_lines.setdefault(reco.get("attribute_id")[0],{'id':reco.get("id"),'value_ids':reco.get("value_ids")})
            #print(reco.get("display_name"),dict_atttribute_lines)"""
    
    
    # add student name to dict
    dict_stud_name_list = {}
    if len(student_record)>0:
        for stud in student_record:
            dict_stud_name_list.setdefault(stud.get("old_stud_id"),stud.get("standard_id"))
    
    # add root name to dict
    dict_root_name_list = {}
    if len(root_record)>0:
        for root in root_record:
            dict_root_name_list.setdefault(root.get("name"),root.get("id"))
    
    # add point to dict
    dict_point_name_list = {}
    if len(point_record)>0:
        for point in point_record:
            dict_point_name_list.setdefault(point.get("name"),{'id':point.get("id"),'amount':{point.get("m_amount")}})
            print("dict_point_name_list")
            
    # add vehicle to dict
    dict_vehicle_name_list = {}
    if len(vehicle_record)>0:
        for vehi in vehicle_record:
            dict_vehicle_name_list.setdefault(vehi.get("vehicle"),vehi.get("id"))
            print("dict_vehicle_name_list")
            
    """# add attribute to dict
    dict_attribute = {}
    if len(attribute_record)>0:
        for attr in attribute_record:
            dict_attribute.setdefault(attr.get("name"),{'id':attr.get("id"),'value_ids':{}})
            print("values of ids",attr.get("value_ids"))"""

    """# add product of to dict
    dict_product_of = {}
    if len(product_of_record)>0:
        for med_type in product_of_record:
            dict_product_of.setdefault(med_type.get("display_name"),med_type.get("id"))
    
    # add medicine type to dict
    dict_medicine_type = {}
    if len(medicine_types_record)>0:
        for med_type in medicine_types_record:
            dict_medicine_type.setdefault(med_type.get("display_name"),med_type.get("id"))

    # add attribute to dict
    dict_attribute = {}
    if len(attribute_record)>0:
        for attr in attribute_record:
            dict_attribute.setdefault(attr.get("name"),{'id':attr.get("id"),'value_ids':{}})
            print("values of ids",attr.get("value_ids"))
            
    # add attribute value to dict
    dict_attribute_value = {}
    if len(attribute_values_record)>0:
        for attr_value in attribute_values_record:
            attribute_name =  attr_value.get("attribute_id")[1]
            attr_dict_val_name = dict_attribute[attribute_name]['value_ids']
            attr_dict_val_name.setdefault( attr_value.get("name") , attr_value.get("id") )
   
    print(dict_attribute) 
    
    #sys.exit()
    # add res partner to dict
    dict_company = {}
    if len(company_record)>0:
        for comp in company_record:
            dict_company.setdefault(comp.get("name"),comp.get("id")) """

    #------------------------------ function to create product --------------------------
    
    @classmethod
    def createParticipant(self,row):
        
        id = self.models.execute_kw(self.db, self.uid, self.password,
                    'transport.registration',
                    'create', [{
                    'part_name': row[1],
                    'name': row[2],
                    'vehicle_id': (row[3]),
                    'point_id' : (row[4]),
                    'for_month': (row[6]),
                    }])
        self.description = ""
        
        id = self.models.execute_kw(self.db, self.uid, self.password,
                    'transport.registration',
                    'write',[[id], {
                    'attribute_line_ids': [[6,0,self.checkAttributeLine(row,id)]],
                    }])
        
  
    @classmethod    
    def checkMedicineType(self,row):
        is_medicine_type_present = False
        med_type_id = 0
        for key,value in self.dict_medicine_type.items() :
            if key == row[6] : 
                is_medicine_type_present = True
                med_type_id = int(value)
                break
                
        if is_medicine_type_present :
            return med_type_id
        else:
            med_type_id = self.models.execute_kw(self.db, self.uid, self.password,
                    'product.medicine.types',
                    'create', [{
                    'medicine_type': row[6],
                    'display_name': row[6],
                    }])
            if med_type_id > 0 :
                self.dict_medicine_type.setdefault(row[6],med_type_id)
            return med_type_id
            
    @classmethod    
    def checkProductOf(self,row):
        is_product_of_present = False
        prod_of_id = 0
        for key,value in self.dict_product_of.items():
            if key == row[7] :
                is_product_of_present = True
                prod_of_id = int(value)
                break
        
        if is_product_of_present :
            return prod_of_id
        else :
            prod_of_id = self.models.execute_kw(self.db, self.uid, self.password,
                    'product.medicine.responsible',
                    'create', [{
                    'name_responsible': row[7],
                    'display_name': row[7],
                    'related_vendor' : self.checkPartner(row),
                    }])
            if prod_of_id > 0 :
                self.dict_product_of.setdefault(row[7],prod_of_id)
            return prod_of_id
            
    @classmethod        
    def checkPartner(self,row):
        is_partner_present = False
        partner_id = 0
        for key,value in self.dict_company.items():
            if key == row[7] :
                is_partner_present = True
                partner_id = value
                break
        
        if is_partner_present :
            return partner_id
        else:
            partner_id = self.models.execute_kw(self.db, self.uid, self.password,
                    'res.partner',
                    'create', [{
                    'name': row[7],
                    'display_name': row[7],
                    'customer' : False,
                    'supplier' : True,
                    'is_company' : True,
                }])
            if partner_id > 0 :
                self.dict_company.setdefault(row[7],partner_id)
            return partner_id
            
    @classmethod
    def checkAttribute(self,attrname):
        is_attribute_present = False
        attribute_id = 0
        for key,value in self.dict_attribute.items():
            if key == attrname :
                is_attribute_present = True
                attribute_id = int(value['id'])
                break
        if is_attribute_present :
            return attribute_id
        else:
            attribute_id = self.models.execute_kw(self.db, self.uid, self.password,
                    'product.attribute',
                    'create', [{
                    'name': attrname,
                    'display_name': attrname,
                }])
            if attribute_id > 0:
                j = {}
                self.dict_attribute.setdefault(attrname,{'id':attribute_id,'value_ids':j})
            return attribute_id
            
    @classmethod
    def checkAttributeValue(self,attrvalues,attr_id,attrName):
        attr_value_list = []
        print("attr values ",attrvalues)
        for attrvalue in attrvalues:
            is_attribute_value_present = False
            attribute_value_id = 0
                        
            for key,value in self.dict_attribute.get(attrName)['value_ids'].items() :
                if key == attrvalue :
                    is_attribute_value_present = True
                    attribute_value_id = value
                    break
            if is_attribute_value_present :
                attr_value_list.append(attribute_value_id)
            else:
                attribute_value_id = self.models.execute_kw(self.db, self.uid, self.password,
                        'product.attribute.value',
                        'create', [{
                        'name': attrvalue,
                        'display_name': attrvalue,
                        'attribute_id': int(attr_id),
                    }])
                if attribute_value_id > 0:
                    print(attrvalue,attr_id,attribute_value_id)
                    #self.dict_attribute_value.setdefault(attribute_value_id,{'attribute_id':attr_id,'name': attrvalue})
                    dict_new_value = self.dict_attribute[attrName]['value_ids']
                    dict_new_value.setdefault(attrvalue,attribute_value_id)
                attr_value_list.append(attribute_value_id)
        return attr_value_list
        
    @classmethod
    def checkDescription(self,row):
        a= []
        description=""
        if "," in row[2] :
            a = row[2].split(",")
        elif "+" in row[2] :
            a = row[2].split("+")
        else : 
            a= row[2].split(",")
        
        for string in a :
            if "Each " in string:
                description = string
                continue
                
        return description
        
    @classmethod
    def checkAttributeLine(self,row,prod_id):
        regex = "\d+&\d+[ ]MG|\d+[ ]mg/+\d+ml|\d+[ ]mg/ml|\d+[ ]mg|\d+ML|\d+[.]+\d+[/]+\d+ml|\d+[/]+\d+ml|\d+[.]+\d+[ ]ml/+\d+ml|\d+[ ]ml|\d+ml|\d+mg[/]+\d+ml|\d+[.]+\d+mg[/]+\d+|\d+[.]+\d+mg[/]+\d+ml|\d+[.]+\d+ml|\d+[ ]Mg|\d+mg[/]ml|\d+[.]+\d+mg[/]ml|\d+mg/+\d+ML|\d+mg|\d+[.]+\d+[ ]mg/+\d+ml|\d+[.]+\d+[ ]mg|\d+Mg|\d+MG|\d+[.]+\d+[ ]MG|\d+[ ]MG|\d+[.]+\d+mcg|\d+[ ]MCG|\d+[ ]mcg|\d+mcg/+\d+ml|\d+mcg|\d+gm[/]+\d+ml|\d+gm|\d+GM|\d+[ ]gm|\d+[.]+\d+mg|\d+[.]+\d+gm|\d+[.]+\d+[ ]gm|\d+[.]+\d+gs|\d+[.]+\d+g|\d+[.]+\d+[ ]+kcal|\d+[.]+\d+kcal|\d+[.]+\d+[ ]Kcal|\d+[ ]Kcal|\d+[.]+\d+Kcal|\d+Kcal|\d+[ ]SR|\d+DT|\d+[.]+\d+[%]+[ ]w/v|\d+[.]+\d+w/v|\d+[.]+\d+[%]+[ ]W/V|\d+[.]+\d+[%]+[ ]W/|\d+m|\d+[%]+[ ]w/v|\d+[.]+\d+[%]+[ ]w/w|\d+[.]+\d+[%]+w/w|\d+[%]+w/v|\d+[% ]+v|\d+[.]+\d+[%]+v/v|\d+[.]+\d+[%]+w/w|\d+[%]+w/w|\d+[%]+[ ]w/w|\d+[.]+\d+[ ][%]|\d+[ ][%]|\d+[%]|\d+[.]+\d+[%]|\d+[ ]IU|\d+ms|\d+iu"
        stringAttrName = "n/a"
        stringAttrValueName = "n/a"
        attribute_line_ids_list = []
        attribute_id = 0
        attribute_value_ids = []
        is_attribute_line_present = False
        attribute_line_id = 0
        
        a= []
        if "," in row[2] :
            a = row[2].split(",")
        elif "+" in row[2] :
            a = row[2].split("+")
        else : 
            a= row[2].split(",")
        
        for string in a :
            if "Each " in string:
                self.description = string
                continue
                
            stringAttrName = "n/a"
            stringAttrValueName = "n/a"
            val_list = re.findall(regex,string)
            if len(val_list)>0:
                stringAttrName = string.replace(val_list[0],"")
                stringAttrName = stringAttrName.strip()
                stringAttrName = stringAttrName.strip()
                if "." in stringAttrName:
                    stringAttrName = stringAttrName.replace(".","")
                elif "-" in stringAttrName[len(stringAttrName)-1]:
                    stringAttrName = stringAttrName.replace("-","")
                stringAttrValueName = val_list[0].strip()
            else:
                stringAttrName = string
            
            # will go in function to check and if need will create the attribute
            attribute_id = self.checkAttribute(stringAttrName)
            print(stringAttrName)
            attribute_value_ids = self.checkAttributeValue([stringAttrValueName],attribute_id,stringAttrName)
            
            for key,value in self.dict_atttribute_lines.items():         
                if key == attribute_id and value['value_ids'] == attribute_value_ids :
                    is_attribute_line_present = True
                    attribute_line_id = int(value['id'])
                    break
                    
            if is_attribute_line_present :
                attribute_line_ids_list.append(attribute_line_id)
            else :
                attribute_line_id = self.models.execute_kw(self.db, self.uid, self.password,
                        'product.attribute.line',
                        'create', [{
                        'display_name': stringAttrName,
                        'attribute_id': attribute_id,
                        'product_tmpl_id': prod_id,
                        'value_ids': [[6,0,attribute_value_ids]],
                    }])
                attribute_line_ids_list.append(attribute_line_id)
        print(attribute_line_ids_list)
        return attribute_line_ids_list
   #--------------------------------------- read the csv file---------------------------------------------------------


with open(r'C:\Users\Administrator\Desktop\SCHOOL 20-AUG-2019\STD_CSV_UPLD\Transport_Details_CSV.csv ', newline='') as f:
    reader = csv.reader(f)
    duplicate_list = []
    i = 0
    for row in reader:
        if len(row[1]) > 0 :
           uploadtransport.createParticipant(row)


        #for key,value in dict_company.items():
                #print(key,value)
        #for key,value in dict_attribute.items():
            #print(key,value) 
        
            
            #id = models.execute_kw(db, uid, password, 'product.attribute', 'create', [{'name': row[1],}])
            #models.execute_kw(db,uid,password,'product.template','write',{'active':True})
                #if id > 0 :
                #    i= i+1
                #    print("product created successfully"+row[1])
                #    product_name_list.append(row[1])
                #else:
                #print("error while creating product")
        #print("product created")
        #print(i)
    #print("record "+record)
    #print("length of record = "+len(record))

    #id = models.execute_kw(db, uid, password, 'product.template', 'create', [{
    #    'name': "pranita",
    #}])
    #print(id)

