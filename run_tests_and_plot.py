import unittest
import matplotlib.pyplot as plt
from test_scc_blackbox import TestSCCBlackBox
from test_scc_whitebox import TestSCCWhiteBox

# Load both test cases
loader = unittest.TestLoader()
suite = unittest.TestSuite()
suite.addTests(loader.loadTestsFromTestCase(TestSCCBlackBox))
suite.addTests(loader.loadTestsFromTestCase(TestSCCWhiteBox))

# Run tests and collect results
result = unittest.TestResult()
suite.run(result)

# Count passed and failed tests
total_tests = result.testsRun
failures = len(result.failures) + len(result.errors)
passed = total_tests - failures

# Print summary
print(f"Total Tests Run: {total_tests}")
print(f"Passed: {passed}")
print(f"Failed: {failures}")

# Plot Pie Chart
labels = 'Passed', 'Failed'
sizes = [passed, failures]
colors = ['#4CAF50', '#F44336']
explode = (0.1, 0)  # explode passed slice

plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)
plt.axis('equal')  # Equal aspect ratio ensures pie is drawn as a circle.
plt.title('SCC White Box and Black Box Test Result Summary')
plt.show()
