"""
Section 1: Sensor Data Cleaning & Sanitization
================================================
Provides a function to clean and normalize raw sensor readings
by filtering invalid entries, removing negatives, and capping values.
"""


def clean_sensor_data(raw_values):
    """
    Clean and normalize a list of mixed sensor readings.

    Processing steps:
        1. Convert each element to float (skip if conversion fails).
        2. Drop None values and negative numbers (< 0).
        3. Cap any value exceeding 500.0 to exactly 500.0.

    Args:
        raw_values (list): A list of mixed inputs (strings, ints, floats,
                           None, or other non-numeric types).

    Returns:
        list[float]: A cleaned list of valid, non-negative floats
                     capped at 500.0.
    """
    # Guard clause: return empty list for None or non-list inputs
    if not isinstance(raw_values, list):
        return []

    cleaned = []

    for value in raw_values:
        # Skip None values explicitly
        if value is None:
            continue

        # Attempt float conversion
        try:
            numeric = float(value)
        except (ValueError, TypeError):
            # Skip entries that can't be converted to float
            continue

        # Drop negative values (error flags)
        if numeric < 0:
            continue

        # Cap values exceeding the 500.0 threshold
        if numeric > 500.0:
            numeric = 500.0

        cleaned.append(numeric)

    return cleaned


# ---------------------------------------------------------------------------
# Test Cases
# ---------------------------------------------------------------------------

def run_tests():
    """Run validation tests for clean_sensor_data."""

    # Test 1: Mixed valid and invalid inputs
    mixed_input = ["42.5", None, -3, "hello", 600, 23.1, "", True, 0]
    expected_1 = [42.5, 500.0, 23.1, 1.0, 0.0]
    result_1 = clean_sensor_data(mixed_input)
    assert result_1 == expected_1, (
        f"Test 1 FAILED -- Expected {expected_1}, got {result_1}"
    )
    print(f"Test 1 PASSED: {mixed_input}")
    print(f"  -> Result: {result_1}\n")

    # Test 2: Empty list returns empty list
    result_2 = clean_sensor_data([])
    assert result_2 == [], (
        f"Test 2 FAILED -- Expected [], got {result_2}"
    )
    print("Test 2 PASSED: [] -> []\n")

    # Test 3: All invalid entries returns empty list
    all_invalid = [None, "abc", "xyz", "", None]
    result_3 = clean_sensor_data(all_invalid)
    assert result_3 == [], (
        f"Test 3 FAILED -- Expected [], got {result_3}"
    )
    print(f"Test 3 PASSED: {all_invalid} -> []\n")

    # Test 4: Boundary values -- exactly 0, exactly 500, just above 500
    boundary_input = [0, 500.0, 500.1, -0.001]
    expected_4 = [0.0, 500.0, 500.0]
    result_4 = clean_sensor_data(boundary_input)
    assert result_4 == expected_4, (
        f"Test 4 FAILED -- Expected {expected_4}, got {result_4}"
    )
    print(f"Test 4 PASSED: {boundary_input}")
    print(f"  -> Result: {result_4}\n")

    print("=" * 40)
    print("All tests passed!")
    print("=" * 40)


if __name__ == "__main__":
    run_tests()
