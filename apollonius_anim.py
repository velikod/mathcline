"""Apollonius' Theorem — visual proof via cline inversion (Manim animation)."""

from manim import *
import numpy as np
import sys

sys.path.insert(0, '/Users/velikodonchev/Documents/mathcline')
from cline import Cline


config.background_color = "#0a1628"


def compute_apollonius():
    """Compute everything for three mutually tangent circles with radii 1, 1.5, 0.8."""
    r1, r2, r3 = 1.0, 1.5, 0.8
    c1 = 0 + 0j
    c2 = (r1 + r2) + 0j
    x3 = ((r1 + r3) ** 2 - (r2 + r3) ** 2 + (r1 + r2) ** 2) / (2 * (r1 + r2))
    y3 = np.sqrt((r1 + r3) ** 2 - x3 ** 2)
    c3 = x3 + 1j * y3

    # Tangent point P between C1 and C2
    P = r1 * (c2 - c1) / abs(c2 - c1)

    # Translate
    c1t, c2t, c3t = c1 - P, c2 - P, c3 - P

    # Invert in unit circle
    S = Cline.from_circle(center=0, radius=1)
    C1i = S.invert(Cline.from_circle(center=c1t, radius=r1))
    C2i = S.invert(Cline.from_circle(center=c2t, radius=r2))
    C3i = S.invert(Cline.from_circle(center=c3t, radius=r3))

    # Line positions
    x_l1 = -C1i.d / (2 * np.real(C1i.alpha))
    x_l2 = -C2i.d / (2 * np.real(C2i.alpha))

    # Solution circles in inverted picture
    mid_x = (x_l1 + x_l2) / 2
    r_sol = abs(x_l2 - x_l1) / 2
    cx3i, cy3i, r3i = C3i.center.real, C3i.center.imag, C3i.radius

    dx = mid_x - cx3i
    dy = np.sqrt(max(0, (r_sol + r3i) ** 2 - dx ** 2))
    sol1i_c = complex(mid_x, cy3i + dy)
    sol2i_c = complex(mid_x, cy3i - dy)

    # Invert solutions back and translate
    Sol1i = Cline.from_circle(center=sol1i_c, radius=r_sol)
    Sol2i = Cline.from_circle(center=sol2i_c, radius=r_sol)
    Sol1t = S.invert(Sol1i)
    Sol2t = S.invert(Sol2i)

    return dict(
        c1=c1, c2=c2, c3=c3, r1=r1, r2=r2, r3=r3, P=P,
        c1t=c1t, c2t=c2t, c3t=c3t,
        x_l1=x_l1, x_l2=x_l2,
        C3i=C3i, mid_x=mid_x, r_sol=r_sol,
        sol1i_c=sol1i_c, sol2i_c=sol2i_c,
        sol1_c=Sol1t.center + P, sol1_r=Sol1t.radius,
        sol2_c=Sol2t.center + P, sol2_r=Sol2t.radius,
    )


