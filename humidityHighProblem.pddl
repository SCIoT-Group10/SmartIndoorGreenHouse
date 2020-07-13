(define (problem humidityHighProblem) (:domain GreenHouse)

(:init
    (humidityHigh)
    (windowClosed)
)

(:goal (and
    (humidityLow)
))
)