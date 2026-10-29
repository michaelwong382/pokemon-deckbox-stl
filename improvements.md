# Improvements to the Game Boy deck box

This documents every change in the remix of Ashwood's [Pokemon tcg deckbox: Gameboy](https://makerworld.com/en/models/828343). It covers what was wrong with the original, what changed, and how the result was checked. The remix files are in [stl/remix/](stl/remix/v2/), and the [README](README.md#remix) covers printing and assembly. Sections 1 to 5 are the first round (fit, hinge, printing). Sections 6 to 9 are a [second round](#round-2) made on top of it, from feedback on the first; the first-round files are kept in [stl/remix/v1/](stl/remix/v1/).

## Summary

| # | Problem in the original | Fix |
|---|---|---|
| 1 | Inside is 92.0 mm tall, the same as a sleeved card | 4 mm more height in the lid: 96.0 mm inside |
| 2 | 1 mm per side for 66–67 mm sleeves | 1 mm more per side: 70.0 mm inside |
| 3 | Fragile snap hinges | Five-knuckle hinge with a printed pin |
| 4 | Needs supports | Prints with supports off |
| 5 | STLs lie on their side in a slicer | STLs exported in print orientation |
| 6 | The lid's screen frame is a 1.8 mm plate hanging 23 mm below the lid walls; it flexes | 4 mm thick frame, about 11× stiffer, flush with the inside of the front wall |
| 7 | Nothing holds the lid shut | Two snap catches in the side seams |
| 8 | The only grip for opening is the window, with the front card behind it | Thumb notch under the lid's bottom edge |
| 9 | Square inner edges on the lid catch cards that sit at an angle | Lead-in chamfers all round the lid's inner rim |

## 1. Interior height: 92 → 96 mm

**Problem.** The inside measures exactly 92.0 mm from floor to lid ceiling, at every point across the box. Standard sleeves are 91–92 mm tall (2⅝ × 3⅝ in is 92.1 mm), so there's no allowance for differences between sleeve brands or for print tolerance. In a test print, sleeved cards didn't fit. The width got 2 mm of clearance, but the height got none.

**Fix.** 4 mm of height was added to the lid only, just under its ceiling and above the screen. Only straight vertical walls pass through that band, so the extra height is a plain extension and nothing else changes shape. The body is untouched.

**Result.** 96.0 mm inside, measured at 9 points across the footprint. That leaves about 4 mm of headroom over a 92 mm sleeve. Cards still sit on the same floor, so the screen frames the same part of the card as before. Outside height goes from 96 to 100 mm.

![Side cross-sections of the original and the remix. The original's 92 mm interior has no headroom above a 92 mm card stack; the remix's 96 mm interior leaves 4 mm](images/remix/height_before_after.png)

## 2. Interior width: 68 → 70 mm

**Problem.** The 68 mm interior leaves 1 mm per side for standard sleeves (66 mm) and less for thicker outer sleeves used for double sleeving.

**Fix.** 1 mm was added just inside each side wall, in both the body and the lid, in a band that only straight walls cross. The side walls move out by 1 mm each. The screen, D-pad, buttons, hinge and side seams stay where they were.

**Result.** 70.0 mm inside and 78 mm outside (was 76 mm).

## 3. Hinge

**Problem.** The original has two small snap hinges. Each lid tab is a ring with a 0.75 mm wall around a 2 mm hole, held by snap bumps on the body that reach only 0.5 mm into the hole. The designer's own assembly notes warn that the parts are delicate and can break. The hinge parts also needed supports to print.

**Fix.** Both snap hinges were cut off flush with the back face, and a five-knuckle hinge runs across 60 mm of the back instead. It alternates body, lid, body, lid, body, and a printed pin runs through all five.

- **Body knuckles (3):** a 2.8 mm hole grips the pin. A 45° web joins each knuckle to the back wall, so it prints upright without supports.
- **Lid knuckles (2):** a 3.1 mm hole lets the lid turn freely on the pin. A 45° gusset under each knuckle lets the lid print face-down without supports.
- **Pin:** an octagonal rod 2.5 mm across the flats (2.7 mm across the corners). Lying on a flat side, every face is flat, vertical or at 45°, so it prints without supports. It has a 5 mm head to push and pull it by, and a chamfered tip.
- **Pin hole:** countersunk at the entry end (left, seen from the back) and closed at the other end, so the pin can't be pushed out the far side.
- **Clearance chamfer:** a 0.6 mm chamfer on the body's back top edge behind each lid knuckle keeps the gusset clear of the body.

