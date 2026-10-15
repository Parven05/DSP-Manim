from manim import *

VALS = [2, 3, 2, 1, 3]
ORIGIN_IDX = 2
X = {i - ORIGIN_IDX: v for i, v in enumerate(VALS)}   # {-2:2, -1:3, 0:2, 1:1, 2:3}
K = 2

COL_X0, COL_DX = 3.3, 0.8


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
    lb = Text("{", font_size=30).move_to(col_pos(0, y) + LEFT * 0.5)
    rb = Text("}", font_size=30).move_to(col_pos(4, y) + RIGHT * 0.5)
    lab = Text(label + " =", font_size=24).next_to(lb, LEFT, buff=0.15)
    return VGroup(lab, lb, rb)


def index_labels(y, start_n):
    """n = start_n ... start_n+4 under each column (n = 0 highlighted)."""
    g = VGroup()
    for i in range(5):
        n = start_n + i
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


class FoldingShiftRight(Scene):
    def construct(self):
        title = Text(f"Folding and Shift Right:  x[-n + {K}]", font_size=32,
                     color=YELLOW).to_edge(UP, buff=0.25)
        caption = Text("Input signal", font_size=20, color=GRAY).next_to(title, DOWN, buff=0.12)
        self.play(Write(title), FadeIn(caption))

        # axes
        ax_in, lab_in = make_axes(LEFT * 3.4 + UP * 1.2)
        ax_out, lab_out = make_axes(LEFT * 3.4 + DOWN * 2.1)
        name_in = Text("x[n]", font_size=24, color=BLUE).next_to(ax_in, UP, buff=0.0).align_to(ax_in, LEFT)
        name_out = Text("x[n]", font_size=24, color=GREEN).next_to(ax_out, UP, buff=0.0).align_to(ax_out, LEFT)
        self.play(Create(ax_in), FadeIn(lab_in), FadeIn(name_in))
        self.play(Create(ax_out), FadeIn(lab_out), FadeIn(name_out))

        # input signal & row 1
        Y1, Y2, Y3 = 1.9, 0.1, -1.7
        x_stems = make_stems(ax_in, X, BLUE)
        frame1 = seq_frame("x[n]", Y1)
        nums1 = number_row(VALS, Y1)
        idx1 = index_labels(Y1, -2)

        self.play(LaggedStart(*[Create(s) for s in x_stems], lag_ratio=0.2))
        self.play(Write(frame1), Write(nums1), FadeIn(idx1))
        self.wait(0.5)

        # step 1: fold
        new_caption = Text("Step 1: fold   x[n]  ->  x[-n]", font_size=20, color=ORANGE).move_to(caption)
        self.play(Transform(caption, new_caption))

        frame2 = seq_frame("x[-n]", Y2)
        idx2 = index_labels(Y2, -2)
        self.play(Write(frame2), FadeIn(idx2))

        mirror = DashedLine(ax_out.c2p(0, 0), ax_out.c2p(0, 4), color=ORANGE)
        mirror_txt = Text("fold about n = 0", font_size=18, color=ORANGE).next_to(mirror, UP, buff=0.08)
        self.play(Create(mirror), FadeIn(mirror_txt))

        y_stems = x_stems.copy().set_color(GREEN)
        down = ax_out.c2p(0, 0) - ax_in.c2p(0, 0)
        self.play(y_stems.animate.shift(down))

        moves = []
        for stem, n in zip(y_stems, sorted(X)):
            dx = ax_out.c2p(-2 * n, 0) - ax_out.c2p(0, 0)      
            moves.append(stem.animate.shift(dx))
        nums2 = nums1.copy()
        for i, num in enumerate(nums2):
            moves.append(num.animate.move_to(col_pos(4 - i, Y2)))   
        self.play(*moves, run_time=3)

        new_name = Text("x[-n]", font_size=24, color=GREEN).move_to(name_out, aligned_edge=LEFT)
        self.play(Transform(name_out, new_name), FadeOut(mirror), FadeOut(mirror_txt))
        self.wait(0.5)

        # step 2: shift right
        new_caption = Text(f"Step 2: shift right by {K}   x[-n]  ->  x[-n + {K}]",
                           font_size=20, color=ORANGE).move_to(caption)
        self.play(Transform(caption, new_caption))

        frame3 = seq_frame(f"x[-n+{K}]", Y3)
        idx3 = index_labels(Y3, -2)                   
        self.play(Write(frame3), FadeIn(idx3))

        # copy the folded numbers into row 3 (same values, same columns)
        nums3 = nums2.copy()
        self.play(nums3.animate.shift(np.array([0, Y3 - Y2, 0])))

        # arrow on the empty side of the graph
        right = ax_out.c2p(K, 0) - ax_out.c2p(0, 0)
        arrow = Arrow(ax_out.c2p(-4.6, 3.0), ax_out.c2p(-2.6, 3.0), buff=0, color=YELLOW)
        arrow_txt = Text(f"t0 = {K}  (right)", font_size=18, color=YELLOW).next_to(arrow, UP, buff=0.05)
        self.play(GrowArrow(arrow), FadeIn(arrow_txt))

        # graph moves right; the n labels of row 3 become n+2 (values stay the same),
        # so the n = 0 label now sits under the first element
        idx3_target = index_labels(Y3, -2 + K)
        orange_idx = ORIGIN_IDX                        
        new_orange_idx = 4 - (ORIGIN_IDX - K)          
        self.play(
            y_stems.animate.shift(right),
            Transform(idx3, idx3_target),
            nums3[orange_idx].animate.set_color(WHITE),
            nums3[new_orange_idx].animate.set_color(ORANGE),
            run_time=2.5,
        )

        new_name = Text(f"x[-n+{K}]", font_size=24, color=GREEN).move_to(name_out, aligned_edge=LEFT)
        self.play(Transform(name_out, new_name))
        self.wait(0.5)

        # example: x[-2] = 2 started at n=-2, is folded to n=2, then shifted right to n=4
        self.play(
            Indicate(x_stems[0], color=YELLOW), Indicate(y_stems[0], color=YELLOW),
            Indicate(nums1[0], color=YELLOW), Indicate(nums3[0], color=YELLOW),
        )
        self.wait(2)