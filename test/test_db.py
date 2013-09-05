__author__ = 'ggercek'

from numpy.ma.testutils import assert_not_equal
from unittest import TestCase

from core import db
from core.data import Analysis


class TestDB(TestCase):

    def test_saveAnalysis(self):
        newAnalysis = Analysis()
        db.saveAnalysis(newAnalysis)
        print '_id:', newAnalysis._id
        assert_not_equal(newAnalysis._id, None)

    def test_userOperations(self):
        result = db.addUser(username="myUsername", password='myPassword', name="myName",
                            surname="mySurname", emailAddress="myEmailAddress@somewhere.com")

        assert result is True

        result = db.getUser("myUsername", "myPassword")
        assert result is not None

        result = db.removeUser("myUsername", "myPassword")
        assert result is None
