# Remix, round 4 (current)

The current remix of Ashwood's box. It is round 3 (fits sleeved cards, five-knuckle hinge with a printed pin, prints without supports, 4 mm screen frame, snap catches, thumb notch, lead-in chamfers, "Yoojin" engraved in the bottom) plus a D-pad and buttons redrawn so they push into the front by hand. Details are in [improvements.md](../../../improvements.md#round-4); printing and assembly are in the [main README](../../../README.md#remix).

| File | Print orientation | What it is |
|---|---|---|
| Case-bottom_remix.stl | Upright, open top facing up | Body: 70 × 35 × 96 mm inside, thumb notch, catch beads, "Yoojin" engraved in the bottom; same file as round 3 |
| Case-top_remix.stl | Front face (screen bezel) on the bed | Lid: 4 mm screen frame, catch grooves, chamfered rim; same file as round 2 |
| Hinge-pin_remix.stl | Lying on one of its flat sides | Octagonal hinge pin with a head; print two; same file as round 1 |
| D-Pad_remix.stl | Face down, peg up | D-pad: the designer's top, 0.15 mm clearance in its seat, crush-rib peg |
| Button_remix.stl | Face down, peg up | A/B button, print two: the designer's top, 0.15 mm clearance in its seat, crush-rib peg |
| StartSelect_remix.stl | Standing on its back face | Start/Select button, print two: the designer's top, 0.15 mm clearance, a rib on each long side |

All six are exported in print orientation, sitting at Z = 0, the buttons centred on the origin. The buttons' seats in the body are the same in every version, so these buttons also fit the earlier bodies and the designer's. Renders of these files, with the buttons in place and as printed, are in [example_images/](example_images/).

## Print settings

Supports **off** for everything.

| | Body and lid | Pin | D-pad and buttons |
|---|---|---|---|
| Layer height | 0.2 mm | 0.12–0.16 mm | 0.12–0.16 mm |
| Walls | 2–3 | 2 | 2 |
| Infill | 10–15 % | 100 % | 100 % |
| Brim | Not needed | Recommended | Start and Select: yes |

- The engraving is in the face that sits on the bed, and its thinnest strokes are 0.6 mm. Level the bed and leave elephant-foot compensation on, or a squashed first layer closes them up.
- The lid's back wall prints as one 70 mm bridge inside the lid; turn on thick bridges if your printer bridges poorly.
- Trim the pin's brim cleanly so nothing catches in the hinge, and the Start/Select brims so nothing stops them going into their seats.
- The bezel is paint, not geometry: paint it in the slicer if you want it black.

## Assembly and use

- **Buttons:** before the lid. Line the D-pad's peg up with its hole and push with a thumb until the cross sits in its seat; the same for the two A/B buttons. Push Start and Select in with a fingertip or the flat of a knife until they stop, 2 mm in. Only the small ribs press. Too tight: run a 3 mm drill through the two peg holes or sand the ribs. Too loose: a drop of glue on the ribs. They can be pushed out again from inside the box through the peg holes.
- **Hinge:** close the lid, push the pin into the left end (seen from the back) until its head stops. Too tight: scale the pin's width and height to 97 %. Too loose: 102 %, or a drop of glue under the head.
- **Open:** thumb in the notch under the screen, push the lid's bottom edge up and forward. Don't reach through the window.
- **Close:** swing the lid down until it clicks. If the click is too stiff, sand the two beads on the body's side walls; if there is no click, build them up with paint or glue.

## What changed from round 3

The third-round files, which use the designer's press-fit buttons, are in [../v3/](../v3/). The designer drew each button the exact size of its seat, so printed ones have to be forced in. Here the parts of each button that sit inside the front wall are 0.15 mm smaller than the seat all round, the D-pad and A/B pegs have a loose 2.6 mm core with four ribs that press in the 3 mm hole, and the Start/Select pills have a rib on each long side. Everything in front of the face is the designer's shape, and the body is untouched. The buttons were produced from the designer's files by [tools/round4_build.py](../../../tools/round4_build.py) and checked on the meshes (watertight, unchanged tops, clearance, where they touch the body); they have not been test-printed yet.
