import argparse
import json

keymap = {
  "KC_NO": [],
  "KC_TRNS": [],
  "KC_MINS": ["-","_"],
  "KC_ESC": ["ESC"],
  "KC_TAB": ["TAB"],
  "KC_QUOT": ["'","\\\""],
  "KC_RSFT": [],
  "KC_LSFT": [{"text":"⇧","size":10}],
  "KC_LALT": ["ALT"],
  "KC_RALT": ["GR", "ALT"],
  "KC_LCTL": ["CTL"],
  "KC_RCTL": [],
  "KC_DEL": ["DEL"],
  "KC_SPC": [],
  "KC_BSPC": [{"text":"⇦","size":10,"offsetY":.2}],
  "KC_ENT": [{"text":"⏎","size":10}],
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
  "KC_GRV": ["`","~"],
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
      self.size = labelData["size"]
      self.y += labelData.get("offsetY",0)

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
  for i,l in enumerate(keyLayers[1:]):
    if l:
      otherLabels += l

  if len(otherLabels) == 0:
    return labelCol(l0labels, 0)

  return labelCol(l0labels, -.8) + labelCol(otherLabels, .8)


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("file")

  args = parser.parse_args()

  f = open(args.file, "r")
  data = json.load(f)
  f.close()
  
  layers = data["layers"]
  nKeys= len(layers[0])

  keys = [[mapKey(l[i]) for l in layers] for i in range(nKeys)]


  print("module labeledKey(index){")

  for i,key in enumerate(keys):
    print("if(index == {})".format(i))
    labelScad = keyLayersToLabels(key)
    for label in labelScad:
      print("  {}".format(label.toScad()))
    print("  children();")

  print("}")

main()
