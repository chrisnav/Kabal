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
        
        if value < 1 or value > 13:
            print("Trying to find card outside legal values:",color,value)
            raise RuntimeError

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
        self.latest_ace_pile_value = {color:0 for color in CARD_COLORS}
        
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

        if index == 0 and len(from_pile.down_cards) > 0:
            #print("Flipping card")
            from_pile.flip_card()        
        
    def move_king_to_empty_pile(self) -> bool:
        
        empty_piles = [p for p in self.piles if len(p.up_cards)+len(p.down_cards) == 0]
        if len(empty_piles) == 0:
            return False

        kings = []
        for p in self.piles:
            for i,c in enumerate(p.up_cards):
                if c.value == 13:
                    
                    if i == 0 and len(p.down_cards) == 0:   #Kings on the bottom of a pile with no hidden cards do not count
                        continue
                    
                    if i == 0:
                        rank = 0
                    else:
                        card_below = p.up_cards[i-1]
                        if card_below.value == 1:
                            rank = 1
                        elif self.latest_ace_pile_value[card_below.color] == card_below.value - 1:
                            rank = 2
                        else:
                            rank = 1000

                    kings.append((rank,i,p))
        
        if len(kings) == 0:
            return False

        kings.sort(key=lambda x: x[0])

        for rank,index,pile in kings:

            to_pile = empty_piles[0]
            self.move_cards(pile,to_pile,index)
            break

        return True

    def move_cards_to_ace_pile(self) -> int:
        
        n_moved = 1
        while n_moved > 0:

            n_moved = 0
            for p in self.piles:
                n_moved += self.move_cards_in_pile_to_ace_pile(p)
        return n_moved   

    def move_cards_in_pile_to_ace_pile(self, p:Pile) -> int:

        n_moved = 0

        new_pass = True
        while new_pass:
            
            new_pass = False
            if len(p.up_cards) == 0:
                return n_moved            

            c = p.up_cards[-1]
            v = self.latest_ace_pile_value[c.color]
            if c.value == v + 1:
                self.move_cards(p,self.ace_piles[c.color],len(p.up_cards)-1)
                self.latest_ace_pile_value[c.color] += 1
                n_moved += 1
                new_pass = True

        return n_moved   


    def play_round(self):

        self.move_cards_to_ace_pile()

        did_something = False      

        for p in self.piles:
            if len(p.up_cards) == 0:
                continue
            
            c = p.up_cards[-1]
            if c.value == 1:
                self.move_cards_to_ace_pile()
                did_something = True 
                continue
                        
            for i,other_p in enumerate(self.piles):
                if other_p == p:
                    continue
                index = other_p.card_index_in_up_pile(c.color,c.value-1)
                if index != -1:
                    #print(f"Found card to move in pile number {i+1}")
                    self.move_cards(other_p,p,index)
                    did_something = True                    

        if not did_something:
            did_something = self.move_king_to_empty_pile()

        return did_something
