import tornado.web
from tornado import template
import json
import decoder as detector

class DoDetection(tornado.web.RequestHandler):
    loader = template.Loader('./web')
    def post(self):
        print "Gonna do detection"
        print "recieved %d files " % len(self.request.files)

        recorded_file = self.request.files['recorded_file'][0]['body'].strip()
        original_file = self.request.files['original_file'][0]['body'].strip()

        name = self.request.files['original_file'][0]['filename'].strip()

        if 'spidey' in name:
            name = 'spidey'


        recorded_luma = eval(recorded_file)
        original_luma = eval(original_file)

        min_robustness = int(self.get_argument('min_robustness').strip())
        bucket_size = int(self.get_argument('bucket_size').strip())
        normal_size = int(self.get_argument('normal_size').strip())
        bitstring_size = int(self.get_argument('bitstring_size').strip())


        data = {'bucket_size': bucket_size, 'min_robustness_count': min_robustness,
                'normal_size': normal_size, 'bitstring_size': bitstring_size,
                'name': name}

        print "%d %d %d %d" % (min_robustness, bucket_size, normal_size, bitstring_size)

        # do the bitstring stuff
        bitstring_result =  detector.main_decoder(data, original_luma, recorded_luma)
        html = self.loader.load('detector.html').generate(bitstring=bitstring_result)


        self.write(html)


class DetectorHandler(tornado.web.RequestHandler):
    loader = template.Loader('./web')
    def post(self):
        print "got request for detector"
        html = self.loader.load('detector.html').generate(bitstring=None)
        data = json.dumps({'html': html})
        self.write(data)

