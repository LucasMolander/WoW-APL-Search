from file_util import FileUtil
from enum_util import EnumUtil
from spec_util import APLClass, CLASS_TO_SPECS

from os import sep
from typing import List, Dict, Set
from enum import Enum
import re



class APL:
  # klass: APLClass = None  # type: ignore
  # name: str = None  # type: ignore

  def __init__(self, aplLines: List[str]) -> None:
    classStrToEnum = EnumUtil.strToVal(APLClass)

    #
    # Process each line individually!
    #
    for l in aplLines:
      # Ignore comments
      if l.startswith("#"):
        continue

      # Get the left-hand side, right-hand side, and type of equality
      m = re.fullmatch(r"^([a-z0-9\._]+)(\+?=)(.*)$", l)
      if not m:
        print(f"\tNOT A MATCH: {l}")
        continue
      lhs = m.groups()[0]
      eq  = m.groups()[1]
      rhs = m.groups()[2]

      # Class and Name
      if lhs in classStrToEnum:
        self.klass = classStrToEnum[lhs]
        self.name = rhs

      # Spec string (post-process it to make sure we have the class)
      if lhs == "spec":
        self.spec_str = rhs

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



class APLUtil:
  """
  This class helps with reading in APLs.
  """
  FOLDER = "APLs"

  @staticmethod
  def getAPL(name: str) -> List[str]:
    fp = f"{APLUtil.FOLDER}{sep}{name}"
    return FileUtil.readLines(fp)
