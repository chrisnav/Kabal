from typing import List
import numpy as np

CARD_COLORS = ["heart","club","diamond","spade"]
CARD_COLORS_ASCII = {"heart":"♥","club":"♣","diamond":"♦","spade":"♠"}
CARD_VALUES_ASCII = {i:str(i) for i in range(1,14)}
CARD_VALUES_ASCII[1] = "A"
CARD_VALUES_ASCII[11] = "J"
CARD_VALUES_ASCII[12] = "Q"
CARD_VALUES_ASCII[13] = "K"
class Card():
    
    def __init__(self,color,value):
        
        if value < 1 or value > 13:
            print(f"Value {value} out of bounds")
            raise RuntimeError
        if color not in CARD_COLORS:
            print(f"Color {color} not recognized")
            raise RuntimeError
                    
        self.color = color
        self.value = value
        
        self.disp = CARD_VALUES_ASCII[self.value] + " "       
        self.disp += CARD_COLORS_ASCII[self.color]

    def __str__(self):
        return self.disp

class Deck():

    def __init__(self):
        
        self.cards = []
        for color in CARD_COLORS:
            for i in range(1,14):
                self.cards.append(Card(color,i))
        
        self.shuffle()
            
    def shuffle(self):
    
        np.random.shuffle(self.cards)
        
        
class Pile():
    
    def __init__(self,up_cards:List[Card],down_cards:List[Card]):
        
        self.up_cards = up_cards
        self.down_cards = down_cards
        
    def card_index_in_up_pile(self,color:str,value:int):
        
        for i,c in enumerate(self.up_cards):
            if c.color == color and c.value == value:
                return i
        return -1
        
    def flip_card(self):
        
        if len(self.up_cards) > 0:
            print(f"There are {len(self.up_cards)} in the pile facing upward, unable to flip a new card.")
            raise RuntimeError
            
        if len(self.down_cards) == 0:
            print("No face down cards to flip in pile!")
            raise RuntimeError
            
        c = self.down_cards.pop()
        
        self.up_cards.append(c)
        
    def remove_cards(self, index:int):
        
        self.up_cards = self.up_cards[:index]
        
    def add_cards(self, cards:List[Card]):
        
        self.up_cards += cards
    
    def __str__(self):
        disp = ""
        
        disp += f"{len(self.down_cards)} downward facing cards\n"
        disp += "Face cards:\n"
        for c in self.up_cards:
            disp += "\t"+str(c)+"\n"
        print("")
                
        return disp
        
   
class Kabal():
    
    def __init__(self,seed=None):
        
        if seed is not None:
            np.random.seed(seed)
            
        self.deck = Deck()
        self.piles = []
        self.ace_piles = {color:Pile([],[]) for color in CARD_COLORS}
        
        k = 0
        for i in range(7):
            n_down = i
            if i == 0:
                n_up = 1
            else:
                n_up = 5
            
            up = self.deck.cards[k:k+n_up]
            k += n_up
            
            down = self.deck.cards[k:k+n_down]            
            k += n_down
            
            p = Pile(up,down)
            self.piles.append(p)
            
    def __str__(self):
        
        disp = ""
        
        for i,p in enumerate(self.piles):
            disp += f"Pile {i+1}:\n"
            disp += str(p)
            disp += "\n"
            
        return disp
        
    def move_cards(self,from_pile:Pile,to_pile:Pile,index:int):
                
        cards_to_move = from_pile.up_cards[index:]
        to_pile.add_cards(cards_to_move)
        from_pile.remove_cards(index)
        
    def move_king_to_empty_pile(self) -> bool:
        
        empty_piles = [p for p in self.piles if len(p.up_cards)+len(p.down_cards) == 0]
        if len(empty_piles) == 0:
            return False

        king_index = -1
        king_pile = None
        for p in self.piles:
            for i,c in enumerate(p.up_cards):
                if c.value == 13:
                    king_index = i
                    king_pile = p
                    break
        
        if king_index == -1:
            return False

        to_pile = empty_piles[0]
        self.move_cards(king_pile,to_pile,king_index)
        return True

    def move_cards_to_ace_pile(self) -> int:
    
        n_moved = 0

        last_value = {color:0 for color in CARD_COLORS}
        for color,p in self.ace_piles.items():
            if len(p.up_cards) > 0:
                last_value[color] = p.up_cards[-1].value

        new_pass = True
        while new_pass:
            
            new_pass = False
            for p in self.piles:
                if len(p.up_cards) == 0:
                    continue            

                c = p.up_cards[-1]
                v = last_value[c.color]
                if c.value == v + 1:
                    self.move_cards(p,self.ace_piles[c.color],len(p.up_cards)-1)
                    last_value[c.color] += 1
                    n_moved += 1
                    new_pass = True

        return n_moved

        
        
        
        
            
    def test(self):
        
        for p in self.piles:
            if len(p.up_cards) == 0:
                continue
            
            c = p.up_cards[-1]
            print(c)
            
            if c.value == 1:
                print("Ace can be moved out")
                continue
            
            for i,other_p in enumerate(self.piles):
                if other_p == p:
                    continue
                if other_p.card_index_in_up_pile(c.color,c.value-1) != -1:
                    print(f"Found card to move in pile number {i+1}")
                    break
        
            print("")
        
        n = self.move_cards_to_ace_pile()
        print(f"Moved {n} cards to ace piles")