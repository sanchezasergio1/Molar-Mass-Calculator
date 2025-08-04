import re
import json
from pathlib import Path
from collections import defaultdict

# Load atomic masses from JSON
DATA_PATH = Path(__file__).parent / 'atomic_masses.json'
with open(DATA_PATH, 'r', encoding='utf-8') as f:
    atomic_masses = json.load(f)


def calculate_molar_mass(formula):
    base_formula, charge = extract_charge(formula)
    element_counts = parse_formula_extended(base_formula)
    total_mass = 0
    for element, count in element_counts.items():
        try:
            atomic_mass = atomic_masses[element]
        except KeyError:
            raise ValueError(f"Unknown element: {element}")
        total_mass += atomic_mass * count
    return total_mass, charge


def extract_charge(formula):
    """
    Extract charge only if given in caret notation (e.g., SO4^2-, NH4^+, [Fe(CN)6]^3-).
    Returns (formula_without_charge, charge_str or None).
    If a charge-like ending (+/-) is present without ^, it's ignored and a note is issued.
    """
    formula = formula.strip()

    # Accept only caret notation (e.g. SO4^2-, NH4^+)
    match = re.search(r'\^(\d*)([+-])$', formula)
    if match:
        number = match.group(1) if match.group(1) else '1'
        sign = match.group(2)
        charge_str = number + sign
        formula_wo_charge = formula[:match.start()]
        return formula_wo_charge, charge_str

    # Inform user that charge was not extracted due to incorrect notation
    if re.search(r'[+-]$', formula):
        print(
            "Note: Charge not extracted. Use '^' notation for charge (e.g. NH4^+, SO4^2-).")

    return formula, None


def parse_formula_extended(formula):
    # Replace alternative bracket symbols with standard parentheses
    formula = formula.replace('[', '(').replace(']', ')')
    formula = formula.replace('{', '(').replace('}', ')')
    formula = formula.replace('·', '.')
    formula = formula.replace(' ', '')

    # Handle dot-separated parts (e.g., CuSO4·5H2O)
    parts = formula.split('.')
    total_counts = defaultdict(int)

    for part in parts:
        # Handle leading numeric multiplier (e.g., 5H2O)
        match = re.match(r'^(\d+)([A-Z\(])', part)
        if match:
            coeff = int(match.group(1))
            subformula = part[len(match.group(1)):]
        else:
            coeff = 1
            subformula = part

        counts = _parse(subformula)
        for el, cnt in counts.items():
            total_counts[el] += cnt * coeff

    return dict(total_counts)


def _parse(formula):
    # Tokenize the formula: elements, numbers, parentheses
    tokens = re.findall(r'[A-Z][a-z]?|\d+|\(|\)', formula)

    def merge_counts(list_of_dicts):
        total = defaultdict(int)
        for d in list_of_dicts:
            for el, cnt in d.items():
                total[el] += cnt
        return total

    def multiply_counts(counts, multiplier):
        return {el: cnt * multiplier for el, cnt in counts.items()}

    def parse(tokens):
        stack = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token == '(':
                # Recursively parse inside parentheses
                sub_counts, jump = parse(tokens[i + 1:])
                i += jump + 1
                multiplier = 1
                if i < len(tokens) and tokens[i].isdigit():
                    multiplier = int(tokens[i])
                    i += 1
                stack.append(multiply_counts(sub_counts, multiplier))
            elif token == ')':
                return merge_counts(stack), i + 1
            elif re.match(r'[A-Z][a-z]?', token):
                # Element symbol possibly followed by a number
                element = token
                count = 1
                if i + 1 < len(tokens) and tokens[i + 1].isdigit():
                    count = int(tokens[i + 1])
                    i += 1
                stack.append({element: count})
                i += 1
            else:
                # Skip unexpected tokens
                i += 1
        return merge_counts(stack), i

    parsed_counts, _ = parse(tokens)
    return parsed_counts


if __name__ == "__main__":
    print("=== Molar Mass Calculator ===")
    print("Type 'exit' to quit the program.")

    while True:
        formula = input(
            "Enter chemical formula (e.g. K4[Fe(CN)6], CuSO4·5H2O, NH4^+, ...): ").strip()

        if formula.lower() == "exit":
            print("Exiting the calculator. Goodbye!")
            break

        try:
            mass, charge = calculate_molar_mass(formula)
            if charge:
                print(
                    f"Molar mass of {formula} is {mass:.3f} g/mol with charge {charge}\n")
            else:
                print(f"Molar mass of {formula} is {mass:.3f} g/mol\n")
        except ValueError as e:
            print(f"Error: {e}\n")
