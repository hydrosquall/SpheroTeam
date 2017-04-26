# initialize.py
# Cameron Yick
# 4/22/2017

# These will probably be called any time you want to control multiple spheros
# Methods that utilize a SpheroManager
# REFACTOR: Make these a class method under the SpheroTeam object
# Need to consider whether to create new class type, or modify the old.

from teamutil import readJsonFile
from core import connect_team
import logging


def load_sphero_roster(manager, configFile):
    '''Initialize Sphero Objects from a configuration file specifying their
        names and MAC addresses.

        :param manager: Team Manager
        :param configFile: Path to configuration file, such as config.json

        :type SpheroManager: SpheroManager created via sphero.SpheroManager()
        :type configFile: String

        Returns modified manager object.
    '''
    config = readJsonFile(configFile)
    roster = readJsonFile(config['teamFile'])
    manager._name_cache = roster

    for bt_addr, bt_name in roster.iteritems():
        manager.add_sphero(bt_addr, bt_name)

    return manager


def connect_sphero_team(manager, botAbbreviations=None):
    '''
        Return list of connected sphero objects.
        By default, attempts to connect to every single robot in config file

        (.e.g RWR, ORG, RYR, etc)

        :param manager: Team Manager
        :param botAbbreviations: List of 3-letter capital Sphero Namestrings

        :type SpheroManager: SpheroManager created via sphero.SpheroManager()
        :type configFile: String
    '''

    # Assumes that every robot requested was already added in the config file.
    bots = []

    if botAbbreviations:
        for abbr in botAbbreviations:
            bot = manager._spheros.get("Sphero-{}".format(abbr))
            if bot:
                bots.append(bot)
            else:  # Consider whether to raise a python Exception too
                logging.warning("Sphero-%s not found", abbr)

    else:
        for bt_name, bot in manager._spheros.iteritems():
            bots.append(bot)

    connect_team(bots)
    return bots
