import numpy as np

class Card():
    
    def __init__(self,color,value):
        
        if value < 1 or value > 13:
            print(f"Value {value} out of bounds")
            raise RuntimeError
        if color not in ["heart","club","diamond","spade"]:
            print(f"Color {color} not recognized")
            raise RuntimeError
                    
        self.color = color
        self.value = value
        
        self.disp = ""
        if self.value == 1:
            self.disp += "A "
        elif self.value == 11:
           self.disp += "J "
        elif self.value == 12:
            self.disp += "Q "
        elif self.value == 13:
            self.disp += "K "           
        else:
            self.disp += str(value)+" "
        
        if color == "heart":
            self.disp += "♥"
        elif color == "diamond":
            self.disp += "♦"
        elif color == "club":
            self.disp += "♣"   
        else:
            self.disp += "♠"               

    def __str__(self):
        return self.disp

class Deck():

    def __init__(self):
        
        self.cards = []
        for color in ["heart","club","diamond","spade"]:
            for i in range(1,14):
                self.cards.append(Card(color,i))
        
        self.shuffle()
            
    def shuffle(self):
    
        np.random.shuffle(self.cards)
        
        
class Pile():
    
    def __init__(self,up_cards,down_cards):
        
        self.up_cards = up_cards
        self.down_cards = down_cards
        
    def card_in_up_pile(self,color,value):
        
        for c in self.up_cards:
            if c.color == color and c.value == value:
                return True
        return False
        
    def flip_card(self):
        
        if len(self.up_cards) > 0:
            print(f"There are {len(self.up_cards)} in the pile facing upward, unable to flip a new card.")
            raise RuntimeError
            
        if len(self.down_cards) == 0:
            print("No face down cards to flip in pile!")
            raise RuntimeError
            
        c = self.down_cards.pop()
        
        self.up_cards.append(c)
        
    def remove_cards(self, index):
        
        self.up_cards = self.up_cards[index:]
        
    def add_cards(self, cards):
        
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
        self.ace_piles = [Pile([],[]),Pile([],[]),Pile([],[]),Pile([],[])]
        
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
        
    def move_cards(self,from_pile,to_pile,index):
                
        cards_to_move = from_pile.up_cards[index:]
        to_pile.add_cards(cards_to_move)
        from_pile.remove_cards(index)
        
    def move_king_to_empty_pile(self,from_pile,to_pile,king_card):
        
        if len(to_pile.up_cards)+len(to_pile.down_cards) > 0:
            print("To-pile not empty!")
            raise RuntimeError
        
        index = -1
        for i,c in enumerate(from_pile.up_cards):
            if c == king_card:
                index = i
                break
        
        if index == -1:
            print(f"King kard {str(king_card)} not found in pile!")
            raise RuntimeError
            
        self.move_cards(from_pile,to_pile,index)
        
    def move_card_to_ace_pile(self, from_pile, card):
    
        ap = None

        if card.value == 1:
            for p in self.ace_piles:
                if len(p.up_cards) == 0:
                    ap = p
                    break
        else:
            for p in self.ace_piles:
                if len(p.up_cards) == 0:
                    continue
                c = p.up_cards[-1]
                if c.color != card.color:
                    continue
                    
                if c.value == card.value-1:
                    ap = p
                    break
                    
        if ap is None:
            print(f"Unable to find ace pile for {card}")
            raise RuntimeError
            
        
        ap.up_cards.append(card)
        from_pile.up_cards.remove(card)    
        
        
        
        
            
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
                if other_p.card_in_up_pile(c.color,c.value-1):
                    print(f"Found card to move in pile number {i+1}")
                    break
                    
            print("")