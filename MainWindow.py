import PySimpleGUI as sg
import WebScraping as ws
#from tkinter import filedialog as fd

def firstWindow():

    layout = [
            [sg.Text("Welcome\n")],
            [sg.Text("Please, to use this app you must have internet.")],
            [sg.Button("Continue", size = (8, 0), key = "internet"), 
            sg.Button("Stop", size = (8, 0), key = "noInternet")]
            ]
    return sg.Window("Begin", layout, finalize=True)

def windowRegionInput(counter):

    layout = [
            [sg.Text("Material Region: " + str(counter) + "\n")], 
            [sg.Text("Reaction", size = (8, 0)), sg.Input(size = (32, 0), key = "reaction")],
            [sg.Text("Target"  , size = (8, 0)), sg.Input(size = (32, 0), key = "target")],
            [sg.Text("\n")],
            [sg.Button("return", size = (8, 0)), sg.Button("Add Region", size = (8, 0)), sg.Button("Finish", size = (8, 0))]
            ]
        
    return sg.Window("Macroscopic Cross Section", layout, finalize=True)

def writeInputTextNjoy():
    layout = [
        [sg.Text("Input Njoy\n")],
        [sg.Radio("Open File", "inputChoise"), sg.Radio("Create File", "inputChoise")],
    ]

    return sg.Window("Njoy21", layout, finalize=True)

"""def inputNjoy(): #optative part of project

    layout = [
            [sg.Text("Njoy Input:\nChose Njoy Modules")],
            [sg.Checkbox("Moder"), sg.Checkbox("Reconr"), sg.Checkbox("Broadr"), sg.Checkbox("Groupr"),
             sg.Checkbox("Heatr"), sg.Checkbox("Gaminar"), sg.Checkbox("Gaminar")
            ] 
            [sg.Text("Reaction", size = (8, 0)), sg.Input(size = (32, 0), key = "reaction")],
            [sg.Text("Target"  , size = (8, 0)), sg.Input(size = (32, 0), key = "target")],
            [sg.Text("\n")],
            [sg.Button("return", size = (8, 0)), sg.Button("Add Region", size = (8, 0)), sg.Button("Finish", size = (8, 0))]
            ]
    return sg.Window("Njoy21", layout, finalize=True)"""

def handleWithUserInput():
    target  = []
    reaction = []
    beginWindow, mainWindow = firstWindow(), None
    beginWindow.force_focus()
    counter = 1

    while True:
        window, event, inputData = sg.read_all_windows()
        print(event)
        if event == "noInternet" or event == None:
            break

        if event == "Add Region" or event == "internet":
            windowRegionInput(counter).force_focus()

            if inputData != {}:
                target.append(inputData["target"] + ";")
                reaction.append(inputData["reaction"] + ";")
                counter = counter + 1
            beginWindow.hide()

        if event == "Finish":

            if inputData != {}:
                target.append(inputData["target"])
                reaction.append(inputData["reaction"])
            
            target = ''.join(target)
            reaction = ''.join(reaction)
            ws.WebScraping(target, reaction, "SIG") #SIG means cross section
            writeInputTextNjoy().force_focus()

        if event == "Open File":
            openFile()

def openFile():
    sg.FileBrowse("Open File", file_types = "txt")
    print("Escolheu abrir")

        
headleWithUserInput = handleWithUserInput()