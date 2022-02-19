import argparse
import json
import re

keymap = {
  "KC_NO": [],
  "KC_TRNS": [],
  "KC_MINS": ["-","_"],
  "KC_ESC": ["ESC"],
  "KC_TAB": [{"text":"TAB", "offsetX":-.2}],
  "KC_QUOT": ["'","\\\""],
  "KC_LSFT": [],
  "KC_RSFT": [{"text":"⇧","size":10}],
  "KC_LALT": [],
  "KC_RALT": ["ALT"],
  "KC_RCTL": ["CTL"],
  "KC_LCTL": [],
  "KC_DEL": ["DEL"],
  "KC_SPC": [],
  "KC_BSPC": [{"text":"⇦","size":10,"offsetY":.2}],
  "KC_ENT": [{"text":"⏎","size":10, "offsetX":-.2}],
  "KC_EQL": ["=","+"],
  "TO(2)": [],
  "KC_DOT": [".",">"],
  "KC_COMM": [",","<"],
  "KC_SLSH": ["/","?"],
  "KC_LEFT": [],
  "KC_RGHT": [],
  "KC_DOWN": [],
  "KC_UP": [],
  "KC_HOME": [],
  "KC_END": [],
  "KC_1": ["1","!"],
  "KC_2": ["2","@"],
  "KC_3": ["3","#"],
  "KC_4": ["4","$"],
  "KC_5": ["5","%"],
  "KC_6": ["6","^"],
  "KC_7": ["7","&"],
  "KC_8": ["8","*"],
  "KC_9": ["9","("],
  "KC_0": ["0",")"],
  "KC_PGUP": [],
  "KC_PGDN": [],
  "KC_SCLN": [";",":"],
  "KC_PSCR": [{"text":"✂","size":10,"offsetY":.25}],
  "KC_LGUI": [{"text":"⚙","size":10}],
  "LT(1,KC_NO)": [],
  "LT(2,KC_NO)": [],
  "TO(0)": [],
  "MO(2)": [],
  "MO(4)": [],
  "KC_GRV": ["`","~"],
  "KC_LBRC": ["["],
  "KC_RBRC": ["]"],
  "KC_BSLS": ["\\\\","|"],
  "TG(1)": ["ME","GA"],
}

def mapKey(code):
  if code in keymap:
    return keymap.get(code)
  return [code[3:]]

class KeyLabel:
  def __init__(self, labelData, x, y):
    self.size = 4
    self.x = x
    self.y = y
    if isinstance(labelData, str):
      self.text = labelData
    else:
      self.text = labelData["text"]
      self.size = labelData.get("size",4)
      self.y += labelData.get("offsetY",0)
      self.x += labelData.get("offsetX",0)

  def toScad(self):
    return 'legend("{}", position=[{},{}], size={})'.format(
      self.text,
      self.x,
      self.y,
      self.size
    )

def labelCol(labels, x):
  if len(labels) == 0:
    return []
  if len(labels) == 1:
    return [KeyLabel(labels[0], x, 0)]

  return [
    KeyLabel(labels[0], x, .8),
    KeyLabel(labels[1], x, -.8),
  ]

def keyLayersToLabels(keyLayers):
  l0labels = keyLayers[0]
  otherLabels = []
  for i,l in enumerate(keyLayers[2:3]):
    if l:
      otherLabels += l

  if len(otherLabels) == 0:
    return labelCol(l0labels, 0)

  return labelCol(l0labels, -.8) + labelCol(otherLabels, .8)


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--keyboard")
  parser.add_argument("--keymap")
  parser.add_argument("--filter")

  args = parser.parse_args()

  # dependencies

  print("include <KeyV2/includes.scad>")

  # generate key labels

  km_file = open(args.keymap, "r")
  km_data = json.load(km_file)
  km_file.close()
  
  layers = km_data["layers"]
  nKeys= len(layers[0])

  key_labels = [[mapKey(l[i]) for l in layers] for i in range(nKeys)]

  print("module labeledKey(index){")

  for i,key in enumerate(key_labels):
    if args.filter:
      if re.match(args.filter, layers[0][i]) is None:
        continue
    print("if(index == {})".format(i))
    labelScad = keyLayersToLabels(key)
    for label in labelScad:
      print("  {}".format(label.toScad()))
    print("  children();")

  print("}")

  # generate kay positions and sizes

  kb_file = open(args.keyboard, "r")
  kb_data = json.load(kb_file)
  kb_file.close()

  key_positions = kb_data["layouts"]["LAYOUT_default"]["layout"]

  print("module positionedKey(index){")

  for i,key in enumerate(key_positions):
    w = key.get("w",1)
    h = key.get("h",1)
    x = key.get("x",0)
    y = key.get("y",0)
    print("if(index == {})".format(i))
    print("  translate_u({}, {})".format(x+w/2, -(y+h/2)))
    print("  u({})".format(w))
    print("  uh({})".format(h))
    print("  children();")

  print("}")

if __name__ == "__main__":
  main()
