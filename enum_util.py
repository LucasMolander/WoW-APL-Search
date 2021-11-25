from typing import TypeVar, Type, Dict, Set, Optional, Generic
from enum import Enum

# ET = TypeVar('ET', Enum, Enum)
T = TypeVar('T')

# ET = Generic[Type[Enum]]

TE = Type[Enum]


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
      # eklass = e.__class__
      # if issubclass(e.__class__, Enum):
      if isinstance(e, Enum):
        strToVal[e.value] = e
        # print(f"\t{eklass._member_map_}")
        # print(f"\t{eklass._member_names_}")
        # print(f"\t{eklass.__dict__}")
        # print(e)
        # print(f"\t{e.__str__()}")
        # print(f"\t{e.__repr__()}")
        # print(f"\t{e.name}")
        # print(f"\t{e.value}")
    if s in strToVal:
      return strToVal[s]
    else:
      return None
