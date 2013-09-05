__author__ = 'ggercek'

from pymongo import Connection
from bson.objectid import ObjectId

connection = Connection('localhost', 27017)

_db = connection['ovizart']
_analysisCollection = _db.analysis
_users = _db.users


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
        result = _users.insert({'username': username, 'password': password, 'dayOfRegister:': datetime.datetime.now(),
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


def getUserById(userid):
    result = _users.find({'_id': ObjectId(userid)})
    if result.count() == 0:
        result = None
    else:
        result = result.next()
    return result