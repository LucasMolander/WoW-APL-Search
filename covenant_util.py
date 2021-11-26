from enum import Enum
from enum_util import EnumUtil
from typing import Optional, List


class APLCovenant(Enum):
  KYRIAN = "kyrian"
  NECROLORD = "necrolord"
  NIGHT_FAE = "night_fae"
  VENTHYR = "venthyr"


class APLSoulbind(Enum):
  # Kyrian
  PELAGOS = "pelagos"
  KLEIA = "kleia"
  MIKANIKOS = "mikanikos"
  # Necrolord
  PLAGUE_DEVISER_MARILETH = "plague_deviser_marileth"
  EMENI = "emeni"
  BONESMITH_HEIRMIR = "bonesmith_heirmir"
  # Night Fae
  NIYA = "niya"
  DREAMWEAVER = "dreamweaver"
  KORAYN = "korayn"
  # Venthyr
  NADJIA = "nadjia"
  THEOTAR = "theotar"
  GENERAL_DRAVEN = "general_draven"


class APLSoulbindTrait(Enum):
  """
  See `void register_special_effects()` in
  simc/engine/player/soulbinds.cpp

  Just Kyrian for now.
  """
  #
  # Kyrian
  #
  # Pelagos
  LET_GO_OF_THE_PAST = "let_go_of_the_past"
  COMBAT_MEDITATION = "combat_meditation"
  BETTER_TOGETHER = "better_together"
  NEWFOUND_RESOLVE = "newfound_resolve"
  # Kleia
  VALIANT_STRIKES = "valiant_strikes"
  POINTED_COURAGE = "pointed_courage"
  SPEAR_OF_THE_ARCHON = "spear_of_the_archon"
  LIGHT_THE_PATH = "light_the_path"
  # Mikanikos
  HAMMER_OF_GENESIS = "hammer_of_genesis"
  BRONS_CALL_TO_ACTION = "brons_call_to_action"
  EFFUSIVE_ANIMA_ACCELERATOR = "effusive_anima_accelerator"
  SOULGLOW_SPECTROMETER = "soulglow_spectrometer"


class APLSoulbindConduit(Enum):
  """
  See `struct conduits_t {...} conduits;` in
  simc/engine/class_modules/paladin/sc_paladin.hpp

  Just paladin for now.
  """
  #
  # Paladin
  #
  RINGING_CLARITY = "ringing_clarity"
  VENGEFUL_SHOCK = "vengeful_shock"
  FOCUSED_LIGHT = "focused_light"
  EXPURGATION = "expurgation"
  TEMPLARS_VINDICATION = "templars_vindication"
  THE_LONG_SUMMER = "the_long_summer"
  TRUTHS_WAKE = "truths_wake"
  VIRTUOUS_COMMAND = "virtuous_command"
  RIGHTEOUS_MIGHT = "righteous_might"
  HALLOWED_DISCERNMENT = "hallowed_discernment"
  PUNISH_THE_GUILTY = "punish_the_guilty"
  RESOLUTE_DEFENDER = "resolute_defender"
  SHIELDING_WORDS = "shielding_words"
  GOLDEN_PATH = "golden_path"
  ROYAL_DECREE = "royal_decree"


class Conduit:
  def __init__(self, conduit: APLSoulbindConduit, rank: int, empowered: bool = False) -> None:
    self.conduit = conduit
    self.rank = rank
    self.empowered = empowered

  def __str__(self):
    return f"{self.conduit.value}:{self.rank}{':1' if self.empowered else ''}"


class SoulbindSetup:
  def __init__(self, soulbind: APLSoulbind, traits: List[APLSoulbindTrait], conduits: List[Conduit]) -> None:
    self.soulbind = soulbind
    self.traits = traits
    self.conduits = conduits

  def __str__(self):
    soulbindStr = self.soulbind.value
    traitsStr = "/".join([t.value for t in self.traits])
    conduitsStr = "/".join([c.__str__() for c in self.conduits])
    return f"{soulbindStr},{traitsStr}/{conduitsStr}"


class CovenantUtil:
  @staticmethod
  def parseSoulbindSetup(rhs: str) -> SoulbindSetup:
    """
    `rhs`
    e.g.
    ```
    "pelagos,combat_meditation/better_together/newfound_resolve/ringing_clarity:9:1/virtuous_command:9:1/expurgation:9:1"
    ```
    """
    sbStrToVal = EnumUtil.strToVal(APLSoulbind)
    soulbindStr = rhs.split(",")[0]
    soulbind = sbStrToVal[soulbindStr]

    traitStrToVal = EnumUtil.strToVal(APLSoulbindTrait)
    conduitStrToVal = EnumUtil.strToVal(APLSoulbindConduit)
    traitsAndConduits = rhs.split(",")[1].split("/")
    traits = [
      traitStrToVal[t]
      for t in traitsAndConduits if ":" not in t
    ]
    conduitsReprs = [t for t in traitsAndConduits if ":" in t]
    conduits: List[Conduit] = []
    for conduitRepr in conduitsReprs:
      parts = conduitRepr.split(":")
      conduit = conduitStrToVal[parts[0]]
      rank = int(parts[1])
      if len(parts) < 3:
        empowered = False
      else:
        empowered = parts[2] == "1"
      conduits.append(Conduit(conduit, rank, empowered))

    return SoulbindSetup(soulbind, traits, conduits)
