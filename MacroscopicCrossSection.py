from decimal import *
getcontext().prec = 10


class macroscopicCrossSection():

    def __init__(self, materialList, region, crossSection, scatteringCrossSection, density):
        self.density       = density       #density = {'625': 2.1, '725': 1.5, '825': 0.5}
        self.region        = region        #region = {1: ["725", "225"], 2: ["725"]}
        self.crossSection  = crossSection  #dict = {'225': ['1.62794E+3', '9.07081E+2'], '725': ['3.81634E+0', '3.80073E+0'], '825': ['3.79641E+0', '3.79483E+0']}
        self.scattering    = scatteringCrossSection
        self.materialList  = materialList  #["725", "825", "625"]

        self.absortionCrossSection()
        self.scatteringCrossSection()

    def absortionCrossSection(self) :
        macroscopicCrossSection = []

        for isotope in self.materialList: #multiply all value by constant
           self.crossSection[isotope] = [ [ value*(self.density[isotope] ) for value in reaction] for reaction in self.crossSection[isotope] ]
        
        for isotopes in self.region:
            if len(isotopes) > 1:
                x = [self.crossSection[isotope] for isotope in isotopes] 
                y = [sameReaction for sameReaction in zip(*x)] 
                aux = []
                for reaction in y:
                    aux.append([sum(group) for group in zip(*reaction)]) #sum all materials
                macroscopicCrossSection.append(aux)
            else:
                macroscopicCrossSection.append(self.crossSection[isotopes[0]])
            
        return macroscopicCrossSection

    def createAuxiliarScatteringMatrix(self):
        matrix = []

        for i in range(29):
            a = []
            for j in range(29):
                b = []
                for l in range(4):
                    b.append(0)
                a.append(b)
            matrix.append(a)
        return matrix


    def scatteringCrossSection(self):

        for isotope in self.scattering:
            aux1 = []
            for valuesPerLegendre in self.scattering[isotope]:
                aux2 = []
                for i in range(2, len(valuesPerLegendre)):
                    aux2.append(valuesPerLegendre[i]*1) #self.density[isotope])

                valuesPerLegendre = valuesPerLegendre[:2] + aux2
                aux1.append(valuesPerLegendre)
            self.scattering[isotope] = aux1
        

        macroscopicScatteringCrossSection = []

        for isotopes in self.region:
            matrix = self.createAuxiliarScatteringMatrix()
            if len(isotopes) > 1:
                x = [self.scattering[isotope] for isotope in isotopes]
                for mat in x:
                    for l in mat:
                        for i in range(len(l)-2):
                             sum = matrix[ int(l[0]-1) ][ int(l[1]-1) ][i] + l[i+2]
                             print(l,  matrix[ int(l[0]-1) ][ int(l[1]-1) ][i], sum)
                             #matrix[ int(l[0]-1) ][ int(l[1]-1) ][i] = sum
            else:
                for l in self.scattering[isotopes[0]]:
                    matrix[ int(l[0]-1) ][ int(l[1]-1) ] = l[2:]
                    print(l, matrix[ int(l[0]-1) ][ int(l[1]-1) ])

            macroscopicScatteringCrossSection.append(matrix) 

        return macroscopicScatteringCrossSection             
                   
                
  
                
