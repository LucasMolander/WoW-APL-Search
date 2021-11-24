from file_util import FileUtil

from os import sep
from typing import List

class APLUtil:
  """
  This class helps with reading in APLs.
  """
  FOLDER = "APLs"

  @staticmethod
  def getAPL(name: str) -> List[str]:
    fp = f"{APLUtil.FOLDER}{sep}{name}"
    return FileUtil.readLines(fp)
