import io
import json
import traceback
from httplib import HTTPMessage
from urllib import addinfourl
from urlparse import urlparse, parse_qsl



class BypassContent(object):

    def response(self, url, bypass_content):  # bypass_content: { url1: [content, headers],
        try:
            data = json.loads(bypass_content)
            for key in data.keys():
                data[self.get_sorted_url(key)] = data[key]

            sorted_url = self.get_sorted_url(url)
            if url in data or sorted_url in data:
                d = data.get(url) or data.get(sorted_url)
                fp = io.BytesIO(d[0].encode('utf-8'))
                headers = HTTPMessage(io.StringIO(unicode(d[1])), 0)
                # for head in d[1].split("\n"):
                #     xy = head.split(":")
                #     headers.addheader(xy[0].strip(), xy[1].strip())

                url = url
                code = 200
                msg = 'OK'
                res = addinfourl(fp, headers, url, code)
                print('Request Bypassed for url -> ' + url)
                return res
            else:
                print('Request Skipped for url -> ' + url + 'Fetching using requests')
                import requests
                r = requests.get(url)
                fp = io.BytesIO(r.text.encode('utf-8'))
                headers = HTTPMessage(io.StringIO(unicode(r.headers)), 0)
                res = addinfourl(fp, headers, url, 200)
                return res
        except Exception as e:
            print('Request Exception for url -> ' + url)
            traceback.print_exc()
            return None

    def get_sorted_url(self, url):
        sorted_url = urlparse(url)
        query_dict = dict(parse_qsl(sorted_url.query))
        qs = "&".join("{}={}".format(a, query_dict[a]) for a in sorted(query_dict))
        sorted_url = url.split("?")[0] + "?" + qs
        return sorted_url
