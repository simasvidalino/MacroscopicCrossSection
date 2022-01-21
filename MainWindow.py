import PySimpleGUI as sg
import WebScraping as ws
import os
import PromptControll as shell
import FilterFromNjoyOutput as filter

sg.theme('BluePurple')

def beginWindow():

    menu_def = [["Help", ["About...", "NJOY16 Manual...", "ENDF Manual...", "ENDF Site..."]]]

    frameEndf= [
                [sg.Text("On the internet:",  font='Roboto 10', size = (20,0), key = "web"), sg.Button("Go", size = (6,0), key = "webscraping")],
                [sg.Text("On this computer:",  font='Roboto 10', size = (20,0), key = "computer"), sg.Input(size = (15, 0), key = "endfNameFile")], #sg.FileBrowse(initial_folder = os.path.dirname(os.path.abspath(__file__)), size = (6,0), key = "browse")],
                ]

    frameRegions= [
                  [sg.Text("\nPlease, enter the number of material regions:")],
                  [sg.Spin([1,2,3,4,5,6,7,8,9,10], size=(3, 0), key="spinBox"), sg.Button("Ok", font="Roboto 8", size=(2, 0), key="okRegions", enable_events=True)]
                  ]

    layout   =  [
                [sg.Titlebar("Macroscopic Cross Sections", font='Roboto 10')],
                [sg.Frame("Material Region:", frameRegions, key="frameRegion")],
                [sg.Frame("Search file ENDF:", frameEndf)],
                [sg.Ok(font="Roboto 10", size=(8, 0), key="ok"), sg.Cancel(font="Roboto 10", size=(8, 0), key="cancel")],
                [sg.Menu(menu_def)]
                ]

    return sg.Window("Begin", layout, finalize = True, resizable = True)

def writeInputTextNjoy():
    layout = [
        [sg.Text("Input Njoy\n")],
        [sg.Radio("Open File", "inputChoise"), sg.Radio("Create File", "inputChoise")],
    ]
    return sg.Window("Njoy21", layout, finalize=True)

def windowRegionInput(counter):
    
    layout = [
            [sg.Text("Material Region: " + str(counter) + "\n", key="title")], 
            [sg.Text("Reaction", size = (8, 0)), sg.Input(size = (32, 0), key = "reaction")],
            [sg.Text("Target"  , size = (8, 0)), sg.Input(size = (32, 0), key = "target")],
            [sg.Text("\n")],
            [sg.Button("Previous", size = (8, 0),  key="previous"), sg.Button("Next", size = (8, 0), key="next"), sg.Button("Finish", size = (8, 0), key="finish")]
            ]
        
    return sg.Window("Macroscopic Cross Section", layout, finalize=True)

def main():
    cmd = shell.shellControll()
    target  = []
    reaction = []
    firstWindow = beginWindow()
    counter = 1
    spinBox = 1
    wasRegionsSet = False

    while True: #event loop
        window, event, inputData = sg.read_all_windows()
        print(event)

        menuHelp(cmd, event)
        
        if event in (sg.WIN_CLOSED, 'Exit', "cancel"):
            break

        if event == "finish":
            window.close()
            firstWindow["spinBox"].Update(int(spinBox))

            target[counter-1]   = inputData["target"] + ";"
            reaction[counter-1] = inputData["reaction"] + ";"

            target = ''.join(target)
            reaction = ''.join(reaction)

            print(target)
            print(reaction)

            if len(target) > 0 and reaction > 0:
                wasRegionsSet = True

            firstWindow._Show()
            
            #writeInputTextNjoy().force_focus()

        if event == "okRegions":
            counter  = 1
            reaction.clear()
            target.clear()
            spinBox = int(inputData["spinBox"])

            for i in range(0,(spinBox)):
                 reaction.append(0)
                 target.append(0)

            firstWindow.hide()
            windowRegionInput(counter)["previous"].Update(disabled = True)

        if event == "next":
            counter = counter + 1
            print(target)
            print(reaction)
            window.close()
            
            target[counter-2]   = inputData["target"] + ";"
            reaction[counter-2] = inputData["reaction"] + ";"

            if counter < spinBox:
                windowRegionInput(counter)
            else:
                windowRegionInput(counter)["next"].Update(disabled = True) 

        if event == "previous":
            counter = counter - 1
            print(target)
            print(reaction)
            window.close()

            target[counter]   = inputData["target"] + ";"
            reaction[counter] = inputData["reaction"] + ";"

            if counter == 1:
                windowRegionInput(counter)["previous"].Update(disabled = True)
            else:
                windowRegionInput(counter)

        if event == "webscraping" and wasRegionsSet:
            ws.WebScraping(target, reaction, "SIG") #SIG means cross section
            fileName = "OutputCrossSection" + target.replace(";", "") + ".txt"
            cmd.setFileNameENDF(fileName)
            

        if event == "ok" and wasRegionsSet:
            print(inputData["endfNameFile"])
            cmd.setFileNameENDF(inputData["endfNameFile"])
              
def menuHelp(cmd, event):

    if event == "NJOY16 Manual...":
        fileName = "njoy16Manual.pdf"
        cmd.viewFile(fileName)
    
    if event == "ENDF Manual...":
        fileName = "endfManual.pdf"
        cmd.viewFile(fileName)
        
    if event == "ENDF Manual...":
        fileName = "endfManual.pdf"
        cmd.viewFile(fileName)

    if event == "ENDF Site...":
        siteAddress = "https://www-nds.iaea.org/exfor/endf.htm"
        cmd.openWebSite(siteAddress)
  
headleWithUserInput = main()