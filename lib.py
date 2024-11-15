from DfrobotGP8403 import *
import utime

def store():
      DAC.store()

def wave():
      vmax = DAC.get_dac_out_range()
      for i in range(10):
          for x in range(vmax+1):
              DAC.set_dac_out_voltage(x*1000,0)
              DAC.set_dac_out_voltage((vmax-x)*1000,1)
              utime.sleep(0.25)

          for x in reversed(range(vmax+1)):
              DAC.set_dac_out_voltage(x*1000,0)
              DAC.set_dac_out_voltage((vmax-x)*1000,1)
              utime.sleep(0.25)

if __name__ == "__main__":   
      DAC = DfrobotGP8403 (0x58, 5, 4, 400000, True)

while DAC.begin() != 0:
      print("Init error")
      utime.sleep(1)
      
print("Init succeed")
DAC.set_dac_out_range(OUTPUT_RANGE_10V)
DAC.set_dac_out_voltage(0,0)
DAC.set_dac_out_voltage(0,1)

# Example usage
if __name__ == "__main__":
    # Configuration
    I2C_ADDR = 0x58  # Default I2C address for GP8403
    I2C_FREQ = 100000  # 100kHz
    SCL_PIN = 5  # Change to your SCL pin
    SDA_PIN = 4  # Change to your SDA pin
    
    # Initialize DAC
    dac = DfrobotGP8403(I2C_ADDR, SCL_PIN, SDA_PIN, I2C_FREQ)
    
    # Begin communication
    if dac.begin() != 0:
        print("DAC initialization failed!")
    else:
        # Set output range to 5V
        dac.set_dac_out_range(OUTPUT_RANGE_5V)
        
        # Set output voltage to 2.5V (2500mV)
        dac.set_dac_out_voltage(2000, CHANNEL0)
        
        # Store settings to DAC (will retain after power cycle)
        dac.store()
        
