def get_perioden(filename):

    file = open(filename, 'r')
    Lines = file.readlines()
    Lines = Lines[1:]
    for i in range(len(Lines)):   
        Lines[i] = int(Lines[i])
    return Lines

def berechne_weg(perioden):
    """
    Berechnet den schnellsten Weg zum Grabmal.

    Args:
        perioden: Eine Liste von Ganzzahlen, die die Perioden der Steinquader in den Abschnitten des Ganges darstellen.

    Returns:
        Eine Liste von Tupeln, die die Instruktionen für Petra darstellen. Jedes Tupel enthält die Zeit in Minuten und die Aktion (Warten oder Weitergehen).
    """

    anzahl_abschnitte = len(perioden)
    max_zeit = 2 * max(perioden) * anzahl_abschnitte  # Maximale Simulationszeit (kann angepasst werden)

    # Initialisierung des Zustands der Quader (True = blockiert, False = frei)
    quader_zustand = [[True] * anzahl_abschnitte for _ in range(max_zeit + 1)]

    # Simulation der Quaderbewegungen
    for t in range(1, max_zeit + 1):
        for i, periode in enumerate(perioden):
            if (t // periode) % 2 == 0:  # Quader blockiert
                quader_zustand[t][i] = True
            else:  # Quader frei
                quader_zustand[t][i] = False
    
    # Suche nach dem schnellsten Weg
    wege = [[(0, 0)]]  # Liste von möglichen Wegen (Startpunkt bei Zeit 0)
    fertige_wege = []  # Liste von abgeschlossenen Wegen zum Grabmal

    while wege:
        aktueller_weg = wege.pop(0)
        aktuelle_zeit, aktuelle_position = aktueller_weg[-1]

        if aktuelle_position == anzahl_abschnitte - 1:  # Grabmal erreicht
            fertige_wege.append(aktueller_weg)
            continue

        # Mögliche Aktionen: Warten oder Weitergehen
        neuer_weg = aktueller_weg[:]        
        # Weitergehen
        if (aktuelle_position + 1 < anzahl_abschnitte) and (aktuelle_zeit + 1 <= max_zeit) and \
                (not quader_zustand[aktuelle_zeit + 1][aktuelle_position]) and \
                (not quader_zustand[aktuelle_zeit + 1][aktuelle_position + 1]):            
            neuer_weg.append((aktuelle_zeit + 1, aktuelle_position + 1))
        else: #Warten
            neuer_weg.append((aktuelle_zeit + 1, aktuelle_position))
       
        wege.append(neuer_weg)

    # Finde den schnellsten Weg
    if fertige_wege:
        schnellster_weg = min(fertige_wege, key=lambda x: x[-1][0])
        instruktionen = []
        start_zeit = -1
        for i in range(1, len(schnellster_weg)):
            zeit, position = schnellster_weg[i]            
            vorherige_zeit, vorherige_position = schnellster_weg[i - 1]
            if start_zeit == -1:
               start_zeit = zeit -1 
            if position != vorherige_position: 
                if position ==   anzahl_abschnitte - 1:    
                    instruktionen.append( "Warte " + str(zeit - start_zeit) + ", laufe zum Grabmal")
                else:         
                    instruktionen.append(( "Warte " + str(zeit - start_zeit) + ", laufe in Abschnitt " + str(position + 1)))
                start_zeit = zeit
        return instruktionen
    else:
        return "Kein Weg zum Grabmal gefunden."

# Aufruf
#perioden = [5, 8, 12, 16, 21,73]
perioden = get_perioden("grabmal4.txt")

instruktionen = berechne_weg(perioden)

if isinstance(instruktionen, list):
    print("Instruktionen für Petra:")
    for aktion in instruktionen:
        print(f"{aktion}")
else:
    print(instruktionen)