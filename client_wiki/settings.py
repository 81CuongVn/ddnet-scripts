#!/usr/bin/env python3

import sys
import re
import html

print('{| class="wikitable"')
print("! Setting")
print("! Description")
print("! Default")
print("! Min")
print("! Max")

names = {}
results = []

def getValue(x):
    return html.escape(x.lstrip()).replace("SERVERINFO_LEVEL_MIN", "0").replace("SERVERINFO_LEVEL_MAX", "2").replace("MAX_CLIENTS", "64")

for line in sys.stdin:
  if sys.argv[1] not in line:
    continue

  x = re.findall(r'(?:[^\s,"]|"(?:\\.|[^"])*")+', line)
  y = line.split('"')
  name = x[1].lstrip()

  if "MACRO_CONFIG_STR" in line:
    result = (html.escape(name), html.escape(y[-2]), getValue(x[3].lstrip()), "", "")
  elif "MACRO_CONFIG_INT" in line:
    result = (html.escape(name), html.escape(y[-2]), getValue(x[2].lstrip()), getValue(x[3]), getValue(x[4]))
  elif "MACRO_CONFIG_COL" in line:
    result = (html.escape(name), html.escape(y[-2]), getValue(x[2].lstrip()), "", "")

  line = "|-\n"
  line += "| %s\n| %s\n| %s\n| %s\n| %s" % result

  if name in names:
    # Always use the last one we find, first ones are platform specific ifdefs
    results[names[name]] = line
  else:
    names[name] = len(results)
    results.append(line)

for line in results:
  print(line)

print('|}')
