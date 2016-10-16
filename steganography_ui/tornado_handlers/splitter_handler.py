import tornado.web
from tornado import template
import json

class SplitterHandler(tornado.web.RequestHandler):
    loader = template.Loader('./web')
    def post(self):
        print "got request for splitter"
        html = self.loader.load('splitter.html').generate()
        data = json.dumps({'html': html})
        self.write(data)

