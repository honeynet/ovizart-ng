
__author__ = "ggercek"

from unittest import TestCase

from core import MissingMethodException, MissingArgumentException
from core.decorators import DataSource, Tagger, Analyzer, Reporter


class TestGenericDecorator(TestCase):

    def test_invalidDataSourceDefinition(self):
        with self.assertRaises(MissingMethodException):
            @DataSource(tags="test")
            class InvalidDataSource:
                pass

    def test_invalidArgumentDataSourceDefinition(self):
        with self.assertRaises(MissingArgumentException):
            @DataSource(tags="test")
            class InvalidAnalyzers:
                def parse(self):
                    pass

    def test_invalidTaggerDefinition(self):
        with self.assertRaises(MissingMethodException):
            @Tagger(tags="test")
            class InvalidTagger:
                pass

    def test_invalidArgumentTaggerDefinition(self):
        with self.assertRaises(MissingArgumentException):
            @Tagger(tags="test")
            class ValidTagger:
                def tag(self):
                    pass

    def test_invalidAnalyzerDefinition(self):
        with self.assertRaises(MissingMethodException):
            @Analyzer(tags="test")
            class InvalidAnalyzers:
                pass

    def test_invalidArgumentAnalyzerDefinition(self):
        with self.assertRaises(MissingArgumentException):
            @Analyzer(tags="test")
            class ValidAnalyzers:
                def analyze(self):
                    pass

    def test_invalidReporterDefinition(self):
        with self.assertRaises(MissingMethodException):
            @Reporter(tags="test")
            class InvalidReporter:
                pass

    def test_invalidArgumentReporterDefinition(self):
        with self.assertRaises(MissingArgumentException):
            @Reporter(tags="test")
            class ValidReporter:
                def report(self):
                    pass
