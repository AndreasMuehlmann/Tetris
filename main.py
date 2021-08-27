import pygame
import random
import copy
pygame.init()
basic_font=pygame.font.SysFont(None, 48)
SCHWARZ = (0, 0, 0)
ROT = (255, 0, 0)
LILA = (255, 0, 255)
LIMETTE = (0, 255, 0)
BLAU = (0, 0, 255)
GRAU = (127, 127, 127)
BREITE = 1000
SEITENABSTAND = 200
DICKE_LINIE = 4
SPIEL_FELD_BREITE = BREITE - SEITENABSTAND * 2
KASTENLÄNGE = int((SPIEL_FELD_BREITE) / 10)
HÖHE = KASTENLÄNGE * 16
SPIEL_FELD_HÖHE = HÖHE - KASTENLÄNGE
FEN = pygame.display.set_mode((BREITE, HÖHE))
pygame.display.set_caption('TETRIS')
FPS = 60
NORMAL_GESCHWINDIGKEIT = 30
VERZÖGERUNG_BEWEGEN = 10
werte_stücke = []


class STÜCK:


    def __init__(self, farbe, drehpunkt, verhältnisse_drehpunkt, ausrichtung, drehbar):
        self.quadrate = []
        self.farbe = farbe
        self.drehpunkt = drehpunkt
        self.verhältnisse_drehpunkt = verhältnisse_drehpunkt
        self.ausrichtung = ausrichtung
        self.drehbar = drehbar
        self.x = self.drehpunkt[0] * KASTENLÄNGE 
        self.y = self.drehpunkt[1] * KASTENLÄNGE
        return

    def aktualisieren_zeichnen(self):
        indexe_stück = self.indexe_stück_geben()
        for quadrat in range(len(indexe_stück)):
            pygame.draw.rect(FEN, self.farbe, pygame.Rect(SEITENABSTAND + indexe_stück[quadrat][0] * KASTENLÄNGE, indexe_stück[quadrat][1] * KASTENLÄNGE, KASTENLÄNGE, KASTENLÄNGE))

    def verschieben_und_prüfen(self):
        möglich = False
        while not möglich:
            verschiebung = random.randint(0, int(SPIEL_FELD_BREITE / KASTENLÄNGE))
            self.x = KASTENLÄNGE * verschiebung
            self.drehpunkt[0] = verschiebung
            indexe_stück = self.indexe_stück_geben()
            for quadrat in range(len(indexe_stück)):
                if indexe_stück[quadrat][0] < 0 or indexe_stück[quadrat][0] >= int(SPIEL_FELD_BREITE / KASTENLÄNGE):
                    break
                elif quadrat == len(indexe_stück) - 1:
                    möglich = True
        return

    def fallen(self):
        self.y += KASTENLÄNGE
        self.drehpunkt[1] += 1
        return

    def nach_rechts_bewegen(self):
        self.x += KASTENLÄNGE
        self.drehpunkt[0] += 1
        return

    def nach_links_bewegen(self):
        self.x -= KASTENLÄNGE
        self.drehpunkt[0] -= 1
        return

    def indexe_stück_geben(self):
        indexe_stück = []
        for quadrat in range(len(self.verhältnisse_drehpunkt)):
            if self.ausrichtung == 0:
                indexe_stück.append([self.drehpunkt[0] + self.verhältnisse_drehpunkt[quadrat][0], self.drehpunkt[1] + self.verhältnisse_drehpunkt[quadrat][1]])
            elif self.ausrichtung == 1:
                indexe_stück.append([self.drehpunkt[0] - self.verhältnisse_drehpunkt[quadrat][1], self.drehpunkt[1] + self.verhältnisse_drehpunkt[quadrat][0]])
            elif self.ausrichtung == 2:
                indexe_stück.append([self.drehpunkt[0] - self.verhältnisse_drehpunkt[quadrat][0], self.drehpunkt[1] - self.verhältnisse_drehpunkt[quadrat][1]])
            elif self.ausrichtung == 3:
                indexe_stück.append([self.drehpunkt[0] + self.verhältnisse_drehpunkt[quadrat][1], self.drehpunkt[1] - self.verhältnisse_drehpunkt[quadrat][0]])
        return indexe_stück

    def ausrichtung_aendern(self, richtung):
        if richtung == 'links':
            if self.ausrichtung == 0:
                self.ausrichtung = 3
            else:
                self.ausrichtung -= 1
        if richtung == 'rechts':
            if self.ausrichtung == 3:
                self.ausrichtung = 0
            else:
                self.ausrichtung += 1
        return


