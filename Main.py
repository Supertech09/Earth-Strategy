import pygame as pygame
import time
import random
from Include import GameInit, TurnNumber, TurnCounter
import Cards
pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.display.init()
pygame.font.init()

global Nitrogen, Phosphorus, Carbon, Pollution
global NitrogenFixation, NitrogenMultiplier, CarbonMultiplier, PhosphorusMultiplier
global last_played_card

last_played_card = None  # Track the last played card
Nitrogen = 0
Phosphorus = 0
Carbon = 0
Pollution = 0
NitrogenFixation = False
NitrogenMultiplier = 1
PhosphorusMultiplier = 1
CarbonMultiplier = 1


class Player:
    def __init__(self, Team, Cards, Points, CardsDrawn):
        self.Team = Team
        self.Cards = Cards
        self.Points = Points
        self.CardsDrawn = CardsDrawn
    def GetCards(self):
        if self.Team == "Environment" and self.CardsDrawn == False:
            card_classes = random.sample(Cards.EnvironmentCardList, 3)
            self.Cards = [cls() for cls in card_classes]
            self.CardsDrawn = True
        elif self.Team == "Industry" and self.CardsDrawn == False:
            card_classes = random.sample(Cards.IndustryCardList, 3)
            self.Cards = [cls() for cls in card_classes]
            self.CardsDrawn = True
        else:
            print("Error: Team not set or cards already drawn.")
            return
        #print("Cards drawn:", self.Cards)

def activate_card_effect(card):
    # Example: apply card's multipliers or other effects
    global NitrogenMultiplier, CarbonMultiplier, PhosphorusMultiplier, Nitrogen, Phosphorus, Carbon, Pollution, NitrogenFixation
    if hasattr(card, "NitrogenMultiplier"):
        NitrogenMultiplier += card.NitrogenMultiplier
    if hasattr(card, "PhosphorusMultiplier"):
        PhosphorusMultiplier += card.PhosphorusMultiplier
    if hasattr(card, "CarbonMultiplier"):
        CarbonMultiplier += card.CarbonMultiplier
    if hasattr(card, "Pollution"):
        Pollution += card.Pollution
    if hasattr(card, "CarbonAddSoil"):
        Carbon += card.CarbonAddSoil * CarbonMultiplier
    if hasattr(card, "NitrogenAddSoil"):
        if NitrogenFixation:
            Nitrogen += card.NitrogenAddSoil * NitrogenMultiplier
        else:
            print("Nitrogen Fixation is not active.")
    if hasattr(card, "PhosAddSoil"):
        Phosphorus += card.PhosAddSoil * PhosphorusMultiplier
    if isinstance(card, Cards.EnvironmentCards.MicrobeCard):
        NitrogenFixation = True
    if isinstance(card, Cards.IndustryCards.DenitrifyingBacteria):
        NitrogenFixation = False
    print(f"Activated effect of {card.name}")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initialize pygame and font module


print("Pygame initialized:", pygame.get_init())
print("Font module initialized:", pygame.font.get_init())

# Create font object
testfont = pygame.font.SysFont("SpaceNova-6Rpd1.otf", 30) 
print("Font object created:", testfont)
# Initialize game display
GameDisplay = pygame.display.set_mode((1000, 750), pygame.RESIZABLE)
pygame.display.set_caption("Earth Strategy")

# Initialize players
Player1 = Player("Environment", [], 0, False)

# Initialize turn counter
Turn = 1
Bot = Player("Industry", [], 0, False)
EnvironmentCardList = Cards.EnvironmentCardList

# Load and scale images
TitleScreen = pygame.image.load('TitleScreen.png')
TitleScreen = pygame.transform.scale(TitleScreen, (1000, 750))
TeamSelectScreen = pygame.image.load('TeamSelect.png')
TeamSelectScreen = pygame.transform.scale(TeamSelectScreen, (1000, 750))
gamesurface = pygame.image.load('Background Test.png')
gamesurface = pygame.transform.scale(gamesurface, (1000, 750))
card_positions = [(100, 525), (325, 525), (550, 525)]
PlayedCards = 325, 200
card_rects = [pygame.Rect(x, y, 150, 225) for (x, y) in card_positions]

# Title Screen buttons
teambutton = pygame.Rect(323, 298, 288, 94)
playbutton = pygame.Rect(323, 413, 288, 100)
cardbutton = pygame.Rect(323, 530, 288, 100)
# Game screen buttons
exitbutton = pygame.Rect(950, 10, 50, 50)
nextturnbutton = pygame.Rect(925, 680, 65, 50)

