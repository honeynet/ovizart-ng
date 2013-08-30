from numpy.ma.testutils import assert_not_equal
from core.db import saveAnalysis

__author__ = 'ggercek'

from unittest import TestCase

from core import db
from core.data import Analysis


class TestDB(TestCase):

    def test_saveAnalysis(self):
        newAnalysis = Analysis()
        db.saveAnalysis(newAnalysis)
        print '_id:', newAnalysis._id
        assert_not_equal(newAnalysis._id, None)
