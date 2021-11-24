from typing import List

class FileUtil:
  """
  Helps with reading and writing files.
  """
  @staticmethod
  def readLines(path: str) -> List[str]:
    """
    Strips whitespace and line endings. Also removes empty lines
    """
    with open(path) as f:
      strippedLines = [l.strip(" \r\n\t") for l in f.readlines()]
      return [sl for sl in strippedLines if len(sl) > 0]