def zufälliges_stück_machen(stücke, werte_stücke):
    werte_stück = werte_stücke[random.randint(0, len(werte_stücke) - 1)]
    stück = copy.deepcopy(STÜCK(werte_stück[0], werte_stück[1], werte_stück[2], random.randint(0, 3), werte_stück[3]))
    stück.verschieben_und_prüfen()
    stücke.append(stück)
    return stücke


def übersicht_liste_machen():
    übersicht_liste = []
    for zeile in range(int(SPIEL_FELD_HÖHE / KASTENLÄNGE)):
        übersicht_liste.append([])
        for spalte in range(int(SPIEL_FELD_BREITE / KASTENLÄNGE)):
            übersicht_liste[zeile].append(False)
    return übersicht_liste


def übersicht_liste_aktualisieren(übersicht_liste, indexe_stück):
    for quadrat in range(len(indexe_stück)):
        übersicht_liste[indexe_stück[quadrat][1]][indexe_stück[quadrat][0]] = True
    return


def übersicht_liste_zurücksetzen(übersicht_liste, indexe_stück):
    for quadrat in range(len(indexe_stück)):
        übersicht_liste[indexe_stück[quadrat][1]][indexe_stück[quadrat][0]] = False
    return


def volle_zeilen_geben(übersicht_liste):
    volle_zeilen = []
    for zeile in range(len(übersicht_liste)):
        for spalte in range(len(übersicht_liste[0])):
            if not übersicht_liste[zeile][spalte]:
                break
            if spalte == len(übersicht_liste[0]) - 1:
                volle_zeilen.append(zeile)
    return volle_zeilen


def volle_zeilen_zurücksetzen_und_fallen_wenn_möglich(übersicht_liste, indexe_stück, stücke, volle_zeilen, score):
    volle_zeilen_aus_übersicht_liste_zurücksetzen(übersicht_liste, volle_zeilen)
    quadrate_voller_zeilen_löschen(stücke, volle_zeilen)
    geteilte_stücke_zu_einzelnen_stücken_machen(stücke)
    nochmal_checken = fallen_oberer_stücke(übersicht_liste, stücke)
    if nochmal_checken:
        volle_zeilen_zurücksetzen_und_fallen_wenn_möglich(übersicht_liste, indexe_stück, stücke, volle_zeilen_geben(übersicht_liste), score)
    score += len(volle_zeilen)
    return score


def volle_zeilen_aus_übersicht_liste_zurücksetzen(übersicht_liste, volle_zeilen):
    for volle_zeile in range(len(volle_zeilen)):
        for spalte in range(len(übersicht_liste[0])):
            übersicht_liste[volle_zeilen[volle_zeile]][spalte] = False
    return


def quadrate_voller_zeilen_löschen(stücke, volle_zeilen):
    schon_gelöschte_stücke = 0    
    for stück in range(len(stücke)):
        stück -= schon_gelöschte_stücke
        indexe_stück = stücke[stück].indexe_stück_geben()
        schon_gelöschte_quadrate = 0
        for quadrat in range(len(indexe_stück)):
            if indexe_stück[quadrat][1] in volle_zeilen:
                del stücke[stück].verhältnisse_drehpunkt[quadrat - schon_gelöschte_quadrate]
                schon_gelöschte_quadrate += 1
        if len(stücke[stück].verhältnisse_drehpunkt) == 0:
            del stücke[stück]
            schon_gelöschte_stücke += 1
    return


def geteilte_stücke_zu_einzelnen_stücken_machen(stücke):
    geteilte_stücke = geteilte_stücke_geben(stücke)
    stücke = []
    for bruch_stück in range(len(geteilte_stücke)):
        stück = copy.deepcopy(STÜCK(geteilte_stücke[bruch_stück][0], geteilte_stücke[bruch_stück][1], geteilte_stücke[bruch_stück][2],geteilte_stücke[bruch_stück][3], geteilte_stücke[bruch_stück][4]))
        stücke.append(stück)


