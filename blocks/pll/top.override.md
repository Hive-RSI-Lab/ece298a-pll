# top.override.json

The top harden's own config override (check_top_harden takes it in place
of digital/harden/config.override.json). It excludes small and delay
buffers from the tile harden. As of 2026-11-13, buf_4 is no longer
excluded. Everything else is unchanged.

**Why buf_4 is allowed.** In the tile harden, post-placement repair
(OpenROAD.RepairDesignPostGPL) never finished. A nor4_1 next to the macro
drove a net that broke the slew limit. The only buffer repair could add
was buf_8, and the nor4_1 can't drive a buf_8 input within slew. So every
split failed the same way, and the recursion ran until it ran out of
memory. Allowing buf_4 alone fixes it, checked on the real step state.

**Why the rest stays excluded.** buf_1..3, clkbuf_1..4 and the dly* cells
stay out. The repeater between u_pfd_up_obuf and the macro pin
u_analog/pfd_up was once sized as buf_2/buf_3/dlya_2, and it failed the
0.5 ns macro-pin slew at ss_125C (up to 1.0 ns). See board post
110406577c1c, thread h0-pll, 2026-11-04. buf_2 was not needed here. Don't
add it back without the same reason, and don't take buf_4 out again
without fixing the repair loop another way.

The macro-pin slew on pfd_up and pfd_dn is still checked at ss_125C by
signoff STA and the slew gate.
