__author__ = 'ggercek'

from pymongo import Connection

connection = Connection('localhost', 27017)

_db = connection['ovizart']
_analysisCollection = _db.analysis


def saveAnalysis(analysis):
    """Saves given analysis object.
    If the analysis _id attribute is None then the object will be inserted otherwise updated."""
    global _analysisCollection
    #d = analysis.__dict__
    d = todict(analysis)
    print 'dict:', d
    if analysis._id:
        # Update analysis object
        _analysisCollection.update({'_id': analysis._id}, d)
    else:
        del d['_id']
        # new analysis created insert to db
        id = _analysisCollection.insert(d)
        d['_id'] = id


def getAnalysis(id=None):
    """Returns the requested analysis object or list of analysis objects if id is now specified."""
    result = []
    if id:
        result.append(_analysisCollection.find({'_id': id}))
    else:
        result.extend(_analysisCollection.find())

    return result


def getStream(analysisId, searchCriteria=None):
    """Returns Stream objects of an analysis according to given searchCriteria"""

    result = []
    if searchCriteria:
        result.extend(_analysisCollection.find(searchCriteria))
    else:
        result.extend(_analysisCollection.find())

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