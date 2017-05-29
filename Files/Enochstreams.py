import re,json,urllib,urlparse,base64

from resources.lib.modules import client
from resources.lib.modules import workers

class streamer:

    def resolve(self, url):
        try:
            if 'cartoonson.com' in url: u = self.cartoonson(url)
            
            if 'ultramovie.me' in url: u = self.ultramovie(url)
            
            if 'soccerstreams.net' in url: u = self.soccerstream(url)
            
            if 'linkmovie25.com' in url: u = self.linkmovie25(url)
            
            if 'movie2k.am' in url: u = self.movie2k(url)
            
            else: u = self.generic(url)

            return u
        except:
            pass


    def generic(self, url):
        try:
            r = client.request(url)
            r = r.replace('\\', '')

            s = re.findall('\s*:\s*\"(http.+?)\"', r) + re.findall('\s*:\s*\'(http.+?)\'', r)
            s = [i for i in s if (urlparse.urlparse(i).path).strip('/').split('/')[-1].split('.')[-1] in ['mp4', 'flv', 'm3u8']]

            if not s: s = re.findall('\s*\(\s*\"(http.+?)\"', r) + re.findall('\s*\(\s*\'(http.+?)\'', r)
            s = [i for i in s if (urlparse.urlparse(i).path).strip('/').split('/')[-1].split('.')[-1] in ['mp4', 'flv', 'm3u8']]

            if not s: s = re.findall('\s*=\s*\'(http.+?)\'', r) + re.findall('\s*=\s*\"(http.+?)\"', r)
            s = [i for i in s if (urlparse.urlparse(i).path).strip('/').split('/')[-1].split('.')[-1] in ['mp4', 'flv', 'm3u8']]

            if not s:s = re.findall('\s*:\s*\"(//.+?)\"', r) + re.findall('\s*:\s*\'(//.+?)\'', r)
            s = [i for i in s if (urlparse.urlparse(i).path).strip('/').split('/')[-1].split('.')[-1] in ['mp4', 'flv', 'm3u8']]

            if not s:s = re.findall('\:\"(\.+?)\"', r) + re.findall('\:\'(\.+?)\'', r)
            s = [i for i in s if (urlparse.urlparse(i).path).strip('/').split('/')[-1].split('.')[-1] in ['mp4', 'flv', 'm3u8']]

            if not s: s = re.findall('\s*\(\s*\"(//.+?)\"', r) + re.findall('\s*\(\s*\'(//.+?)\'', r)
            s = [i for i in s if (urlparse.urlparse(i).path).strip('/').split('/')[-1].split('.')[-1] in ['mp4', 'flv', 'm3u8']]

            if not s: s = re.findall('\s*=\s*\'(//.+?)\'', r) + re.findall('\s*=\s*\"(//.+?)\"', r)
            s = [i for i in s if (urlparse.urlparse(i).path).strip('/').split('/')[-1].split('.')[-1] in ['mp4', 'flv', 'm3u8']]

            if not s: s = re.findall('\w*:\s*\"(http.+?)\"', r) + re.findall('\w*:\s*\'(http.+?)\'', r)
            s = [i for i in s if (urlparse.urlparse(i).path).strip('/').split('/')[-1].split('.')[-1] in ['mp4', 'flv', 'm3u8']]
            
            if not s: s = re.findall('\w*=\'([^\']*)', r) + re.findall('\w*="([^"]*)', r)
            s = [i for i in s if (urlparse.urlparse(i).path).strip('/').split('/')[-1].split('.')[-1] in ['mp4', 'flv', 'm3u8']]

            if not s: s = client.parseDOM(r, 'source', ret='src', attrs = {'type': 'video.+?'})

            s = ['http:' + i if i.startswith('//') else i for i in s]
            s = [urlparse.urljoin(url, i) if not i.startswith('http') else i for i in s]
            s = [x for y,x in enumerate(s) if x not in s[:y]]

            self.u = []
            def request(i):
                try:
                    c = client.request(i, output='headers')
                    checks = ['video','mpegurl']
                    if any(f for f in checks if f in c['Content-Type']): self.u.append((i, int(c['Content-Length'])))
                except:
                    pass
            threads = []
            for i in s: threads.append(workers.Thread(request, i))
            [i.start() for i in threads] ; [i.join() for i in threads]

            u = sorted(self.u, key=lambda x: x[1])[::-1]
            u = client.request(u[0][0], output='geturl', referer=url)
            return u
        except:
            pass
            
            
    def cartoonson(self, url):
        try:
            u = client.request(url)
            e = re.findall('(?s)col-sm-6 col-sm-offset-3.+?a\s*href="([^"]*)', u)[0]
            u = client.request('http://www.cartoonson.com' + e)
            if not u: u = client.request(e)
            e = re.findall('(?s)"col-sm-12">.+?src="(.+?)"', u)[0]
            return e
        except:
            return
            
    def ultramovie(self, url):
        try:
            u = client.request(url)
            e = re.findall('<li.+?on ([^"]*).+?f="([^"]*)', u)
            e = [(i[0],i[1]) for i in e if 'ultramovie' not in i[1]]
            return e
        except:
            return
#Link provider and quality            
    def soccerstream(self, url):
        try:
            u = client.request(url)
            e = re.findall('(?s)class="clickable-row.+?f="([^"]*).+?quality="([^"]*).+?age="([^"]*).+?ageV.+?able">\n\s+([^\n]*)', u)
            return e
        except:
            return
            
    def linkmovie25(self, url):
        try:
            u = client.request(url).lower()
            e = re.findall('iframe src="([^"]*)', u)[0]
            return e
        except:
            return
            
    def movie2k(self, url):
        try:
            u = client.request(url)
            e = re.findall('<li.+?on ([^"]*).+?f="([^"]*)', u)
            e = re.findall('iframe src="([^"]*)', u)[0]
            return e
        except:
            return re.findall('(?s)id="tab-popular">.+?href="([^"]*)', u)[0]
