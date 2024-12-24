from typing import Optional
from time import sleep

from backend.bng_python.bng_api_connector import BungieConnector
from backend.python_mysql.mysql_executor import DatabaseExecutor
from backend.python_mysql.mysql_connector import SQLConnector
from backend.bng_python.bng_data import DataFactory
from backend.bng_python.bng_types import *
from backend.bng_python.bng_data import (
    PlayerData, 
    CharacterData, 
    WeaponData,
    EquippedWeaponData, 
    ArmorData,
    EquippedArmorData, 
    ActivityData, 
    ActivityInstanceData, 
    ActivityStatsData
)

BNG_CONN = BungieConnector("10E792629C2A47E19356B8A79EEFA640")

class DatabasePlayerManager:
    def __init__(self, db_control: DatabaseExecutor) -> None:
        self.__control: DatabaseExecutor = db_control
        self.__players: list[PlayerData] = []
    
    def read_data(self) -> None:
        db_data = self.__control.retrieve_all("`Player`")
        
        if db_data:
            for tuple in db_data:
                self.add_existing_player(tuple)

    def add_existing_player(self, data) -> None:
        player = PlayerData(BNG_CONN, tuple[1], PLATFORM[tuple[6]].value) # type: ignore
        player.define_data()
        if player not in self.__players:
            self.__players.append(player)

    def add_new_player(self, member_id: int, member_type: int) -> None:
        # existing_player = self.__control.select_rows("`Player`", ["*"], {"destiny_id": member_id})
        
        # if not existing_player:
            new_player = DataFactory.get_player(member_id, member_type)
            if new_player not in self.__players:
                self.__players.append(new_player)

            self.__control.insert_row("`Player`", new_player)
        # else:
        #     self.add_existing_player(existing_player)

    def get_character_and_player_ids(self, member_id: int):
        result = self.__control.select_rows("`Player`", ["character_ids", "player_id"], {"destiny_id": member_id})

        character_ids = str(result[0][0].replace("[", ""))  # type: ignore
        character_ids = character_ids.replace("]", "")
        character_ids = character_ids.replace("\'", "")
        character_ids = character_ids.split(", ")
        for i in range(len(character_ids)):
            character_ids[i] = int(character_ids[i])  # type: ignore

        return character_ids, result[0][1] # type: ignore

class DatabaseCharacterManager:
    def __init__(self, db_control: DatabaseExecutor) -> None:
        self.__control: DatabaseExecutor = db_control
        self.__characters: list[CharacterData] = []

    def add_new_character(self, member_id: int, member_type: int, character_id: int, player_id: int=-1) -> None:
        # exisitng_char = self.__control.select_rows("`Character`", ["character_id"], {"bng_character_id": character_id})

        # if not exisitng_char:
            if player_id == -1:
                player = self.__control.select_rows("`Player`", ["player_id"], {"destiny_id": member_id})
                if player:
                    player_id = player[0][0]  # type: ignore
            
            new_char = DataFactory.get_character(member_id, member_type, character_id, player_id)
            
            if new_char not in self.__characters:
                self.__characters.append(new_char)

            self.__control.insert_row("`Character`", new_char)

    def get_activity_history(self, character_id: int, mode: int, count: int):
        character = self.find_character(character_id)
        if character:
            instance_ids = character.get_activity_hist_instances(mode, count)
            return instance_ids

    def find_character(self, character_id: int) -> Optional[CharacterData]:
        for character in self.__characters:
            if character.character_id == character_id:
                return character

class DatabaseWeaponManager:
    def __init__(self, db_control: DatabaseExecutor) -> None:
        self.__control: DatabaseExecutor = db_control
        self.__weapons: list[WeaponData] = []

    def add_new_weapon(self, weapon_id: int) -> None:
        # exisiting_weapon = self.__control.select_rows("`Weapon`", ["weapon_id"], {"bng_weapon_id": weapon_id})
        
        # if not exisiting_weapon:
            new_weapon = DataFactory.get_weapon(weapon_id)  
            if new_weapon not in self.__weapons:
                self.__weapons.append(new_weapon)

            self.__control.insert_row("`Weapon`", new_weapon)

    def get_weapon(self, bng_weapon_id: int) -> Optional[WeaponData]:
        for weapon in self.__weapons:
            if weapon.data["bng_weapon_id"] == bng_weapon_id:
                return weapon

class DatabaseArmorManager:
    def __init__(self, db_control: DatabaseExecutor) -> None:
        self.__control: DatabaseExecutor = db_control
        self.__armor: list[ArmorData] = []

    def add_new_armor(self, armor_id: int) -> None:
        # existing_armor = self.__control.select_rows("`Armor`", ["armor_id"], {"bng_armor_id": armor_id})
        
        # if not existing_armor:
            new_armor = DataFactory.get_armor(armor_id)
            if new_armor not in self.__armor:
                self.__armor.append(new_armor)

            self.__control.insert_row("`Armor`", new_armor)

    def get_armor(self, bng_armor_id: int) -> Optional[ArmorData]:
        for armor in self.__armor:
            if armor.data["bng_armor_id"] == bng_armor_id:
                return armor
