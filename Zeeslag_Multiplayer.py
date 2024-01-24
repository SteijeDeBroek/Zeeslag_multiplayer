from random import randint
from turtle import color
from termcolor import colored

let_to_num = {'A': 0, 'B': 1, 'C': 2, 'D': 3}

def print_bord(bord):
    print(' A B C D'[:len(bord[0]) * 2 + 1])
    print(' ' + '-' * (len(bord[0]) * 2))
    row_num = 1
    for row in bord:
        print("%d|%s|" % (row_num, "|".join(row)))
        row_num += 1

def print_leeg_bord():
    leeg_bord = [[' '] * 4 for _ in range(4)]
    print("Leeg bord:")
    print_bord(leeg_bord)

def get_ship_location(bord):
    row = input(f'Gelieve een rij in te voeren tussen 1 en {len(bord)} ').upper()
    while not row or row not in '1234':
        if not row:
            print(colored("Input mag niet leeg zijn. Probeer opnieuw.",'red'))
        else:
            print(colored("Kies een bestaande rij.",'red'))
        row = input(f'Gelieve een rij in te voeren tussen 1 en {len(bord)} ').upper()

    column = input(f'Gelieve een kolom in te voeren van A tot {chr(ord("A") + len(bord[0]) - 1)} ').upper()
    while not column or column not in 'ABCD':
        if not column:
            print(colored("Input mag niet leeg zijn. Probeer opnieuw.",'red'))
        else:
            print(colored(f"Kies een bestaande kolom van A tot {chr(ord('A') + len(bord[0]) - 1)}",'red'))
        column = input(f'Gelieve een kolom in te voeren van A tot {chr(ord("A") + len(bord[0]) - 1)} ')

    return int(row) - 1, let_to_num[column]

def handmatige_plaatsing_schepen(bord, speler):
    schepen_locaties = []  # Lijst om schepenlocaties bij te houden

    print(colored(f"Speler {speler}, plaats je schepen:",'light_blue'))
    print_leeg_bord()  # Toon een leeg bord 
    for _ in range(4):  # In totaal 4 schepen
        while True:
            try:
                locatie = get_ship_location(bord)
                if bord[locatie[0]][locatie[1]] == ' ':
                    bord[locatie[0]][locatie[1]] = 'X'
                    schepen_locaties.append(locatie)
                    break
                else:
                    print(colored("Deze locatie is al bezet. Kies een andere.",'red'))
            except ValueError:
                print(colored("Ongeldige invoer. Probeer opnieuw.",'red'))
          
    return schepen_locaties


# Bord voor speler 1
Verborgen_speler1 = [[' '] * 4 for _ in range(4)]
Gok_speler1 = [[' '] * 4 for _ in range(4)]
schepen_locaties_speler1 = handmatige_plaatsing_schepen(Verborgen_speler1, 1)

# Bord voor speler 2
Verborgen_speler2 = [[' '] * 4 for _ in range(4)]
Gok_speler2 = [[' '] * 4 for _ in range(4)]
schepen_locaties_speler2 = handmatige_plaatsing_schepen(Verborgen_speler2, 2)

def count_hit_schepen(bord):
    count = 0
    for row in bord:
        for column in row:
            if column == 'X':
                count += 1
    return count

speler1_aan_zet = True

while True:
    if speler1_aan_zet:
        print("Speler 1:")
        Verborgen = Verborgen_speler2  
        Gok = Gok_speler1
        schepen_locaties = schepen_locaties_speler2
    else:
        print("Speler 2:")
        Verborgen = Verborgen_speler1 
        Gok = Gok_speler2
        schepen_locaties = schepen_locaties_speler1

    turns = 6

    while turns > 0:
        print('De kapitein wacht op jouw orders!')
        print_bord(Gok)
        row, column = get_ship_location(Gok)

        if Gok[row][column] == '-':
            print(colored("Deze plek was al eens geraden, Matroos! We hebben geen ammunitie in overvloed!",'light_red'))
        elif Gok[row][column] == 'X':
            print(colored("Je hebt hier al geschoten, Matroos! We hebben geen onbeperkte kogels!",'light_red'))
        elif Verborgen[row][column] == 'X':
            print(colored("Geraakt!",'yellow'))
            Gok[row][column] = 'X'
            turns -= 1
        else:
            print(colored("Dat was ernaast!",'light_red'))
            Gok[row][column] = '-'
            turns -= 1

        if count_hit_schepen(Gok) == 4:  # Aantal schepen in totaal
            print(colored(f"PROFICIAT! de torpedo's zijn onderweg naar alle vijandelijke schepen, we gaan huiswaarts. Speler {1 if speler1_aan_zet else 2} heeft alles geraakt!",'yellow'))
            break

        print(' Nog ' + str(turns) + ' Kogels ')
        if turns == 0:
            print(f'Game Over! Hier zijn de locaties van de vijandelijke schepen voor speler {1 if speler1_aan_zet else 2}:')
            for locatie in schepen_locaties:
                print(f"Schip op locatie: {chr(ord('A') + locatie[1])}{locatie[0] + 1}")

    opnieuw_spelen = input(colored("Speler 2, klaar? (ja/nee): ",'light_blue')).lower()
    if opnieuw_spelen != 'ja':
        print("De vijandelijke vloot geeft forfeit")
        break  # Stop de lus als de gebruiker niet opnieuw wil spelen

    # Wissel de beurt tussen de spelers
    speler1_aan_zet = not speler1_aan_zet
