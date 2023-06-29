import os, re, winsound, lxml, requests
from lxml import etree
from io import StringIO

class SaveTools:
    @staticmethod
    def addToClipBoard(text):
        command = 'echo | set /p nul=' + text.strip() + '| clip'
        os.system(command)

class GravitiCraftParserTools:
    @staticmethod
    def getWordRegExp():
        return '\[..:..:..] \[Client thread/INFO] \[net\.minecraft\.client\.gui\.GuiNewChat]: \[CHAT] Задание: Расшифруй слово \[(\w+)]'

    @staticmethod
    def getMathRegExp():
        return '\[..:..:..] \[Client thread/INFO] \[net\.minecraft\.client\.gui\.GuiNewChat]: \[CHAT] Задание: Реши пример: (\d+) \+ (\d+)'

    @staticmethod
    def getRendomRegExp():
        return '\[..:..:..] \[Client thread/INFO] \[net\.minecraft\.client\.gui\.GuiNewChat]: \[CHAT] Задание: Угадай число, число варьирует от 0 до 10!'

    @staticmethod
    def getRendomAnswerRegExp():
        return '\[..:..:..] \[Client thread/INFO] \[net\.minecraft\.client\.gui\.GuiNewChat]: \[CHAT] >>> Это было число - (\d)'

class AnagrammAPI:
    @staticmethod
    def resolveAnagramm(letters):
        pageResponse = requests.get(
            'https://anagram.poncy.ru/words.html?inword='
            + letters
            + '&answer_type=3&count_letters=' + str(len(letters))
        )
        return AnagrammAPI.getAnswerFromPage(pageResponse) if (pageResponse.status_code == 200) else None

    @staticmethod
    def getAnswerFromPage(page):
        parser = etree.HTMLParser()
        html = page.content.decode('utf-8')
        tree = etree.parse(StringIO(html), parser=parser)
        element = tree.xpath("//*[@id='helphref0']")
        return element[0].xpath('string(normalize-space())').lower()

class GravitiCraftSolverTools:
    @staticmethod
    def solveNumberExampleInLine(line):
        match = re.match(GravitiCraftParserTools.getMathRegExp(), line)
        if match:
            answer = int(match.groups().__getitem__(0)) + int(match.groups().__getitem__(1))
            SaveTools.addToClipBoard(str(answer))
            print(line + ' = ' + str(answer))
            winsound.Beep(300, 200)
            return answer

    @staticmethod
    def solveAnagramInLine(line):
        match = re.match(GravitiCraftParserTools.getWordRegExp(), line)
        if match:
            letters = match.groups().__getitem__(0)
            answer = AnagrammAPI.resolveAnagramm(letters)
            SaveTools.addToClipBoard(answer if answer else letters)
            print(line + ' = ' + answer)
            winsound.Beep(300, 200)
            return answer

    @staticmethod
    def printRandomAskLine(line):
        match = re.match(GravitiCraftParserTools.getRendomRegExp(), line)
        if match:
            print(line)
            winsound.Beep(300, 200)
            return line

    @staticmethod
    def printRandomAnswerFromLine(line):
        match = re.match(GravitiCraftParserTools.getRendomAnswerRegExp(), line)
        if match:
            print(line)
            winsound.Beep(300, 200)
            return line

def readFile(file):
    file.seek(0, 2)

    while True:
        line = file.readline()
        GravitiCraftSolverTools.solveNumberExampleInLine(line)
        GravitiCraftSolverTools.solveAnagramInLine(line)
        GravitiCraftSolverTools.printRandomAskLine(line)
        GravitiCraftSolverTools.printRandomAnswerFromLine(line)

def tests():
    assert GravitiCraftSolverTools.solveNumberExampleInLine(
        '[10:28:36] [Client thread/INFO] [net.minecraft.client.gui.GuiNewChat]: [CHAT] Задание: Реши пример: 88 + 211'
    ) == 299, "Should be 299"

    assert GravitiCraftSolverTools.solveAnagramInLine(
        '[19:53:59] [Client thread/INFO] [net.minecraft.client.gui.GuiNewChat]: [CHAT] Задание: Расшифруй слово [уХпонлот]'
    ) == 'хлопотун', "Should be хлопотун"

    assert GravitiCraftSolverTools.printRandomAskLine(
        '[19:32:24] [Client thread/INFO] [net.minecraft.client.gui.GuiNewChat]: [CHAT] Задание: Угадай число, число варьирует от 0 до 10!'
    ) == '[19:32:24] [Client thread/INFO] [net.minecraft.client.gui.GuiNewChat]: [CHAT] Задание: Угадай число, число варьирует от 0 до 10!', \
        "Should be '[19:32:24] [Client thread/INFO] [net.minecraft.client.gui.GuiNewChat]: [CHAT] Задание: Угадай число, число варьирует от 0 до 10!'"

    assert GravitiCraftSolverTools.printRandomAnswerFromLine(
        '[19:32:24] [Client thread/INFO] [net.minecraft.client.gui.GuiNewChat]: [CHAT] >>> Это было число - 4'
    ) == 'Это было число - 4', "Should be 'Это было число - 4'"

if __name__ == '__main__':
    tests()
    logfile = open('C:\\Users\\Andrew\\AppData\\Roaming\\GravityCraft\\updates\\Industrial\\logs\\debug.log', "r")
    readFile(logfile)