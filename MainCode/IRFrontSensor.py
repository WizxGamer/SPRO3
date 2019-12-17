import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

GPIO.setwarnings(False)
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(0, 0))

if __name__ == "__main__":
    time.sleep(0.1)
    print(mcp.read_adc(3))