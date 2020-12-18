import requests as r
import json
import re
import random
import string


class NADA:  # getnada.com
    mainurl = 'https://getnada.com/api/v1/'
    domains = ['abyssmail.com', 'boximail.com', 'clrmail.com', 'dropjar.com', 'getairmail.com', 'givmail.com',
               'inboxbear.com', 'robot-mail.com', 'tafmail.com', 'vomoto.com', 'zetmail.com']  # Mail domains

    def randomString(self, stringLength=10):  # Random string generator
        letters = 'abcdefghijklmnopqrstuvwxyz'
        return ''.join([random.choice(letters) for n in range(stringLength)])

    def __init__(self, email=None, domain=None):
        self.sess = r.Session()
        self.email = None
        self.messinfo = []
        if domain != None and 0 <= domain <= 11:
            if email != None and email != '':
                if '@' in email:
                    email = email.split('@')[0]
                self.email = email + '@' + self.domains[domain]  # If domain AND email are set
            else:
                self.email = self.randomString() + '@' + self.domains[domain]  # If only domain isset
        else:
            if email != None and email != '':
                if '@' in email:
                    email = email.split('@')[0]
                self.email = email + '@' + random.choice(self.domains)  # If only email isset
            else:
                self.email = self.randomString() + '@' + random.choice(self.domains)  # If nothing isset

    def newEmail(self):
        self.sess = r.Session()
        self.email = None
        self.messinfo = []
        self.email = self.randomString() + '@' + random.choice(self.domains)

    def setEmail(self, email, domain=None):
        self.sess = r.Session()
        self.email = None
        self.messinfo = []
        if email == None or email == '':
            return 'ERROR|EMAIL_NOT_SET'
        if domain != None and 0 <= domain <= 11:
            if '@' in email:
                email = email.split('@')[0]
            self.email = email + '@' + self.domains[domain]
        else:
            if '@' in email:
                email = email.split('@')[0]
            self.email = email + '@' + random.choice(self.domains)

    def getMessages(self):
        if self.email == None or self.email == '':
            return 'ERROR|EMAIL_NOT_SET'
        resp = self.sess.get(self.mainurl + 'inboxes/' + self.email).json()
        if 'error' in resp:
            return 'ERROR|' + resp['error']
        self.messinfo = []
        for info in resp['msgs']:
            self.messinfo.append([info['uid'], info['fe'], info['s']])
        return [self.messinfo, len(self.messinfo)]

    def getMessage(self, email_id):
        if self.email == None or self.email == '':
            return 'ERROR|EMAIL_NOT_SET'
        if email_id == None or email_id == '':
            return 'ERROR|ID_NOT_SET'
        resp = self.sess.get(self.mainurl + 'messages/' + email_id).json()
        if 'error' in resp:
            return 'ERROR|' + resp['error']
        return [resp]

    def getAll(self):
        if self.email == None or self.email == '':
            return 'ERROR|EMAIL_NOT_SET'
        return [self.messinfo, len(self.messinfo)]

    def getData(self):
        if self.email == None or self.email == '':
            return 'ERROR|EMAIL_NOT_SET'
        return self.email


class TenMMail:  # 10minutemail.com
    mainurl = 'https://10minutemail.com/session/'

    def __init__(self):
        status = self.newEmail()
        if status != None:
            raise Exception(status)

    def newEmail(self):  # Create new email
        self.sess = r.Session()
        self.email = None
        self.messinfo = []
        self.messcontent = []
        resp = self.sess.get(self.mainurl + 'address').json()
        self.email = resp['address']  # Set got email

    def getMessages(self):  # Get new messages
        if self.email == None or self.email == '':
            return 'ERROR|EMAIL_NOT_SET'
        resp = self.sess.get(self.mainurl.replace('session', 'messages') + 'messagesAfter/0').json()
        self.messinfo = []  # New messages
        self.messcontent = []
        for info in resp:
            self.messinfo.append([info['id'], info['sender'], info['subject']])  # Append new message
            self.messcontent.append(
                [info['id'], info['bodyPlainText'], info['bodyHtmlContent']])  # Append message id and its content
        return [self.messinfo, len(self.messinfo)]

    def getMessage(self, email_id):  # Get message body
        if self.email == None or self.email == '':
            return 'ERROR|EMAIL_NOT_SET'
        if email_id == None or email_id == '':
            return 'ERROR|ID_NOT_SET'
        retvalue = None
        for message in self.messcontent:
            if message[0] == email_id:
                retvalue = [message[1], message[2]]  # Return content of the message with specified id
                break
        return retvalue

    def getAll(self):
        if self.email == None or self.email == '':
            return 'ERROR|EMAIL_NOT_SET'
        return [self.messinfo, len(self.messinfo)]

    def resetTime(self):
        if self.email == None or self.email == '':
            return 'ERROR|EMAIL_NOT_SET'
        self.sess.get(self.mainurl + 'reset')

    def getData(self):  # Get email data
        if self.email == None or self.email == '':
            return 'ERROR|EMAIL_NOT_SET'
        return self.email
