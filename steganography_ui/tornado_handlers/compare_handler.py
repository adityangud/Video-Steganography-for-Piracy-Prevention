import tornado.web
from tornado import template
import json

from custom_utils import *

class CompareHandler(tornado.web.RequestHandler):
    loader = template.Loader('./web')
    def post(self):
        print "got request for overview"
        documents = get_documents()
        print documents
        html = self.loader.load('compare_page.html').generate(documents=documents)

        data = json.dumps({'html': html})
        self.write(data)

