#_*_ coding:utf-8 _*_

from urllib.parse import urlparse,urljoin
if __name__ == '__main__':
    o = urlparse( 'http://www.cwi.nl:80/%7Eguido/Python.html' )
    print(o.geturl())
    d = urljoin('https://segmentfault.com/q/1010000004708543/a-1020000004954370', 'www.segmentfault.com/img/bVtWkL')
    print(d)
