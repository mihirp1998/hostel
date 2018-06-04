import httplib
c = httplib.HTTPSConnection("https://www.html2-f.scribdassets.com/vok4xl9a82ga3tj/pages/1070-6eac73f2f7.jsonp")
c.request("GET", "/")
response = c.getresponse()
print response.status, response.reason
data = response.read()
print data
