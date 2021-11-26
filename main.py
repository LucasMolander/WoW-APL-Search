from apl_util import APLUtil, APL
from pprint import pprint

def main():
  aplLines = APLUtil.getAPL("T27_Paladin_Retribution.simc")
  # pprint(aplLines)
  apl = APL(aplLines)
  print(f"Name:     {apl.name}")
  print(f"Class:    {apl.klass}")
  print(f"Spec:     {apl.spec}")
  print(f"Race:     {apl.race}")
  print(f"Role:     {apl.role}")
  print(f"Pos:      {apl.position}")
  print(f"Talents:  {apl.talents}")
  print(f"Covenant: {apl.covenant}")
  print(f"Soulbind: {apl.soulbindSetup}")

if __name__ == '__main__':
  main()
