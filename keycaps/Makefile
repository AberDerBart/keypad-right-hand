KEYBOARD=../qmk_firmware/keyboards/ergodox_gaming_right/info.json
KEYMAP=../qmk_firmware/keyboards/ergodox_gaming_right/keymaps/AberDerBart/ergodox_gaming_right.json

labeledKeys.scad: ${KEYBOARD} ${KEYMAP} qmkToOpenscad.py
	python qmkToOpenscad.py --keyboard ${KEYBOARD} --keymap ${KEYMAP} ${ARGS} > labeledKeys.scad

.PHONY: clean
clean:
	rm -f labeledKeys.scad
