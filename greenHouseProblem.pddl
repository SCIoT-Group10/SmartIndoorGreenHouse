(define (problem greenHouseProblem) (:domain GreenHouse)

(:init
    (brightnessLow)
    (moistureLow)
    (humidityHigh)
    (temperatureHigh)
    (windowClosed)
    (pumpOff)
    (lightsOff)
    (waterHigh)
    (day)
)

(:goal (and
    (brightnessHigh)
    (moistureHigh)
    (temperatureLow)
))

;un-comment the following line if metric is needed
;(:metric minimize (???))
)
