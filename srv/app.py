#! /usr/bin/env python
import os
import traceback
from flask import Flask, request, jsonify, make_response
from fem_utils.master_file import find_master

app = Flask(__name__)

#test  curl -H "Content-Type: application/json"  -X POST -i -d '{"fpath":"/home/dreamcs/3dfiles/A320"}'  http://127.0.0.1:5000/api/findmasterfile
@app.route('/api/findmasterfile', methods=['POST'])
def main():

    if request.method == 'POST':
        args = request.get_json()
        fpath = args.get('fpath')
        print 'fpath =', fpath
        if fpath is None or len(fpath) == 0:
            return make_response('Bad arguments', 400)

        #if fpath is empty, return ...
        master_file_path = None
        try:
            master_file_path = find_master(fpath)
        except :
            print traceback.format_exc()
            return make_response("when find master file, it's error", 400)

        if master_file_path is None:
            return make_response(jsonify({'masterfile':'', 'status':'1'}), 200)
        else:
            return make_response(jsonify({'masterfile':master_file_path, 'status':'0'}), 200)

    
    return make_response('Bad Request', 400)


if __name__ == '__main__':
    app.run()