class ApolloniusProof(Scene):
    def construct(self):
        d = compute_apollonius()
        s = 1.1  # display scale

        # === Colors ===
        A_COLOR = BLUE_C
        B_COLOR = GREEN_C
        C_COLOR = PURPLE_C
        SOL_1 = RED
        SOL_2 = ORANGE
        INV_COLOR = YELLOW_D
        GHOST = 0.12

        def sub(text, prev=None):
            t = Text(text, font_size=26, color=GREY_A).to_edge(DOWN)
            anims = [FadeIn(t)]
            if prev is not None:
                anims.insert(0, FadeOut(prev))
            self.play(*anims)
            return t

        # Helper: complex to screen position (centered)
        centroid = (d['c1'] + d['c2'] + d['c3']) / 3
        def cpos(z):
            return np.array([(z.real - centroid.real) * s,
                             (z.imag - centroid.imag) * s - 0.3, 0])

        def cpos_t(z):
            """For translated coords (centered at origin)."""
            return np.array([z.real * s, z.imag * s, 0])

        # ============================================================
        # THEOREM STATEMENT with final picture
        # ============================================================
        title = Text("Apollonius' Theorem", font_size=44, weight=BOLD)
        title.to_edge(UP, buff=0.4)

        statement = VGroup(
            Text("Given three mutually tangent circles,", font_size=28),
            Text("there exist exactly two circles", font_size=28),
            Text("tangent to all three.", font_size=28, weight=BOLD),
        ).arrange(DOWN, buff=0.2).next_to(title, DOWN, buff=0.25)

        # Build preview of final result
        sc = 0.45
        preview = VGroup(
            Circle(radius=d['r1']*s*sc, color=A_COLOR, stroke_width=2).move_to(cpos(d['c1'])*sc),
            Circle(radius=d['r2']*s*sc, color=B_COLOR, stroke_width=2).move_to(cpos(d['c2'])*sc),
            Circle(radius=d['r3']*s*sc, color=C_COLOR, stroke_width=2).move_to(cpos(d['c3'])*sc),
            Circle(radius=d['sol1_r']*s*sc, color=SOL_1, stroke_width=3).move_to(cpos(d['sol1_c'])*sc),
            Circle(radius=d['sol2_r']*s*sc, color=SOL_2, stroke_width=3).move_to(cpos(d['sol2_c'])*sc),
        )
        preview.move_to(DOWN * 1.4)

        self.play(Write(title))
        self.wait(0.3)
        for line in statement:
            self.play(FadeIn(line), run_time=0.8)
        self.wait(0.5)
        self.play(FadeIn(preview), run_time=1.5)
        self.wait(2)

        proof_label = Text("Proof by inversion", font_size=28,
                           color=YELLOW_D, slant=ITALIC)
        proof_label.next_to(statement, DOWN, buff=0.3)
        self.play(FadeIn(proof_label))
        self.wait(1)

        self.play(FadeOut(statement), FadeOut(proof_label), FadeOut(preview))
        title_sm = Text("Apollonius' Theorem — Proof",
                        font_size=28, weight=BOLD).to_edge(UP)
        self.play(ReplacementTransform(title, title_sm))

        # ============================================================
        # WHAT IS INVERSION?
        # ============================================================
        self.play(FadeOut(title_sm))
        inv_title = Text("What is inversion?", font_size=32,
                         weight=BOLD, color=YELLOW_D).to_edge(UP, buff=0.6)
        self.play(Write(inv_title), run_time=0.8)

        inv_def = VGroup(
            Text("Given a circle with center O and radius r,", font_size=22),
            Text("the inverse of a point z is the point z* such that", font_size=22),
        ).arrange(DOWN, buff=0.2).next_to(inv_title, DOWN, buff=0.5)

        inv_formula = MathTex(
            r"z^* = O + \frac{r^2}{\overline{z - O}}",
            font_size=36
        ).next_to(inv_def, DOWN, buff=0.5)

        inv_props = VGroup(
            Text("Key properties:", font_size=22, weight=BOLD, color=YELLOW_D),
            MathTex(r"\bullet \text{ Maps circles and lines (clines) to clines}",
                    font_size=22),
            MathTex(r"\bullet \text{ Preserves tangency (touch points)}",
                    font_size=22),
            MathTex(r"\bullet \text{ Circles through } O \text{ become lines}",
                    font_size=22),
            MathTex(r"\bullet \text{ It is an involution: } (z^*)^* = z",
                    font_size=22),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).next_to(inv_formula, DOWN, buff=0.5)

        self.play(FadeIn(inv_def), run_time=1)
        self.play(Write(inv_formula), run_time=1)
        self.wait(1)
        for prop in inv_props:
            self.play(FadeIn(prop), run_time=0.6)
            self.wait(0.3)
        self.wait(3)

        self.play(
            FadeOut(inv_title), FadeOut(inv_def),
            FadeOut(inv_formula), FadeOut(inv_props),
            run_time=0.8
        )

        # Bring title back
        title_sm = Text("Apollonius' Theorem — Proof",
                        font_size=28, weight=BOLD).to_edge(UP)
        self.play(FadeIn(title_sm))

        # ============================================================
        # REMARK: external tangency
        # ============================================================
        remark = VGroup(
            Text("We consider the case where no circle", font_size=24),
            Text("contains the other two (external tangency).", font_size=24),
        ).arrange(DOWN, buff=0.2).move_to(ORIGIN)
        self.play(FadeIn(remark), run_time=1)
        self.wait(2.5)
        self.play(FadeOut(remark))

        # ============================================================
        # STEP 1: Three tangent circles
        # ============================================================
        cur_sub = sub("Consider three mutually externally tangent circles")

        cA = Circle(radius=d['r1']*s, color=A_COLOR, stroke_width=3).move_to(cpos(d['c1']))
        cB = Circle(radius=d['r2']*s, color=B_COLOR, stroke_width=3).move_to(cpos(d['c2']))
        cC = Circle(radius=d['r3']*s, color=C_COLOR, stroke_width=3).move_to(cpos(d['c3']))
        circles = VGroup(cA, cB, cC)

        self.play(Create(cA), Create(cB), Create(cC), run_time=1.5)
        self.wait(0.8)

        # Mark tangent point P
        p_screen = cpos(d['P'])
        p_dot = Dot(p_screen, color=WHITE, radius=0.08)
        p_label = MathTex("P", font_size=28).next_to(p_dot, DOWN, buff=0.12)

        cur_sub = sub("Choose a tangent point P where two circles touch", cur_sub)
        self.play(FadeIn(p_dot), FadeIn(p_label))
        self.wait(1)

        # ============================================================
        # STEP 2: Translate P → origin
        # ============================================================
        cur_sub = sub(
            "Step 1.  Translate P to the origin — tangency is unchanged",
            cur_sub
        )

        ghosts_orig = VGroup(
            cA.copy().set_stroke(opacity=GHOST),
            cB.copy().set_stroke(opacity=GHOST),
            cC.copy().set_stroke(opacity=GHOST),
        )
        self.add(ghosts_orig)

        # Shift so P goes to screen origin
        shift_vec = -p_screen
        self.play(
            circles.animate.shift(shift_vec),
            p_dot.animate.shift(shift_vec),
            p_label.animate.shift(shift_vec),
            run_time=1.5
        )
        self.wait(0.3)

        # Draw axes
        axes_group = VGroup(
            Line(LEFT*4.5, RIGHT*4.5, color=WHITE, stroke_width=1, stroke_opacity=0.3),
            Line(DOWN*3.5, UP*3.5, color=WHITE, stroke_width=1, stroke_opacity=0.3),
        )
        ox_lab = MathTex("x", font_size=20, color=GREY_B).next_to(axes_group[0], RIGHT, buff=0.1)
        oy_lab = MathTex("y", font_size=20, color=GREY_B).next_to(axes_group[1], UP, buff=0.1)
        o_lab = MathTex("0", font_size=20, color=WHITE).next_to(ORIGIN, DL, buff=0.1)

        self.play(
            Create(axes_group), FadeIn(ox_lab), FadeIn(oy_lab), FadeIn(o_lab),
            FadeOut(p_label),
            run_time=0.8
        )

        cur_sub = sub(
            "Call them A, B, C.   Note: A and B now pass through the origin",
            cur_sub
        )

        lA = MathTex("A", font_size=30, color=A_COLOR).move_to(cA.get_center())
        lB = MathTex("B", font_size=30, color=B_COLOR).move_to(cB.get_center())
        lC = MathTex("C", font_size=30, color=C_COLOR).move_to(cC.get_center())
        labels = VGroup(lA, lB, lC)

        self.play(FadeIn(labels))
        self.wait(1.5)

        # ============================================================
        # STEP 3: Inversion
        # ============================================================
        cur_sub = sub(
            "Step 2.  Invert A, B, C in the unit circle",
            cur_sub
        )

        inv_circle = Circle(radius=s, color=INV_COLOR, stroke_width=2,
                            stroke_opacity=0.4).move_to(ORIGIN)
        inv_lbl = MathTex("|z|=1", font_size=22, color=INV_COLOR)
        inv_lbl.next_to(inv_circle, UR, buff=-0.2)
        self.play(Create(inv_circle), FadeIn(inv_lbl))
        self.wait(2)

        ghosts_trans = VGroup(
            cA.copy().set_stroke(opacity=GHOST),
            cB.copy().set_stroke(opacity=GHOST),
            cC.copy().set_stroke(opacity=GHOST),
        )
        self.add(ghosts_trans)

        # Inverted objects: two lines + circle
        xl1, xl2 = d['x_l1'] * s, d['x_l2'] * s
        lineA = Line(np.array([xl1, -3.5, 0]), np.array([xl1, 3.5, 0]),
                     color=A_COLOR, stroke_width=3)
        lineB = Line(np.array([xl2, -3.5, 0]), np.array([xl2, 3.5, 0]),
                     color=B_COLOR, stroke_width=3)

        C3i = d['C3i']
        cC_inv = Circle(radius=C3i.radius*s, color=C_COLOR, stroke_width=3)
        cC_inv.move_to(np.array([C3i.center.real*s, C3i.center.imag*s, 0]))

        lAp = MathTex("A'", font_size=26, color=A_COLOR)
        lAp.next_to(lineA, LEFT, buff=0.08).shift(DOWN*1.5)
        lBp = MathTex("B'", font_size=26, color=B_COLOR)
        lBp.next_to(lineB, RIGHT, buff=0.08).shift(DOWN*1.5)
        lCp = MathTex("C'", font_size=26, color=C_COLOR)
        lCp.next_to(cC_inv, RIGHT, buff=0.15)

        cur_sub = sub(
            "A and B pass through 0  →  they become lines A' and B'",
            cur_sub
        )

        self.play(
            ReplacementTransform(cA, lineA),
            ReplacementTransform(cB, lineB),
            ReplacementTransform(cC, cC_inv),
            FadeOut(labels), FadeOut(p_dot),
            FadeOut(inv_circle), FadeOut(inv_lbl),
            run_time=3
        )
        self.play(FadeIn(lAp), FadeIn(lBp), FadeIn(lCp))
        self.wait(2)

        cur_sub = sub(
            "A and B were tangent at 0  →  A' and B' are parallel.   C becomes circle C'",
            cur_sub
        )
        self.wait(3)

        cur_sub = sub(
            "Inversion preserves tangency  →  C' is tangent to both lines A' and B'",
            cur_sub
        )
        self.wait(3)

        # ============================================================
        # STEP 4: Construct solution circles
        # ============================================================
        cur_sub = sub(
            "Step 3.  Two parallel lines and a tangent circle between them",
            cur_sub
        )
        self.wait(2)

        r_sol_s = d['r_sol'] * s
        sol1_inv = Circle(radius=r_sol_s, color=SOL_1, stroke_width=4)
        sol1_inv.move_to(np.array([d['sol1i_c'].real*s, d['sol1i_c'].imag*s, 0]))
        sol2_inv = Circle(radius=r_sol_s, color=SOL_2, stroke_width=4)
        sol2_inv.move_to(np.array([d['sol2i_c'].real*s, d['sol2i_c'].imag*s, 0]))

        cur_sub = sub(
            "There exist exactly two circles tangent to all three — one above, one below",
            cur_sub
        )
        self.play(Create(sol1_inv), run_time=1.5)
        self.play(Create(sol2_inv), run_time=1.5)
        self.wait(3)

        # ============================================================
        # STEP 5: Invert back + translate
        # ============================================================
        cur_sub = sub(
            "Step 4.  Invert back and translate — tangency is preserved throughout",
            cur_sub
        )
        self.wait(1.5)

        cA_f = Circle(radius=d['r1']*s, color=A_COLOR, stroke_width=2.5).move_to(cpos(d['c1']))
        cB_f = Circle(radius=d['r2']*s, color=B_COLOR, stroke_width=2.5).move_to(cpos(d['c2']))
        cC_f = Circle(radius=d['r3']*s, color=C_COLOR, stroke_width=2.5).move_to(cpos(d['c3']))
        sol1_f = Circle(radius=d['sol1_r']*s, color=SOL_1, stroke_width=4).move_to(cpos(d['sol1_c']))
        sol2_f = Circle(radius=d['sol2_r']*s, color=SOL_2, stroke_width=4).move_to(cpos(d['sol2_c']))

        lA_f = MathTex("A", font_size=28, color=A_COLOR).move_to(cA_f)
        lB_f = MathTex("B", font_size=28, color=B_COLOR).move_to(cB_f)
        lC_f = MathTex("C", font_size=28, color=C_COLOR).move_to(cC_f)

        self.play(
            ReplacementTransform(lineA, cA_f),
            ReplacementTransform(lineB, cB_f),
            ReplacementTransform(cC_inv, cC_f),
            ReplacementTransform(sol1_inv, sol1_f),
            ReplacementTransform(sol2_inv, sol2_f),
            FadeOut(lAp), FadeOut(lBp), FadeOut(lCp),
            FadeOut(ghosts_orig), FadeOut(ghosts_trans),
            FadeOut(axes_group), FadeOut(ox_lab), FadeOut(oy_lab), FadeOut(o_lab),
            run_time=2.5
        )
        self.play(FadeIn(lA_f), FadeIn(lB_f), FadeIn(lC_f))
        self.wait(1)

        # ============================================================
        # FINALE
        # ============================================================
        self.play(FadeOut(cur_sub), FadeOut(title_sm))

        final_group = VGroup(cA_f, cB_f, cC_f, sol1_f, sol2_f, lA_f, lB_f, lC_f)
        self.play(final_group.animate.scale(0.7).shift(DOWN * 0.5), run_time=1)

        final_title = Text("Apollonius' Theorem", font_size=40, weight=BOLD)
        final_title.to_edge(UP, buff=0.4)
        final_stmt = VGroup(
            Text("Given three mutually tangent circles,", font_size=26),
            Text("there exist exactly two circles tangent to all three.  ∎",
                 font_size=26, weight=BOLD),
        ).arrange(DOWN, buff=0.15).next_to(final_title, DOWN, buff=0.3)

        self.play(Write(final_title), run_time=1)
        self.play(FadeIn(final_stmt), run_time=1)
        self.wait(3)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1.5)

        # ============================================================
        # CREDITS
        # ============================================================
        credits = VGroup(
            Text("Veliko Donchev", font_size=36, weight=BOLD),
            Text("2025–2026", font_size=24, color=GREY_B),
            Text("Built with mathcline and Manim", font_size=20, color=GREY_C),
        ).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        self.play(FadeIn(credits), run_time=1.5)
        self.wait(3)
        self.play(FadeOut(credits), run_time=1.5)
