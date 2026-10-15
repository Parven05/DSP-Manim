from manim import *

VALS = [2, 3, 2, 1, 3]
ORIGIN_IDX = 2                                        # index of n = 0 in the list
X = {i - ORIGIN_IDX: v for i, v in enumerate(VALS)}   # {-2:2, -1:3, 0:2, 1:1, 2:3}

COL_X0, COL_DX = 3.0, 0.8

def col_pos(i, y):
    return np.array([COL_X0 + COL_DX * i, y, 0])

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

def seq_frame(label, y):
    """'x[n] = {   }' frame; the numbers are placed on the columns separately."""
    lb = Text("{", font_size=30).move_to(col_pos(0, y) + LEFT * 0.5)
    rb = Text("}", font_size=30).move_to(col_pos(4, y) + RIGHT * 0.5)
    lab = Text(label + " =", font_size=24).next_to(lb, LEFT, buff=0.15)
    return VGroup(lab, lb, rb)


def index_labels(y):
    """n = -2 ... n = 2 under each column (n = 0 highlighted)."""
    g = VGroup()
    for i in range(5):
        n = i - ORIGIN_IDX
        g.add(Text(f"n = {n}", font_size=16, color=ORANGE if n == 0 else GRAY)
              .move_to(col_pos(i, y - 0.45)))
    return g

def number_row(vals, y):
    g = VGroup()
    for i, v in enumerate(vals):
        n = i - ORIGIN_IDX
        g.add(Text(str(v), font_size=26, color=ORANGE if n == 0 else WHITE)
              .move_to(col_pos(i, y)))
    return g

class Folding(Scene):
    def construct(self):
        title = Text("Time Folding (Reflection):  x[-n]", font_size=32,
                     color=YELLOW).to_edge(UP, buff=0.25)
        self.play(Write(title))

        # axes
        ax_in, lab_in = make_axes(LEFT * 3.4 + UP * 1.3)
        ax_out, lab_out = make_axes(LEFT * 3.4 + DOWN * 2.0)
        name_in = Text("x[n]", font_size=24, color=BLUE).next_to(ax_in, UP, buff=0.0).align_to(ax_in, LEFT)
        name_out = Text("x[-n]", font_size=24, color=GREEN).next_to(ax_out, UP, buff=0.0).align_to(ax_out, LEFT)
        self.play(Create(ax_in), FadeIn(lab_in), FadeIn(name_in))
        self.play(Create(ax_out), FadeIn(lab_out), FadeIn(name_out))

        # input signal & input sequence with n labels
        Y_IN, Y_OUT = 1.7, -1.3
        x_stems = make_stems(ax_in, X, BLUE)
        frame_in = seq_frame("x[n]", Y_IN)
        nums_in = number_row(VALS, Y_IN)
        idx_in = index_labels(Y_IN)

        self.play(LaggedStart(*[Create(s) for s in x_stems], lag_ratio=0.2))
        self.play(Write(frame_in), Write(nums_in), FadeIn(idx_in))
        self.wait(0.5)

        # empty output sequence (only the n labels)
        frame_out = seq_frame("x[-n]", Y_OUT)
        idx_out = index_labels(Y_OUT)
        self.play(Write(frame_out), FadeIn(idx_out))

        # mirror line at n = 0 on the output graph 
        mirror = DashedLine(ax_out.c2p(0, 0), ax_out.c2p(0, 4), color=ORANGE)
        mirror_txt = Text("fold about n = 0", font_size=18, color=ORANGE)
        mirror_txt.next_to(mirror, UP, buff=0.08)
        self.play(Create(mirror), FadeIn(mirror_txt))

        # step 1: copy the signal down (same positions)
        y_stems = x_stems.copy().set_color(GREEN)
        down = ax_out.c2p(0, 0) - ax_in.c2p(0, 0)
        self.play(y_stems.animate.shift(down))

        # step 2: fold. value at n goes to position -n
        # graph: each stem moves from n to -n
        moves = []
        for stem, n in zip(y_stems, sorted(X)):
            dx = ax_out.c2p(-2 * n, 0) - ax_out.c2p(0, 0)
            moves.append(stem.animate.shift(dx))

        # sequence: each number flies to the column of -n (index i -> 4 - i)
        nums_out = nums_in.copy()
        for i, num in enumerate(nums_out):
            moves.append(num.animate.move_to(col_pos(4 - i, Y_OUT)))

        self.play(*moves, run_time=3)
        self.wait(0.5)

        # example: x[-2] = 2 now sits at n = 2
        self.play(
            Indicate(x_stems[0], color=YELLOW), Indicate(y_stems[0], color=YELLOW),
            Indicate(nums_in[0], color=YELLOW), Indicate(nums_out[0], color=YELLOW),
        )
        self.wait(2)