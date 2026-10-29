# Remix, round 2

The second round of the remix of Ashwood's box: fits sleeved cards, five-knuckle hinge with a printed pin, prints without supports, and (new in this round) a 4 mm screen frame, snap catches, a thumb notch and lead-in chamfers. Details are in [improvements.md](../../../improvements.md); printing and assembly are in the [main README](../../../README.md#remix).

Round 3 ([../v3/](../v3/)) is this box with "Yoojin" engraved in the bottom instead of Ashwood's signature, and round 4 ([../v4/](../v4/), the current version) adds a D-pad and buttons that push in by hand; the lid and pin are the same files throughout. Print these if you want the original signature.

| File | Print orientation | What it is |
|---|---|---|
| Case-bottom_remix.stl | Upright, open top facing up | Body: 70 × 35 × 96 mm inside, thumb notch, catch beads |
| Case-top_remix.stl | Front face (screen bezel) on the bed | Lid: 4 mm screen frame, catch grooves, chamfered rim |
| Hinge-pin_remix.stl | Lying on one of its flat sides | Octagonal hinge pin with a head; print two |

All three are exported in print orientation, sitting at Z = 0. The D-pad and buttons are unchanged: print them from [../../original/](../../original/).

## Print settings

Supports **off** for all three parts.

| | Body and lid | Pin |
|---|---|---|
| Layer height | 0.2 mm | 0.12–0.16 mm |
| Walls | 2–3 | 2 |
| Infill | 10–15 % | 100 % |
| Brim | Not needed | Recommended |

- The lid's back wall prints as one 70 mm bridge inside the lid; turn on thick bridges if your printer bridges poorly.
- Trim the pin's brim cleanly so nothing catches in the hinge.
- The bezel is paint, not geometry: paint it in the slicer if you want it black.

## Assembly and use

- **Hinge:** close the lid, push the pin into the left end (seen from the back) until its head stops. Too tight: scale the pin's width and height to 97 %. Too loose: 102 %, or a drop of glue under the head.
- **Open:** thumb in the notch under the screen, push the lid's bottom edge up and forward. Don't reach through the window.
- **Close:** swing the lid down until it clicks. If the click is too stiff, sand the two beads on the body's side walls; if there is no click, build them up with paint or glue.

## What changed from round 1

The first-round files are in [../v1/](../v1/). Compared with them, the lid's screen frame went from a 1.8 mm plate to a 4 mm frame, the body's front tongue was cut back to make room for it, two snap catches were added in the side seams, a thumb notch was cut under the lid, and the lid's inner rim was chamfered. The pin is identical. These files were produced from v1 by [tools/round2_build.py](../../../tools/round2_build.py) and checked on the meshes (watertight, fit, hinge sweep, interior size, overhangs); they have not been test-printed yet.
