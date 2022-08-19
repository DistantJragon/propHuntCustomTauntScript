import os
import sys


class Taunt:
    def __init__(self):
        self.name = ""
        self.fileName = ""
        self.path = ""  # Relative to sound folder
        self.team = 1  # 0 = Hunters, 1 = Props
        self.category = ""


if __name__ == "__main__":
    directoryOfThisPythonScript = os.getcwd()  # Might need this later
    # Directory paths are strings
    # os.chdir() to change working directory
    pathOfTauntFolder = "D:\\SteamLibrary\\gmoddistantserver\\garrysmod\\gamemodes\\prop_hunt\\content\\sound\\distantserver_custom_phtaunts"
    tauntFolderName = os.path.basename(pathOfTauntFolder)
    firstLevelDirs = os.listdir(pathOfTauntFolder)
    categoriesFirst = True  # Keeps track of whether taunt directory goes category/1/taunt.mp3 or 1/category/taunt.mp3
    if len(firstLevelDirs) == 2 and firstLevelDirs[0] == "1" and firstLevelDirs[1] == "2":
        categoriesFirst = False
    tauntList = []
    categoryDictionary = {}

    # Get all taunts as objects in a single list
    tempCategory = ""
    tempTeam = "1"
    tempSecondLevelDirs = []
    tempFiles = []
    tempPath = tauntFolderName
    for firstLvlDir in firstLevelDirs:
        os.chdir(pathOfTauntFolder)
        tempSecondLevelDirs = os.listdir(firstLvlDir)
        os.chdir(firstLvlDir)
        for secondLvlDir in tempSecondLevelDirs:
            os.chdir(pathOfTauntFolder)
            os.chdir(firstLvlDir)
            tempFiles = os.listdir(secondLvlDir)
            os.chdir(secondLvlDir)
            for file in tempFiles:
                if file[-4:] == ".wav" or file[-4:] == ".mp3" or file[-4:] == ".ogg":
                    tauntList.append(Taunt())
                    tauntList[-1].name = file[:-4]
                    tauntList[-1].fileName = file
                    tauntList[-1].path = "{0}/{1}/{2}/{3}".format(tauntFolderName, firstLvlDir, secondLvlDir, file)
                    tauntList[-1].category = firstLvlDir if categoriesFirst else secondLvlDir
                    tauntList[-1].team = secondLvlDir if categoriesFirst else firstLvlDir
                    tauntList[-1].team = int(tauntList[-1].team) - 1

    # Organize taunts for easy manipulation
    for taunt in tauntList:
        if taunt.category not in categoryDictionary:
            categoryDictionary[taunt.category] = [[], []]
        categoryDictionary[taunt.category][taunt.team].append(taunt)

    # Make the string to write to file
    output = ""
    for key in categoryDictionary:
        output += "local " + key + " = {}\n"
        for i in range(2):
            output += key + "[" + str(i + 1) + "] = {"
            if len(categoryDictionary[key][i]) == 0:
                output += "}\n"
                continue
            for taunt in categoryDictionary[key][i]:
                output += "\n\t[\"{0}\"] = \"{1}\",".format(taunt.name, taunt.path)
            output = output[:-1] + "\n}\n"
        output += "list.Set(\"PHX.CustomTaunts\", \"{0}\", {0})\n\n".format(key)

    os.chdir(pathOfTauntFolder)
    os.chdir("../")
    additionalTauntsFile = open("customTauntOutputToCopyAndDelete.txt", "wt")  # opens file in python for overwriting
    additionalTauntsFile.write(output)
    additionalTauntsFile.close()
    # File is created if it doesn't exist
