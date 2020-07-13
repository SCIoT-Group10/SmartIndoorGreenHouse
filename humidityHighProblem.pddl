(define (problem humidityHighProblem) (:domain GreenHouse)

(:init
    (humidityHigh)
    (windowClosed)
    (day)
)

(:goal (and
    (humidityLow)
))
)