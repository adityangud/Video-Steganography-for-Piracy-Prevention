from tornado import template
import tornado.web
import json
import time
import os

from custom_utils import *

class ArchiveHandler(tornado.web.RequestHandler):

    loader = template.Loader('./web')

    def post(self):
        self.loader = template.Loader('./web')
        documents = get_documents()
        html_data = self.loader.load('archives.html').generate(documents=documents)
        data = json.dumps({'html': html_data})
        self.write(data)

