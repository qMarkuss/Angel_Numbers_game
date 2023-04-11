import pygame
import time
import random

pygame.init()

win = (800, 400)
screen = pygame.display.set_mode(win)
pygame.display.set_caption("Angel Numbers")

# Mainīgie
fontSmall = pygame.font.Font(None, 36)
fontBig = pygame.font.Font(None, 70)

blackColor = (0, 0, 0)
whiteColor = (255, 255, 255)

numberList = [1, 1, 1, 1, 1, 2, 2, 2]
playerScores = [6, 6]
isPlayerTurn = 0
gameOver = False
isMaximizing = False

playerHistory = []
computerHistory = []

# Funkcija uz ekrāna parāda spēlētāju punktu skaitus un gājienu vēsturi
def updateScores():
    playerScore = fontSmall.render("Player: " + str(playerScores[0]), True, whiteColor)
    computerScore = fontSmall.render("Computer: " + str(playerScores[1]), True, whiteColor)

    screen.blit(playerScore, (20, 15))
    screen.blit(computerScore, (285, 15))

    for i in range(len(playerHistory)):
        playerTurn = fontSmall.render(str(playerHistory[i]), True, whiteColor)
        screen.blit(playerTurn, (500, 50 + (i * 30)))

    for j in range(len(computerHistory)):
        computerTurn = fontSmall.render(str(computerHistory[j]), True, whiteColor)
        screen.blit(computerTurn, (650, 50 + (j * 30)))

# Funckija no skaitļu virknes velk ārā skaitļus, kurus apvieno vienā string un parāda uz ekrāna
def updateNumberList():
    numberString = "".join(str(i) for i in numberList)
    numberText = fontBig.render(numberString, True, whiteColor)
    screen.blit(numberText, (100, 150))

# Funckija, kas paņem kādu 2 no skaitļu virknes un sadala to divos 1
def splitNumber():
    global numberList, playerScores

    numberList.remove(2)
    numberList.append(1)
    numberList.append(1)

    # Vēsturei pievieno gājienu attiecīgajam spēlētājam
    if isPlayerTurn == 0:
        playerHistory.append("Split")
    else:
        computerHistory.append("Split")

# Funckija brīdī, kad tā tiek izsaukta izņem no skaitļu virknes izvēlēto skaitli. (Piemēram: "removeNumber(2))
def removeNumber(number):
    global numberList, playerScores

    numberList.remove(number)

    # Vēsturei pievieno gājienu attiecīgajam spēlētājam
    if isPlayerTurn == 0:
        playerScores[0] -= number
        playerHistory.append("TAKE[-" + str(number) + "]")
    else:
        playerScores[1] -= number
        computerHistory.append("TAKE[-" + str(number) + "]")


# Funkcija, kas pārbauda vai skaitļu virkne ir beigusies. Ja ir, tad uz ekrāna parāda, kurš uzvarēja spēli, salīdzinot punktu skaitu.
def checkIfGameOver():
    if len(numberList) == 0:
        if playerScores[0] > playerScores[1]:
            winnerText = fontBig.render("   Player wins!", True, whiteColor)
        elif playerScores[0] < playerScores[1]:
            winnerText = fontBig.render("Computer wins!", True, whiteColor)
        else:
            winnerText = fontBig.render("    Tie game!", True, whiteColor)

        screen.blit(winnerText, (40, 150))