def geteilte_stücke_geben(stücke):
    geteilte_stücke = []
    for stück in range(len(stücke)):
        indexe_stück = stücke[stück].indexe_stück_geben()
        alle_quadrate_eingeordnet = False
        while not alle_quadrate_eingeordnet:
            geteilte_stücke.append([stücke[stück].farbe, indexe_stück[0], [[0,0]], 0, stücke[stück].drehbar])
            del indexe_stück[0]
            war_verbindung = True
            while war_verbindung:
                war_verbindung = verbindung_festellen_und_einordnen(indexe_stück, geteilte_stücke[stück])
            if len(indexe_stück) == 0:
                alle_quadrate_eingeordnet = True
    return geteilte_stücke


def verbindung_festellen_und_einordnen(indexe_stück, geteilte_stücke):
    war_verbindung = False
    vergleichs_quadrat = 0
    while vergleichs_quadrat < len(indexe_stück):
        if ist_verbindung(geteilte_stücke, indexe_stück, vergleichs_quadrat):
            geteilte_stücke[2].append(verhältnis_drehpunkt_geben(indexe_stück[vergleichs_quadrat], geteilte_stücke[1], 0))
            del indexe_stück[vergleichs_quadrat]
            vergleichs_quadrat -= 1
            war_verbindung = True
        vergleichs_quadrat +=1
    return war_verbindung


def ist_verbindung(geteiltes_stück, indexe_stück, vergleichs_quadrat):
    for quadrat in range(len(geteiltes_stück[2])):
        ist_x_unterschied_kleiner_gleich_1 = -1 <= geteiltes_stück[1][0] + geteiltes_stück[2][quadrat][0] - indexe_stück[vergleichs_quadrat][0] <= 1
        ist_y_unterschied_kleiner_gleich_1 = -1 <= geteiltes_stück[1][1] + geteiltes_stück[2][quadrat][1] - indexe_stück[vergleichs_quadrat][1] <= 1
        if ist_x_unterschied_kleiner_gleich_1 and ist_y_unterschied_kleiner_gleich_1:
            return True
    return False


def verhältnis_drehpunkt_geben(quadrat, drehpunkt, ausrichtung):
    if ausrichtung == 0:
        return [quadrat[0] - drehpunkt[0], quadrat[1] - drehpunkt[1]]
    elif ausrichtung == 1:
        return [quadrat[1] + drehpunkt[0], quadrat[0] - drehpunkt[1]]
    elif ausrichtung == 2:
        return [quadrat[0] + drehpunkt[0], quadrat[1] + drehpunkt[1]]
    elif ausrichtung == 3:
        return [quadrat[1] - drehpunkt[0], quadrat[0] + drehpunkt[1]]


def fallen_oberer_stücke(übersicht_liste, stücke):
    verhindernde_stücke = {}
    nochmal_checken = False
    stück = 0
    while stück < len(stücke):
        indexe_stück = stücke[stück].indexe_stück_geben()
        übersicht_liste_zurücksetzen(übersicht_liste, indexe_stück)
        ist_gefallen= fallen_und_verhakungen_entfernen(stücke, stück, indexe_stück, verhindernde_stücke, übersicht_liste)
        indexe_stück = stücke[stück].indexe_stück_geben()
        übersicht_liste_aktualisieren(übersicht_liste, indexe_stück)
        if ist_gefallen:
            nochmal_checken = True
        stück += 1
    return nochmal_checken


def fallen_und_verhakungen_entfernen(stücke, stück, indexe_stück, verhindernde_stücke, übersicht_liste):
    ist_gefallen = False
    möglich = fallen_oberes_stück(stücke, stück, übersicht_liste)
    if möglich:
        ist_gefallen = True
    else:
        ist_verhakung_entfernt = verhakung_entfernen(stücke, stück, indexe_stück, verhindernde_stücke, übersicht_liste)
        if ist_verhakung_entfernt:
            fallen_und_verhakungen_entfernen(stücke, stück, indexe_stück, verhindernde_stücke, übersicht_liste)
    return ist_gefallen


