#!/usr/bin/env python
# coding: utf-8

# In[3]:


import random

class Card():
    def __init__(self, num, sym):
        self.num=num
        self.sym=sym
        
    def __str__(self):
        return '('+str(self.num)+','+self.sym+')'

class Deck():
    
    closedCards=[]
    openCards=[]
    def __init__(self):
        for i in range(0,4):
            for sym in ['Spade','Club','Heart','Diamond']:           
                for num in range(2,11):
                    self.closedCards.append(Card(num,sym))
                for num in ['J','Q','K','A']:
                    self.closedCards.append(Card(num,sym))
        self.shuffle()
    
    def shuffle(self):
        random.shuffle(self.closedCards)
        
    def draw(self):
        self.openCards.append(self.closedCards.pop(0))
        return self.openCards[-1]
    
    def cleanTable(self):
        random.shuffle(self.openCards)
        self.closedCards.append(self.openCards)
        self.openCards=[]

class Player():
    
    winnings=0
    wins=0
    loses=0
    bet=0
    
    
    def __init__(self, buyIn, name):
        self.chips=buyIn
        self.name=name
        self.cards=[]
        
    def __str__(self):
        string = self.name
        if self.name!='Dealer':
            string+=" has " + str(self.chips) + " chips ("
        if self.winnings>0:
            string+="+"+str(self.winnings)+')'
        elif self.winnings<0:
            string+=str(self.winnings)+')'
        elif self.name!='Dealer':
            string+="-)"
        string+="\nWon " + str(self.wins) + " rounds, and lost " + str(self.loses) + " rounds\n"
        return string
    
    def showHand(self,end):
        if self.name=="Dealer" and end==False:
            cardString="Dealer:\n(X,X)"
        else:
            cardString=self.name+"\n"+str(self.cards[0])
        for card in self.cards[1:]:
            cardString+=","+str(card)
        if self.name!="Dealer":
            cardString+="\nBet: "+str(self.bet)
        if self.name=="Dealer" and end==False:
            cardString+="\nScore: X\n"
        else:
            cardString+="\nScore: "+str(self.score())+"\n"
        print (cardString)
    
    def openCard(self,card):
        self.cards.append(card)
        
    def score(self):
        score=0
        for card in self.cards:
            if card.num=='A':
                score+=11
            elif type(card.num)==str:
                score+=10
            else:
                score+=card.num
        for card in self.cards:
            if card.num=='A' and score > 21:
                score-=10
        if score > 21:
            return "Bust!"
        elif score==21 and len(self.cards)==2:
            for card in self.cards:
                if card.num==10:
                    return score
            return 'BlackJack!'
        else:
            return score
    
    def checkWin(self,dealer):
        if self.score()=='Bust!' or dealer.score()=='BlackJack!':
            return False
        elif dealer.score()=='Bust!'or self.score()=='BlackJack!' or self.score()>dealer.score():
            return True
        else:
            return False        
        
    def win(self):
        self.wins+=1
        if self.name!='Dealer':
            if self.score()=='BlackJack!':
                self.winnings+=1.5*self.bet
                self.chips+=1.5*self.bet
            else:
                self.winnings+=self.bet
                self.chips+=self.bet
            self.cards=[]
        
    def lose(self):
        self.loses+=1
        if self.name!='Dealer':
            self.winnings-=self.bet
            self.chips-=self.bet
            self.cards=[]
        
    def cashOut(self,amount=0):
        if amount==self.chips or amount ==0:
            print(f"{self.name} left with {self.chips} chips")            
            if self.winnings>0:
                print(f"after winning {self.winnings} chips")
            elif self.winnings<0:
                print(f"after losing {-self.winnings} chips")
            else:
                print(f"after balancing out")
            print(f"with winning {self.wins} rounds and losing {self.loses} rounds!\n")
            self.chips=0
        else:
            self.chips-=amount
            print(f"{self.name} cashed out {amount} chips")

def roundStatus(dealer,players,endOfRound=False):
    #round hands and bets
    #clear_output()
    dealer.showHand(endOfRound)
    for player in players:
        player.showHand(endOfRound)
        
def showStatus(dealer,players):
    #everyone's balance
    #clear_output()
    i=len(players)
    while i >0:
        if players[-i].chips==0:
            players[-i].cashOut()
            players.pop(-i)
            i-=1
        else:
            print(f"{players[-i]}")
            i-=1
    print (dealer)
        
def bjRound(dealer,players,deck,roundsPlayed):
    #clear_output()
    if roundsPlayed==0:
        print("Lets play BlackJack!\nRound #1:")
    else:
        print(f"New round! Round #{roundsPlayed+1}:")
    # placing bets
    for player in players:
        player.bet=int(input(f"{player.name}, how much would you like to bet this round? "))
    clear_output()
       
    # first 2 cards       
    for i in [0,1]:
        for player in players:
            player.openCard(deck.draw())
        dealer.openCard(deck.draw())
    roundStatus(dealer,players)
    
    # players' turn accordingly
    move=True
    for player in players:
        if player.score()!=21 and player.score()!='BlackJack!':
            while move!='s':
                move=input(f"{player.name}, it is your turn! do you want to hit or stay? h / s")
                if move.lower()=='h' or move.lower()=='hit':
                    player.openCard(deck.draw())
                    if player.score()=='Bust!'or player.score()==21 or player.score()=='BlackJack!':
                        move='s'
                elif move.lower()=='stay' or move.lower()=='s':
                    move='s'
                clear_output()
                roundStatus(dealer,players)
        move=True
    input("Players ready for dealer's move?")
    

        
    # dealer's move
    while(move!='s'):
        try:
            if dealer.score()<17:
                clear_output()
                roundStatus(dealer,players,True)
                input("Ready for dealer's hit?")
                dealer.openCard(deck.draw())
            else:
                move='s'
            clear_output()

        except TypeError:
            move ='s'
    
    # 'True' parameter for showing dealer's cards
    roundStatus(dealer,players,True)
    
    for player in players:
        if player.checkWin(dealer):
            print(f"{player.name} wins")
            player.win()
            dealer.lose()
        else:
            print(f"{player.name} loses")
            player.lose()
            dealer.win()
    dealer.cards=[]
    input("Showing players status")
    clear_output()
    showStatus(dealer,players)
    deck.cleanTable()

def letsPlay():
    deck=Deck()
    dealer=Player(99999,'Dealer')
    play=True
    roundsPlayed=0
    while True:
        #clear_output()
        try:
            numOfPlayers=int(input("Let's play!\nHow many players will you be? "))
        except:
            pass
        else:
            break
    players=[]
    for i in range (1,numOfPlayers+1):
        #clear_output()
        playerName=input(f"Player {i}, what is your name? ")
        while True:
            try:
                playerChips=int(input(f"{playerName}, how much is your first Buy-In in $? "))
            except:
                pass
            else:
                break
        players.append(Player(playerChips,playerName))
    clear_output()

    showStatus(dealer,players)
    while play==True:
        bjRound(dealer,players,deck,roundsPlayed)
        roundsPlayed+=1      
        if players!=[]:
            play=input("Do you want to continue to the next round? ")
            if play=="yes" or play=="y" or play =="":
                play=True
        else:
            print('Game Over!')
            play = False
            
#Main     
from IPython.display import clear_output
action=input("Want to play BlackJack? y / n\n")
if action == 'y' or action == 'yes':
    letsPlay()


# 

# In[ ]:





# In[ ]:





# In[ ]:




