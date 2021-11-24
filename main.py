from apl_util import APLUtil
from pprint import pprint

def main():
  print("main()")
  apl = APLUtil.getAPL("T27_Paladin_Retribution.simc")
  pprint(apl)

if __name__ == '__main__':
  main()
