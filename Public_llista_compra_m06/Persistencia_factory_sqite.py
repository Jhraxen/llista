#!/usr/bin/python3
# -*- coding: utf-8 -*-

import Persistencia_factory, Persistencia_usuari_sqlite

"""
    Persistencia_factory_redis.py
    Classe que defineix la interficie amb la fàbrica de persistencia per a redis.
"""

class Persistencia_factory_redis(Persistencia_factory.Persistencia_factory):
    def __init__(self, ruta, configurador):
        self.ruta = ruta
        self.configurador = configurador

    def get_Persistencia_usuari_factory(self):
        return Persistencia_usuari_sqlite.Persistencia_usuari_redis(
            self.ruta, 
            self.configurador
            )

    