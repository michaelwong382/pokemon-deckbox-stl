# Remix, round 3

The third round of the remix of Ashwood's box. Round 4 in [../v4/](../v4/) is the current version: this box with a D-pad and buttons redrawn to push in by hand; the body, lid and pin are the same files. Round 3 is round 2 with "Yoojin" engraved in the bottom in place of the designer's signature: fits sleeved cards, five-knuckle hinge with a printed pin, prints without supports, 4 mm screen frame, snap catches, thumb notch and lead-in chamfers. Details are in [improvements.md](../../../improvements.md#round-3); printing and assembly are in the [main README](../../../README.md#remix).

| File | Print orientation | What it is |
|---|---|---|
| Case-bottom_remix.stl | Upright, open top facing up | Body: 70 × 35 × 96 mm inside, thumb notch, catch beads, "Yoojin" engraved in the bottom |
| Case-top_remix.stl | Front face (screen bezel) on the bed | Lid: 4 mm screen frame, catch grooves, chamfered rim; same file as round 2 |
| Hinge-pin_remix.stl | Lying on one of its flat sides | Octagonal hinge pin with a head; print two; same file as round 2 |

All three are exported in print orientation, sitting at Z = 0. The D-pad and buttons are unchanged: print them from [../../original/](../../original/). Renders of these files, including the engraved bottom, are in [example_images/](example_images/).

## Print settings

Supports **off** for all three parts.

| | Body and lid | Pin |
|---|---|---|
| Layer height | 0.2 mm | 0.12–0.16 mm |
| Walls | 2–3 | 2 |
| Infill | 10–15 % | 100 % |
| Brim | Not needed | Recommended |

- The engraving is in the face that sits on the bed, and its thinnest strokes are 0.6 mm. Level the bed and leave elephant-foot compensation on, or a squashed first layer closes them up.
- The lid's back wall prints as one 70 mm bridge inside the lid; turn on thick bridges if your printer bridges poorly.
- Trim the pin's brim cleanly so nothing catches in the hinge.
- The bezel is paint, not geometry: paint it in the slicer if you want it black.

## Assembly and use

- **Hinge:** close the lid, push the pin into the left end (seen from the back) until its head stops. Too tight: scale the pin's width and height to 97 %. Too loose: 102 %, or a drop of glue under the head.
- **Open:** thumb in the notch under the screen, push the lid's bottom edge up and forward. Don't reach through the window.
- **Close:** swing the lid down until it clicks. If the click is too stiff, sand the two beads on the body's side walls; if there is no click, build them up with paint or glue.

## What changed from round 2

The second-round files, with Ashwood's signature, are in [../v2/](../v2/). Only the body's bottom 1 mm differs: Ashwood's 1 mm recess is filled, and "Yoojin" is engraved 1 mm deep in its place, 60 × 24 mm and centred, reading the right way round with the box tipped back (front edge at the top). It is traced from [images/Elegant_Yoojin_Calligraphy.png](../../../images/Elegant_Yoojin_Calligraphy.png), with strokes thinner than 0.6 mm widened to 0.6 mm so they print, and the joins between strokes rounded off. The lid and pin are byte-for-byte copies of round 2's. The body was produced from v2 by [tools/round3_build.py](../../../tools/round3_build.py) and checked on the mesh (watertight, nothing changed above 1 mm, stroke widths, loop sizes); it has not been test-printed yet.