def fallen_oberes_stück(stücke, stück, übersicht_liste):
    möglich = False
    indexe_stück = stücke[stück].indexe_stück_geben()
    if fallen_möglich(übersicht_liste, indexe_stück):
        stücke[stück].fallen()
        möglich = True
        fallen_oberes_stück(stücke, stück, übersicht_liste)
    return möglich


def verhakung_entfernen(stücke, stück, indexe_stück, verhindernde_stücke, übersicht_liste):
    ist_verhakung_entfernt = False
    verhindernde_stücke[stück] = verhindernde_stücke_geben(stücke, stück, indexe_stück)
    if len(verhindernde_stücke[stück]) > 0:
        verhaktes_stück = verhakung_geben(stück, verhindernde_stücke)
        if verhaktes_stück is not None:
            zu_einem_stück_machen(stücke, stück, verhaktes_stück)
            indexe_stück = stücke[stück].indexe_stück_geben()
            übersicht_liste_aktualisieren(übersicht_liste, indexe_stück)
            abhängigkeiten_zurücksetzen(stücke, stück, verhindernde_stücke, verhaktes_stück)
            indexe_stück = stücke[stück].indexe_stück_geben()
            übersicht_liste_zurücksetzen(übersicht_liste, indexe_stück)
            ist_verhakung_entfernt = True
    return ist_verhakung_entfernt


def verhindernde_stücke_geben(stücke, stück, indexe_stück):
    verhindernde_stücke = []
    for quadrat in range(len(indexe_stück)):
        for vergleichs_stück in range(len(stücke)):
            if vergleichs_stück != stück:
                indexe_vergleichs_stück = stücke[vergleichs_stück].indexe_stück_geben()
                for vergleichs_quadrat in range(len(indexe_vergleichs_stück)):
                    if indexe_stück[quadrat][0] == indexe_vergleichs_stück[vergleichs_quadrat][0]:
                        if indexe_stück[quadrat][1] + 1 == indexe_vergleichs_stück[vergleichs_quadrat][1]:
                            verhindernde_stücke.append(vergleichs_stück)
                            break
    return verhindernde_stücke


def verhakung_geben(stück, verhindernde_stücke):
    for verhinderndes_stück in range(len(verhindernde_stücke[stück])):
        if verhindernde_stücke[stück][verhinderndes_stück] in verhindernde_stücke and stück in  verhindernde_stücke[verhindernde_stücke[stück][verhinderndes_stück]]:
            return verhindernde_stücke[stück][verhinderndes_stück]            


def zu_einem_stück_machen(stücke, stück, verhaktes_stück):
    indexe_stück_verhakt = stücke[verhaktes_stück].indexe_stück_geben()
    for quadrat in range(len(indexe_stück_verhakt)):
        stücke[stück].verhältnisse_drehpunkt.append(verhältnis_drehpunkt_geben(indexe_stück_verhakt[quadrat], stücke[stück].drehpunkt, stücke[stück].ausrichtung))        
    return


def abhängigkeiten_zurücksetzen(stücke, stück, verhindernde_stücke, verhaktes_stück):
    verhindernde_stücke[stück] = verhindernde_stücke[stück] + verhindernde_stücke[verhaktes_stück]
    verhindernde_stücke[stück].remove(stück)
    verhindernde_stücke[stück].remove(verhaktes_stück)
    del stücke[verhaktes_stück]
    return


def drehen_möglich(indexe_stück, übersicht_liste, stück, richtung):
    stück.ausrichtung_aendern(richtung)
    indexe_stück = stück.indexe_stück_geben()
    for quadrat in range(len(indexe_stück)):
        if indexe_stück[quadrat][0] < 0 or indexe_stück[quadrat][0] > len(übersicht_liste[0]) - 1 or indexe_stück[quadrat][1] < 0 or indexe_stück[quadrat][1] > len(übersicht_liste) - 1 or übersicht_liste[indexe_stück[quadrat][1]][indexe_stück[quadrat][0]]:
            if richtung == 'links':
                stück.ausrichtung_aendern('rechts')
            else:
                stück.ausrichtung_aendern('links')
            return False
    if richtung == 'links':
        stück.ausrichtung_aendern('rechts')
    else:
        stück.ausrichtung_aendern('links')
    return True


