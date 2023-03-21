### w5.py     # coding=utf-8  #注意這註解有特別意義, 還有 utf-8 的 - 減號不可省喔
from flask import Flask
from flask import redirect

app = Flask(__name__)
@app.route("/")
def webRoot( ):
   return '<font color=Red size=7>Hello World!  &nbsp; &nbsp; 這是網站喔 !</font>'
@app.route('/bulb')
@app.route('/bulb/')
@app.route('/Bulb')
def bulb():   #注意 function name 可隨意, 但不可以重複(廢話:-)
  return redirect('/static/ggyy/index.html')

@app.route('/rctl/')
@app.route('/Remote_control/')
def remote_control():   #注意 function name 可隨意, 但不可以重複(廢話:-)
  return redirect('/static/rcm/index.html')


app.run('0.0.0.0' , port=80)