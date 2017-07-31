from html.parser import HTMLParser


class StockListParserAction( HTMLParser ):
    #from http://quote.eastmoney.com/stock_list.html#sz
    def __init__(self):
        HTMLParser.__init__( self )
        self.links = []
        self.a_text = False

    def handle_starttag(self, tag, attrs):
        # print "Encountered the beginning of a %s tag" % tag<li><a target="_blank" href="http://quote.eastmoney.com/
        if tag == "a":
            if len( attrs ) == 0:
                pass
            else:
                for (variable, value) in attrs:
                    if variable == "href":
                        if str(value).startswith("http://quote.eastmoney.com/sh") or str(value).startswith("http://quote.eastmoney.com/sz"):
                            self.a_text = True
                            # self.links.append( value )
                            # print(dir(attrs))

    def handle_data(self,data):
        if self.a_text:
            self.links.append( data )

    def handle_endtag(self, tag):
        self.a_text = False

    def getJsonContent(self):
        jo = {}
        if (len( self.links ) > 0):
            jo["success"] = True
            jo["result"] = self.links
        else:
            jo["success"] = True

        return jo