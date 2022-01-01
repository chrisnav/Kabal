from classes import Kabal
import sys

j = 0
N = 1000000
for i in range(N):
    if i == 0:
        k = Kabal(seed = 0)
    else:
        k = Kabal()

    #if i == 276:
    #    print(k)
    #    print("")
#
    #    for m,p in enumerate(k.piles):
    #        print(f"Pile {m+1}:")
    #        for c in p.down_cards:
    #            print("\t",c)
#
    #    sys.exit()

    ok = True
    while ok:
                                                                
        ok = k.play_round()

    n = 0
    for p in k.piles:
        n += len(p.up_cards) + len(p.down_cards)
    if n == 0:
        j += 1

        #print(k)
        #for color,ap in k.ace_piles.items():
        #    print(color,ap)
        #break

print(j,f"{100*j/N} %")