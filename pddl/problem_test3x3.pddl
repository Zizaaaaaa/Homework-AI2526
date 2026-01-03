(define (problem npuzzle_problem)
  (:domain npuzzle_domain)
  (:objects
    t1 t2 t3 t4 t5 t6 t7 t8 - tile
    p1 p2 p3 p4 p5 p6 p7 p8 p9 - pos)
  (:init
    (adj p1 p2) (adj p2 p1)
    (adj p2 p3) (adj p3 p2)
    (adj p4 p5) (adj p5 p4)
    (adj p5 p6) (adj p6 p5)
    (adj p7 p8) (adj p8 p7)
    (adj p8 p9) (adj p9 p8)
    (adj p1 p4) (adj p4 p1)
    (adj p2 p5) (adj p5 p2)
    (adj p3 p6) (adj p6 p3)
    (adj p4 p7) (adj p7 p4)
    (adj p5 p8) (adj p8 p5)
    (adj p6 p9) (adj p9 p6)
    (at t1 p1) (at t2 p2) (at t3 p3)
    (at t4 p4) (at t5 p5) (at t6 p6)
    (at t7 p7) (at t8 p9)
    (empty p8))
  (:goal
    (and
      (at t1 p1) (at t2 p2) (at t3 p3)
      (at t4 p4) (at t5 p5) (at t6 p6)
      (at t7 p7) (at t8 p8)
      (empty p9))))
