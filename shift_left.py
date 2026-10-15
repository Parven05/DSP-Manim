from manim import *

VALS = [2, 3, 2, 1, 3]
ORIGIN_IDX = 2                                        # index of n = 0 in the list
X = {i - ORIGIN_IDX: v for i, v in enumerate(VALS)}   # {-2:2, -1:3, 0:2, 1:1, 2:3}
K = 2

def make_axes(center):
    ax = Axes(x_range=[-5, 5, 1], y_range=[0, 4, 1],
        x_length=6.5, y_length=2.2, tips=False,
        y_axis_config={"include_ticks": False, "stroke_opacity": 0.3}).move_to(center)
    labels = VGroup(*[
        Text(str(n), font_size=16).next_to(ax.c2p(n, 0), DOWN, buff=0.1)
        for n in range(-4, 5)
    ])
    n_label = Text("n", font_size=20).next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
    return ax, VGroup(labels, n_label)


def make_stems(ax, sig, color):
    stems = VGroup()
    for n in sorted(sig):
        v = sig[n]
        line = Line(ax.c2p(n, 0), ax.c2p(n, v), color=color)
        dot = Dot(ax.c2p(n, v), color=color, radius=0.07)
        val = Text(str(v), font_size=20).next_to(dot, UP, buff=0.05)
        val.set_stroke(BLACK, width=5, background=True)
        stems.add(VGroup(line, dot, val))
    return stems


def seq_row(label, vals):
    """Text like  x[n] = { 2, 3, 2, 1, 3 }"""
    lab = Text(label + " =", font_size=24)
    items = VGroup(*[
        Text(str(v) + ("," if i < len(vals) - 1 else ""), font_size=24)
        for i, v in enumerate(vals)
    ]).arrange(RIGHT, buff=0.25)
    row = VGroup(lab, Text("{", font_size=28), items, Text("}", font_size=28))
    row.arrange(RIGHT, buff=0.15)
    return row, items


def origin_marker(items, idx):
    """Arrow under element idx + 'n=0' label."""
    base = items[idx].get_bottom()
    arr = Arrow(base + DOWN * 0.6, base + DOWN * 0.05, buff=0,
                color=ORANGE, stroke_width=4)
    txt = Text("n=0", font_size=18, color=ORANGE).next_to(arr, DOWN, buff=0.05)
    return VGroup(arr, txt)


class ShiftLeft(Scene):
    def construct(self):
        title = Text("Time Shifting - Left Shift:  x[n + 2]", font_size=32,
                     color=YELLOW).to_edge(UP, buff=0.25)
        self.play(Write(title))

        # axes
        ax_in, lab_in = make_axes(LEFT * 3.4 + UP * 1.3)
        ax_out, lab_out = make_axes(LEFT * 3.4 + DOWN * 2.0)
        name_in = Text("x[n]", font_size=24, color=BLUE).next_to(ax_in, UP, buff=0.0).align_to(ax_in, LEFT)
        name_out = Text("x[n+2]", font_size=24, color=GREEN).next_to(ax_out, UP, buff=0.0).align_to(ax_out, LEFT)
        self.play(Create(ax_in), FadeIn(lab_in), FadeIn(name_in))
        self.play(Create(ax_out), FadeIn(lab_out), FadeIn(name_out))

        # input signal & sequence notation
        x_stems = make_stems(ax_in, X, BLUE)
        row_in, items_in = seq_row("x[n]", VALS)
        row_in.move_to(RIGHT * 3.3 + UP * 1.5)
        mark_in = origin_marker(items_in, ORIGIN_IDX)

        self.play(LaggedStart(*[Create(s) for s in x_stems], lag_ratio=0.2))
        self.play(Write(row_in))
        self.play(FadeIn(mark_in))
        self.wait(0.5)

        # output sequence row (same numbers, arrow still at old origin)
        row_out, items_out = seq_row("x[n+2]", VALS)
        row_out.move_to(RIGHT * 3.3 + DOWN * 1.2)
        mark_out = origin_marker(items_out, ORIGIN_IDX)
        self.play(Write(row_out), FadeIn(mark_out))

        # step 1: copy signal down
        y_stems = x_stems.copy().set_color(GREEN)
        down = ax_out.c2p(0, 0) - ax_in.c2p(0, 0)
        self.play(y_stems.animate.shift(down))

        # step 2: shift left by 2
        left = ax_out.c2p(-K, 0) - ax_out.c2p(0, 0)
        arrow = Arrow(ax_out.c2p(4.6, 3.0), ax_out.c2p(2.6, 3.0), buff=0, color=YELLOW)
        arrow_txt = Text("t0 = 2  (left)", font_size=18, color=YELLOW).next_to(arrow, UP, buff=0.05)
        self.play(GrowArrow(arrow), FadeIn(arrow_txt))

        # origin arrow moves from the 3rd element to the last element (value 3)
        move_x = items_out[-1].get_center()[0] - items_out[ORIGIN_IDX].get_center()[0]
        self.play(
            y_stems.animate.shift(left),
            mark_out.animate.shift(RIGHT * move_x),
            run_time=2,
        )
        self.wait(0.5)

        self.play(Indicate(x_stems[-1], color=YELLOW), Indicate(y_stems[-1], color=YELLOW))
        self.wait(2)