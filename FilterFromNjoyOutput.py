import re  

class filter():
    
    def __init__(self, nameOutputFileFromNjoy, isotopesPerRegion): #python builder

        self.nameOutputFileFromNjoy = nameOutputFileFromNjoy
        self.isotopesPerRegion = isotopesPerRegion
        self.crossSection = [] # Dictionary
        self.scattering = []
    
    def filterNjoyFile(self):

        file = open(self.nameOutputFileFromNjoy, "r")

        key1 = '\\bmf'  # O \b é um meta-caractere para encontrar uma correspondência no início ou no final de uma palavra
        key2 = '\\bmt'  # key1 e key2 identifica o começo de algum dado do Njoy
        key3 = 'mat to be processed'  # It can indentify when there is a new isotope
        nIsotope = 0
        nReaction = 0
        crossSectionPerMaterial = []
        scatteringMatrixPerMaterial = []

        for line in file:

            if re.search(key3, line):
                nIsotope = nIsotope + 1  # count isotopes number in the outputNjoy
                material = line.split()[-1]  # save the mat number to be used in the dictionary

            if re.search(key1, line) and re.search(key2, line) and not re.search('error', line):

                crossSection = []  
                scattering = []
                crossSectionDictionary = {}
                
                for j in range(0, 5):  # skip 4 lines for scattering
                    line = file.readline()

                while not len(line) <= 2:  # while not find a empty line

                    if 'flx' in line:
                        pass  # Ignore output data groupr Njoy 
                    else:
                        if len(line) < 59:
                            crossSection.append(
                                self.formatValue(line.rstrip('\n').split())[1])
                            
                        else:
                            scattering.append(
                                self.formatValue(line.rstrip('\n').split()))

                    line = file.readline()

                if not crossSection == []:
                    crossSectionDictionary[material] = crossSection
                    crossSectionPerMaterial.append(crossSectionDictionary)
                    print(crossSectionDictionary)

                if not scattering == []:
                    scatteringMatrixPerMaterial.append(self.createScatteringDictionary(material, scattering, 3, 29))
                    
                nReaction = nReaction + 1

                line = file.readline()
                print("\n\n")

        self.findError(nIsotope, nReaction)
 
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
                lineOutput.append(line[n].replace("-", "E-").replace("E-", "-", 1))

            elif qt_negative == 1 and qt_positive == 0:
                lineOutput.append(line[n].replace("-", "E-"))

            elif qt_negative == 0 and qt_positive == 0:
                lineOutput.append(line[n])

            else:
                lineOutput.append(line[n].replace("+", "E+"))

        return lineOutput

    def createScatteringDictionary(self, material, scattering, legendreOrder, nEnergyGroup):
        dictionary = {}
        data = [0.]*(legendreOrder + 1) # fill matrix with zero
        scatteringMatrix = [ [ data for y in range(nEnergyGroup+1) ] for x in range(nEnergyGroup+1) ]

        for values in scattering:
            ge1 = int(values[0])
            ge0 = int(values[1])

            for l in range(legendreOrder + 1): # ignore 2 values of energy group
                scatteringMatrix[ge1 - 1][ge0 - 1][l] = float(values[l + 2])

        dictionary[material] = scatteringMatrix
        return dictionary
            
obj = filter("Saida.txt", 0)
obj.filterNjoyFile()
