#!/usr/bin/python

import time
from datetime import date, datetime

import pycurl

try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO


# query 2014
    # whole last year (2014)
since = '2014-01-01T00:00:00Z' # this is how github reads dates, first date.  
until = '2014-12-31T23:59:59Z'

print('Fetching D3 commit history since: ' + since)

#from bytes documentation.  
headers = {}
def header_function(header_line):
    header_line = header_line.decode('iso-8859-1')
    if ':' not in header_line:
        return
    name, value = header_line.split(':', 1)
    name = name.strip()
    value = value.strip()
    name = name.lower()
    headers[name] = value

# cURL fetch
def fetch(url):
    buffer = BytesIO() # what bytes url is writing to.  from pycurl documentation. 
    c = pycurl.Curl() 
    c.setopt(c.URL, url)
    c.setopt(c.WRITEFUNCTION, buffer.write)
    # Set our header function.
    c.setopt(c.HEADERFUNCTION, header_function)
    c.perform()
    c.close()

    save_filename = headers['etag'].replace('"', '') + '.json' #setting variable for filename
    print('Saving: ' + save_filename)
    f = open(save_filename, 'w') # builtin where you are opening the file with the save_filename, for writing.  
    f.write(buffer.getvalue()) #write what we got in buffer.  
    # Save in a file using the encoding we figured out.
    f.close()


fetch('https://api.github.com/repos/mbostock/d3/commits?since=' + since + '&until=' + until)

while headers['status'] == '200 OK':
    print headers
    if 'rel="next"' not in headers['link']: #from github tells if there is a next page.  
        break
    next_page = headers['link'].split('>', 1)[0].replace('<', '') #making it a proper url
    print('Fetching: ' + next_page)
    headers = {} #empty header object
    fetch(next_page) #calling fetch function.  


print("Finished fetching data.")



