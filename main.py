#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import os


class Player:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.score = 0

    def __str__(self):
        return "%s : %i" % (self.name, self.score)


class Contract:
    def __init__(self, id):
        self.id = id
        self.mult = {'p': 1, 'g': 2, 'gs': 4, 'gc': 8, 'c': 16}[id]
        self.value = 25
        self.add_value = 0
        self.oudlers = -1

    def get_score(self, points):
        goal = {'0': 56, '1': 51, '2': 41, '3': 36}[self.oudlers]
        winner_mult = 1 if goal <= points else -1
        return ((contract.value + abs(goal - points)) * contract.mult + contract.add_value) * winner_mult

    help_message = """
Points à faire :
0 bout  : 56
1 bout  : 51
2 bouts : 41
3 bouts : 36"""

    def get_player(message, players):
        player_id = raw_input(message + ' : ' + ' / '.join([str(p.id) + ' - ' + p.name for p in players]) + ' ?\n')
        return next((p for p in players if p.id == int(player_id)), None)

    def raise_error():
        raise ValueError('Merci de rentrer un id valide et d\'ARRÊTER L\'ALCOOL')

    def input(message):
        message = message.replace('[', '[\033[31m\033[1m')
        message = message.replace(']', '\033[0m]')
        return raw_input(message)

    if __name__ == '__main__':

        players = []
        for i in range(1, 6):
            name = raw_input('Player %i: ' % i)
            players.append(Player(i, name))

        try:
            f = open('tarot.save', 'a')
            f.write('\n=============== NEW GAME ===============\n')
            f.close()
        except:
            print "Impossible d'ouvrir le fichier de sauvegarde 'toto.save'. La partie ne sera pas sauvegardée."

        stop = False
        clear = True

        while not stop:
            if not clear:
                raw_input('')
                clear = True
                continue
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
                clear = False
            try:
                save = ' | '.join([p.name + ':' + str(p.score) for p in players]) + '\n'
                f = open('toto.save', 'a')
                f.write(save)
                f.close()
            except:
                pass
            print '\n===================================== \033[32m\033[1mTAROT\033[0m =====================================\n'
            try:
                command = input('Commandes: [s]cores / [h]elp / [e]ntrer points / [j]ouer une partie / [q]uitter\n')
                if command == 's':
                    for player in sorted(players, key=lambda p: -1 * p.score):
                        print player
                    continue
                if command == 'h':
                    print help_message
                    continue
                if command == 'e':
                    for player in players:
                        points = input('Points de %s: ' % player.name)
                        player.score = int(points)
                    s = 0
                    for player in players:
                        s += player.score
                    if s != 0:
                        print "Score invalide. La somme des scores vaut %d" % s
                        for player in players:
                            player.score = 0
                if command == 'j':
                    contract_id = input('Contrat joué: [p]etite / [g]arde / [gs] garde sans / [gc] garde contre / [c]helem:\n')
                    if contract_id not in ['p', 'g', 'gs', 'gc', 'c']:
                        raise_error()
                    contract = Contract(contract_id)

                    main_player = get_player('Joué par', players)
                    if main_player is None:
                        raise_error()
                    second_player = get_player('Allié avec', players)
                    if second_player is None:
                        raise_error()

                    team1 = [main_player, second_player]
                    team2 = [p for p in players if p not in team1]
                    supp = input('Autres trucs: petit au [b]out / [m]isère / [p]oignée (8) / [d]ouble poignée (10) / [t]riple poignée (13) ?\n')

                    for char in supp:
                        if char == 'b':
                            player = get_player('Petit au bout pour', players)
                            if player is None:
                                raise_error()
                            tmp_mult = 1 if player in team1 else -1
                            main_player.score += tmp_mult * 20 * contract.mult
                            second_player.score += tmp_mult * 10 * contract.mult * (1 if main_player != second_player else 2)
                            for p in team2:
                                p.score += -tmp_mult * 10 * contract.mult

                        if char == 'm':
                            player = get_player('Misère pour', players)
                            if player is None:
                                raise_error()
                            player.score += 40
                            for p in players:
                                if p.id != player.id:
                                    p.score -= 10

                        if char == 'p':
                            contract.add_value += 20
                        if char == 'd':
                            contract.add_value += 30
                        if char == 't':
                            contract.add_value += 40

                    score_made = int(input('Points faits: '))
                    contract.oudlers = input('Nombre de bouts: ')

                    points = contract.get_score(score_made)
                    main_player.score += 2 * points
                    second_player.score += (1 if main_player != second_player else 2) * points
                    for p in team2:
                        p.score -= points
                if command == 'q':
                    stop = True
            except ValueError as e:
                print '\nUne erreur s\'est produite, c\'est certainement de votre faute. Pour votre gouverne, voici le détail de l\'erreur en question :'
                print e.message
                print '\nReprenons\n'
