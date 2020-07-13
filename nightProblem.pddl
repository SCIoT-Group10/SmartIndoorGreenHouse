(define (problem nightProblem) (:domain GreenHouse)

(:init
    (night)
    (pumpOn)
    (lightsOn)
    (windowOpen)
)

(:goal (and
    (pumpOff)
    (lightsOff)
    (windowClosed)
))
)