# Team selection buttons
EnvironmentTeam = pygame.Rect(0, 0, 500, 750)
IndustryTeam = pygame.Rect(500, 0, 1000, 750)

# Game states
Game = False
TeamSelect = False

# Main game loop
while True:

    for event in pygame.event.get():
        # Handle quit events
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

        # Handle mouse button clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if not Game and not TeamSelect:
                    if teambutton.collidepoint(event.pos):
                        pygame.draw.rect(GameDisplay, RED, teambutton)
                        print('Team Select clicked.')
                        TeamSelect = True
                    elif playbutton.collidepoint(event.pos):
                        pygame.draw.rect(GameDisplay, RED, playbutton)
                        print('Play clicked.')
                        if Player1.Team == "Environment":
                            Team = random.randint(1, 2)
                            if Team == 1:
                                Player1.Team = "Environment"
                                Bot.Team = "Industry"
                            elif Team == 2:
                                Player1.Team = "Industry"
                                Bot.Team = "Environment"
                        Game = True
                    elif cardbutton.collidepoint(event.pos):
                        pygame.draw.rect(GameDisplay, RED, cardbutton)
                        print('Cards clicked.')
                elif TeamSelect:
                    if EnvironmentTeam.collidepoint(event.pos):
                        print('Environment Team selected.')
                        Player1.Team = "Environment"
                        Bot.Team = "Industry"
                        Game = True
                        TeamSelect = False
                    elif IndustryTeam.collidepoint(event.pos):
                        print('Industry Team selected.')
                        Player1.Team = "Industry"
                        Bot.Team = "Environment"
                        Game = True
                        TeamSelect = False
                elif Game:
                    for i, rect in enumerate(card_rects):
                        if rect.collidepoint(event.pos) and i < len(Player1.Cards):
                            card = Player1.Cards[i]
                            if Player1.Points >= card.cost:
                                card = Player1.Cards.pop(i)
                                Player1.Points -= card.cost
                                print(f"Played card: {card.name}")
                                activate_card_effect(card)
                                last_played_card = card  # Store the played card
                            else:
                                print("Not enough points to play this card!")
                            break  # Only play one card per click
                    if exitbutton.collidepoint(event.pos):
                        print('Exit clicked.')
                        last_played_card = None
                        Player1.Cards = []
                        Player1.Points = 0
                        Bot.Cards = []
                        Bot.Points = 0
                        Player1.CardsDrawn = False
                        Bot.CardsDrawn = False
                        NitrogenFixation = False
                        NitrogenMultiplier = 1
                        PhosphorusMultiplier = 1
                        CarbonMultiplier = 1
                        Nitrogen = 0
                        Phosphorus = 0
                        Carbon = 0
                        Pollution = 0

                        Game = False
                    if nextturnbutton.collidepoint(event.pos):
                        print('Next Turn clicked.')
                        if Turn == 1:
                            Turn = 2
                            Bot.CardsDrawn = False   # Reset for Bot's turn
                        elif Turn == 2:
                            Turn = 1
                            Player1.CardsDrawn = False  # Reset for Player1's turn


    #Game logic
    if Game == True:
        if Turn == 1 and Player1.CardsDrawn == False:
            Player1.Points += 2
            Player1.GetCards()
            print("Player 1 Cards:", Player1.Cards)
        elif Turn == 2 and Bot.CardsDrawn == False:
            Bot.Points += 2
            Bot.GetCards()
            print("Bot Cards:", Bot.Cards)
            affordable_cards = [card for card in Bot.Cards if hasattr(card, "cost") and Bot.Points >= card.cost]
            if affordable_cards:
                if Bot.Team == "Industry":
                    # Pick the card with the highest Pollution value (default to 0 if not present)
                    best_card = max(affordable_cards, key=lambda c: getattr(c, "Pollution", 0))
                else:  # Environment team
                    best_card = random.choice(affordable_cards)
                Bot.Cards.remove(best_card)
                Bot.Points -= best_card.cost
                print(f"Bot played card: {best_card.name}")
                activate_card_effect(best_card)
                last_played_card = best_card
            # End bot's turn
            Turn = 1
            Player1.CardsDrawn = False
        if Carbon >= 50 and Nitrogen >= 25 and Phosphorus >= 10 and Player1.Team == "Environment":
            print("You win!")
            last_played_card = None
            Player1.Cards = []
            Player1.Points = 0
            Bot.Cards = []
            Bot.Points = 0
            Player1.CardsDrawn = False
            Bot.CardsDrawn = False
            NitrogenFixation = False
            NitrogenMultiplier = 1
            PhosphorusMultiplier = 1
            CarbonMultiplier = 1
            Nitrogen = 0
            Phosphorus = 0
            Carbon = 0
            Pollution = 0
            Game = False
        elif Pollution >= 50 and Player1.Team == "Industry":
            print("You Win!")
            last_played_card = None
            Player1.Cards = []
            Player1.Points = 0
            Bot.Cards = []
            Bot.Points = 0
            Player1.CardsDrawn = False
            Bot.CardsDrawn = False
            NitrogenFixation = False
            NitrogenMultiplier = 1
            PhosphorusMultiplier = 1
            CarbonMultiplier = 1
            Nitrogen = 0
            Phosphorus = 0
            Carbon = 0
            Pollution = 0
            Game = False
        elif Pollution >= 50 and Player1.Team == "Environment":
            print("You lose!")
            Game = False
            pygame.quit()
        elif Carbon >= 50 and Nitrogen >= 25 and Phosphorus >= 10 and Player1.Team == "Industry":
            print("You lose!")
            Game = False
            pygame.quit()


    # Render the appropriate screen
    if not Game and not TeamSelect:
        GameDisplay.blit(TitleScreen, (0, 0))
    elif TeamSelect:
        GameDisplay.fill(WHITE)
        GameDisplay.blit(TeamSelectScreen, (0, 0))
    elif Game:
        GameDisplay.fill(WHITE)
        GameDisplay.blit(gamesurface, (0, 0))

        Player1Display = testfont.render(f"You: {Player1.Team}", True, BLACK)
        Player2Display = testfont.render(f"Bot: {Bot.Team}", True, BLACK)
        TurnDisplay = testfont.render(f"Turn: {Turn}", True, BLACK)
        PointsDisplay = testfont.render(f"Points: {Player1.Points}", True, BLACK)

        CarbonDisplay = testfont.render(f"Carbon: {Carbon}", True, BLACK)
        NitrogenDisplay = testfont.render(f"Nitrogen: {Nitrogen}", True, BLACK)
        PhosphorusDisplay = testfont.render(f"Phosphorus: {Phosphorus}", True, BLACK)
        CMultiplierDisplay = testfont.render(f"Carbon Mult: {CarbonMultiplier}", True, BLACK)
        NMultiplierDisplay = testfont.render(f"Nitrogen Mult: {NitrogenMultiplier}", True, BLACK)
        PMultiplierDisplay = testfont.render(f"Phosphorus Mult: {PhosphorusMultiplier}", True, BLACK)
        FixationDisplay = testfont.render(f"Fixation: {NitrogenFixation}", True, BLACK)
        PollutionDisplay = testfont.render(f"Pollution: {Pollution}", True, BLACK)

        GameDisplay.blit(Player1Display, (5, 250))
        GameDisplay.blit(Player2Display, (5, 300))
        GameDisplay.blit(TurnDisplay, (5, 350))
        GameDisplay.blit(PointsDisplay, (5, 400))

        GameDisplay.blit(PollutionDisplay, (800, 150))
        GameDisplay.blit(CarbonDisplay, (800, 200))
        GameDisplay.blit(NitrogenDisplay, (800, 250))
        GameDisplay.blit(PhosphorusDisplay, (800, 300))
        GameDisplay.blit(CMultiplierDisplay, (775, 350))
        GameDisplay.blit(NMultiplierDisplay, (775, 400))
        GameDisplay.blit(PMultiplierDisplay, (775, 450))
        GameDisplay.blit(FixationDisplay, (800, 100))

        NextLabel = testfont.render("Next", True, BLACK)
        for i, card in enumerate(Player1.Cards):
            card_image = pygame.image.load(card.image_path)
            card_image = pygame.transform.scale(card_image, (150,225))
            pos = card_positions[i]
            GameDisplay.blit(card_image, pos)
        # Draw the last played card at PlayedCards position
        if last_played_card is not None:
            played_image = pygame.image.load(last_played_card.image_path)
            played_image = pygame.transform.scale(played_image, (150,225))
            GameDisplay.blit(played_image, PlayedCards)
        pygame.draw.rect(GameDisplay, RED, exitbutton)
        pygame.draw.rect(GameDisplay, RED, nextturnbutton)
        GameDisplay.blit(NextLabel, (930, 690))

    pygame.display.update()


