from typing import TypeVar, Type, Dict, Set, Optional, Generic
from enum import Enum

T = TypeVar('T')


class EnumUtil:
  """
  Generally helps with Enums.
  """

  @staticmethod
  def strToVal(enumName: Type[T]) -> Dict[str, T]:
    if issubclass(enumName, Enum):
      return enumName._value2member_map_  # type: ignore
    else:
      return {}

  @staticmethod
  def getEnumVal(s: str, enums: Set[T]) -> Optional[T]:
    strToVal: Dict[str, T] = {}
    for e in enums:
      if isinstance(e, Enum):
        strToVal[e.value] = e
    if s in strToVal:
      return strToVal[s]
    else:
      return None
