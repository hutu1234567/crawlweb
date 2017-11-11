﻿from hdfs import *
from hdfs.ext.kerberos import KerberosClient

class HdfsClient:

    '''hdfs客户端'''

    def __init__(self, url, root=None, proxy=None):
        self.client = KerberosClient(url, root=root, proxy=proxy)
       
       
    '''打印指定目录下面的所有文件目录或文件'''
    def printFileNames(self,hdfsPath):
        for name in self.list(hdfsPath):
            print name,

    '''读取指定路径的文件'''
    def readByPath(self,hdfspath):
        file=self.client.read(hdfspath)
        with self.client.read(hdfspath) as reader:
            print reader.read()

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
        allpathname = [item for item in path.split('/') if item != '/' and item != '' and item != fileName]
        increPath = '/'
        for itemPath in allpathname:
            increPath = increPath + itemPath + '/'
        if fileName in self.list(increPath):
            return True;
        else:
            return False;

    def existPath(self,path):
        '''判断文件是否存在'''
        allpathname = [item for item in path.split('/') if item != '/' and item != '' and item.find('csv')]
        increPath = '/'
        pathList=['/']
        for i in range(len(allpathname)-1):

            if i<len(allpathname)-1:
             increPath = increPath + allpathname[i] + '/'
             pathList.append(increPath[:len(increPath)-1])
            else:
             increPath = increPath + allpathname[i]
             pathList.append(increPath[:len(increPath) - 1])

        #子路径是否存在 以/wnn/1109为例,1109是否存在
        count=0
        for i in range(len(pathList)-1):
            if allpathname[i] not in self.list(pathList[i]):
             return False
            else:
              count+=1
        if count==len(pathList)-1:
            return True

    def write(self,hdfsPath,filename,data,append=True):
        '''如果文件存在则追加，否则创建'''
        if self.existPath(hdfsPath):
            if self.existFile(hdfsPath, filename):
                self.client.write(hdfsPath + '/' + filename.replace(' ', ''), data, append=True)
            else:
                self.client.write(hdfsPath + '/' + filename.replace(' ', ''), data, append=False)

            self.client.write(hdfsPath + '/' + filename.replace(' ', ''), '\n', append=True)
        else:
            print '\n %s 不存在，那就创建吧' %(hdfsPath)
            self.mkdirs(hdfsPath)
            self.client.write(hdfsPath + '/' + filename.replace(' ', ''), data, append=False)
            self.client.write(hdfsPath + '/' + filename.replace(' ', ''), '\n', append=True)


if __name__ == '__main__':
    testclient = HdfsClient('http://10.10.10.23:50070')
    csvfile=open('ftgoodfile3.csv','r')
    csvcontent=csvfile.read()
    csvfile.close()
    testclient.write('/wnm/1109/djla','ftgoodfile3.csv',csvcontent,append=True)
    testclient.printFileNames('/wnm/1109/djla')
    testclient.readByPath('/wnm/1109/djla/ftgoodfile3.csv')

    
