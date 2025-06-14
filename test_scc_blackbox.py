import unittest
from scc import SCC  # Ensure you have SCC defined in scc.py

class TestSCCBlackBox(unittest.TestCase):
    def setUp(self):
        self.scc = SCC()

    #   Should PASS – Standard charging within range
    def test_valid_charge(self):
        self.scc.set_PV(1500)
        self.scc.set_BatVoltage(52.0)
        self.scc.set_BatTemp(25)
        self.assertGreater(self.scc.suggest()['BAT'], 0)

    #   Should PASS – Standard discharging case
    def test_valid_discharge(self):
        self.scc.set_PV(0)
        self.scc.set_LightLevel(1000)
        self.scc.set_HeatpumpLevel(300)
        self.scc.set_BatVoltage(52.0)
        self.scc.set_BatTemp(20)
        self.assertGreaterEqual(self.scc.suggest()['BAT'], 0)

    #   Should PASS – Charging at low temperature boundary
    def test_charge_at_temp_boundary_low(self):
        self.scc.set_PV(1800)
        self.scc.set_BatVoltage(52.0)
        self.scc.set_BatTemp(0)
        self.assertGreaterEqual(self.scc.suggest()['BAT'], 0)

    #   Should PASS – Charging at high temperature boundary
    def test_charge_at_temp_boundary_high(self):
        self.scc.set_PV(1800)
        self.scc.set_BatVoltage(52.0)
        self.scc.set_BatTemp(45)
        self.assertGreaterEqual(self.scc.suggest()['BAT'], 0)

    #   Should PASS – Discharging at low temperature boundary
    def test_discharge_at_temp_boundary_low(self):
        self.scc.set_PV(0)
        self.scc.set_LightLevel(1200)
        self.scc.set_HeatpumpLevel(500)
        self.scc.set_BatVoltage(50.0)
        self.scc.set_BatTemp(-25)
        self.assertGreaterEqual(self.scc.suggest()['BAT'], 0)

    #   Should PASS – Discharging at high temperature boundary
    def test_discharge_at_temp_boundary_high(self):
        self.scc.set_PV(0)
        self.scc.set_LightLevel(1200)
        self.scc.set_HeatpumpLevel(500)
        self.scc.set_BatVoltage(50.0)
        self.scc.set_BatTemp(65)
        self.assertGreaterEqual(self.scc.suggest()['BAT'], 0)

    #   Should PASS – Required keys present in suggestion
    def test_injectors_present(self):
        self.scc.set_PV(1000)
        self.scc.set_BatVoltage(52.0)
        self.scc.set_BatTemp(25)
        result = self.scc.suggest()
        self.assertIn('BAT', result)
        self.assertIn('BATHEAT', result)

    #   Should PASS – Charging when net power is positive
    def test_power_calculation_positive_net(self):
        self.scc.set_PV(2000)
        self.scc.set_LightLevel(300)
        self.scc.set_HeatpumpLevel(300)
        self.scc.set_BatVoltage(50.0)
        self.scc.set_BatTemp(20)
        self.assertGreater(self.scc.suggest()['BAT'], 0)

    #   Should PASS – Heater should be ON below 5°C
    def test_battery_heater_on_below_5(self):
        self.scc.set_BatTemp(2)
        self.assertTrue(self.scc.suggest()['BATHEAT'])

    #   Should PASS – Heater should be OFF above 5°C
    def test_battery_heater_off_above_5(self):
        self.scc.set_BatTemp(10)
        self.assertFalse(self.scc.suggest()['BATHEAT'])

    #   Should PASS – Charging should be blocked at high voltage
    def test_charge_blocked_high_voltage(self):
        self.scc.set_PV(1800)
        self.scc.set_BatVoltage(55.2)
        self.scc.set_BatTemp(20)
        self.assertEqual(self.scc.suggest()['BAT'], 0)

    #   Should PASS – Discharging should be blocked at low voltage
    def test_discharge_blocked_low_voltage(self):
        self.scc.set_PV(0)
        self.scc.set_LightLevel(1500)
        self.scc.set_HeatpumpLevel(300)
        self.scc.set_BatVoltage(46.0)
        self.scc.set_BatTemp(25)
        self.assertEqual(self.scc.suggest()['BAT'], 0)

    #   Should PASS – Charging should be blocked at too low temp
    def test_charge_blocked_low_temp(self):
        self.scc.set_PV(1500)
        self.scc.set_BatVoltage(52.0)
        self.scc.set_BatTemp(-10)
        self.assertEqual(self.scc.suggest()['BAT'], 0)

    #   Should PASS – Discharging should be blocked at too high temp
    def test_discharge_blocked_high_temp(self):
        self.scc.set_PV(0)
        self.scc.set_LightLevel(1200)
        self.scc.set_HeatpumpLevel(400)
        self.scc.set_BatVoltage(50.0)
        self.scc.set_BatTemp(70)
        self.assertEqual(self.scc.suggest()['BAT'], 0)

    #   Should PASS – Restart blocked if voltage < 51V
    def test_restart_block_if_not_reached_51(self):
        self.scc.set_BatVoltage(54.0)
        self.scc.set_BatVoltage(50.0)
        self.scc.set_PV(2000)
        self.scc.set_BatTemp(25)
        self.assertEqual(self.scc.suggest()['BAT'], 0)

    #   Should PASS – PV over max still handled
    def test_max_pv_handled(self):
        self.scc.set_PV(2500)  # above max, should still be capped internally
        self.scc.set_BatVoltage(50.0)
        self.scc.set_BatTemp(25)
        self.assertLessEqual(self.scc.suggest()['BAT'], 3000)

    #   Should PASS – Injectors enabled still drain power
    def test_injectors_consume_power(self):
        self.scc.set_LightLevel(0)
        self.scc.set_HeatpumpLevel(0)
        self.scc.set_PV(0)
        self.scc.set_BatVoltage(52.0)
        self.scc.set_BatTemp(20)
        suggestion = self.scc.suggest()
        self.assertGreaterEqual(suggestion['HPInjector'], True)

    #   Should PASS – No charging if both temp and voltage are invalid
    def test_charge_zero_if_all_invalid(self):
        self.scc.set_PV(2000)
        self.scc.set_BatVoltage(56.0)
        self.scc.set_BatTemp(-10)
        self.assertEqual(self.scc.suggest()['BAT'], 0)

    #   Failing Test – charging should NOT happen above 55.1V
    def test_fail_invalid_charge_at_high_voltage(self):
        self.scc.set_PV(2000)
        self.scc.set_BatVoltage(56.0)
        self.scc.set_BatTemp(25)
        self.assertTrue(self.scc.suggest()['BAT'] > 0)  # Should fail

    #   Should Fail – Charging below 0°C should fail
    def test_fail_charge_at_cold_temperature(self):
        self.scc.set_BatTemp(-5)
        self.scc.set_PV(1500)
        self.scc.set_BatVoltage(52.0)
        self.assertGreater(self.scc.suggest()['BAT'], 0)  # Should fail

    #   Should Fail – Discharging over 65°C should fail
    def test_fail_discharge_overhot_battery(self):
        self.scc.set_BatTemp(70)
        self.scc.set_BatVoltage(50)
        self.scc.set_PV(0)
        self.scc.set_LightLevel(1000)
        self.scc.set_HeatpumpLevel(200)
        self.assertGreater(self.scc.suggest()['BAT'], 0)  # Should fail

    #   Should Fail – Charging at 56V and 50°C (both invalid)
    def test_fail_charge_double_invalid(self):
        self.scc.set_PV(1500)
        self.scc.set_BatVoltage(56.0)
        self.scc.set_BatTemp(50)
        self.assertGreater(self.scc.suggest()['BAT'], 0)  # Should fail

    #   Should Fail – Restart charging without reaching 51.0V
    def test_fail_restart_before_threshold(self):
        self.scc.set_BatVoltage(54.3)
        self.scc.set_BatVoltage(50.5)
        self.scc.set_PV(1800)
        self.scc.set_BatTemp(25)
        self.assertGreater(self.scc.suggest()['BAT'], 0)  # Should fail