def miniMax(depth, isMaxOrMin):
    # Gadijumā, kad rekursijas dziļums sasniedz 0 vai skaitļu sarakstā nav palicis neviens skaitlis, tad funckija tiek pārtraukta.
    if depth == 0 or len(numberList) == 0:
        return 0

    if isMaxOrMin:   # Atkarībā, kurš sāk spēli, datoram tiek piešķirts min or max. Gadijumā, ja dators sāk, tad tas ir min.
        bestScore = float('-inf')

        for i in range(len(numberList)):
            if numberList[i] == 2:   # For loop iziet cauri skaitļu virknei un noņem katru skaitli, kas nav viens. Un izveido temp virkni.
                tempNumberList = numberList[:]
                tempNumberList.remove(numberList[i])

                score = miniMax(depth - 1, isMaxOrMin)
                bestScore = max(score, bestScore)    # Rekursīvi salīdzina vērtibas un atgriež lielāko vērtību.
        return bestScore
    else:
        bestScore = float('inf')

        for i in range(len(numberList)):
            tempNumberList = numberList[:]
            tempNumberList.remove(numberList[i])

            score = miniMax(depth - 1, isMaxOrMin)
            bestScore = min(score, bestScore) # Rekursīvi salīdzina vērtibas un atgriež mazāko vērtību.
        return bestScore


def computerMove():
    global numberList, playerScores, isPlayerTurn, playerHistory, computerHistory

    bestScore = float('-inf')
    bestIndex = -1  # Izmanto index, lai vieglāk izsaukt pareizo funkciju pēc tam.

    for i in range(len(numberList)):
        if numberList[i] == 2:     # For loop iziet cauri skaitļu virknei un noņem katru skaitli, kas nav viens. Un izveido temp virkni, kā arī sāk rekursiju.
            tempNumberList = numberList[:]
            tempNumberList.remove(numberList[i])
            score = miniMax(3, isMaximizing)
            if score > bestScore:
                bestScore = score
                bestIndex = i

    # Gadijumā, ja ir kāds divnieks sarakstā, tad bestIndex tiek piešķirts to skaits, bet ja nav tad bestIndex kļūst par -1.
    # Tātad, ja ir kāds divnieks sarakstā, tad algoritms to sadalīs divos divniekos, pretēji, ja nav divnieku, tad izņems no saraksta vieninieku.
    if bestIndex == -1:
        removeNumber(numberList[bestIndex])
    else:
        splitNumber()

    # Dators ir pabeidzis savu gājienu, un tālāk turpina lietotājs.
    isPlayerTurn = 0


