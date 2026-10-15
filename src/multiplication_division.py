from manim import *

ORIGIN_IDX = 2
V1 = [2, 3, 2, 1, 3]
V2 = [1, 2, 3, 2, 1]
X1 = {i - ORIGIN_IDX: v for i, v in enumerate(V1)}
X2 = {i - ORIGIN_IDX: v for i, v in enumerate(V2)}

COL_X0, COL_DX = 3.3, 0.8

def fmt(v):
    """2.0 -> '2', 1.5 -> '1.5', 0.6667 -> '0.67'"""
    return f"{v:.2f}".rstrip("0").rstrip(".")


def col_pos(i, y):
    return np.array([COL_X0 + COL_DX * i, y, 0])


def make_axes(center, y_range, y_length):
    ax = Axes(x_range=[-5, 5, 1], y_range=y_range,
              x_length=6.5, y_length=y_length, tips=False,
              y_axis_config={"include_ticks": False, "stroke_opacity": 0.3}).move_to(center)
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
        val = Text(fmt(v), font_size=22).next_to(dot, UP if v >= 0 else DOWN, buff=0.06)
        val.set_stroke(BLACK, width=5, background=True)   # halo so the number is never hidden by a line
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


class MulDiv(Scene):
    def construct(self):
        title = Text("Signal Multiplication & Division", font_size=32,
                     color=YELLOW).to_edge(UP, buff=0.25)
        caption = Text("Two input signals", font_size=20, color=GRAY).next_to(title, DOWN, buff=0.12)
        self.play(Write(title), FadeIn(caption))

        # three graphs: x1, x2, result
        ax1, lab1 = make_axes(LEFT * 3.4 + UP * 1.8, [0, 4, 1], 1.3)
        ax2, lab2 = make_axes(LEFT * 3.4 + DOWN * 0.4, [0, 4, 1], 1.3)
        axo, labo = make_axes(LEFT * 3.4 + DOWN * 2.75, [0, 7, 1], 1.6)   # fits products up to 6

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

        def do_op(sym, fn, color, ax_res):
            """Go through n = -2 ... 2: highlight the two inputs, show the calculation, draw the result."""
            res_stems, res_nums = VGroup(), VGroup()
            eq = None
            for i, n in enumerate(sorted(X1)):
                a, b = X1[n], X2[n]
                c = fn(a, b)
                new_eq = Text(f"n = {n}:   {a} {sym} {b} = {fmt(c)}", font_size=24,
                              color=YELLOW).move_to(eq_pos)
                flash = [Indicate(stems1[i], color=YELLOW), Indicate(stems2[i], color=YELLOW),
                         Indicate(nums1[i], color=YELLOW), Indicate(nums2[i], color=YELLOW)]
                if eq is None:
                    eq = new_eq
                    flash.append(FadeIn(eq))
                else:
                    flash.append(Transform(eq, new_eq))
                self.play(*flash, run_time=1.0)

                stem = make_stems(ax_res, {n: c}, color)[0]
                num = Text(fmt(c), font_size=26,
                           color=ORANGE if n == 0 else WHITE).move_to(col_pos(i, Y3))
                self.play(Create(stem), Write(num), run_time=0.7)
                res_stems.add(stem)
                res_nums.add(num)
            return res_stems, res_nums, eq

        # multiplication
        cap = Text("Multiplication:  y[n] = x1[n] × x2[n]   (samples with the same n)",
                   font_size=20, color=ORANGE).move_to(caption)
        self.play(Transform(caption, cap))
        mul_stems, mul_nums, eq = do_op("×", lambda a, b: a * b, GREEN, axo)
        self.wait(1.5)

        # division
        # the results are small (0.5 ... 3), so the result graph gets a smaller y-axis
        axo2, labo2 = make_axes(LEFT * 3.4 + DOWN * 2.75, [0, 4, 1], 1.6)
        new_name = Text("y[n]", font_size=22, color=RED).move_to(nameo, aligned_edge=LEFT)
        cap = Text("Division:  y[n] = x1[n] ÷ x2[n]   (x2[n] must not be 0)",
                   font_size=20, color=ORANGE).move_to(caption)
        self.play(FadeOut(mul_stems), FadeOut(mul_nums), FadeOut(eq),
                  FadeOut(axo), FadeOut(labo),
                  Transform(nameo, new_name), Transform(caption, cap))
        self.play(Create(axo2), FadeIn(labo2))
        div_stems, div_nums, eq = do_op("÷", lambda a, b: a / b, RED, axo2)
        
        self.wait(2)