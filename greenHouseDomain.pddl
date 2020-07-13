(define (domain GreenHouse)



    (:predicates
        (brightnessHigh)
        (brightnessLow)
        (moistureHigh)
        (moistureLow)
        (waterHigh)
        (waterLow)
        (temperatureHigh)
        (temperatureLow)
        (humidityHigh)
        (humidityLow)
        (day)
        (night)
        (pumpOn)
        (pumpOff)
        (lightsOn)
        (lightsOff)
        (windowOpen)
        (windowClosed)
    )


    (:action turnLightOff
        :precondition (and (brightnessHigh) (lightsOn) (not (lightsOff)))
        :effect (and (not(lightsOn)) (lightsOff) (brightnessLow) (not(brightnessHigh)))
    )
    
    (:action turnLightOn
        :precondition (and (brightnessLow) (lightsOff) (not(lightsOn)) (day))
        :effect (and (lightsOn) (not(lightsOff)) (brightnessHigh) (not(brightnessLow)))
    )
    
    (:action waterPlants
        :precondition (and (moistureLow) (waterHigh) (pumpOff) (not(pumpOn)) (day))
        :effect (and (moistureHigh) (not(moistureLow)) (pumpOn) (not(pumpOff)))
    )
    
    (:action stopWaterPlantsMoisture
        :precondition (and (moistureHigh) (pumpOn) (not(pumpOff)))
        :effect (and (pumpOff) (not(pumpOn)) (not(moistureHigh)) (moistureLow))
    )
    
    (:action stopWaterPlantsEmptyTank
        :precondition (and (waterLow) (pumpOn) (not(pumpOff)))
        :effect (and (pumpOff) (not(pumpOn)) (not(waterLow)) (waterHigh))
    )
    
    (:action getTemperatureDown
        :precondition (and (temperatureHigh) (windowClosed) (not(windowOpen)) (day))
        :effect (and (temperatureLow) (not(temperatureHigh)) (windowOpen) (not(windowClosed)))
    )
    
    (:action getTemperatureUp
        :precondition (and (temperatureLow) (windowOpen) (not(windowClosed)))
        :effect (and (temperatureHigh) (not(temperatureLow)) (windowClosed) (not(windowOpen)))
    )
    
    (:action getHumidityDown
        :precondition (and (humidityHigh) (windowClosed) (not(windowOpen)))
        :effect (and (humidityLow) (not(humidityHigh)) (windowOpen) (not(windowClosed)))
    )
    
    (:action getHumidityUp
        :precondition (and (humidityLow) (windowOpen) (not(windowClosed)) (day))
        :effect (and (humidityHigh) (not(humidityLow)) (windowClosed) (not(windowOpen)))
    )
    
    (:action turnOffAtNight
        :precondition (and (night))
        :effect (and  (windowClosed) (not(windowOpen))
        (pumpOff) (not(pumpOn))
        (not(lightsOn)) (lightsOff)
        )
    )
    
)