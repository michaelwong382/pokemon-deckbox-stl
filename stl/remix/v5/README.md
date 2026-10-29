# Remix, round 5 (current)

The current remix of Ashwood's box. It is round 4 (fits sleeved cards, five-knuckle hinge with a printed pin, prints without supports, 4 mm screen frame, snap catches, thumb notch, lead-in chamfers, "Yoojin" engraved in the bottom, D-pad and buttons that push in by hand) with three changes for printing and handling: the engraving is 0.8 mm deep with its two smallest loops filled, so no island of first layer is under 2.4 mm across; the pin's head sits flush in a recess in the end knuckle, with a knock-out hole at the other end; and three small test coupons let you check the button and hinge fits in under an hour of printing before the five-hour body. Details are in [improvements.md](../../../improvements.md#round-5); printing and assembly are in the [main README](../../../README.md#remix).

| File | Print orientation | What it is |
|---|---|---|
| Case-bottom_remix.stl | Upright, open top facing up | Body: 70 × 35 × 96 mm inside, thumb notch, catch beads, "Yoojin" engraved 0.8 mm deep, a recess for the pin head in the left knuckle and a 1.6 mm knock-out hole in the right one |
| Case-top_remix.stl | Front face (screen bezel) on the bed | Lid: 4 mm screen frame, catch grooves, chamfered rim; same file as round 2 |
| Hinge-pin_remix.stl | Lying on its flat side | Octagonal hinge pin, 58.5 mm, with a 4 mm round head; print two |
| D-Pad_remix.stl | Face down, peg up | D-pad with 0.15 mm clearance and a crush-rib peg; same file as round 4 |
| Button_remix.stl | Face down, peg up | A/B button, print two; same file as round 4 |
| StartSelect_remix.stl | Standing on its back face | Start/Select button, print two; same file as round 4 |
| Test-seats.stl | Upright, as it sits in the body | Optional coupon: the front wall with all five button seats, on a foot. 57 × 8 × 35 mm |
| Test-hinge-body.stl | Upright, as it sits in the body | Optional coupon: the top of the back wall with the three body knuckles, the pin recess and the knock-out hole, on a foot. 66 × 20 × 16 mm |
| Test-hinge-lid.stl | Cut face on the bed | Optional coupon: the lid's back wall with its two knuckles. 78 × 18 × 10 mm |

All nine are exported in print orientation, sitting at Z = 0; the pin, buttons and coupons are centred on the origin. The coupons are cut from these very files, so what fits a coupon fits the box. Renders of everything are in [example_images/](example_images/).

## Print settings

Supports **off** for everything.

| | Body and lid | Pin | D-pad and buttons | Coupons |
|---|---|---|---|---|
| Layer height | 0.2 mm | 0.12–0.16 mm | 0.12–0.16 mm | As the part they come from |
| Walls | 2–3 | 2 | 2 | 2–3 |
| Infill | 10–15 % | 100 % | 100 % | 10–15 % |
| Brim | Not needed | Recommended | Start and Select: yes | Not needed |

- The engraving is in the face that sits on the bed, 0.8 mm deep, and its thinnest strokes are 0.6 mm. Level the bed and leave elephant-foot compensation on, or a squashed first layer closes them up.
- The lid's back wall prints as one 70 mm bridge inside the lid; turn on thick bridges if your printer bridges poorly.
- Trim the pin's brim cleanly so nothing catches in the hinge, and the Start/Select brims so nothing stops them going into their seats.
- The bezel is paint, not geometry: paint it in the slicer if you want it black.

## Test the fits first

Print the three coupons with the pin and one of each button: about 20 cm³ in all, against 90 cm³ for the body and lid.

- **Buttons:** push the D-pad, an A/B button and a Start/Select button into Test-seats. They should go in with a thumb and stay put. If a peg won't go in, the holes printed small: run a 3 mm drill through the two peg holes of the body when you print it, or sand the ribs. If a button is loose, plan on a drop of glue.
- **Hinge:** set Test-hinge-lid on Test-hinge-body so the knuckles interleave and push the pin in at the end with the round recess until the head is flush. The lid strip should swing freely through about 160° before it meets the foot. If the pin is too tight, scale its width and height to 97 % for the real print, or plan on a 2.8 mm drill through the body knuckles; if it turns too easily in the body strip, scale to 102 %. Push it out again with a straightened paperclip through the small hole at the other end.

The coupons test the seats and the hinge, not the snap catches or the lid's friction fit, which need the full parts.

## Assembly and use

- **Buttons:** before the lid. Line the D-pad's peg up with its hole and push with a thumb until the cross sits in its seat; the same for the two A/B buttons. Push Start and Select in with a fingertip or the flat of a knife until they stop, 2 mm in. Only the small ribs press. They can be pushed out again from inside the box through the peg holes.
- **Hinge:** close the lid and, looking at the back of the box, push the pin tip-first into the left end, the knuckle with the round recess, until its head is flush. To take the lid off, push the pin out from the other end with a straightened paperclip through the 1.6 mm hole in the right-hand knuckle. Too tight: scale the pin's width and height to 97 %. Too loose: 102 %, or a drop of glue on the head.
- **Open:** thumb in the notch under the screen, push the lid's bottom edge up and forward. Don't reach through the window.
- **Close:** swing the lid down until it clicks. If the click is too stiff, sand the two beads on the body's side walls; if there is no click, build them up with paint or glue.

## What changed from round 4

The fourth-round files are in [../v4/](../v4/). The lid, D-pad and buttons are byte-for-byte copies of round 4's; the body changes only in its bottom 0.8 mm and inside the hinge's two end knuckles, and the pin is new.

- **Engraving:** the same trace of "Yoojin", 0.8 mm deep instead of 1.0 (the floor under the cards grows from 1.0 to 1.2 mm), with the two small loops at the tops of the o's filled in. In round 4 those loops were 1.3 mm islands of first-layer material, 1 mm tall, that a nozzle can knock off; the smallest island is now 2.45 mm across.
- **Pin head:** round 1's 5 × 3.75 mm block head stood 1.5 mm proud of the hinge. The knuckle is only 3 mm in radius, so the new pin has a 4 mm round head with a flat bottom (it still prints lying on its side), 1.7 mm long, sitting in a 4.3 mm recess 1.7 mm deep in the left knuckle, flush with its end, with 0.85 mm of wall left around it. The right-hand hole is blind, so the pin is 1.5 mm shorter (58.5 mm) and that end gets a 1.6 mm knock-out hole.
- **Coupons:** three pieces cut from the finished body and lid with a 2 mm foot where they need one.

The files were produced from round 4 by [tools/round5_build.py](../../../tools/round5_build.py) and checked on the meshes (watertight, body differs from round 4 only where intended, buttons fit the coupon exactly as the body, hinge strips and pin assemble with no overlap, lid sweep unchanged); they have not been test-printed yet.
