(define (problem humidityLowProblem) (:domain GreenHouse)

(:init
    (humidityLow)
    (windowOpen)
    (day)
)

(:goal (and
    (humidityHigh)
))
)