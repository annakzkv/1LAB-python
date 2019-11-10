import os
import json
from flask import Flask, render_template, request, send_file, redirect
app = Flask(__name__)
app.debug = True

def path_to_dict(path):
    d = {'name': os.path.basename(path)}
    if os.path.isdir(path):
        d['type'] = "directory"
        d['path'] = path
        d['children'] = [{"name": os.path.basename(os.path.join(path,i)), "type": "folder" if os.path.isdir(os.path.join(path,i)) else "file"} for i in os.listdir(path)]
    else:
        d['type'] = "file"
        d['path'] = path
    return d

@app.route('/')
def index():
    curdir = request.args['d']
    return render_template('index.html',json = json.dumps(path_to_dict(curdir)))

@app.route("/create")
def create():
    curdir = request.args['d']
    os.makedirs(curdir)
    return redirect('/?d='+os.path.dirname(curdir))

@app.route('/delete')
def delete():
    curdir = request.args['d']
    os.removedirs(curdir)
    return redirect('/?d='+os.path.dirname(curdir))

@app.route('/download', methods=['GET'])
def download():
    curdir = request.args['d']
    return send_file(curdir, as_attachment=True, attachment_filename=curdir.rsplit('/', 1)[-1])

if __name__ == '__main__':
    app.run()
