class GetProxyList():
    def __init__(self,filname):
        #'ip_prot.csv'
        self.filname = filname

    def getfilelist(self):
        file = open(self.filname,'r')
        content = file.read()
        rows = content.split()
        final_list = []
        for row in rows:
            final_list.append(row.split(','))
        return final_list

    def getproxiselist(self):
        final_list = self.getfilelist()
        # proxy:{'http': 'http://{}:{},'https': 'https://{}:{}''}
        proxies_list = []
        proxy = {}
        for proxy_list in final_list:
            proxy['http'] = proxy_list[0]
            proxy['https'] = proxy_list[1]
            proxies_list.append(proxy)
        return proxies_list


    def main(self):
        content_list = self.getproxiselist()
        print(content_list)

if __name__ == '__main__':
    proxy = GetProxyList('ip_prot.csv')
    proxy.main()



