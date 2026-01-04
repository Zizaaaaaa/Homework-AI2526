(define (problem npuzzle-4x4)
  (:domain npuzzle_domain)

  (:objects
    t1 t2 t3 t4 t5 t6 t7 t8 t9 t10 t11 t12 t13 t14 t15 - tile
    p0_0 p0_1 p0_2 p0_3 p1_0 p1_1 p1_2 p1_3 p2_0 p2_1 p2_2 p2_3 p3_0 p3_1 p3_2 p3_3 - pos
  )

  (:init
    (adj p0_0 p1_0) (adj p0_0 p0_1) (adj p0_1 p1_1) (adj p0_1 p0_0) (adj p0_1 p0_2) (adj p0_2 p1_2) (adj p0_2 p0_1) (adj p0_2 p0_3) (adj p0_3 p1_3) (adj p0_3 p0_2) (adj p1_0 p0_0) (adj p1_0 p2_0) (adj p1_0 p1_1) (adj p1_1 p0_1) (adj p1_1 p2_1) (adj p1_1 p1_0) (adj p1_1 p1_2) (adj p1_2 p0_2) (adj p1_2 p2_2) (adj p1_2 p1_1) (adj p1_2 p1_3) (adj p1_3 p0_3) (adj p1_3 p2_3) (adj p1_3 p1_2) (adj p2_0 p1_0) (adj p2_0 p3_0) (adj p2_0 p2_1) (adj p2_1 p1_1) (adj p2_1 p3_1) (adj p2_1 p2_0) (adj p2_1 p2_2) (adj p2_2 p1_2) (adj p2_2 p3_2) (adj p2_2 p2_1) (adj p2_2 p2_3) (adj p2_3 p1_3) (adj p2_3 p3_3) (adj p2_3 p2_2) (adj p3_0 p2_0) (adj p3_0 p3_1) (adj p3_1 p2_1) (adj p3_1 p3_0) (adj p3_1 p3_2) (adj p3_2 p2_2) (adj p3_2 p3_1) (adj p3_2 p3_3) (adj p3_3 p2_3) (adj p3_3 p3_2)
    (at t1 p0_0) (at t2 p0_1) (at t3 p0_2) (at t4 p0_3) (at t5 p1_0) (at t6 p1_1) (at t7 p1_2) (empty p1_3) (at t8 p2_0) (at t9 p2_1) (at t10 p2_2) (at t11 p2_3) (at t12 p3_0) (at t13 p3_1) (at t14 p3_2) (at t15 p3_3)
  )

  (:goal (and
    (at t1 p0_0) (at t2 p0_1) (at t3 p0_2) (at t4 p0_3) (at t5 p1_0) (at t6 p1_1) (at t7 p1_2) (at t8 p1_3) (at t9 p2_0) (at t10 p2_1) (at t11 p2_2) (at t12 p2_3) (at t13 p3_0) (at t14 p3_1) (at t15 p3_2) (empty p3_3)
  ))
)
