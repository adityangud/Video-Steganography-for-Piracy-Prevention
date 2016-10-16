import tornado.web
from tornado import template
import json

class EmbedderHandler(tornado.web.RequestHandler):
    loader = template.Loader('./web')
    def post(self):
        print "got request for embedder"
        html = self.loader.load('embedder.html').generate()
        data = json.dumps({'html': html})
        self.write(data)

