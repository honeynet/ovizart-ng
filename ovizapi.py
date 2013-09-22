__author__ = "ggercek"

from ovizconf import UPLOAD_FOLDER
from ovizconf import DYNAMIC_ANALYZER_FOLDER
from ovizart import Ovizart
from core.webserver import API
from core.webserver import ACTION_SERVE_FILE
import json
import os
from core import db
import shutil


@API(method="POST", url=r"^/login$", isAuth=False)
def login(data):
    response = {"Status": "FAILED"}
    # Check user name
    username = data['username']
    password = data['password']

    userid = db.getUser(username, password)
    if userid:
    #if username == "admin" and password == "admin":
        data['cookie'].isAuth = True
        data['cookie'].data['ovizart'] = Ovizart()
        data['cookie'].data['userid'] = userid
        response["Status"] = "OK"
        response["username"] = username
        response["userid"] = userid

    return json.dumps(response)


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


@API(method="GET", url=r"^/pcap/(?P<analysisId>.+)/(?P<streamKey>.+)$")
def download_pcap(data):
    userid = data['cookie'].data['userid']
    analysisId = data['analysisId']
    streamKey = data['streamKey']
    originalFilePath = db.getPcap(userid, analysisId, streamKey)
    return ACTION_SERVE_FILE, originalFilePath


@API(method="GET", url=r"^/attachment/(?P<analysisId>.+)/(?P<streamKey>.+)/(?P<filePath>.+)$")
def download_attachment(data):
    userid = data['cookie'].data['userid']
    analysisId = data['analysisId']
    filepath = data['filePath']
    streamKey = data['streamKey']
    originalFilePath = db.getAttachment(userid, analysisId, streamKey, filepath)
    return ACTION_SERVE_FILE, originalFilePath


@API(method="GET", url=r"^/reassembled/(?P<analysisId>.+)/(?P<streamKey>.+)/(?P<trafficType>[012])$")
def download_reassembled(data):

    userid = data['cookie'].data['userid']
    analysisId = data['analysisId']
    trafficType = data['trafficType']
    streamKey = data['streamKey']

    # Check the user has right to download the file.
    originalFilePath = db.getReassembledTraffic(userid, analysisId, streamKey, trafficType)

    return ACTION_SERVE_FILE, originalFilePath


@API(method="POST", url=r"^/set/config$")
def set_config(data):
    # Set config parameters
    pass


@API(method="POST", url=r"^/start$")
def start(data):
    # Start the analyzer and return the analysis id
    userid = data['cookie'].data['userid']
    analysis = data['cookie'].data['ovizart'].startASync(userid)
    data['cookie'].data['ovizart'] = Ovizart()
    return json.dumps({'AnalysisId': analysis._id, 'Status': analysis.status})


@API(method="POST", url=r"^/stop$")
def stop(data):
    # Stop the analysis based on id
    pass


@API(method="GET", url=r"^/analysis$")
def get_analysisList(data):
    userid = data['cookie'].data['userid']
    analysisList = db.getAnalysisByUserId(userid)
    return json.dumps(analysisList)


# TODO: Merge this 2 in one !!!
@API(method="GET", url=r"^/analysis/(?P<analysisId>.+)$")
def get_analysisDetails(data):
    userid = data['cookie'].data['userid']
    analysisId = data['analysisId']
    analysisDetails = db.getAnalysisById(userid, analysisId)
    return json.dumps(analysisDetails)


@API(method="DELETE", url=r"^/analysis/(?P<analysisId>.+)$")
def removeAnalysis(data):
    userid = data['cookie'].data['userid']
    analysisId = data['analysisId']
    analysisDetails = db.getAnalysisById(userid, analysisId)
    # Remove the folders as well
    #analysisDetails
    print 'Uploaded files'
    for f in analysisDetails['files']:
        os.remove(f['filename'])
    shutil.rmtree(analysisDetails['config']['output_folder'])

    db.removeAnalysis(userid, analysisId)
    analysisDetails = {'Status': 'OK'}
    return json.dumps(analysisDetails)


@API(method="PUT", url=r"^/analyzer/(?P<filename>.+)$")
def add_analyzer(data):
    userid = data['cookie'].data['userid']
    wanted_filename = data['filename']
    actual_filename = data['uploaded_filename']
    filesize = os.path.getsize(actual_filename)
    p = os.path.join(DYNAMIC_ANALYZER_FOLDER, wanted_filename)
    # TODO: Check file type for more intense way
    tmp = p
    ext = p.rfind('.py')
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
    # dynamically register the analyzer
    dotIndex = wanted_filename.rfind('.')
    module_name = 'analyzer.dynamic.%s' % wanted_filename[:dotIndex]
    __import__(module_name)

    return json.dumps({'Status': 'OK', "filename": wanted_filename})
