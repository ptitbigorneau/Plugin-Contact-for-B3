# Contact Plugin

__author__  = 'PtitBigorneau www.ptitbigorneau.fr'
__version__ = '1.5'

import b3,threading, thread
import b3.plugin
from b3 import clients
import smtplib
#from email.MIMEText import MIMEText
from email import *
import time
import calendar
from time import gmtime, strftime

def cdate():
        
    time_epoch = time.time() 
    time_struct = time.gmtime(time_epoch)
    date = time.strftime('%Y-%m-%d %H:%M:%S', time_struct)
    mysql_time_struct = time.strptime(date, '%Y-%m-%d %H:%M:%S') 
    cdate = calendar.timegm( mysql_time_struct)

    return cdate

class ContactPlugin(b3.plugin.Plugin):

    _adminPlugin = None    
    _minlevel = 1
    _bancontactlevel = 100
    _acontactlevel = 20
    _comeplaylevel = 100   
    _frommail = None
    _tomail = None
    _nameserver = "My Server"
    _smtpserver = "localhost"
    _maxmessage = 5
    _tempmaxmessage = 60
    _tempmessage = 5
    _gmailusername = None
    _gmailpwd = None 
    
    def onStartup(self):
        
        self._adminPlugin = self.console.getPlugin('admin')
        
        if not self._adminPlugin:

            self.error('Could not find admin plugin')
            return False

        self._adminPlugin.registerCommand(self,'contact',self._minlevel, self.cmd_contact)
        self._adminPlugin.registerCommand(self,'listmail',self._acontactlevel, self.cmd_listmail, 'lmail')
        self._adminPlugin.registerCommand(self,'addmail',self._acontactlevel, self.cmd_addmail,)
        self._adminPlugin.registerCommand(self,'delmail',self._acontactlevel, self.cmd_delmail)
        self._adminPlugin.registerCommand(self,'acontact',self._acontactlevel, self.cmd_acontact)
        self._adminPlugin.registerCommand(self,'bancontact',self._bancontactlevel, self.cmd_bancontact, 'bcontact')
        self._adminPlugin.registerCommand(self,'unbancontact',self._bancontactlevel, self.cmd_unbancontact, 'ucontact')
        self._adminPlugin.registerCommand(self,'listcontact',self._bancontactlevel, self.cmd_listcontact, 'ltcontact')   
        self._adminPlugin.registerCommand(self,'lookcontact',self._acontactlevel, self.cmd_lookcontact, 'lkcontact')
        self._adminPlugin.registerCommand(self,'comeplay',self._comeplaylevel, self.cmd_comeplay)

    def onLoadConfig(self):
    
        try:

            self._minlevel = self.config.getint('settings', 'minlevel')
        
        except Exception, err:
        
            self.warning("Using default value %s for Autoreg. %s" % (self._minlevel, err))
        
        self.debug('minlevel : %s' % (self._minlevel))


        try:

            self._acontactlevel = self.config.getint('settings', 'acontactlevel')
        
        except Exception, err:
            
            self.warning("Using default value %s for acontactlevel. %s" % (self._acontactlevel, err))
        
        self.debug('acontactlevel : %s' % (self._acontactlevel))


        try:

            self._bancontactlevel = self.config.getint('settings', 'bancontactlevel')
        
        except Exception, err:
            
            self.warning("Using default value %s for bancontactlevel. %s" % (self._bancontactlevel, err))
        
        self.debug('bancontactlevel : %s' % (self._bancontactlevel))

        try:

            self._comeplaylevel = self.config.getint('settings', 'comeplaylevel')
        
        except Exception, err:
            
            self.warning("Using default value %s for comeplaylevel. %s" % (self._comeplaylevel, err))
        
        self.debug('comeplaylevel : %s' % (self._comeplaylevel))


        try:

            self._frommail = self.config.get('settings', 'frommail')
        
        except Exception, err:
            
            self.warning("value for frommail is None. %s" % (err))
        
        self.debug('frommail : %s' % (self._frommail))


        try:

            self._tomail = self.config.get('settings', 'tomail')
        
        except Exception, err:
            
            self.warning("value for tomail is None. %s" % (err))
        
        self.debug('tomail : %s' % (self._tomail))


        try:

            self._nameserver = self.config.get('settings', 'nameserver')
        
        except Exception, err:
            
            self.warning("Using default value %s for nameserver. %s" % (self._nameserver, err))
        
        self.debug('nameserver : %s' % (self._nameserver))


        try:

            self._smtpserver = self.config.get('settings', 'smtpserver')
        
        except Exception, err:
            
            self.warning("Using default value %s for smtpserver. %s" % (self._smtpserver, err))
        
        self.debug('smtpserver : %s' % (self._smtpserver))


        try:

            self._maxmessage = self.config.getint('settings', 'maxmessage')
        
        except Exception, err:
            
            self.warning("Using default value %s for maxmessage. %s" % (self._maxmessage, err))
        
        self.debug('maxmessage : %s' % (self._maxmessage))


        try:

            self._tempmaxmessage = self.config.getint('settings', 'tempmaxmessage')
        
        except Exception, err:
            
            self.warning("Using default value %s for tempmaxmessage. %s" % (self._tempmaxmessage, err))
        
        self.debug('tempmaxmessage : %s' % (self._tempmaxmessage))


        try:

            self._tempmessage = self.config.getint('settings', 'tempmessage')
        
        except Exception, err:
            
            self.warning("Using default value %s for tempmessage. %s" % (self._tempmessage, err))
        
        self.debug('tempmessage : %s' % (self._tempmessage))


        try:

            self._gmailusername = self.config.get('settings', 'gmailusername')
        
        except Exception, err:
            
            self.warning("value for gmailusername is None. %s" % (err))
        
        self.debug('gmailusername : %s' % (self._gmailusername))


        try:

            self._gmailpwd = self.config.get('settings', 'gmailpwd')
        
        except Exception, err:
            
            self.warning("value for gmailpwd is None. %s" % (err))
        
        if self._gmailpwd == None:

            self.debug('gmailpwd : None')

        else:

            self.debug('gmailpwd : ********')

    def comeplaymessage(self):

        server = self._nameserver
        mto = self.mail
        mfrom = self._frommail
        server = self._nameserver
        smtpserver = self._smtpserver
        gmailusername = self._gmailusername
        gmailpwd = self._gmailpwd
            
        sujetmail = 'Invitation to play on the server: ' + server

        message= 'Hi ' + self.recipient + '\r\n\n ' + self.sender + ' invite you to come and play on' + server + '\r\n\n'
                                          
        if smtpserver == 'smtp.gmail.com' :
           
            email = MIMEText.MIMEText(message) 
            email['From']=mfrom
            email['To']=mto 
            email['Subject']=sujetmail 
            server = smtplib.SMTP('smtp.gmail.com',587)
            server.set_debuglevel(1)
            server.ehlo(gmailusername)
            server.starttls()
            server.ehlo()
            server.login(gmailusername, gmailpwd)
            server.sendmail(mfrom, mto, email.as_string())
            server.quit()

        else:
               
            email = MIMEText.MIMEText(message) 
            email['From']=mfrom
            email['To']=mto 
            email['Subject']=sujetmail 
            server = smtplib.SMTP(smtpserver) 
            server.sendmail(mfrom, mto, email.as_string())
            server.quit()
	
        return
			
    def cmd_contact(self, data, client, cmd=None):
        """\
        <message> - Message to administrator server
        """

        mdate = cdate() 
        
        cursor = self.console.storage.query("""
        SELECT *
        FROM contact n 
        WHERE n.client_id = '%s'
        """ % (client.id))
           
        if cursor.rowcount > 0:
            
            sr = cursor.getRow()
            cnenvois=sr['nenvois']
            cmdate=sr['date']
            cauthoriz=sr['authoriz']            
            maxmessage=self._maxmessage
            tempmaxmessage=self._tempmaxmessage*60
            tempmessage=self._tempmessage*60
            
            if mdate - tempmaxmessage > cmdate:
            
                cnenvois=0
                cursor = self.console.storage.query("""
                UPDATE contact
                SET nenvois= '%s'
                WHERE client_id = '%s'
                """ % (cnenvois, client.id))
                cursor.close()
            
            if cauthoriz==0:
                
                client.message('You are not authorized to send a message')
                return False

            if (cnenvois>=maxmessage) and (client.maxLevel<self._acontactlevel):
                     
                client.message('Your not authorized for the moment to send messages')
                return False            
            
            if (mdate - tempmessage < cmdate) and (client.maxLevel<self._bancontactlevel):
                
                client.message('Wait! You have already send a message')
                return False              
        
        cursor.close()

        if data:
            
            smessage = data
        
        else:
            
            client.message('!contact <message to admin>')
            return
        
        smessage = smessage.replace('. ', '.\r\n')
        smessage = smessage.replace('? ', '?\r\n')
        smessage = smessage.replace('! ', '!\r\n')
        
        if not smessage:
            
            client.message('!contact <message to admin>')
            return False
               
        if smessage:
            
            mto = self._tomail
            mfrom = self._frommail
            server = self._nameserver
            smtpserver = self._smtpserver
            gmailusername = self._gmailusername
            gmailpwd = self._gmailpwd
            
            sujetmail = 'Message from B3 Plugin Contact from server: ' + server
            id =  str(client.id)
            message='Server : ' + server + ' - Message from : ' + client.name + ' - Guid : ' + client.guid + ' - Id Player : @' + id + ' - Ip : ' + client.ip + '\r\n\n ' + client.name + ' writes :\r\n\n' + smessage
                                          
            if smtpserver == 'smtp.gmail.com' :
            
                email = MIMEText.MIMEText(message) 
                email['From']=mfrom
                email['To']=mto 
                email['Subject']=sujetmail 
                server = smtplib.SMTP('smtp.gmail.com',587)
                server.set_debuglevel(1)
                server.ehlo(gmailusername)
                server.starttls()
                server.ehlo()
                server.login(gmailusername, gmailpwd)
                server.sendmail(mfrom, mto, email.as_string())
                server.quit()

            else:
                
                email = MIMEText.MIMEText(message) 
                email['From']=mfrom
                email['To']=mto 
                email['Subject']=sujetmail 
                server = smtplib.SMTP(smtpserver) 
                server.sendmail(mfrom, mto, email.as_string())
                server.quit()
                
            client.message('Your message has been sent')
            client.message('Your nickname, ip, guid and id appear in the message sent')
            
            cursor = self.console.storage.query("""
            SELECT *
            FROM contact n 
            WHERE n.client_id = '%s'
            """ % (client.id))
            
            if cursor.rowcount > 0:
                
                sr = cursor.getRow()
                cnenvois=sr['nenvois']
                cnenvois = cnenvois + 1
                cursor = self.console.storage.query("""
                UPDATE contact
                SET nenvois= '%s', date= '%s' 
                WHERE client_id = '%s'
                """ % (cnenvois, mdate, client.id))
                cursor.close()
                return False
            
            cursor.close()
            
            cursor = self.console.storage.query("""
            INSERT INTO contact
            VALUES (%s, %s, %s, %s)
            """ % (client.id, 1, 1, mdate))

            cursor.close()
            
        else:
            return False
    
    def cmd_addmail(self, data, client, cmd=None):
        """\
        <message> - Register or change your mail address 
        """

        if data:

            input = self._adminPlugin.parseUserCmd(data)
        
        else:
            
            client.message('!addmail <your mail address>')
            return
        
        smail=input[0]
        test1= smail.count('@')
        test2 = smail.count('.')         
        
        if (test1==0) or (test2==0):
            client.message('Mail address is not valid')
            return False        
        
        if smail:
            
            cursor = self.console.storage.query("""
            SELECT *
            FROM adminmail n 
            WHERE n.client_id = '%s'
            """ % (client.id))

            if cursor.rowcount > 0:
                cursor = self.console.storage.query("""
                UPDATE adminmail
                SET mail='%s' 
                WHERE client_id = %s
                """ % (smail, client.id))
                client.message('Your new mail address : %s is now registered' %(smail))
                cursor.close()
                return False
            cursor.close()
            cursor = self.console.storage.query("""
            INSERT INTO adminmail
            VALUES (%s, '%s')
            """ % (client.id,  smail))

            cursor.close()
            client.message('Your mail address : %s is now registered' %(smail))
       
        else:
            return False
    
    def cmd_delmail(self, data, client, cmd=None):
        """\
        <message> - Delete your mail address 
        """

        cursor = self.console.storage.query("""
        SELECT n.client_id
        FROM adminmail n 
        WHERE n.client_id = '%s'
        """ % (client.id))
        
        if cursor.rowcount == 0:
            client.message("^7You don't have a registered mail address")
            return False
        
        cursor.close()
        
        cursor = self.console.storage.query("""
        DELETE FROM adminmail
        WHERE client_id = '%s'
        """ % (client.id))
        
        cursor.close()
        
        client.message("^7Your mail address has been deleted")
    
    def cmd_listmail(self, data, client, cmd=None):
        """\
        <message> - Admins list with an mail address registered 
        """
        
        thread.start_new_thread(self.listmail, (data, client))
        
    def listmail(self, data, client):
            
        cursor = self.console.storage.query("""
        SELECT *
        FROM adminmail
        """)
        c = 1
        
        if cursor.EOF:
          
            client.message('Admins list with an mail address registered is empty')
            cursor.close()            
            return False
        
        while not cursor.EOF:
            sr = cursor.getRow()
            cid = sr['client_id']
            scid= '@'+str(cid)
            sclient = self._adminPlugin.findClientPrompt(scid, client)
            client.message('^2%s^7 - id : ^2@%s^7 - level : (^1%s^7)' % (sclient.exactName, cid, sclient.maxLevel))
            cursor.moveNext()
            c += 1
            
        cursor.close()
    
    def cmd_acontact(self, data, client, cmd=None):
        """\
        <message> - Message to admin or moderator server
        """

        mdate = cdate()
        
        cursor = self.console.storage.query("""
        SELECT *
        FROM contact n 
        WHERE n.client_id = '%s'
        """ % (client.id))
           
        if cursor.rowcount > 0:
            
            sr = cursor.getRow()
            cnenvois=sr['nenvois']
            cmdate=sr['date']
            cauthoriz=sr['authoriz']            
            tempmessage=self._tempmessage*60
            
            if cauthoriz==0:
                
                client.message('You are not authorized to send a message')
                return False

            if (mdate - tempmessage < cmdate) and (client.maxLevel<self._bancontactlevel):
                
                client.message('Wait! You have already send a message')
                return False              
        
        cursor.close()
        
        if data:
            input = self._adminPlugin.parseUserCmd(data)
        
        else:
            client.message('!acontact <admin> <message>')
            return
        
        sclient = self._adminPlugin.findClientPrompt(input[0], client)    
        
        smessage = input[1]
        smessage = smessage.replace('. ', '.\r\n')
        smessage = smessage.replace('? ', '?\r\n')
        smessage = smessage.replace('! ', '!\r\n')
        
        if not sclient:
            
            client.message('!acontact <admin> <message>')
            client.message('!listcontact For Admins list with an mail address registered')
            return False
        
        if not smessage:
            
            client.message('!acontact <admin> <message>')
            return False
        
        if sclient:
            
            cursor = self.console.storage.query("""
            SELECT n.client_id
            FROM adminmail n 
            WHERE n.client_id = '%s'
            """ % (sclient.id))
            
            if sclient.maxLevel<self._acontactlevel:
                
                client.message("%s is not admin or moderator"%(sclient.exactName))
                return False
            
            if cursor.rowcount == 0:
                
                client.message("^7Admin don't have a registered mail address")
                return False
            
            cursor.close()
            cursor = self.console.storage.query("""
            SELECT *
            FROM adminmail n
            WHERE n.client_id = '%s'
            """ % (sclient.id))
                        
            sr = cursor.getRow()
            
            mto=sr['mail']
                                   
            cursor.close()
        
        if smessage:
            
            mfrom = self._frommail
            server = self._nameserver
            smtpserver = self._smtpserver
            gmailusername = self._gmailusername
            gmailpwd = self._gmailpwd
            
            sujetmail = 'Message from ' + client.name + ' from a Server : ' + server
            level =  str(client.maxLevel)
            message='Server : ' + server + ' - Message from : ' + client.name + ' - level : ' + level + '\r\n\n ' + client.name + ' writes :\r\n\n' + smessage

            if smtpserver == 'smtp.gmail.com' :
            
                email = MIMEText.MIMEText(message) 
                email['From']=mfrom
                email['To']=mto 
                email['Subject']=sujetmail 
                server = smtplib.SMTP('smtp.gmail.com',587)
                server.set_debuglevel(1)
                server.ehlo(gmailusername)
                server.starttls()
                server.ehlo()
                server.login(gmailusername, gmailpwd)
                server.sendmail(mfrom, mto, email.as_string())
                server.quit()            
            
            else:
            
                email = MIMEText.MIMEText(message)
                email['From']=mfrom
                email['To']=mto 
                email['Subject']=sujetmail 
                server = smtplib.SMTP(smtpserver) 
                server.sendmail(mfrom, mto, email.as_string())
                server.quit() 
            
            client.message('Your message has been sent to %s'%(sclient.exactName))
            
            cursor = self.console.storage.query("""
            SELECT *
            FROM contact n 
            WHERE n.client_id = '%s'
            """ % (client.id))
            
            if cursor.rowcount > 0:
                
                sr = cursor.getRow()
                cnenvois=sr['nenvois']
                cnenvois = cnenvois + 1
                cursor = self.console.storage.query("""
                UPDATE contact
                SET nenvois= '%s', date= '%s' 
                WHERE client_id = '%s'
                """ % (cnenvois, mdate, client.id))
                
                cursor.close()
                return False
            
            cursor.close()
            cursor = self.console.storage.query("""
            INSERT INTO contact
            VALUES (%s, %s, %s, %s)
            """ % (client.id, 1, 1, mdate))

            cursor.close()            
       
        else:
            return False

    def cmd_comeplay(self, data, client, cmd=None):
        """\
        <message> - Message to invite all players who have their email addresses in the list
        """
         
        thread.start_new_thread(self.comeplay, (data, client))
        
    def comeplay(self, data, client):
        """\
        <message> - Message to invite all players who have their email addresses in the list
        """

        self.sender = client.name
       
        cursor = self.console.storage.query("""
        SELECT *
        FROM adminmail
        """)
        c = 1
        
        if cursor.EOF:
          
            client.message('Admins list with an mail address registered is empty')
            cursor.close()            
            return False
        
        while not cursor.EOF:
            sr = cursor.getRow()
            cid = sr['client_id']
            scid = '@'+str(cid)
            self.mail = sr['mail']
            sclient = self._adminPlugin.findClientPrompt(scid, client)
            self.recipient = sclient.name
            
            self.comeplaymessage()
            cursor.moveNext()
            c += 1
            
        cursor.close()           

        client.message('All invitations have been sent !')

    def cmd_bancontact(self, data, client, cmd=None):
        """\
        <message> - ban from Contact 
        """

        mdate = cdate() 
        
        if data:

            input = self._adminPlugin.parseUserCmd(data)

        else:
            
            client.message('!banacontact <name or id>')
            return
        
        sclient = self._adminPlugin.findClientPrompt(input[0], client)
        
        if sclient:
            
            if sclient.maxLevel>=self._bancontactlevel:
                
                client.message("%s can not be banned from Contact"%(sclient.exactName))
                return False
            
            cursor = self.console.storage.query("""
            SELECT *
            FROM contact n 
            WHERE n.client_id = '%s'
            """ % (sclient.id))

            if cursor.rowcount > 0:
                
                cursor = self.console.storage.query("""
                UPDATE contact
                SET authoriz="0" , date=%s
                WHERE client_id = %s
                """ % (sclient.id, mdate))
                
                client.message('%s is now ban from Contact' %(sclient.exactName))
                
                cursor.close()
                
                return False
            cursor.close()
            
            cursor = self.console.storage.query("""
            INSERT INTO contact
            VALUES (%s, %s, %s, %s)
            """ % (sclient.id, 0, 0, mdate))

            cursor.close()        
            
            client.message('%s is now ban from Contact' %(sclient.exactName))
       
        else:
            return False

    def cmd_unbancontact(self, data, client, cmd=None):
        """\
        <message> - unban from Contact
        """
        
        if data:
            
            input = self._adminPlugin.parseUserCmd(data)
        
        else:
            
            client.message('!unbanacontact <name or id>')
            return
        
        sclient = self._adminPlugin.findClientPrompt(input[0], client)
        
        if sclient:
            
            cursor = self.console.storage.query("""
            SELECT n.authoriz
            FROM contact n 
            WHERE n.client_id = %s
            """ % (sclient.id))
        
            if cursor.rowcount == 0:
                
                client.message("%s^7 not ban from Contact"%(sclient.exactName))
                return False
            
            cursor.close()
        
            cursor = self.console.storage.query("""
            UPDATE contact
            SET authoriz="1"
            WHERE client_id = %s
            """ % (sclient.id))
            
            cursor.close()
            
            client.message("%s^7 is unban from Contact"%(sclient.exactName))
    
    def cmd_listcontact(self, data, client, cmd=None):
        """\
        <message> - Send by e_mail the users list from Contact and see the last 10 users
        """
        thread.start_new_thread(self.listcontact, (data, client))

    def listcontact(self, data, client, cmd=None):
    
        cursor = self.console.storage.query("""
        SELECT *
        FROM contact
        ORDER BY date DESC LIMIT 0, 10
        """)
        c = 1
        
        if cursor.EOF:
          
            client.message('Users list from Contact is empty')
            cursor.close()            
        
        while not cursor.EOF:
        
            sr = cursor.getRow()
            cid = sr['client_id']
            cdate = time.strftime('%d-%m-%Y %H:%M',time.localtime(sr['date']))
            cauthoriz = sr['authoriz']
            scid= '@'+str(cid)
            
            if cauthoriz==0:
                cstatus='^1Banned'
            if cauthoriz==1:
                cstatus='^2Authorized'                   
            
            sclient = self._adminPlugin.findClientPrompt(scid, client)
            client.message('^2%s^7- ID : ^2@%s^7 - Date : ^2%s^7 - Status %s^7' %(sclient.name, sclient.id, cdate, cstatus))
            
            cursor.moveNext()
            
            c += 1
        
        cursor.close()
                
        cursor = self.console.storage.query("""
        SELECT *
        FROM contact
        """)

        c = 1

        message = '\r\n'
        
        if cursor.EOF:
          
            message='Users list from Contact is empty'
            cursor.close() 
            return False
            
        while not cursor.EOF:
        
            sr = cursor.getRow()
            cid = sr['client_id']
            cdate = time.strftime('%d-%m-%Y %H:%M',time.localtime(sr['date']))
            cauthoriz = sr['authoriz']
            scid= '@'+str(cid)

            if cauthoriz==0:
                cstatus='Banned'
            if cauthoriz==1:
                cstatus='Authorized'                   

            sclient = self._adminPlugin.findClientPrompt(scid, client)
            message= message + '%s - ID : @%s - Guid : %s - IP : %s - Date : %s - Status : %s\r\n' % (sclient.name, sclient.id, sclient.guid, sclient.ip, cdate, cstatus)
            
            cursor.moveNext()
            
            c += 1
            
        cursor.close()    
        
        mto = self._tomail
        mfrom = self._frommail
        server = self._nameserver
        smtpserver = self._smtpserver
        sujetmail = 'Clients list from Contact Server : ' + server
                                                   
        email = MIMEText.MIMEText(message) 
        email['From']=mfrom
        email['To']=mto 
        email['Subject']=sujetmail 
        server = smtplib.SMTP(smtpserver) 
        server.sendmail(mfrom, mto, email.as_string())
        server.quit()
        client.message('Clients list from Contact has been sent by e_mail to %s'%(mto))
        
    def cmd_lookcontact(self, data, client, cmd=None):
        """\
        <message> - Look if player is in Contact list 
        """

        if data:
        
            input = self._adminPlugin.parseUserCmd(data)

        else:
            
            client.message('!lookcontact <name or id>')
            return
        
        sclient = self._adminPlugin.findClientPrompt(input[0], client)
        
        if sclient:        
        
            cursor = self.console.storage.query("""
            SELECT *
            FROM contact n 
            WHERE n.client_id = %s
            """ % (sclient.id))
        
            if cursor.rowcount == 0:
                client.message("%s^7 is not in Contact list"%(sclient.exactName))
                return False
            
        
            sr = cursor.getRow()
            cauthoriz = sr['authoriz']
            cdate = time.strftime('%d-%m-%Y %H:%M',time.localtime(sr['date']))
            
            if cauthoriz==0:
                cstatus='^1Banned'
            if cauthoriz==1:
                cstatus='^2authorized'                   
                        
            client.message('^2%s^7 - id : ^2@%s^7 - Date : ^2%s^7' % (sclient.exactName, sclient.id, cdate))
            client.message('^7Status : %s^7' % (cstatus))

            cursor.close()
        else:
            return False