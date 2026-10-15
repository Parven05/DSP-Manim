from manim import *

ORIGIN_IDX = 2
V1 = [2, 3, 2, 1, 3]
V2 = [1, 2, 3, 2, 1]
X1 = {i - ORIGIN_IDX: v for i, v in enumerate(V1)}
X2 = {i - ORIGIN_IDX: v for i, v in enumerate(V2)}

COL_X0, COL_DX = 2.6, 0.8

def col_pos(i, y):
    return np.array([COL_X0 + COL_DX * i, y, 0])


def make_axes(center, y_range, y_length):
    ax = Axes(x_range=[-5, 5, 1], y_range=y_range,
        x_length=6.5, y_length=y_length, tips=False,
        y_axis_config={"include_ticks": False, "stroke_opacity": 0.3}).move_to(center)
    # n labels at the bottom edge so they never touch negative stems
    labels = VGroup(*[
        Text(str(n), font_size=16).next_to(ax.c2p(n, y_range[0]), DOWN, buff=0.1)
        for n in range(-4, 5)
    ])
    n_label = Text("n", font_size=20).next_to(ax.c2p(5, y_range[0]), RIGHT, buff=0.1)
    return ax, VGroup(labels, n_label)


def make_stems(ax, sig, color):
    stems = VGroup()
    for n in sorted(sig):
        v = sig[n]
        line = Line(ax.c2p(n, 0), ax.c2p(n, v), color=color)
        dot = Dot(ax.c2p(n, v), color=color, radius=0.07)
        val = Text(str(v), font_size=22).next_to(dot, UP if v >= 0 else DOWN, buff=0.06)
        val.set_stroke(BLACK, width=5, background=True)  
        stems.add(VGroup(line, dot, val))
    return stems


def seq_frame(label, y):
    lb = Text("{", font_size=30).move_to(col_pos(0, y) + LEFT * 0.5)
    rb = Text("}", font_size=30).move_to(col_pos(4, y) + RIGHT * 0.5)
    lab = Text(label + " =", font_size=24).next_to(lb, LEFT, buff=0.15)
    return VGroup(lab, lb, rb)


def index_labels(y):
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


class AddSub(Scene):
    def construct(self):
        title = Text("Signal Addition & Subtraction", font_size=32,
                     color=YELLOW).to_edge(UP, buff=0.25)
        caption = Text("Two input signals", font_size=20, color=GRAY).next_to(title, DOWN, buff=0.12)
        self.play(Write(title), FadeIn(caption))

        # three graphs: x1, x2, result
        ax1, lab1 = make_axes(LEFT * 3.4 + UP * 1.8, [0, 4, 1], 1.3)
        ax2, lab2 = make_axes(LEFT * 3.4 + DOWN * 0.4, [0, 4, 1], 1.3)
        axo, labo = make_axes(LEFT * 3.4 + DOWN * 2.7, [-3, 6, 1], 1.75)

        def name(text, ax, color):
            return Text(text, font_size=22, color=color).next_to(ax, UP, buff=0.0).align_to(ax, LEFT)

        name1 = name("x1[n]", ax1, BLUE)
        name2 = name("x2[n]", ax2, PURPLE_B)
        nameo = name("y[n]", axo, GREEN)

        self.play(Create(ax1), FadeIn(lab1), FadeIn(name1))
        self.play(Create(ax2), FadeIn(lab2), FadeIn(name2))
        self.play(Create(axo), FadeIn(labo), FadeIn(nameo))

        # input signals & sequences
        Y1, Y2, Y3 = 2.1, 0.3, -2.0
        stems1 = make_stems(ax1, X1, BLUE)
        stems2 = make_stems(ax2, X2, PURPLE_B)
        frame1, frame2, frame3 = seq_frame("x1[n]", Y1), seq_frame("x2[n]", Y2), seq_frame("y[n]", Y3)
        nums1, nums2 = number_row(V1, Y1), number_row(V2, Y2)
        idx1, idx2, idx3 = index_labels(Y1), index_labels(Y2), index_labels(Y3)

        self.play(LaggedStart(*[Create(s) for s in stems1], lag_ratio=0.15),
                  LaggedStart(*[Create(s) for s in stems2], lag_ratio=0.15))
        self.play(Write(frame1), Write(nums1), FadeIn(idx1),
                  Write(frame2), Write(nums2), FadeIn(idx2))
        self.play(Write(frame3), FadeIn(idx3))
        self.wait(0.5)

        eq_pos = np.array([COL_X0 + 2 * COL_DX, -0.95, 0])

        def do_op(sym, fn, color):
            """Go through n = -2 ... 2: highlight the two inputs, show the calculation, draw the result."""
            res_stems, res_nums = VGroup(), VGroup()
            eq = None
            for i, n in enumerate(sorted(X1)):
                a, b = X1[n], X2[n]
                c = fn(a, b)
                new_eq = Text(f"n = {n}:   {a} {sym} {b} = {c}", font_size=24,
                              color=YELLOW).move_to(eq_pos)
                flash = [Indicate(stems1[i], color=YELLOW), Indicate(stems2[i], color=YELLOW),
                         Indicate(nums1[i], color=YELLOW), Indicate(nums2[i], color=YELLOW)]
                if eq is None:
                    eq = new_eq
                    flash.append(FadeIn(eq))
                else:
                    flash.append(Transform(eq, new_eq))
                self.play(*flash, run_time=1.0)

                stem = make_stems(axo, {n: c}, color)[0]
                num = Text(str(c), font_size=26,
                           color=ORANGE if n == 0 else WHITE).move_to(col_pos(i, Y3))
                self.play(Create(stem), Write(num), run_time=0.7)
                res_stems.add(stem)
                res_nums.add(num)
            return res_stems, res_nums, eq

        # addition
        cap = Text("Addition:  y[n] = x1[n] + x2[n]   (samples with the same n)", font_size=20,
                   color=ORANGE).move_to(caption)
        self.play(Transform(caption, cap))
        add_stems, add_nums, eq = do_op("+", lambda a, b: a + b, GREEN)
        self.wait(1.5)

        # subtraction
        new_name = Text("y[n]", font_size=22, color=RED).move_to(nameo, aligned_edge=LEFT)
        cap = Text("Subtraction:  y[n] = x1[n] - x2[n]   (samples with the same n)", font_size=20,
                   color=ORANGE).move_to(caption)
        self.play(FadeOut(add_stems), FadeOut(add_nums), FadeOut(eq),
                  Transform(nameo, new_name), Transform(caption, cap))
        sub_stems, sub_nums, eq = do_op("-", lambda a, b: a - b, RED)
        self.wait(2)