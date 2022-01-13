import os, stat

#https://t2.lanl.gov/nis/endf/intro05.html

class shellControll():

    def __init__(self, fileNameENDF):
        self.filePath = os.path.dirname(os.path.abspath(__file__))
        self.fileNameENDF = fileNameENDF
        print("\n\nPasta")
        print(self.filePath)

        if not os.path.isdir("NJOY21"):
            self.installNjoy21()

    def installNjoy21(self):
        
        os.chmod(self.filePath + "\installNjoy21.sh", stat.S_IXOTH)
        os.system("cd " + self.filePath)
        os.system(".\installNjoy21.sh")

    def setFileNameENDF(self, nameFile):
        self.nameFile = nameFile

shellControll("endfb")