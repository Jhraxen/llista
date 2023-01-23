#!/usr/bin/python3
# -*- coding: utf-8 -*-

import Persistencia_usuari, Usuari
import sqlite3

class Persistencia_usuari_sqlite(Persistencia_usuari.Persistencia_usuari):
    con = sqlite3.connect('bbdd.sql')
    c = con.cursor()
    def __init__(self, ruta, configurador):
        self.ruta = ruta
        self.configurador = configurador

    def get(self, id):
        db = self.__get_db_connection()
        query = "Select usuari, password_hash from usuaris where id="+str(id)+";"
        cursor = db.cursor()
        cursor.execute(query)

        registres = cursor.fetchall()
        if len(registres) > 0:
            usuari_nom = registres[0][0]
            usuari_password_hash = registres[0][1]
            resultat = Usuari.Usuari(self.configurador.get_Persistencia_factory().get_Persistencia_usuari_factory(), id, usuari_nom, usuari_password_hash)
            return resultat
        return None

    def get_from_apikey(self, id_sessio):
        db = self.__get_db_connection()
        query = "select id, usuaris.usuari, password_hash from usuaris inner join sessions_usuaris on (sessions_usuaris.usuari = usuaris.id) where sessions_usuaris.uuid =\'"+id_sessio+"\';"
        cursor = db.cursor()
        cursor.execute(query)

        registres = cursor.fetchall()
        if len(registres) > 0:
            usuari_id = registres[0][0]
            usuari_nom = registres[0][1]
            usuari_password = registres[0][2]
            resultat = Usuari.Usuari(self.configurador.get_Persistencia_factory().get_Persistencia_usuari_factory(), usuari_id, usuari_nom, usuari_password)
            return resultat
        return None

    def desa(self, usuari):
        db = self.__get_db_connection()
        id = self.__get_id_by_nom(usuari.get_nom())
        if id is None:
            query = "Insert into usuaris (usuari, password_hash) " + "values(\'"+usuari.get_nom()+"\',\'" + usuari.get_password_hash().decode('utf-8')+"\');"

            cursor = db.cursor()
            resultat = None
            try:
                cursor.execute(query)
                db.commit()
                id = self.__get_id_by_nom(usuari.get_nom())
            except sqlite3.IntegrityError as error:
                print(str(error))
                id = None
            cursor.close()
            db.close()
        return id

    def get_llista(self):
        llista = []
        db = self.__get_db_connection()
        
        query = "Select id from usuaris;"
        cursor = db.cursor()
        cursor.execute(query)

        registres = cursor.fetchall()
        cursor.close()
        db.close()
        for id in registres:
            llista.append(self.get(id[0]))
        return llista

    def delete(self, id):
        db = self.__get_db_connection()
        query = "Delete from usuaris " + \
                "Where id="+str(id)+";"

        cursor = db.cursor()
        resultat = None
        cursor.execute(query)
        db.commit()
        resultat = True
        cursor.close()
        db.close()
        return resultat


    def __get_db_connection(self):
        return sqlite3.connect(
          database = self.ruta)
          
    def __get_id_by_nom(self, nom):
        db = self.__get_db_connection()
        
        query = "Select id from usuaris where usuari=\'"+nom+"\';"
        cursor = db.cursor()
        cursor.execute(query)

        registres = cursor.fetchall()
        if len(registres) > 0:
            return registres[0][0]
        return None 

    def set_sessio(self, id_sessio, usuari):
        db = self.__get_db_connection()

        query = "Insert into sessions_usuaris (uuid, usuari) values(\'"+id_sessio+"\',"+str(usuari.get_id())+")"
        cursor = db.cursor()
        resultat = cursor.execute(query)
        db.commit()
        cursor.close()
        db.close()
        return id_sessio