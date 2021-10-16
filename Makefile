
labeledKeys.scad: ergodox_gaming_right_hand.json qmkToOpenscad.py
	python qmkToOpenscad.py ergodox_gaming_right_hand.json > labeledKeys.scad

.PHONY: clean
clean:
	rm -f labeledKeys.scad
