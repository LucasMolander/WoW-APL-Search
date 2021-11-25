from enum import Enum
from typing import Dict, Set

class APLClass(Enum):
  WARRIOR = "warrior"
  PALADIN = "paladin"
  HUNTER = "hunter"
  ROGUE = "rogue"
  PRIEST = "priest"
  SHAMAN = "shaman"
  MAGE = "mage"
  WARLOCK = "warlock"
  MONK = "monk"
  DRUID = "druid"
  DEMON_HUNTER = "demon_hunter"
  DEATH_KNIGHT = "death_knight"

class APLSpec(Enum):
  WARRIOR_ARMS = "arms"
  WARRIOR_FURY = "fury"
  WARRIOR_PROTECTION = "protection"
  PALADIN_HOLY = "holy"
  PALADIN_PROTECTION = "protection"
  PALADIN_RETRIBUTION = "retribution"
  HUNTER_BEAST_MASTERY = "beast_mastery"
  HUNTER_MARKSMANSHIP = "marksmanship"
  HUNTER_SURVIVAL = "survival"
  ROGUE_ASSASSINATION = "assassination"
  ROGUE_OUTLAW = "outlaw"
  ROGUE_SUBTLETY = "subtlety"
  PRIEST_DISCIPLINE = "discipline"
  PRIEST_HOLY = "holy"
  PRIEST_SHADOW = "shadow"
  SHAMAN_ELEMENTAL = "elemental"
  SHAMAN_ENHANCEMENT = "enhancement"
  SHAMAN_RESTORATION = "restoration"
  MAGE_ARCANE = "arcane"
  MAGE_FIRE = "fire"
  MAGE_FROST = "frost"
  WARLOCK_AFFLICTION = "affliction"
  WARLOCK_DEMONOLOGY = "demonology"
  WARLOCK_DESTRUCTION = "destruction"
  MONK_BREWMASTER = "brewmaster"
  MONK_MISTWEAVER = "mistweaver"
  MONK_WINDWALKER = "windwalker"
  DRUID_BALANCE = "balance"
  DRUID_FERAL = "feral"
  DRUID_GUARDIAN = "guardian"
  DRUID_RESTORATION = "restoration"
  DEMON_HUNTER_HAVOC = "havoc"
  DEMON_HUNTER_VENGEANCE = "vengeance"
  DEATH_KNIGHT_BLOOD = "blood"
  DEATH_KNIGHT_FROST = "frost"
  DEATH_KNIGHT_UNHOLY = "unholy"


CLASS_TO_SPECS: Dict[APLClass, Set[APLSpec]] = {
  APLClass.WARRIOR: {
    APLSpec.WARRIOR_ARMS,
    APLSpec.WARRIOR_FURY,
    APLSpec.WARRIOR_PROTECTION,
  },
  APLClass.PALADIN: {
    APLSpec.PALADIN_HOLY,
    APLSpec.PALADIN_PROTECTION,
    APLSpec.PALADIN_RETRIBUTION,
  },
  APLClass.HUNTER: {
    APLSpec.HUNTER_BEAST_MASTERY,
    APLSpec.HUNTER_MARKSMANSHIP,
    APLSpec.HUNTER_SURVIVAL,
  },
  APLClass.ROGUE: {
    APLSpec.ROGUE_ASSASSINATION,
    APLSpec.ROGUE_OUTLAW,
    APLSpec.ROGUE_SUBTLETY,
  },
  APLClass.PRIEST: {
    APLSpec.PRIEST_DISCIPLINE,
    APLSpec.PRIEST_HOLY,
    APLSpec.PRIEST_SHADOW,
  },
  APLClass.SHAMAN: {
    APLSpec.SHAMAN_ELEMENTAL,
    APLSpec.SHAMAN_ENHANCEMENT,
    APLSpec.SHAMAN_RESTORATION,
  },
  APLClass.MAGE: {
    APLSpec.MAGE_ARCANE,
    APLSpec.MAGE_FIRE,
    APLSpec.MAGE_FROST,
  },
  APLClass.WARLOCK: {
    APLSpec.WARLOCK_AFFLICTION,
    APLSpec.WARLOCK_DEMONOLOGY,
    APLSpec.WARLOCK_DESTRUCTION,
  },
  APLClass.MONK: {
    APLSpec.MONK_BREWMASTER,
    APLSpec.MONK_MISTWEAVER,
    APLSpec.MONK_WINDWALKER,
  },
  APLClass.DRUID: {
    APLSpec.DRUID_BALANCE,
    APLSpec.DRUID_FERAL,
    APLSpec.DRUID_GUARDIAN,
    APLSpec.DRUID_RESTORATION,
  },
  APLClass.DEMON_HUNTER: {
    APLSpec.DEMON_HUNTER_HAVOC,
    APLSpec.DEMON_HUNTER_VENGEANCE,
  },
  APLClass.DEATH_KNIGHT: {
    APLSpec.DEATH_KNIGHT_BLOOD,
    APLSpec.DEATH_KNIGHT_FROST,
    APLSpec.DEATH_KNIGHT_UNHOLY,
  },
}
