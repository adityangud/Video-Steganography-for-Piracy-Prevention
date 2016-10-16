import tornado.web
from tornado import template
import os
import json
import glob
import plotter
from custom_utils import *


class CompareFilesHandler(tornado.web.RequestHandler):
    loader = template.Loader('./web')
    def post(self):
        print "got request to compare files"

        # get arguments
        files_to_compare = self.get_argument('files', default=None)
        num_selects = self.get_argument('num_selects', default=0)

        if not files_to_compare:
            data = json.dumps({'html': '<div> no files selected</div>'})
            self.write(data)
            return

        files_to_compare = [i.strip() for i in files_to_compare.split(',')]
        files_to_compare = [i for i in files_to_compare if i != '']

        documents = []

        for _file in files_to_compare:
            files_with_prefix = glob.glob('uploads/%s' % _file)
            if not files_with_prefix:
                documents.append(file_not_found(_file))
                continue

            if not renderable_as_graph(_file):
                documents.append(file_not_supported(_file))
                continue

            documents.append(file_supported(_file))

        # generate images for them
        for document in documents:
            if not document['compatiable']:
                document['image_link'] = '/images/not_found.jpg'
                continue

            images = map(os.path.basename, glob.glob('images/*.png'))
            images = [i[:-4] for i in images]

            name, ext = os.path.splitext(document['name'])
            if name not in images:
                # plotting it
                plotter.plotter('uploads/%s' % document['name'], 'images/%s' % (name + '.png'))

            document['image_link'] = '/images/%s' % (name + '.png')

        operations = AVAILABLE_TRANSFORMATIONS
        col_width = 90.0 / len(documents)

        html = self.loader.load('compare.html').generate(documents=documents, operations=operations, col_width=col_width, num_selects=num_selects)

        data = json.dumps({'html': html})
        self.write(data)