def playScreen():
    global gameOver,isPlayerTurn,numberList,playerScores

    # Šajā funkcijā ir while loop, kas atkārto sevi bezgalīgi ilgi, kamēr spēle nav beigusies. (while gameOver == false --> run code).
    while not gameOver:
        # Ar while loop palīdzību ekrāns tiek piepildīts melns un uz ekrāna ir saliktas visas redzamās pogas, radot ilūziju, ka tiek pārslēgti ekrāni.
        screen.fill(blackColor)

        pygame.draw.line(screen, whiteColor, (450, 0), (450, 400), 3)
        history = fontSmall.render("Move History:", True, whiteColor)
        screen.blit(history, (550, 10))

        splitButtonRect = pygame.Rect(180, 350, 100, 50)
        splitButtonText = fontSmall.render("SPLIT", True, whiteColor)
        take1ButtonRect = pygame.Rect(30, 350, 100, 50)
        take1ButtonText = fontSmall.render("TAKE[1]", True, whiteColor)
        take2ButtonRect = pygame.Rect(310, 350, 100, 50)
        take2ButtonText = fontSmall.render("TAKE[2]", True, whiteColor)

        restartButtonRect = pygame.Rect(500, 350, 100, 50)
        restartButtonText = fontSmall.render("Restart", True, whiteColor)
        exitButtonRect = pygame.Rect(700, 350, 100, 50)
        exitButtonText = fontSmall.render("Exit", True, whiteColor)

        screen.blit(splitButtonText, splitButtonRect)
        screen.blit(take1ButtonText, take1ButtonRect)
        screen.blit(take2ButtonText, take2ButtonRect)
        screen.blit(restartButtonText, restartButtonRect)
        screen.blit(exitButtonText, exitButtonRect)

        # Šeit tiek reģistrēti visi "inputs", pogas exit, restart, split, take[1], take[2].
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if splitButtonRect.collidepoint(event.pos) and isPlayerTurn == 0:
                    for number in numberList:        # Pārbauda vai virknē ir palicis kāds 2, pirms tiek izsaukta nākamā funkcija.
                        if number == 2:
                            splitNumber()
                            isPlayerTurn = 1
                            break
                elif take1ButtonRect.collidepoint(event.pos) and isPlayerTurn == 0:
                    for number in numberList:        # Pārbauda vai virknē ir palicis kāds 1, pirms tiek izsaukta nākamā funkcija.
                        if number == 1:
                            removeNumber(1)
                            isPlayerTurn = 1
                            break
                elif take2ButtonRect.collidepoint(event.pos) and isPlayerTurn == 0:
                    for number in numberList:       # Pārbauda vai virknē ir palicis kāds 2, pirms tiek izsaukta nākamā funkcija.
                        if number == 2:
                            removeNumber(2)
                            isPlayerTurn = 1
                            break
                elif exitButtonRect.collidepoint(event.pos):
                    gameOver = True
                elif restartButtonRect.collidepoint(event.pos):     # Spēles restartēšana.
                    numberList = [1, 1, 1, 1, 1, 2, 2, 2]
                    playerScores = [6, 6]
                    isPlayerTurn = 0
                    playerHistory.clear()
                    computerHistory.clear()
                    menuScreen()

        # Rekursīvi tiek izsauktas funkcijas, lai atjauninātu punktu skaitu, skaitļu virkni un pārbaudītu vai spēle ir beigusies.
        updateScores()
        updateNumberList()
        checkIfGameOver()

        # Brīdī, kad pienāk datora gājiens un spēle nav beigusies tiek izsaukta computerMove() funckija ar mazu aizskavēšanos (0.5 līdz 1 sekundei), radot ilūziju, ka dators "domā".
        if isPlayerTurn == 1 and len(numberList) > 0:
            pygame.display.update()
            delay = random.uniform(0.5, 1)
            time.sleep(delay)
            computerMove()

        # Tiek atsvaidzināts ekrāns, lai parādītu jebkādas izmaiņas
        pygame.display.update()

def menuScreen():
    # Palaižot programmu tiek izsaukta funkcija menuScreen(), kas ir pirmais ekrāns, ko lietotājs redz.
    # Ekrāns tiek aizpildīts ar melnu bildi un tiek parādīti 3 elementi. Teksts "Who starts first?" un divas pogas "Player" vai "Computer"
    global gameOver, isPlayerTurn, isMaximizing
    pygame.display.set_caption("Menu")

    # While loop, kas atkārto sevi bezgalīgi ilgi, kamēr spēle nav beigusies. (while gameOver == false --> run code).
    while not gameOver:
        screen.fill(blackColor)

        whoStartsText = fontSmall.render("Who starts?", True, whiteColor)
        screen.blit(whoStartsText, [300, 100])

        playerStartsText = fontSmall.render("Player", True, whiteColor)
        playerStartsRect = pygame.Rect(200, 200, 150, 50)
        screen.blit(playerStartsText, playerStartsRect)

        computerStartsRect = pygame.Rect(450, 200, 150, 50)
        computerStartsText = fontSmall.render("Computer", True, whiteColor)
        screen.blit(computerStartsText, computerStartsRect)

        # Šeit tiek reģistrēti visi "inputs", pogas "Player" vai "Computer".
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playerStartsRect.collidepoint(event.pos):
                    isPlayerTurn = 0
                    isMaximizing = True     # Iestata max pozīcīju datoram.
                    playScreen()
                elif computerStartsRect.collidepoint(event.pos):
                    isPlayerTurn = 1
                    isMaximizing = False    # Iestata min pozīcīju datoram.
                    playScreen()

        #  Tiek atsvaidzināts ekrāns, lai parādītu jebkādas izmaiņas
        pygame.display.update()

# Pirmā funkcija, kas tiek izsaukta, parādot pirmo ekrānu, kas ir menuScreen.
menuScreen()
pygame.quit()