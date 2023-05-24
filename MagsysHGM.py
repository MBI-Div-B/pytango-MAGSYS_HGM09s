#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of the MagsysHGM project
#
#
#
# Distributed under the terms of the MIT license.
# See LICENSE.txt for more info.

""" pytango-MagsysHGM

Control and read Magsys HGM09s Gaussmeter. 
Device implements a serial adapter via USB and is controlled 
using VISA commands.
"""

# PyTango imports
import tango
from tango import DebugIt
from tango.server import run
from tango.server import Device
from tango.server import attribute, command
from tango.server import device_property
from tango import AttrQuality, DispLevel, DevState
from tango import AttrWriteType, PipeWriteType
import enum
# Additional import
# PROTECTED REGION ID(MagsysHGM.additionnal_import) ENABLED START #
import sys
import pyvisa
# PROTECTED REGION END #    //  MagsysHGM.additionnal_import

__all__ = ["MagsysHGM", "main"]


class Unit(enum.IntEnum):
    """Python enumerated type for Unit attribute."""
    TESL = 0
    APM = 1
    GAUS = 2
    OE = 3


class Mode(enum.IntEnum):
    """Python enumerated type for Mode attribute."""
    DC = 0
    AC = 1


class MagsysHGM(Device):
    """
    Control and read Magsys HGM09s Gaussmeter. 
    Device implements a serial adapter via USB and is controlled 
    using VISA commands.

    **Properties:**

    - Device Property
        visa_address
            - Type:'DevString'
    """
    # PROTECTED REGION ID(MagsysHGM.class_variable) ENABLED START #
    # PROTECTED REGION END #    //  MagsysHGM.class_variable

    # -----------------
    # Device Properties
    # -----------------

    visa_address = device_property(
        dtype='DevString',
        default_value="ASRL/dev/ttyUSB0"
    )

    # ----------
    # Attributes
    # ----------

    field = attribute(
        dtype='DevDouble',
        format='8.5e',
    )

    unit = attribute(
        dtype=Unit,
    )

    measrange = attribute(
        dtype='DevLong',
    )

    mode = attribute(
        dtype=Mode,
    )

    # ---------------
    # General methods
    # ---------------

    def init_device(self):
        """Initialises the attributes and properties of the MagsysHGM."""
        Device.init_device(self)
        # PROTECTED REGION ID(MagsysHGM.init_device) ENABLED START #
        self._field = 0.0
        self._unit = 0
        self._range = 0
        self._mode = Mode.DC
        self.rm = pyvisa.ResourceManager("@py")
        self.inst = self.rm.open_resource(self.visa_address)
        self.inst.read_termination = '\n\r'
        try:
            idn = self.inst.query("*IDN?")
            self.info_stream(f"Connected to {idn}")
            self.set_state(DevState.ON)
        except Exception as ex:
            self.error_stream(ex)
            sys.exit(255)

        # PROTECTED REGION END #    //  MagsysHGM.init_device

    def always_executed_hook(self):
        """Method always executed before any TANGO command is executed."""
        # PROTECTED REGION ID(MagsysHGM.always_executed_hook) ENABLED START #
        # PROTECTED REGION END #    //  MagsysHGM.always_executed_hook

    def delete_device(self):
        """Hook to delete resources allocated in init_device.

        This method allows for any memory or other resources allocated in the
        init_device method to be released.  This method is called by the device
        destructor and by the device Init command.
        """
        # PROTECTED REGION ID(MagsysHGM.delete_device) ENABLED START #
        self.inst.close()
        # PROTECTED REGION END #    //  MagsysHGM.delete_device
    # ------------------
    # Attributes methods
    # ------------------

    def read_field(self):
        # PROTECTED REGION ID(MagsysHGM.field_read) ENABLED START #
        """Return the field attribute."""
        self._field = float(self.inst.query(":MEAS?"))
        return self._field
        # PROTECTED REGION END #    //  MagsysHGM.field_read

    def read_unit(self):
        # PROTECTED REGION ID(MagsysHGM.unit_read) ENABLED START #
        """Return the unit attribute."""
        self._unit = Unit[self.inst.query(":UNIT?")]
        return self._unit
        # PROTECTED REGION END #    //  MagsysHGM.unit_read

    def read_measrange(self):
        # PROTECTED REGION ID(MagsysHGM.range_read) ENABLED START #
        """Return the range attribute."""
        self._range = int(self.inst.query(":RANG?"))
        return self._range
        # PROTECTED REGION END #    //  MagsysHGM.range_read

    def read_mode(self):
        # PROTECTED REGION ID(MagsysHGM.mode_read) ENABLED START #
        """Return the mode attribute."""
        self._mode = Mode[self.inst.query(":MODE?")]
        return self._mode
        # PROTECTED REGION END #    //  MagsysHGM.mode_read

    # def write_mode(self, value):
    #     # PROTECTED REGION ID(MagsysHGM.mode_write) ENABLED START #
    #     """Set the mode attribute."""
    #     self.inst.write(":PAR:ACDC {value.name}")
    #     self.inst.write(":PAR:SAVE")
    #     # PROTECTED REGION END #    //  MagsysHGM.mode_write

    # --------
    # Commands
    # --------

    @command(
        dtype_in='DevLong',
    )
    @DebugIt()
    def set_range(self, argin):
        # PROTECTED REGION ID(MagsysHGM.set_range) ENABLED START #
        """

        :param argin: 'DevLong'

        :return:None
        """
        if (argin >= 0) and (argin <= 3):
            self.inst.write(f":PAR:RANG {argin})")
            self.inst.write(f":PAR:SAVE")
        else:
            self.error_stream("Measurement range argument out of range [0, 3]")
        # PROTECTED REGION END #    //  MagsysHGM.set_range

    @command(
        dtype_in='DevLong',
    )
    @DebugIt()
    def set_unit(self, argin):
        # PROTECTED REGION ID(MagsysHGM.set_unit) ENABLED START #
        """

        :param argin: 'DevEnum'

        :return:None
        """
        value = Unit(argin)
        self.inst.write(f":PAR:RANG {value.name}")
        self.inst.write(f":PAR:SAVE")
        # PROTECTED REGION END #    //  MagsysHGM.set_unit

# ----------
# Run server
# ----------


def main(args=None, **kwargs):
    """Main function of the MagsysHGM module."""
    # PROTECTED REGION ID(MagsysHGM.main) ENABLED START #
    return run((MagsysHGM,), args=args, **kwargs)
    # PROTECTED REGION END #    //  MagsysHGM.main


if __name__ == '__main__':
    main()
