from file_util import FileUtil
from enum_util import EnumUtil
from spec_util import APLClass, CLASS_TO_SPECS
from race_util import APLRace
from covenant_util import CovenantUtil, APLCovenant

from os import sep
from typing import List, Dict, Set
from enum import Enum
import re


class APL:
  # klass: APLClass = None  # type: ignore
  # name: str = None  # type: ignore

  def __init__(self, aplLines: List[str]) -> None:
    self._classStrToEnum = EnumUtil.strToVal(APLClass)
    self._raceStrToEnum = EnumUtil.strToVal(APLRace)
    self._covenantStrToEnum = EnumUtil.strToVal(APLCovenant)

    #
    # Process each line individually!
    #
    for l in aplLines:
      if l.startswith("#"):
        continue
      # Get the left-hand side, right-hand side, and type of equality
      m = re.fullmatch(r"^([a-z0-9\._]+)(\+?=)(.*)$", l)
      if not m:
        print(f"\tNOT A MATCH: {l}")
        continue
      self.processLine(m.groups()[0], m.groups()[1], m.groups()[2])

    #
    # Post-processing - yay!
    #

    # Spec
    if self.spec_str:
      self.spec = EnumUtil.getEnumVal(self.spec_str, CLASS_TO_SPECS[self.klass])
      if self.spec is None:
        print(f"\tWARNING - Could not get spec from string '{self.spec_str}'!")
    else:
      print(f"\tWARNING - No spec string found in the APL!")

  def processLine(self, lhs: str, eq: str, rhs: str) -> None:
    if lhs in self._classStrToEnum:
      self.klass = self._classStrToEnum[lhs]
      self.name = rhs
    elif lhs == "spec":
      # Post-process it to make sure we have the class
      self.spec_str = rhs
    elif lhs == "level":
      self.level = int(rhs)
    elif lhs == "race":
      self.race = self._raceStrToEnum[rhs]
    elif lhs == "role":
      self.role = rhs
    elif lhs == "position":
      self.position = rhs
    elif lhs == "talents":
      self.talents = [int(t) for t in rhs]
    elif lhs == "covenant":
      self.covenant = self._covenantStrToEnum[rhs]
    elif lhs == "soulbind":
      self.soulbindSetup = CovenantUtil.parseSoulbindSetup(rhs)
    elif lhs == "renown":
      self.renown = int(rhs)
    elif lhs == "position":
      self.position = rhs





class APLUtil:
  """
  This class helps with reading in APLs.
  """
  FOLDER = "APLs"

  @staticmethod
  def getAPL(name: str) -> List[str]:
    fp = f"{APLUtil.FOLDER}{sep}{name}"
    return FileUtil.readLines(fp)
