from apl_util import APLUtil, APL
from pprint import pprint

def main():
  aplLines = APLUtil.getAPL("T27_Paladin_Retribution.simc")
  # pprint(aplLines)
  apl = APL(aplLines)
  print(f"Name:  {apl.name}")
  print(f"Class: {apl.klass}")
  print(f"Spec:  {apl.spec}")

if __name__ == '__main__':
  main()
