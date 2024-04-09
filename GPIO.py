from machine import Pin
import time

class Sound_Sensor():
    def __init__(self, max_level, min_level, time_on  = 1e-5):
        self.max_level = max_level
        self.min_level = min_level
        self.trigger = Pin(12, Pin.OUT)
        self.echo = Pin(14, Pin.IN)
        self.time_on = time_on
        self.trigger.value(0)
        self.input_led_valve = Pin(15, Pin.OUT)
        self.output_led_valve = Pin(2, Pin.OUT)
        self.button_start_filling = Pin(19, Pin.IN, pull = Pin.PULL_UP)
        self.button_start_draining = Pin(18, Pin.IN, pull = Pin.PULL_UP) 
        self.button_stop = Pin(5, Pin.IN, pull = Pin.PULL_UP)
        self.button_start_filling.irq(handler = self.start_filling, trigger = Pin.IRQ_FALLING)
        self.button_start_draining.irq(handler = self.start_draining, trigger = Pin.IRQ_FALLING)
        self.button_stop.irq(handler = self.stop, trigger = Pin.IRQ_FALLING)
        self.distance = 0
        self.flag1 = False
        self.flag2 = False
        
    def trigger_on(self):
        self.trigger.value(1)
        time.sleep(self.time_on)
        self.trigger.value(0)
        
    def echo_on(self):
        while self.echo.value() == 0:
            pass
        start = time.ticks_us()
        while self.echo.value() == 1:
            pass
        stop = time.ticks_us()
        time_diff = stop - start
        
        self.distance = 0.0184 * time_diff - 0.2132
        print("Tiempo",time_diff)
        print(self.distance)
        
        
    def start_filling(self, pin):
        if self.button_start_filling.value() == 0 and self.flag2 != True:
            self.input_led_valve.value(1)
            self.flag1 = True
            
            
    def start_draining(self, pin):
       if self.button_start_draining.value() == 0 and self.flag1 != True:
            self.output_led_valve.value(1)
            self.flag2 = True
            
    def stop(self, pin):
        self.output_led_valve.value(0)
        self.input_led_valve.value(0)
        self.flag1 = False
        self.flag2 = False
    def meassure(self):
        while True:
            self.trigger_on()
            self.echo_on() 
            if self.distance >= self.max_level:
                self.input_led_valve.value(0)
            if self.distance <= self.min_level:
                self.output_led_valve.value(0)
                
            time.sleep(1)
            
                
                
            
        
        
    
        
    
        
if __name__ == "__main__":
    ss = Sound_Sensor(10,3)
    ss.meassure()
