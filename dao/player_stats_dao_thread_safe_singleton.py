from tinydb import TinyDB, Query
from domain.visit import Dart

import threading


class PlayerStatsDao:
    __instance = None

    @staticmethod
    def get_instance():
        if PlayerStatsDao.__instance is None:
            with threading.Lock():
                if PlayerStatsDao.__instance is None:  # Double locking mechanism
                    PlayerStatsDao()
        return PlayerStatsDao.__instance

    def __init__(self):
        if PlayerStatsDao.__instance is not None:
            raise Exception("This is a singleton!")
        else:
            PlayerStatsDao.__instance = self
        self.db = TinyDB('player_stats.json')
        self.lock = threading.Lock()

    def add(self, stat):
        self.lock.acquire()

        player_stats = Query()
        dart_count = 0
        dart_total = 0
        for d in stat[2]:
            dart_count = dart_count + 1
            dart_total = dart_total + Dart(d[0], d[1]).get_score()
            # maybe a static get_score would use less resources
        if not self.db.contains(player_stats.player == stat[0]):
            self.db.insert({'player': stat[0], 'numDarts': dart_count, 'totalScore': dart_total})
        else:
            my_stat = self.db.get(player_stats.player == stat[0])
            print(my_stat)
            self.db.update({'player': stat[0],
                            'numDarts': my_stat["numDarts"] + dart_count,
                            'totalScore': my_stat["totalScore"] + dart_total},
                           player_stats.player == stat[0])

        self.lock.release()
