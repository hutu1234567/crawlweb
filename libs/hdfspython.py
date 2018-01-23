from hdfs import *
from hdfs.ext.kerberos import KerberosClient
import os

class HdfsClient:

    '''hdfs客户端'''
    def __init__(self, ip='', root=None, proxy=None):
        self.client=self.selectClient(ip)

    def selectClient(self, ip='',root=None, proxy=None):
        """寻找可用hdfs链接"""
        self.initKerberos()
        urlMaping = {'10.10.10.23': 'http://10.10.10.23:50070', '10.10.10.21': 'http://10.10.10.21:50070',
                     '10.10.10.22': 'http://10.10.10.22:50070'}

        def testip(ip,root=None, proxy=None):
            print ip

            if ip == '':
                return process()
            else:
                client = KerberosClient(urlMaping[ip], root=root, proxy=proxy)
                try:
                    print 'test %s' % urlMaping[ip]
                    client.list("/")
                    return client
                except:

                    return process()

        def process():
            for key in urlMaping.keys():
                client = KerberosClient(urlMaping[key], root=root, proxy=proxy)
                try:
                    client.list("/")
                    return client
                except:
                    continue

        return testip(ip)


    def initKerberos(self):
        '''初始化kerberos'''
        os.chdir('/etc/security/keytabs')
        os.system('kinit -kt hdfs.headless.keytab  hdfs-cluster1@IDAP.COM')

    def list(self,hdfspath):
        '''用于列出hdfspath所在路径下面的所有文件'''
        files =self.client.list(hdfspath)
        return files

    def upload(self,hdfsPath,localFilePath):
        '''用于上传本地文件到hdfs路径'''
        allPaths=self.client.list("/")
        if hdfsPath not  in allPaths:
            print(hdfsPath+'is not exists!')
        self.client.upload(hdfsPath, localFilePath)


    def mkdirs(self,hdfsPath):
        '''用于创建hdfs路径'''
        self.client.makedirs(hdfsPath,permission=777)
        print('mkdir'+hdfsPath+' ok')


    def existFile(self, path, fileName):
        '''判断文件是否存在'''
        allpath = [item for item in path.split('/') if item != '/' and item != '' and item != fileName]
        increPath = '/'
        for itemPath in allpath:
            increPath = increPath + itemPath + '/'
        if fileName in self.list(increPath):
            return True;
        else:
            return False;

    def existPath(self,path):
        '''判断文件是否存在'''
        allpath = [item for item in path.split('/') if item != '/' and item != '' and item.find('csv')]
        increPath = '/'
        for i in range(len(allpath)-1):
            if i<len(allpath)-1:
             increPath = increPath + allpath[i] + '/'
            else:
             increPath = increPath + allpath[i]
        if allpath[-1] in self.list(increPath):
            return True;
        else:
            return False

    def write(self,hdfsPath,filename,data,append=True):
        '''如果文件存在则追加，否则创建'''
        if self.existPath(hdfsPath):
            if self.existFile(hdfsPath, filename):
                self.client.write(hdfsPath + '/' + filename.replace(' ', ''), data, append=True)
            else:
                self.client.write(hdfsPath + '/' + filename.replace(' ', ''), data, append=False)

            self.client.write(hdfsPath + '/' + filename.replace(' ', ''), '\n', append=True)
        else:
            self.mkdirs(hdfsPath)
            self.client.write(hdfsPath + '/' + filename.replace(' ', ''), data, append=False)
            self.client.write(hdfsPath + '/' + filename.replace(' ', ''), '\n', append=True)
        print('has done')





if __name__ == '__main__':
    testclient = HdfsClient( 'http://10.10.10.23:50070' )
    csvfile = open( 'ftgoodfile3.csv', 'r' )
    csvcontent = csvfile.read()
    csvfile.close()
    testclient.write( '/wnm/1109/djla', 'ftgoodfile3.csv', csvcontent, append=True )
    testclient.printFileNames( '/wnm/1109/djla' )
    testclient.readByPath( '/wnm/1109/djla/ftgoodfile3.csv' )