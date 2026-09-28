def _clamp_int(x, lo, hi):
    return max(lo, min(hi, int(x)))

class I2CDriver:
    CMD_PICKUP = 1
    CMD_DROPOFF = 2

    def __init__(self, bus_num=1, addr=0x08):
        from smbus2 import SMBus, i2c_msg
        self._i2c_msg = i2c_msg
        self.addr = addr
        self.bus = SMBus(bus_num)

    @staticmethod
    def _to_int16_bytes(v):
        v &= 0xFFFF
        return (v >> 8) & 0xFF, v & 0xFF

    def send(self, left_pwm, right_pwm):
        left_pwm = _clamp_int(left_pwm, -255, 255)
        right_pwm = _clamp_int(right_pwm, -255, 255)
        l_hi, l_lo = self._to_int16_bytes(left_pwm)
        r_hi, r_lo = self._to_int16_bytes(right_pwm)
        msg = self._i2c_msg.write(self.addr, [l_hi, l_lo, r_hi, r_lo])
        self.bus.i2c_rdwr(msg)

    def stop(self):
        self.send(0, 0)

    def _send_cmd(self, cmd):
        msg = self._i2c_msg.write(self.addr, [_clamp_int(cmd, 0, 255)])
        self.bus.i2c_rdwr(msg)

    def send_pickup(self):
        self._send_cmd(self.CMD_PICKUP)

    def send_dropoff(self):
        self._send_cmd(self.CMD_DROPOFF)

    def close(self):
        try:
            self.bus.close()
        except Exception:
            pass
