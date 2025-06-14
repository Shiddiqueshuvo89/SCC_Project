import unittest
from scc import SCC

class TestSCCWhiteBox(unittest.TestCase):
    def setUp(self):
        self.scc = SCC()

    #   Should PASS – Charging must be blocked above 55.1V
    def test_voltage_gate_over_55v(self):
        self.scc.set_BatVoltage(55.2)
        self.scc.set_BatTemp(25)
        self.scc.set_PV(1500)
        self.assertEqual(self.scc.suggest()['BAT'], 0)

    #   Should PASS – Discharging blocked if voltage < 47V
    def test_voltage_gate_under_47v(self):
        self.scc.set_BatVoltage(46.5)
        self.scc.set_BatTemp(25)
        self.scc.set_PV(0)
        self.scc.set_LightLevel(800)
        self.scc.set_HeatpumpLevel(500)
        self.assertEqual(self.scc.suggest()['BAT'], 0)

    #   Should PASS – Charging not allowed until battery reaches 51V after being <54.4V
    def test_charge_restart_path_blocked(self):
        self.scc.set_BatVoltage(54.0)
        self.scc.set_BatVoltage(50.9)
        self.scc.set_BatTemp(25)
        self.scc.set_PV(2000)
        self.assertEqual(self.scc.suggest()['BAT'], 0)

    #   Should PASS – Charging resumes after reaching 51V again
    def test_charge_restart_path_allowed(self):
        self.scc.set_BatVoltage(54.0)
        self.scc.set_BatVoltage(51.0)
        self.scc.set_BatTemp(25)
        self.scc.set_PV(2000)
        self.assertGreater(self.scc.suggest()['BAT'], 0)

    #   Should PASS – Charging allowed at 0°C
    def test_temp_low_bound_charge(self):
        self.scc.set_BatTemp(0)
        self.scc.set_BatVoltage(50)
        self.scc.set_PV(2000)
        self.assertGreaterEqual(self.scc.suggest()['BAT'], 0)

    #   Should PASS – Charging allowed at 45°C
    def test_temp_high_bound_charge(self):
        self.scc.set_BatTemp(45)
        self.scc.set_BatVoltage(50)
        self.scc.set_PV(2000)
        self.assertGreaterEqual(self.scc.suggest()['BAT'], 0)

    #   Should PASS – Discharge blocked below -25°C
    def test_temp_low_discharge_block(self):
        self.scc.set_BatTemp(-26)
        self.scc.set_BatVoltage(50)
        self.scc.set_PV(0)
        self.assertEqual(self.scc.suggest()['BAT'], 0)

    #   Should PASS – Discharge blocked above 65°C
    def test_temp_high_discharge_block(self):
        self.scc.set_BatTemp(66)
        self.scc.set_BatVoltage(50)
        self.scc.set_PV(0)
        self.assertEqual(self.scc.suggest()['BAT'], 0)

    #   Should PASS – Net power is negative; discharging allowed
    def test_net_power_handling_negative(self):
        self.scc.set_PV(500)
        self.scc.set_LightLevel(1500)
        self.scc.set_HeatpumpLevel(500)
        self.scc.set_BatVoltage(50)
        self.scc.set_BatTemp(20)
        self.assertGreaterEqual(self.scc.suggest()['BAT'], 0)

    #   Should PASS – Net power is positive; charging allowed
    def test_net_power_handling_positive(self):
        self.scc.set_PV(2000)
        self.scc.set_LightLevel(200)
        self.scc.set_HeatpumpLevel(200)
        self.scc.set_BatVoltage(50)
        self.scc.set_BatTemp(20)
        self.assertGreaterEqual(self.scc.suggest()['BAT'], 0)

    #   Should PASS – Heater ON below 5°C
    def test_battery_heater_on_when_temp_below_5(self):
        self.scc.set_BatTemp(2)
        self.assertTrue(self.scc.suggest()['BATHEAT'])

    #   Should PASS – Heater OFF above 5°C
    def test_battery_heater_off_above_5(self):
        self.scc.set_BatTemp(10)
        self.assertFalse(self.scc.suggest()['BATHEAT'])

    #   Should PASS – Charging blocked at >45°C
    def test_charge_zero_if_temp_too_high(self):
        self.scc.set_BatTemp(50)
        self.scc.set_PV(1800)
        self.scc.set_BatVoltage(50)
        self.assertEqual(self.scc.suggest()['BAT'], 0)

    #   Should PASS – Discharging blocked at < -25°C
    def test_discharge_zero_if_temp_too_low(self):
        self.scc.set_BatTemp(-30)
        self.scc.set_PV(0)
        self.scc.set_LightLevel(1000)
        self.scc.set_HeatpumpLevel(300)
        self.scc.set_BatVoltage(50)
        self.assertEqual(self.scc.suggest()['BAT'], 0)

    #   Should PASS – Net power exactly zero; no charging/discharging
    def test_net_power_exact_zero(self):
        self.scc.set_PV(1500)
        self.scc.set_LightLevel(1000)
        self.scc.set_HeatpumpLevel(500)
        self.scc.set_BatVoltage(50)
        self.scc.set_BatTemp(25)
        self.assertEqual(self.scc.suggest()['BAT'], 0)

    #   Should PASS – Charge power capped at 3000W
    def test_max_charge_limit_enforced(self):
        self.scc.set_PV(5000)
        self.scc.set_LightLevel(0)
        self.scc.set_HeatpumpLevel(0)
        self.scc.set_BatVoltage(50)
        self.scc.set_BatTemp(25)
        self.assertLessEqual(self.scc.suggest()['BAT'], 3000)

    #   Should PASS – Light clamped at 1800W
    def test_light_power_clamped(self):
        self.scc.set_LightLevel(5000)
        self.assertLessEqual(self.scc.suggest()['Light'], 1800)

    #   Should PASS – Heat pump clamped at 400W
    def test_heatpump_power_clamped(self):
        self.scc.set_HeatpumpLevel(800)
        self.assertLessEqual(self.scc.suggest()['HP'], 400)

    #   Should PASS – Normal charge scenario
    def test_charge_allowed_midrange(self):
        self.scc.set_PV(1500)
        self.scc.set_BatVoltage(52.0)
        self.scc.set_BatTemp(25)
        self.assertGreater(self.scc.suggest()['BAT'], 0)

    #   Should PASS – Normal discharge scenario
    def test_discharge_allowed_midrange(self):
        self.scc.set_PV(0)
        self.scc.set_LightLevel(1000)
        self.scc.set_HeatpumpLevel(300)
        self.scc.set_BatVoltage(52.0)
        self.scc.set_BatTemp(25)
        self.assertGreaterEqual(self.scc.suggest()['BAT'], 0)

    #   Should FAIL – Charging should be blocked above 55.1V
    def test_fail_charge_above_voltage(self):
        self.scc.set_PV(2000)
        self.scc.set_BatVoltage(56.0)
        self.scc.set_BatTemp(25)
        self.assertTrue(self.scc.suggest()['BAT'] > 0)

    #   Should FAIL – Discharge should be blocked at voltage < 47V
    def test_fail_discharge_below_voltage(self):
        self.scc.set_PV(0)
        self.scc.set_LightLevel(1000)
        self.scc.set_HeatpumpLevel(300)
        self.scc.set_BatVoltage(46.0)
        self.scc.set_BatTemp(25)
        self.assertTrue(self.scc.suggest()['BAT'] > 0)

    #   Should FAIL – Charging restart not allowed until reaching 51.0V
    def test_fail_restart_without_51v(self):
        self.scc.set_BatVoltage(54.0)
        self.scc.set_BatVoltage(50.8)
        self.scc.set_PV(2000)
        self.scc.set_BatTemp(25)
        self.assertGreater(self.scc.suggest()['BAT'], 0)

    #   Should FAIL – Charging should not happen below 0°C
    def test_fail_charge_temp_too_low(self):
        self.scc.set_BatTemp(-5)
        self.scc.set_BatVoltage(52.0)
        self.scc.set_PV(1500)
        self.assertGreater(self.scc.suggest()['BAT'], 0)

    #   Should FAIL – Charging should not happen above 45°C
    def test_fail_charge_temp_too_high(self):
        self.scc.set_BatTemp(46)
        self.scc.set_BatVoltage(52.0)
        self.scc.set_PV(1500)
        self.assertGreater(self.scc.suggest()['BAT'], 0)
