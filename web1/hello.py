#import wsgiref.handlers
bind="0.0.0.0:8080"
pythonpath='/etc/guricon.d/hello.py'
def wsgi_application(environ, start_response):

    resp = environ['QUERY_STRING'].split("&")
    resp = [item+"\r\n" for item in resp]

    status = '200 OK'
    headers = [
        ('Content-Type', 'text/plain')
    ]
    start_response(status, headers)
    print (resp)
    return [resp]

#if __name__ == '__main__':
#    wsgiref.handlers.CGIHandler.run(wsgi_application)