| | Original | Remix |
|---|---|---|
| Hinges | 2 snap hinges | 1 hinge, 5 knuckles across 60 mm |
| Lid bearing length | 2 × 4.6 mm | 2 × 11.7 mm |
| Wall around the pin hole | 0.75 mm | 1.6 mm (body), 1.45 mm (lid) |
| Retention | 0.5 mm snap bumps | Printed pin through every knuckle, press-fit in the body |
| Sticks out behind the box | 4.3 mm | 7.5 mm |
| Supports needed | Yes | No |

**Result.** The lid swings back about 210° before it touches the box, with about 0.2 mm of clearance the whole way. To assemble, push the pin in until its head stops; see the [README](README.md#hinge-assembly).

![Cross-sections of the hinge. The original lid tab is a thin ring around a 2 mm hole; the remix body knuckle has a 45° underside and holds the octagonal pin in a 2.8 mm hole; the remix lid knuckle has a 45° gusset and turns on the pin in a 3.1 mm hole](images/remix/hinge_before_after.png)

| Hinge dimension | Value |
|---|---|
| Knuckle diameter | 6.0 mm |
| Knuckle length | 11.68 mm, with 0.4 mm gaps |
| Pin hole | 2.8 mm (body), 3.1 mm (lid) |
| Pin | Octagonal, 2.5 mm across flats (2.71 mm across corners), 58.45 mm from head to tip |
| Pin head | 5.0 mm across flats, 1.5 mm thick, flat-bottomed to sit on the bed |
| Pin clearance | 0.05 mm at the corners in the body (a light press fit once printed), 0.2 mm in the lid |
| Closed end of the pin hole | 1.2 mm thick; the tip stops 0.4 mm short of it |
| Axis | 4.45 mm behind the back face, level with the lid seam |

## 4. Support-free printing

**Problem.** The original 3MF profile has tree supports turned on. They're needed for the hinge parts and for the inside of the lid's back wall.

**Fix.**

- The new hinge has 45° undersides on both parts (section 3).
- The pin is octagonal and prints lying on a flat side.
- The inside of the lid's back wall still prints as a bridge, 70 × 13 mm. It's the only large bridge on any part, and it's hidden inside the lid. The wall's inner face was set back 1 mm (the wall is now 3 mm thick instead of 4), so a little sag can't reach the cards.

**Result.** None of the three parts needs supports. Apart from that bridge, only small features are flatter than 45°: the tops of the button holes, grille slots and pin holes, the 1 mm signature recess on the bottom, and the rounded bottom edge. The original prints those the same way.

Print orientation is the same as the designer's 3MF: the body upright, and the lid on its front face with the screen bezel on the bed.

## 5. Print-ready files

The original STLs use Y as the up axis, so they import lying on their sides in a slicer. The remix STLs are exported with Z up, already in print orientation and sitting at Z = 0.

| File | Orientation |
|---|---|
| [Case-bottom_remix.stl](stl/remix/v2/Case-bottom_remix.stl) | Upright, open top facing up |
| [Case-top_remix.stl](stl/remix/v2/Case-top_remix.stl) | Front face (screen bezel) on the bed |
| [Hinge-pin_remix.stl](stl/remix/v2/Hinge-pin_remix.stl) | Lying on one of its flat sides |

## Round 2

The first round was test-fitted on paper only. Feedback on it raised four points: the square frame protruding from the lid feels flimsy, nothing locks the lid, opening the lid means hooking a finger through the window onto the front card, and the lid catches cards that sit at an angle after the box has been tilted. Sections 6 to 9 answer those. They were made on the first-round meshes with the same boolean approach, using [tools/round2_build.py](tools/round2_build.py).

![Before and after cross-sections. Left: the lid cut through a bezel bar, 1.8 mm before and 4 mm after, with the lead-in chamfer at the ceiling. Middle and right: the front seam at the centre, before with the body's tongue and the thin lid bar, after with the 4 mm bar flush inside and the thumb notch below it](images/remix/round2_sections.png)

## 6. Screen frame: 1.8 → 4 mm

**Problem.** The lid's front is a 1.8 mm plate. Inside the bezel outline that plate hangs 23 mm below the bottom of the lid's side walls, as a U-shaped frame around the window with 5 mm bars at the sides and a 6 mm bar along the bottom. With the lid open, nothing backs it, and it flexes when handled.

**Fix.** Everything inside the bezel outline except the outermost 1.8 mm strip is now 4 mm thick, the same as the body's front wall, from the lid's bottom edge up to the ceiling. The window is unchanged (53 × 33 mm) and simply got 4 mm deep, which reads as a recessed screen. The thicker region grows inward, so the front face, the grooves and the painted bezel outline are untouched and the lid still prints face down with nothing new to support.

Inward growth needs room, so the body's tongue (the 2 mm inner layer of the front wall that the lid's plate used to lap over) is cut down to the top of the wall across the middle 59 mm. The lid's frame takes its place: its inner face is exactly in the plane of the body's inner front face, so the inside of the front wall is now one flat surface from the floor to 93.5 mm up, with the window in it. The tongue strips at the sides stay, 5.3 mm wide and up to 74 mm tall; they still hold the cards' edges when the lid is open, and the lid's outer 1.8 mm strip still laps over them for alignment.

The bottom edge of the frame's inner face has a 1 mm 45° chamfer. If a bowed front card sits a little proud of the stack, the chamfer pushes it back as the lid comes down instead of pinching it against the top of the wall.

**Result.** Bending stiffness scales with thickness cubed, so the frame is about 11 times stiffer. The frame has 0.2 mm of clearance to the body all round when closed, measured on the meshes. Lid volume goes from 20.9 to 22.5 cm³; the body loses 1.3 cm³.

![Render of the inside of the lid, showing the thick frame around the window, the chamfered side walls and the two hinge knuckles](images/remix/remix_lid_inside.png)

## 7. Snap catches

**Problem.** Only the 0.05 mm friction fit along the side seams holds the lid closed. Tip the box forward and the lid swings open.

**Fix.** A catch on each side. The side seam is a sloping lap joint: the body's inner wall layer rises above the seam line, and the lid's outer wall layer comes down over it. On the outer face of each body inner layer there is now a bead, 8 mm long along the seam, 1.2 mm wide and 0.3 mm tall, with a half-elliptical profile. The lid's outer layer has a matching groove, 9 × 1.4 mm and 0.4 mm deep, on its inner face. Closing the lid springs the 2 mm outer wall out by 0.3 mm over the bead and lets it drop into the groove with a click.

The catches sit 17 mm behind the front face and 76 mm up, in the front half of the seam where the lap is deepest. That is also the only place on the box with a flexible member: the lid's side wall, which at that point is 15 mm from the front plate and 22 mm from the ceiling and bends about 0.4 % to clear the bead, well inside what PLA tolerates. Nothing can go at the front seam itself: the lid prints face down, so nothing may stand proud of its front face, and the inside of the frame is the card face. The catches still act on the front of the lid, since the beads are 31 mm from the hinge axis and the lid's front edge 63 mm, so a pull at the front needs about half the force the catches hold with.

**Result.** With the lid closed the beads sit inside the grooves and nothing touches except the pre-existing 0.05 mm side-seam overlap, which the grooves reduce from 11.2 to 10.0 mm³. From 1° to 3.5° of opening the beads are 0.35 mm inside the lid's walls, which is the snap; from 8° to 210° nothing touches, as before.

![Cross-section of the catch across the side seam: the body's inner wall layer with the 0.3 mm bead, and the lid's outer wall layer with the groove over it](images/remix/round2_latch_section.png)

## 8. Thumb notch

**Problem.** The lid's front is flush with the body's, and the seam is a plain line. The only thing to get a finger behind is the window, and when the box is full the front card is right behind it.

**Fix.** A notch in the top edge of the body's front wall, centred under the screen: 22 mm wide, 7 mm tall and 2.6 mm deep at the seam, with a floor that slopes out to the face at the bottom. It exposes the underside of the lid's 4 mm bottom bar, so a thumb pushes the lid up and forward and the lid pivots open against the catches. The wall behind the notch stays at least 1.4 mm thick, and the inner face that the cards see is untouched. The notch sits between the D-pad and the A/B buttons, clear of both, and its floor faces upward, so the body still prints upright without supports.

![Render of the body from the front, showing the thumb notch under the screen, the flat top of the front wall and the hinge knuckles](images/remix/remix_body_front.png)

## 9. Lead-in chamfers

**Problem.** Tilt the box with the lid open and the cards shift. Some end up at an angle, with a top corner above a wall. The lid's inner edges were square, so closing it could land an edge on a card.

**Fix.** Every edge of the lid's inner rim is now a ramp that pushes a card back into the box as the lid comes down:

- **Front:** the top of the frame's inner face runs into a chamfer from 93.5 mm up to the ceiling at 98 mm, leaning 2.8 mm forward (32° from vertical). A card top up to 2.8 mm in front of the stack plane is pushed back. The flush frame also removes the 2.2 mm step that used to sit at the top of the tongue.
- **Sides:** a 1.2 mm 45° chamfer along the bottom inner edge of each side wall's inner layer, the sloping edge that rests on the body.
- **Back:** a 1.5 mm 45° chamfer along the bottom inner edge of the back wall, which already sat 1 mm behind the body's inner face. This also narrows the one bridge on the lid.

**Result.** The chamfers remove square edges only; the interior is still 70.0 × 35.0 × 96.0 mm, measured by ray casts at 12 points, and the lid still clears the body through the whole swing.

## What didn't change

- **Depth:** still 35 mm inside, so the box holds about 60 single-sleeved or about 50 double-sleeved cards.
- **Front details:** the screen, bezel, D-pad recess, button holes and speaker grille.
- **Buttons and D-pad:** unchanged. Print them from [Case-GB.3mf](stl/original/Case-GB.3mf) or the original STLs.
- **Signature:** Ashwood's name on the bottom.
- **Lid friction fit:** the lid and body overlap by 0.05 mm along the side seams, which acts as a light friction fit. The closed lid overlaps the body by 10.0 mm³, down from the original's 11.2 mm³ only because the catch grooves take a little of that strip away.

## Verification

These checks were run on the finished second-round models. The remix hasn't been test-printed yet.

| Check | Result |
|---|---|
| Watertight, no open or non-manifold edges | Pass, all three parts |
| Degenerate or near-duplicate geometry | None |
| Lid and body when closed | The 0.05 mm friction strips only (10.0 mm³); zero overlap anywhere else |
| Screen frame and notch against the body | 0.20 mm clearance everywhere when closed |
| Snap catches | Beads inside the grooves when closed; 0.35 mm engaged from 1° to 3.5° of opening |
| Pin seated in the hinge | No overlap: 0.05 mm clearance in the body, 0.2 mm in the lid |
| Lid opening sweep | No contact from 8° to 210° (the catches engage below 4°) |
| Interior | 70.0 × 35.0 × 96.0 mm (W × D × H); the inside of the front wall is one plane from the floor to 93.5 mm |
| Overhangs in print orientation | Only the features listed in section 4; the lid's bridge is 1.5 mm narrower, the body gains 2 mm² under the beads |

## Known limitations

- **Catch stiffness:** the beads are 0.3 mm tall, so 0.1 mm either way on the print changes the click a lot. Sand the beads if the lid is hard to open; build them up with paint or glue if it doesn't click.
- **Pin fit:** the press fit depends on how accurately your printer makes small holes and rods. If the pin is too tight, scale its width and height (not its length) to 97% in the slicer, or run a 2.8 mm drill bit through the body knuckles. If it's loose, scale those to 102% or glue the head.
- **Color:** STLs carry no color. The original 3MF paints the bezel black, so repaint it in Bambu Studio.
- **One bridge:** the lid's back wall is a 70 mm bridge. It's hidden and set back from the cards, but printers that bridge poorly will leave it rough.
- **Capacity:** at 35 mm deep the box doesn't hold 100 double-sleeved or 120 single-sleeved cards. A 72 mm-deep version (70 × 72 × 96 mm inside) was built and checked during this work, but it wasn't exported.

## How the changes were made

There's no CAD source for the original, so the changes were made directly on Ashwood's meshes:

- **Height and width:** inserted in bands where every surface runs parallel to the direction of the change. Those surfaces just get longer, so the rest of the shape is exact.
- **Hinge:** the old snap hinges were cut off and the new knuckles, pin holes and chamfers added with solid-geometry operations. The pin is a new part, modeled from scratch.
- **Checks:** each part was re-checked after every change for watertightness, fit, hinge clearance, interior size and overhangs.
- **Round 2:** the frame, catches, notch and chamfers were added the same way, as boolean unions and cuts on the first-round meshes. The script is [tools/round2_build.py](tools/round2_build.py); it reads [stl/remix/v1/](stl/remix/v1/) and writes [stl/remix/](stl/remix/v2/).
