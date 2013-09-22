__author__ = 'ggercek'

from pymongo import Connection
from bson.objectid import ObjectId
import time
import os

connection = Connection('localhost', 27017)

_db = connection['ovizart']
_analysisCollection = _db.analysis
_users = _db.users

# TODO: Improve this module! Check the best practices as well as the attacks


def saveAnalysis(analysis):
    """Saves given analysis object.
    If the analysis _id attribute is None then the object will be inserted otherwise updated."""
    global _analysisCollection
    #d = analysis.__dict__
    d = todict(analysis)
    if analysis._id:
        # Update analysis object
        #_analysisCollection.update({'_id': ObjectId(unicode(d['_id']))}, d)
        d['_id'] = ObjectId(d['_id'])
        _analysisCollection.save(d)
        d['_id'] = str(d['_id'])
    else:
        del d['_id']
        # new analysis created insert to db
        id = _analysisCollection.insert(d)
        analysis._id = str(id)


def getAnalysis(id=None):
    """Returns the requested analysis object or list of analysis objects if id is now specified."""
    result = []
    if id:
        result.extend(_analysisCollection.find({'_id': ObjectId(unicode(id))}))
    else:
        result.extend(_analysisCollection.find())

    return result


def getStream(analysisId, searchCriteria=None):
    """Returns Stream objects of an analysis according to given searchCriteria"""

    result = []
    _analysis = _analysisCollection.find({'_id': ObjectId(unicode(id))})

    # TODO:Revise this part !!!
    # if searchCriteria:
    #     result.extend(_analysisCollection.find(searchCriteria))
    # else:
    #     result.extend()

    return result


def todict(obj, classkey=None):
    # Taken from stackoverflow: http://stackoverflow.com/questions/1036409/recursively-convert-python-object-graph-to-dictionary
    if isinstance(obj, dict):
        for k in obj.keys():
            obj[k] = todict(obj[k], classkey)
        return obj
    elif hasattr(obj, "__iter__"):
        return [todict(v, classkey) for v in obj]
    elif hasattr(obj, "__dict__"):
        data = dict([(key, todict(value, classkey)) for key, value in obj.__dict__.iteritems() if not callable(value) and not key.startswith('__')])
        if classkey is not None and hasattr(obj, "__class__"):
            data[classkey] = obj.__class__.__name__
        return data
    else:
        return obj


def addUser(username, password, name, surname, emailAddress):
    import datetime
    # Check for username, is in use?
    users = _users.find({'username': username})
    if users.count() > 0:
        return False
    else:
        result = _users.insert({'username': username, 'password': password, 'dayOfRegister:': time.time(),
                       'name': name, 'surname': surname, 'email': emailAddress})
        return True


def removeUser(username, password):
    result = _users.remove({'username': username, 'password': password})
    return result


def getUser(username, password):
    result = _users.find({'username': username, 'password': password}, {'_id': 1})
    if result.count() == 0:
        result = None
    else:
        result = str(result.next()['_id'])

    return result


def getUserByName(username):
    result = _users.find({'username': username}, {'_id': 1})
    if result.count() == 0:
        result = None
    else:
        result = str(result.next()['_id'])
    return result


def getUserById(userid):
    result = _users.find({'_id': ObjectId(userid)})
    if result.count() == 0:
        result = None
    else:
        result = result.next()
    return result


def getAnalysisByUserId(userid):
    result = []
    for a in _analysisCollection.find({'user': userid}, {'_id':1, 'status': 1, 'startTime':1, 'files':1}):
        a['_id'] = str(a['_id'])
        result.append(a)

    return result


def getAnalysisById(userid, analysisId):
    result = _analysisCollection.find({'user': userid, '_id': ObjectId(analysisId)})
    if result.count() == 0:
        return None
    else:
        result = result.next()
        result['_id'] = str(result['_id'])
        return result


def removeAnalysis(userid, analysisId):
    print 'remove:', _analysisCollection.remove({'user': userid, '_id': ObjectId(analysisId)})


def removeAllAnalysis():
    print 'drop:', _analysisCollection.drop()


def getPcap(userid, analysisId, streamKey):
    analysis = _analysisCollection.find({'user': userid, '_id': ObjectId(analysisId)},
                                    {'data._Data__tags.attachments': 1, 'data._Data__data.stream.key': 1,
                                     'data._Data__data.stream.pcapFileName': 1})

    # TODO: this must be changed!!!
    if analysis:
        while True:
            a = analysis.next()
            if a is None:
                break

            data = a['data']
            for a in data:
                if a['_Data__data']['stream']['key'] == streamKey:
                    return a['_Data__data']['stream']['pcapFileName']


def getAttachment(userid, analysisId, streamKey, filename):
    analysis = _analysisCollection.find({'user': userid, '_id': ObjectId(analysisId)},
                                    {'data._Data__tags.attachments': 1, 'data._Data__data.stream.key': 1,
                                     'data._Data__data.stream.outputFolder': 1})

    # TODO: this must be changed!!!
    if analysis:
        while True:
            a = analysis.next()
            if a is None:
                break

            data = a['data']
            for a in data:
                if a['_Data__data']['stream']['key'] == streamKey:
                    for f in a['_Data__tags']['attachments']:
                        if f[0] == filename:
                            return os.path.join(a['_Data__data']['stream']['outputFolder'], 'attachments', filename)

    return None


#if __name__ == '__main__':
#
#    print getPcap('5236a6141e75ed7ce17b4011', '523e1f711e75ed15d40ab6e5', '6_10.1.1.101_3188_10.1.1.1_80')
#