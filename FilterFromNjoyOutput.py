import re  
import MacroscopicCrossSection as mc

class filter():
    
    def __init__(self, nameOutputFileFromNjoy, isotopesList): #python builder

        self.nameOutputFileFromNjoy = nameOutputFileFromNjoy
        self.isotopesList = isotopesList
        self.crossSection = [] 
        self.scattering = []

    def filterNjoyFile(self):

        file = open(self.nameOutputFileFromNjoy, "r")

        key1 = '\\bmf'  # The \b is a metacharacter to find a match at the beginning or end of a word
        key2 = '\\bmt'  # key1 e key2 identifies the beginning of some Njoy data
        key3 = 'mat to be processed'  # It can indentify when there is a new isotope
        nIsotope = 0
        nReaction = 0
        crossSectionDictionary = {}
        scatteringDictionary = {}

        for line in file:

            if re.search(key3, line):
                isMaterialInList = line.split()[-1] in self.isotopesList

                if isMaterialInList:
                    material = line.split()[-1] # save the mat number to be used in the dictionary
                    nIsotope = nIsotope + 1  # count isotopes number in the outputNjoy

            if re.search(key1, line) and re.search(key2, line) and not re.search('error', line) and isMaterialInList:
                crossSection = [[]]  
                scattering = []

                for j in range(0, 5):  # skip 4 lines for scattering
                    line = file.readline()

                while not len(line) <= 2:  # while not find a empty line

                    if 'flx' in line:
                        pass  # Ignore flux data in mt  1 Total
                    else:
                        if len(line) < 59:
                            crossSection[0].append(
                                self.formatValue(line.rstrip('\n').split())[1])

                        else:
                            scattering.append(
                                self.formatValue(line.rstrip('\n').split()))

                    line = file.readline()

                if not crossSection == []:

                    if material in crossSectionDictionary.keys():
                        list = crossSectionDictionary[material] 
                        list = list + crossSection
                        crossSectionDictionary[material] = list
                    else:
                        crossSectionDictionary[material] = crossSection

                if not scattering == []:
                    scatteringDictionary[material] = scattering

                nReaction = nReaction + 1
                line = file.readline()

        self.findError(nIsotope, nReaction)

        mc.macroscopicCrossSection(self.isotopesList, [["725", "625", "825"], ["725"]], 
        crossSectionDictionary, scatteringDictionary, {'625': 2.1, '725': 1.5, '825': 0.5}) #Build object
        
        file.close()
    
    def findError(self, nIsotope, nReaction):
        n = nReaction/nIsotope # n must be a integer number 
        if not ((n) - (int(n))) == 0:
            print("Some reaction was not processed correctly by NJOY\n")
            exit
 
    def formatValue(self, line):
        lineOutput = []

        for n in range(0, len(line)):
            qt_negative = len([c for c in line[n] if c == '-'])
            qt_positive = len([c for c in line[n] if c == '+'])

            if qt_negative == 2:
                lineOutput.append(float(line[n].replace("-", "E-").replace("E-", "-", 1)))

            elif qt_negative == 1 and qt_positive == 0:
                lineOutput.append(float(line[n].replace("-", "E-")))

            elif qt_negative == 0 and qt_positive == 0:
                lineOutput.append(float(line[n]))

            else:
                lineOutput.append(float(line[n].replace("+", "E+")))

        return lineOutput

            
obj = filter("Saida.txt", ["625", "725", "825"])
obj.filterNjoyFile()