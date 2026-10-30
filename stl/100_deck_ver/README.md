# 100-card version

The round-5 remix made 37 mm deeper, for a 100-card deck in double sleeves. Inside it is 70 × 72 × 96 mm (W × D × H) instead of 70 × 35 × 96, outside 78 × 80 × 100 mm. Everything else is round 5: the same front with the thumb notch, D-pad and buttons, the same five-knuckle hinge with the recessed pin head and knock-out hole, the same snap catches 17 mm behind the front face, the same lead-in chamfers, and "Yoojin" engraved 0.8 mm into the bottom, moved to the middle of the longer floor. How it was made is in [improvements.md](../../improvements.md#100-card-version); printing and assembly are as for round 5 in the [main README](../../README.md#remix).

| File | Print orientation | What it is |
|---|---|---|
| Case-bottom_remix.stl | Upright, open top facing up | Body: 70 × 72 × 96 mm inside; thumb notch, catch beads, "Yoojin" engraved 0.8 mm deep, a recess for the pin head in the left knuckle and a 1.6 mm knock-out hole in the right one |
| Case-top_remix.stl | Front face (screen bezel) on the bed | Lid: 80 mm deep, so 87 mm tall as printed; 4 mm screen frame, catch grooves, chamfered rim |
| Hinge-pin_remix.stl | Lying on its flat side | Same file as round 5; print two |
| D-Pad_remix.stl | Face down, peg up | Same file as round 4 |
| Button_remix.stl | Face down, peg up | Same file as round 4; print two (A and B) |
| StartSelect_remix.stl | Standing on its back face | Same file as round 4; print two |
| Test-seats.stl, Test-hinge-body.stl, Test-hinge-lid.stl | As in round 5 | The round-5 coupons, unchanged: the front wall and the hinge are the same, so they test this box too |

All nine are exported in print orientation, sitting at Z = 0. Renders are in [example_images/](example_images/).

## What fits

| | |
|---|---|
| Inside | 70 mm wide, 72 mm deep, 96 mm tall |
| Double-sleeved cards: a perfect-fit inner sleeve and a standard 66–67 × 91–92 mm outer sleeve | 100, with room to spare. A card is about 0.30 mm thick, the inner sleeve adds about 0.10 mm and the outer about 0.22 mm, so 100 cards stack to 62–66 mm and sit at 68–70 mm in a box |
| Single-sleeved cards | About 120 |
| Oversized outer sleeves, 69 × 94 mm | No. The width and height are the same as in every version of this box |

With fewer cards the deck leans back. A folded piece of card or a block of foam behind it keeps the front card against the screen.

## Printing

Same settings as round 5: 0.2 mm layers, 2–3 walls, 10–15 % infill, supports off for everything; pin and buttons at 0.12–0.16 mm layers with 100 % infill, a brim under the pin and under Start and Select. The body needs an 80 × 80 mm footprint and uses about 40 % more material than the round-5 body (96 cm³ against 68). The lid prints standing on its bezel, 87 mm tall, with the same 70 mm bridge inside its back wall. If you have not printed this box before, print the three coupons, the pin and one of each button first: the fits they test are the ones in this box.

## Assembly

As round 5. Buttons first. Close the lid and, looking at the back, push the pin tip-first into the left end knuckle, the one with the round recess, until its head is flush; a straightened paperclip through the 1.6 mm hole in the right-hand knuckle pushes it out again. The light friction fit along the side seams acts over twice the length it does on the 60-card box, so the lid may feel a little firmer to open: if it is hard to open, sand the outer face of the body's two side tongues lightly.

## What changed from round 5

- **Depth:** 37 mm more inside (35 → 72 mm), all of it between the catches and the back wall. The front wall with its seats and notch, the catches at 17 mm behind the front face, the back wall, the hinge and the pin are the round-5 geometry. The hinge axis is 59.2 mm behind the front face instead of 22.2.
- **Side seam:** the sloping seam where the lid's wall meets the body's runs from the same point at the front corner (66 mm up) to the same point at the back wall (85 mm up), so it is a gentler straight line, 14° instead of 25°. The lid's side walls are still 32 mm deep at the front and 15 mm at the back, and the lid still sits 0.22 mm above the body's seam all the way along.
- **Engraving:** the same trace of "Yoojin", 0.8 mm deep, moved 18.5 mm back to the middle of the 74 × 76 mm bottom.
- **Everything else:** the pin, the three button files and the three coupons are byte-for-byte copies of round 5's.

The files were produced from the round-5 files by [tools/deck100_build.py](../../tools/deck100_build.py) and checked on the meshes: watertight; the front wall, back wall and hinge identical to round 5; the seam and tongue planes straight to 0.001 mm with the lid 0.22 mm above the seam everywhere; a 67 × 69 × 92 mm block, a 100-card double-sleeved deck with 1.5 mm to spare each way, clears the body and the closed lid; the lid swings clear from 15° to 210°; the pin seats with zero overlap. They have not been test-printed.
