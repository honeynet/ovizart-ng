__author__ = "ggercek"

from ovizconf import UPLOAD_FOLDER
from ovizart import Ovizart
from core.webserver import API
import json
import os

@API(method="POST", url=r"^/login$", isAuth=False)
def login(data):
    response = {"Status": "FAILED"}
    # Check user name
    username = data['username']
    password = data['password']

    # TODO: Replace this dummy check
    if username == "admin" and password == "admin":
        data['cookie'].isAuth = True
        data['cookie'].data['ovizart'] = Ovizart()
        response["Status"] = "OK"

    return json.dumps(response)

#@API(method="POST", url=r"^/upload$")
@API(method="POST", url=r"^/upload/(?P<filename>.+)$")
def upload(data):
    wanted_filename = data['filename']
    actual_filename = data['uploaded_filename']
    filesize = os.path.getsize(actual_filename)
    p = os.path.join(UPLOAD_FOLDER, wanted_filename)

    # TODO: Check file type for more intense way
    tmp = p
    ext = p.rfind('.pcap')
    if ext == -1:
        ext = p.rfind('.cap')
        if ext == -1:
            # Can not process file !!!!
            # Remove file and invalided cookie
            data['cookie'].isExpired = True
            os.remove(actual_filename)
            return json.dumps({'Status': 'FAILED', 'Description': 'Invalid file type!!!!'})

    counter = 1
    while os.path.exists(tmp):
        tmp = "%s_%d%s" % (p[:ext], counter, p[ext:])
        counter += 1
    p = tmp

    wanted_filename = os.path.basename(p)

    os.rename(actual_filename, p)
    data['cookie'].data['ovizart'].setInputFile(p)

    response = {"Status": "OK", "Filesize": filesize, "filename": wanted_filename}
    print '[upload] response: ', json.dumps(response)
    return json.dumps(response)

@API(method="POST", url=r"^/set/config$")
def set_config(data):
    # Set config parameters
    pass


@API(method="POST", url=r"^/start$")
def start(data):
    # Start the analyzer and return the analysis id
    analysis = data['cookie'].data['ovizart'].startASync()
    return json.dumps({'AnalysisId': analysis._id, 'Status': analysis.status})


@API(method="POST", url=r"^/stop$")
def stop(data):
    # Stop the analysis based on id
    pass
