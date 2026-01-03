(define (problem npuzzle-3x3)
  (:domain npuzzle_domain)

  (:objects
    t1 t2 t3 t4 t5 t6 t7 t8 - tile
    p0_0 p0_1 p0_2 p1_0 p1_1 p1_2 p2_0 p2_1 p2_2 - pos
  )

  (:init
    (adj p0_0 p1_0) (adj p0_0 p0_1) (adj p0_1 p1_1) (adj p0_1 p0_0) (adj p0_1 p0_2) (adj p0_2 p1_2) (adj p0_2 p0_1) (adj p1_0 p0_0) (adj p1_0 p2_0) (adj p1_0 p1_1) (adj p1_1 p0_1) (adj p1_1 p2_1) (adj p1_1 p1_0) (adj p1_1 p1_2) (adj p1_2 p0_2) (adj p1_2 p2_2) (adj p1_2 p1_1) (adj p2_0 p1_0) (adj p2_0 p2_1) (adj p2_1 p1_1) (adj p2_1 p2_0) (adj p2_1 p2_2) (adj p2_2 p1_2) (adj p2_2 p2_1)
    (at t1 p0_0) (at t2 p0_1) (at t3 p0_2) (at t4 p1_0) (at t5 p1_1) (at t6 p1_2) (at t7 p2_0) (empty p2_1) (at t8 p2_2)
  )

  (:goal (and
    (at t1 p0_0) (at t2 p0_1) (at t3 p0_2) (at t4 p1_0) (at t5 p1_1) (at t6 p1_2) (at t7 p2_0) (at t8 p2_1) (empty p2_2)
  ))
)
