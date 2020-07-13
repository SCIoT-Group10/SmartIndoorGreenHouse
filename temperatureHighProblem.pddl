(define (problem temperatureHighProblem) (:domain GreenHouse)

(:init
    (temperatureHigh)
    (windowClosed)
    (day)
)

(:goal (and
    (temperatureLow)
))
)