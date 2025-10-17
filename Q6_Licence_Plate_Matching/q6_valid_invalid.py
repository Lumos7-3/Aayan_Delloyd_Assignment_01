import random
import string
from difflib import SequenceMatcher
import time

# ------------------ Similarity Function ------------------
def get_similarity(s1, s2):
    matcher = SequenceMatcher(None, s1, s2)
    return matcher.ratio() * 100

# ------------------ License Plate Generators ------------------
def random_valid_plate():
    state = ''.join(random.choices(string.ascii_uppercase, k=2))
    district = ''.join(random.choices(string.digits, k=2))
    series = ''.join(random.choices(string.ascii_uppercase, k=2))
    number = str(random.randint(1, 9999))
    return f"{state}{district}{series}{number}"

def random_invalid_plate(valid_plate, failure_chance=0.05):
    """Generate invalid plate; occasional accidental match to create failures."""
    if random.random() < failure_chance:
        return valid_plate
    plate = list(valid_plate)
    while True:
        idx = random.randint(0, len(plate)-1)
        new_char = random.choice(string.ascii_uppercase + string.digits)
        if plate[idx] != new_char:
            plate[idx] = new_char
            break
    return ''.join(plate)

# ------------------ Generate Test Plates ------------------
NUM_TESTS = 1000
valid_plates = [random_valid_plate() for _ in range(NUM_TESTS // 2)]
invalid_plates = [random_invalid_plate(p, failure_chance=0.05) for p in valid_plates]

# ------------------ ANSI Colors ------------------
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

# ------------------ Run Tests with Gradual Display ------------------
valid_passed = 0
valid_failed = 0
invalid_passed = 0
invalid_failed = 0

print("\nStarting License Plate Similarity Tests...\n")

# Test valid plates
for i, plate in enumerate(valid_plates, 1):
    sim = get_similarity(plate, plate)
    status = "PASS" if sim == 100 else "FAIL"
    if status == "PASS":
        valid_passed += 1
        color = GREEN
    else:
        valid_failed += 1
        color = RED
    print(f"Valid Plate {i:03}: {plate} | Similarity: {sim:.2f}% | {color}{status}{RESET}", flush=True)
    time.sleep(0.002)

# Test invalid plates
for i, (v, inval) in enumerate(zip(valid_plates, invalid_plates), 1):
    sim = get_similarity(v, inval)
    status = "PASS" if sim < 100 else "FAIL"
    if status == "PASS":
        invalid_passed += 1
        color = GREEN
    else:
        invalid_failed += 1
        color = RED
    print(f"Invalid Plate {i:03}: {inval} vs {v} | Similarity: {sim:.2f}% | {color}{status}{RESET}", flush=True)
    time.sleep(0.002)

# ------------------ Summary ------------------
total_valid = valid_passed + valid_failed
total_invalid = invalid_passed + invalid_failed
total_tests = total_valid + total_invalid
total_failed = valid_failed + invalid_failed
total_passed = valid_passed + invalid_passed

print("\n--- License Plate Test Summary ---") 
print(f"Valid Plates:   Passed = {valid_passed}, Failed = {valid_failed} "
      f"({(valid_failed/total_valid)*100:.2f}% failed)")
print(f"Invalid Plates: Passed = {invalid_passed}, Failed = {invalid_failed} "
      f"({(invalid_failed/total_invalid)*100:.2f}% failed)")
print(f"Total Tests:    Passed = {total_passed}, Failed = {total_failed} "
      f"({(total_failed/total_tests)*100:.2f}% failed)")

# Final highlight
print(f"\n>>> TOTAL FAILED PLATES = {total_failed} out of {total_tests} "
      f"({(total_failed/total_tests)*100:.2f}%) <<<\n")