def fallen_möglich(übersicht_liste, indexe_stück):
    for quadrat in range(len(indexe_stück)):
        if not indexe_stück[quadrat][1] < len(übersicht_liste) - 1 or übersicht_liste[indexe_stück[quadrat][1] + 1][indexe_stück[quadrat][0]]:
             return False
    return True


def nach_links_bewegen_möglich(übersicht_liste, indexe_stück):
    for quadrat in range(len(indexe_stück)):
        if not indexe_stück[quadrat][0] > 0 or übersicht_liste[indexe_stück[quadrat][1]][indexe_stück[quadrat][0] - 1]:
             return False
    return True


def nach_rechts_bewgen_möglich(übersicht_liste, indexe_stück):
    for quadrat in range(len(indexe_stück)):
        if not indexe_stück[quadrat][0] < len(übersicht_liste[0]) - 1 or übersicht_liste[indexe_stück[quadrat][1]][indexe_stück[quadrat][0] + 1]:
             return False
    return True


def ist_spiel_fertig(übersicht_liste, indexe_stück):
    for quadrat in range(len(indexe_stück)):
         if indexe_stück[quadrat][1] < 2:
             if not fallen_möglich(übersicht_liste, indexe_stück):
                return True
    return False


def pausieren(Uhr):
    tasten_gedrückt = pygame.key.get_pressed()
    while not tasten_gedrückt[pygame.K_u]:
        Uhr.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        tasten_gedrückt = pygame.key.get_pressed()
    return True


def FEN_zeichnen(stücke, score):
    FEN.fill(SCHWARZ)
    pygame.draw.line(FEN, GRAU, (SEITENABSTAND - DICKE_LINIE, 0), (SEITENABSTAND - DICKE_LINIE, HÖHE + DICKE_LINIE + 2 - KASTENLÄNGE), DICKE_LINIE)
    pygame.draw.line(FEN, GRAU, (BREITE - SEITENABSTAND + DICKE_LINIE, 0), (BREITE - SEITENABSTAND + DICKE_LINIE, HÖHE + DICKE_LINIE + 2 - KASTENLÄNGE), DICKE_LINIE)
    pygame.draw.line(FEN, GRAU, (SEITENABSTAND - int(DICKE_LINIE / 2),HÖHE + DICKE_LINIE - KASTENLÄNGE), (BREITE - SEITENABSTAND + int(DICKE_LINIE / 2),HÖHE + DICKE_LINIE - KASTENLÄNGE), DICKE_LINIE)
    for kasten in range(1, int(SPIEL_FELD_BREITE/ KASTENLÄNGE)):
        pygame.draw.line(FEN, GRAU, (SEITENABSTAND - DICKE_LINIE + kasten, 0), (SEITENABSTAND - DICKE_LINIE + kasten, HÖHE + int(DICKE_LINIE * 1.5) - KASTENLÄNGE), int(DICKE_LINIE / 2))
    for stück in range(len(stücke)):
        stücke[stück].aktualisieren_zeichnen()
    score_text = basic_font.render('SCORE: ' + str(score), True, (255,255,255))
    FEN.blit(score_text, (20,20))
    pygame.display.update()


