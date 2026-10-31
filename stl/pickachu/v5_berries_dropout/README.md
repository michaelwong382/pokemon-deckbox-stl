# Pikachu remix, version 5: Pikachu in berries, edge to edge with the lines dropping out

The round-5 remix ([../../remix/v5/](../../remix/v5/)) with the Pikachu-in-berries pattern engraved 0.8 mm into the whole back wall of the body, complete in the middle and breaking up towards the edges. Every file except the body is a byte-for-byte copy of round 5, so printing, assembly and the test coupons are exactly as described in the [round-5 README](../../remix/v5/README.md); the body changes only in the outer 0.8 mm of its back wall.

![The engraved box seen from behind](example_images/02_engraved_back_iso.png)

| File | Print orientation | What it is |
|---|---|---|
| Case-bottom_remix.stl | Upright, open top facing up | Round-5 body with the breaking-up pattern in the back wall; "Yoojin" is still in the bottom |
| Case-top_remix.stl | Front face (screen bezel) on the bed | Lid, unchanged |
| Hinge-pin_remix.stl | Lying on its flat side | Hinge pin, print two, unchanged |
| D-Pad_remix.stl, Button_remix.stl, StartSelect_remix.stl | As in round 5 | Buttons, unchanged |
| Test-seats.stl, Test-hinge-body.stl, Test-hinge-lid.stl | As in round 5 | Optional fit-test coupons, unchanged |

## The engraving

- **Design:** 14 berries, drop-out: the same upright window of the all-over drawing as [v2](../v2_berries/) and [v4](../v4_berries_fade/) (columns 270 to 1250 of the 1536 px source), over the whole flat wall, 71 × 74 mm, from 1.6 to 76 mm above the base and out to the rounded side edges. Preview [14_berries_dropout_back.png](../14_berries_dropout_back.png).
- **Drop-out:** every groove is the full 0.8 mm deep; what changes towards the edges is which lines are there. More than 12 mm from an edge the drawing is complete. Closer in, strokes are cut into fragments a few millimetres long by a smooth random field, and the share that survives falls linearly to zero at the edge, so the picture breaks up into dashes and specks and stops, with no rectangular boundary. Fragments smaller than 0.25 mm² (a 0.56 mm dot) were dropped as unprintable; 79 fragments remain. The random field is seeded, so the build is repeatable.
- **Depth and wall:** 0.8 mm into a 3.95 mm wall, so 3.15 mm remains behind the picture. The top edge is set by the 45° support wedge under the hinge knuckles, which meets the wall at 76.4 mm.
- **Line width:** strokes thickened by 0.15 mm a side: the narrowest groove is 0.52 mm and the median 0.85 mm. Gaps under 0.45 mm were merged and any solid between two grooves thinner than 0.4 mm was taken into the groove.
- **Printing:** vertical wall, shallow recess, no supports, no first-layer islands. Each groove's top edge overhangs 0.8 mm, fine at 0.2 mm layers; 0.12 to 0.16 mm layers make the small berries and the fragment ends crisper.

| | |
|---|---|
| ![Straight at the back wall](example_images/01_engraved_back.png) | ![The break-up at the lower left edge](example_images/05_fade_at_the_edge.png) |

[03_engraving_close_up.png](example_images/03_engraving_close_up.png) is Pikachu's face; [04_engraving_raking_light.png](example_images/04_engraving_raking_light.png) is the whole wall lit from the side. Compare [v4](../v4_berries_fade/), where the same picture keeps all its lines and fades in depth instead.

Built from round 5 by [tools/pickachu_build.py](../../../tools/pickachu_build.py) (design index 13, output folder v5_berries_dropout) and checked: watertight, removed volume equals the surviving pattern's area times 0.8 mm (1066.7 mm³), nothing added, all changes inside the back wall. Not yet test-printed. The other versions and all design previews are in the [folder README](../README.md).
