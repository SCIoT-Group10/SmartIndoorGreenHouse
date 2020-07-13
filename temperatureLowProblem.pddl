(define (problem temperatureLowProblem) (:domain GreenHouse)

(:init
    (temperatureLow)
    (windowOpen)
    (day)
)

(:goal (and
    (temperatureHigh)
))
)