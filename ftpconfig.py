import configparser
class FtpConfig():
    def __init__(self):
        # HostName=10.201.171.13
        self.SendFiles=''
        # UserName=stky
        self.OutputPath=''
        self.OutputFileName=''
        # Password=stky99
        self.shortname=''
#        # LocalOutBox1=d:\qqctn2017\out\
#        self.LocalOutPath=''
#        # RemoteInBox1=/depot_modify_qqctn/
#        self.RemoteInPath=''
#        # SendFiles1=*.*
#        self.SendLocalFiles=''
#        # LocalInBox1=d:\qqctn2017\in\
#        self.LocalInPath=''
#        # RemoteOutBox1=/depot_modify_qqctn/aa/
#        self.RemoteOutPath=''
#        # ReceiveFiles1=*.*
#        self.ReceiveRemoteFiles=''
#        # AutoDelLocal=1
#        self.AutoDelLocal=True
#        # AutoDelRemote=0
#        self.AutoDelRemote=False

    def setFromIni(self, path):
        iniFileUrl = path
        conf = configparser.ConfigParser()  #
        conf.read(iniFileUrl)  #
        sections = conf.sections()
        # HostName=10.201.171.13
        # self.RemoteHost = conf.get("Begin", "HostName")
        # # UserName=stky
        # self.RemoteUserName = conf.get("Begin", "UserName")
        # # Password=stky99
        # self.RemotePwd = conf.get("Begin", "Password")
        # # LocalOutBox1=d:\qqctn2017\out\
        #self.LocalOutPath = conf.get("Begin", "LocalOutBox1")
        # # RemoteInBox1=/depot_modify_qqctn/
        # self.RemoteInPath = conf.get("Begin", "RemoteInBox1")
        # # SendFiles1=*.*
        self.SendFiles = conf.get("Begin", "SendFiles")
        # LocalInBox1=d:\qqctn2017\in\
        self.OutputPath = conf.get("Begin", "OutputPath")
        self.OutputFileName = conf.get("Begin", "OutputFileName")
        # RemoteOutBox1=/depot_modify_qqctn/aa/
        self.shortname = conf.get("Begin", "shortname")
        # ReceiveFiles1=*.*
        # self.ReceiveRemoteFiles = conf.get("Begin", "ReceiveFiles1")
        # # AutoDelLocal=1
        # self.AutoDelLocal = conf.getint("Begin", "AutoDelLocal")
        # # AutoDelRemote=0
        # self.AutoDelRemote = conf.getint("Begin", "AutoDelRemote")
    pass

