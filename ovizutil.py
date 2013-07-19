__author__ = 'ggercek'


def createFolder(outputFolder):
    # TODO: make this cross platform or convert it to python-only portable code
    import subprocess
    subprocess.check_output(['mkdir', '-p', outputFolder])