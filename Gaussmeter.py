
    
    
import serial
from tango import AttrWriteType, DevState, DeviceProxy, DispLevel, Attr
from tango.server import Device, attribute, command, device_property


class Gaussmeter(Device):

    '''
    Gaussmeter MAGSYS HGM09s
    
    This controls the Thorlabs SC10 shutter controller
    '''

    Port = device_property(dtype=str, default_value="/dev/ttyGaussmeter")
    Baudrate = device_property(dtype=int, default_value=9600)
    Timeout = device_property(dtype=float, default_value=1)
    
    field = attribute(
        dtype='float',
        format='%.5f',
        label='Field',
        access=AttrWriteType.READ,
        display_level=DispLevel.OPERATOR,
        unit='mT',
        doc='Magnetic field'
    )
    

    def init_device(self):
        Device.init_device(self)
        # Initialize serial port
        try:
            self.ser = serial.Serial()
            self.ser.port = self.Port
            self.ser.baudrate = self.Baudrate
            self.ser.bytesize = serial.EIGHTBITS
            self.ser.parity = serial.PARITY_NONE
            self.ser.stopbits = serial.STOPBITS_ONE
            self.ser.timeout = self.Timeout
            self.open_communication()
            self.set_state(DevState.ON)
        except:
            self.error_stream('Cannot Connect')
            self.set_state(DevState.OFF)
    
    def open_communication(self):
        # Open serial communication with the gaussmeter
        self.ser.open()
        
    def close_communication(self):
        # Close serial communication with the gaussmeter
        self.ser.close()
            
    def delete_device(self):
        self.close_communication()
        self.set_state(DevState.OFF)
        super().delete_device()
        
    def read_field(self):
        # Return the current field value
        command = ":MEAS?\r"
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(command.encode())
        result = self.ser.readline().decode().rstrip('\n')
        return float(result)


    %@command
    %def test(self):
    %    # Print a confirmation to the console
    %    print("Gaussmeter module is working")

    %@attribute(dtype=float, access=AttrWriteType.READ, label="Field", unit="T", display_level=DispLevel.OPERATOR)
    %def field(self):
    %    # Attribute for the current field value
    %    return self.read_field()

    %@attribute(dtype=str, access=AttrWriteType.READ, label="Device Model")
    %def device_model(self):
    %    return "MAGSYS HGM09s"

    %@attribute(dtype=str, access=AttrWriteType.READ, label="Manufacturer")
    %def manufacturer(self):
    %    return "MAGSYS Magnet Systeme GmbH"


if __name__ == "__main__":
    # Start the device server
    Gaussmeter.run_server()
    