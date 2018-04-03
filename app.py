#!/usr/bin/env python3
import os
import tornado.ioloop
import tornado.web
import tornado.log

import requests


from jinja2 import \
  Environment, PackageLoader, select_autoescape

ENV = Environment(
  loader=PackageLoader('weather', 'templates'),
  autoescape=select_autoescape(['html', 'xml'])
)

class TemplateHandler(tornado.web.RequestHandler):
  def render_template (self, tpl, context):
    template = ENV.get_template(tpl)
    self.write(template.render(**context))

class MainHandler(TemplateHandler):
  def get (self):
    template = ENV.get_template('index.html')
    self.write(template.render())

class WeatherHandler(TemplateHandler):
  def get (self):
    template = ENV.get_template('weather.html')
    self.write(template.render())

  def post (self):
    city = self.get_body_argument('city')


    url = "http://api.openweathermap.org/data/2.5/weather"

    querystring = {"q":city,"APIKEY":"2d9a500b15c2b6ea12cd0298f2df8696",'units':'imperial'}

    headers = {
        'cache-control': "no-cache",
        'postman-token': "93bd509e-5f98-e8b9-540d-2c8a019ee099"
        }

    r = requests.request("GET", url, headers=headers, params=querystring)

    r.json()

    template = ENV.get_template('weather.html')

    self.write(template.render({'data': r.json()}))


def make_app():
  return tornado.web.Application([
    (r"/", MainHandler),
    (r"/weather", WeatherHandler),
    (r"/static/(.*)",
      tornado.web.StaticFileHandler, {'path': 'static'}),
  ], autoreload=True)

if __name__ == "__main__":
  tornado.log.enable_pretty_logging()
  app = make_app()
  app.listen(int(os.environ.get('PORT', '8888')))
  tornado.ioloop.IOLoop.current().start()
