(define (problem temperatureHighProblem) (:domain GreenHouse)

(:init
    (temperatureHigh)
    (windowClosed)
)

(:goal (and
    (temperatureLow)
))
)