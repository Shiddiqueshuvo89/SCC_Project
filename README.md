# Test Report

**Report generated on:** 14-Jun-2025 at 15:38:55  
**Tool used:** [pytest-html](https://github.com/pytest-dev/pytest-html) v4.1.1

---

## 🧪 Environment

| Property   | Value                              |
|------------|------------------------------------|
| Python     | 3.12.7                             |
| Platform   | Windows-10-10.0.19045-SP0          |
| Packages   | pytest: 7.4.4<br>pluggy: 1.0.0     |
| Plugins    | anyio: 4.2.0<br>html: 4.1.1<br>metadata: 3.1.1 |

---

## ✅ Summary

- **Total tests**: 23  
- **Duration**: 19 ms  
- **Passed**: ✅ 17  
- **Failed**: ❌ 6  
- **Skipped**: ⚠️ 0  
- **Expected Failures**: 0  
- **Unexpected Passes**: 0  
- **Errors**: 0  
- **Reruns**: 0  

---

## ❌ Failed Tests

| Result | Test Name |
|--------|-----------|
| Failed | `test_scc_blackbox.py::TestSCCBlackBox::test_fail_charge_at_cold_temperature` |
| Failed | `test_scc_blackbox.py::TestSCCBlackBox::test_fail_charge_double_invalid` |
| Failed | `test_scc_blackbox.py::TestSCCBlackBox::test_fail_discharge_overhot_battery` |
| Failed | `test_scc_blackbox.py::TestSCCBlackBox::test_fail_invalid_charge_at_high_voltage` |
| Failed | `test_scc_blackbox.py::TestSCCBlackBox::test_fail_invalid_charge_at_high_voltage` |
| Failed | `test_scc_blackbox.py::TestSCCBlackBox::test_fail_invalid_charge_at_high_voltage` |

---

## ✅ Passed Tests

| Result | Test Name |
|--------|-----------|
| Passed | `test_scc_blackbox.py::TestSCCBlackBox::test_fail_invalid_charge_at_high_voltage` |
| Passed | `test_scc_blackbox.py::TestSCCBlackBox::test_battery_heater_off_above_5	1 ms`|	
| Passed | `test_scc_blackbox.py::TestSCCBlackBox::test_battery_heater_on_below_5	1 ms`|	
| Passed | `test_scc_blackbox.py::TestSCCBlackBox::test_charge_at_temp_boundary_high	1 ms`|	
| Passed | `test_scc_blackbox.py::TestSCCBlackBox::test_charge_at_temp_boundary_low	1 ms`|	
| Passed | `test_scc_blackbox.py::TestSCCBlackBox::test_charge_blocked_high_voltage	1 ms`|	
| Passed | `test_scc_blackbox.py::TestSCCBlackBox::test_charge_blocked_low_temp	1 ms`|
| Passed | `test_scc_blackbox.py::TestSCCBlackBox::test_charge_zero_if_all_invalid	1 ms`|
| Passed | `test_scc_blackbox.py::TestSCCBlackBox::test_discharge_at_temp_boundary_high	1 ms`|
| Passed | `test_scc_blackbox.py::TestSCCBlackBox::test_discharge_at_temp_boundary_low	1 ms`|	
| Passed | `test_scc_blackbox.py::TestSCCBlackBox::test_discharge_blocked_high_temp	1 ms`|	
| Passed | `test_scc_blackbox.py::TestSCCBlackBox::test_discharge_blocked_low_voltage	1 ms`|	
| Passed | `test_scc_blackbox.py::TestSCCBlackBox::test_injectors_consume_power	1 ms`|	
| Passed | `test_scc_blackbox.py::TestSCCBlackBox::test_injectors_present	1 ms`|	
| Passed | `test_scc_blackbox.py::TestSCCBlackBox::test_max_pv_handled	1 ms`|	
| Passed | `test_scc_blackbox.py::TestSCCBlackBox::test_restart_block_if_not_reached_51	1 ms`|
| Passed | `test_scc_blackbox.py::TestSCCBlackBox::test_valid_charge	1 ms`|
| Passed | `test_scc_blackbox.py::TestSCCBlackBox::test_valid_discharge	1 ms`|
