import os, stat


def installNjoy21():
    filePath = os.path.dirname(os.path.abspath(__file__))
    os.chmod(filePath + "\installNjoy21.sh", stat.S_IXOTH)
    os.system("cd " + filePath)
    os.system(".\installNjoy21.sh")

def inputNjoy():
    

installNjoy21()