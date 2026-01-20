import requests
import hashlib 
import time 
import json 
import re 

class WISEIOBox():

    def __init__(self, URL, u = 'root', p = '00000000'):
        self.IOURL = URL; #provide URL with :80 port
        self.u = u;
        self.p = p;
        self.loginEndpoint =  '/config/index.html';
        self.doEndpoint = '/do_value/slot_0';
        self.diEndpoint = '/di_value/slot_0';
        self.seedData = '';

    def setUser(self, u):
        self.u = u;
    
    def setPass(self, p):
        self.p = p;
    
    def login(self):
        res = requests.get(self.IOURL + self.loginEndpoint);
        print('module response: ');
        print(res.reason);
        pattern = r'[0-9A-F]{8}'; 
        self.seedData = re.findall(pattern, str(res.content))[0];
        loginString = self.seedData + ':' + self.u + ':' + self.p;
        authdata = hashlib.md5(loginString.encode());
        self.loginString = 'seeddata=' + self.seedData + '&authdata=' + str(authdata.hexdigest());
        loginHeader = {'Content-Length': str(len(loginString))};
        print('attempting login with ' + loginString);
        self.loginData = requests.post( self.IOURL + self.loginEndpoint, 
                                        headers = loginHeader, 
                                        data = self.loginString,
                                        );
        
    def getDI(self, di_num):
        res = requests.get(self.IOURL + self.diEndpoint, 
                       cookies = self.loginData.cookies, 
                       data = self.loginString,
                       headers = {});
        diStruct = json.loads(res.content);
        return diStruct['DIVal'][di_num]['Val'];

    def getDO(self, do_num):
        res = requests.get(self.IOURL + self.doEndpoint, 
                       cookies = self.loginData.cookies, 
                       data = self.loginString,
                       headers = {});
        diStruct = json.loads(res.content);
        return diStruct['DOVal'][do_num]['Val'];

    def setDO(self, do_num, state):
        print(self.IOURL + self.doEndpoint);
        payload = '{\"DOVal\":[{\"Ch\":' + str(do_num) + ',\"Val\":' + str(state) + '}]}';
        print('sending payload:');
        print(payload);
        h = {'Content-Length': str(len(payload))};
        res = requests.patch(self.IOURL + self.doEndpoint,
                             cookies = self.loginData.cookies, 
                             data = payload,
                             headers = h);
        return res;
        
    