def main():
    score = 0
    übersicht_liste = übersicht_liste_machen()
    werte_l_stück_rechts = [LIMETTE, [0, 1], [[0, -1], [0, 0], [0, 1], [1, 1]], [True]]
    werte_l_stück_links = [LILA, [0, 1], [[0, -1], [0, 0], [0, 1], [-1, 1]], [True]]
    werte_platte = [BLAU, [0, 1], [[0, -2], [0, -1], [0, 0], [0, 1]], [True]]
    werte_quadrat = [ROT, [0, 0], [[0, 0], [1, 0], [0, 1], [1, 1]], [False]]
    werte_werte_l_stück_rechts_kurz = [(125, 0, 0), [0, 1], [[0, -1], [0, 0], [1, 0]], [True]]
    werte_dreieck = [(0,125,0), [0, 1], [[0, -1], [0, 0], [1, 0], [0, 1]], [True]]
    werte_punkt = [(125,125,0), [0, 2], [[0, 0]], [False]]
    werte_u = [(0,0,125), [0, 2], [[-1, -1], [-1, 0], [0, 0], [1, 0], [1, -1]], [True]]
    werte_stücke  = [werte_punkt, werte_platte]
    stücke = []
    stücke = zufälliges_stück_machen(stücke, werte_stücke)
    uhr = pygame.time.Clock()
    schnelligkeit = NORMAL_GESCHWINDIGKEIT
    zähler_fallen = 0
    zähler_bewegen = VERZÖGERUNG_BEWEGEN
    zähler_drehen = VERZÖGERUNG_BEWEGEN
    FEN_zeichnen(stücke, score)
    laufen = pausieren(uhr)
    while laufen:
        uhr.tick(FPS)
        FEN_zeichnen(stücke, score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                laufen = False
                break
        stück = len(stücke) - 1
        indexe_stück = stücke[stück].indexe_stück_geben()
        tasten_gedrückt = pygame.key.get_pressed()
        if tasten_gedrückt[pygame.K_p]:
            laufen = pausieren(uhr)
        if tasten_gedrückt[pygame.K_a] and nach_links_bewegen_möglich(übersicht_liste, indexe_stück) and zähler_bewegen >= VERZÖGERUNG_BEWEGEN:
            stücke[stück].nach_links_bewegen()
            indexe_stück = stücke[stück].indexe_stück_geben()
            zähler_bewegen = -1
        if tasten_gedrückt[pygame.K_d] and nach_rechts_bewgen_möglich(übersicht_liste, indexe_stück) and zähler_bewegen >= VERZÖGERUNG_BEWEGEN:
            stücke[stück].nach_rechts_bewegen()
            indexe_stück = stücke[stück].indexe_stück_geben()
            zähler_bewegen = -1
        if zähler_fallen >= schnelligkeit and ist_spiel_fertig(übersicht_liste, indexe_stück):
            laufen = False
        if zähler_fallen >= schnelligkeit:
            if fallen_möglich(übersicht_liste, indexe_stück):
                stücke[stück].fallen()
                indexe_stück = stücke[stück].indexe_stück_geben()
                zähler_fallen = -1
            else:
                übersicht_liste_aktualisieren(übersicht_liste, indexe_stück)
                volle_zeilen = volle_zeilen_geben(übersicht_liste)
                if len(volle_zeilen) > 0:
                     score = volle_zeilen_zurücksetzen_und_fallen_wenn_möglich(übersicht_liste, indexe_stück, stücke, volle_zeilen, score)
                stücke = zufälliges_stück_machen(stücke, werte_stücke)
                zähler_fallen = -1
                continue
        if tasten_gedrückt[pygame.K_RIGHT] and stücke[stück].drehbar and drehen_möglich(indexe_stück, übersicht_liste, stücke[stück],'rechts') and not stücke[stück].drehpunkt == [0, 0] and zähler_drehen >= VERZÖGERUNG_BEWEGEN:
            stücke[stück].ausrichtung_aendern('rechts')
            indexe_stück = stücke[stück].indexe_stück_geben()
            zähler_drehen = -1
        if tasten_gedrückt[pygame.K_LEFT] and stücke[stück].drehbar and drehen_möglich(indexe_stück, übersicht_liste, stücke[stück],'links') and not stücke[stück].drehpunkt == [0, 0] and zähler_drehen >= VERZÖGERUNG_BEWEGEN:
            stücke[stück].ausrichtung_aendern('links')
            indexe_stück = stücke[stück].indexe_stück_geben()
            zähler_drehen = -1
        if tasten_gedrückt[pygame.K_s]:
            schnelligkeit = int(NORMAL_GESCHWINDIGKEIT / 5)
        else:
            schnelligkeit = NORMAL_GESCHWINDIGKEIT
        zähler_fallen += 1
        zähler_bewegen += 1
        zähler_drehen += 1
    pygame.quit()


if __name__ == '__main__':
    main()