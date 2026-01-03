(define (domain npuzzle_domain)
  (:requirements :adl)
  (:types tile pos - object)
  (:predicates
    (at ?t - tile ?p - pos)
    (empty ?p - pos)
    (adj ?from - pos ?to - pos))
  (:action slide
    :parameters (?t - tile ?from - pos ?to - pos)
    :precondition (and (at ?t ?from) (empty ?to) (adj ?from ?to))
    :effect (and (not(at ?t ?from)) (at ?t ?to) (empty ?from) (not(empty ?to)) )))
