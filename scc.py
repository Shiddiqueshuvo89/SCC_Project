
import time

class SCC:
    def __init__(self):
        self.pv_power = 0               # [W]
        self.light_level = 0            # [W]
        self.heatpump_level = 0         # [W]
        self.battery_voltage = 50.0     # [V]
        self.battery_temp = 25.0        # [°C]
        self.last_voltage_under_54_4 = False
        self.last_update = time.time()

    def _check_timing(self):
        now = time.time()
        if now - self.last_update > 0.1:
            print("Warning: Update took longer than 100 ms")
        self.last_update = now

    def set_PV(self, value):
        self.pv_power = value
        self._check_timing()

    def set_LightLevel(self, value):
        self.light_level = value
        self._check_timing()

    def set_HeatpumpLevel(self, value):
        self.heatpump_level = value
        self._check_timing()

    def set_BatVoltage(self, value):
        if value < 54.4:
            self.last_voltage_under_54_4 = True
        self.battery_voltage = value
        self._check_timing()

    def set_BatTemp(self, value):
        self.battery_temp = value
        self._check_timing()

    def suggest(self):
        injectors = {}

        can_charge = (
            0 <= self.battery_temp <= 45 and
            self.battery_voltage < 55.1 and
            (not self.last_voltage_under_54_4 or self.battery_voltage >= 51.0)
        )

        can_discharge = (
            -25 <= self.battery_temp <= 65 and
            self.battery_voltage > 47.0
        )

        net_power = self.pv_power - self.light_level - self.heatpump_level

        injectors['HPInjector'] = True
        injectors['LightInjector1'] = True
        injectors['LightInjector2'] = True

        injectors['HP'] = min(400, max(0, self.heatpump_level))
        injectors['Light'] = min(1800, max(0, self.light_level))

        if net_power > 0 and can_charge:
            injectors['BAT'] = min(3000, net_power)
        elif net_power < 0 and can_discharge:
            injectors['BAT'] = max(0, net_power + 3000)
        else:
            injectors['BAT'] = 0

        injectors['BATHEAT'] = self.battery_temp < 5

        return injectors
