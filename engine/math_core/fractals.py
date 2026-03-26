import math

def generate_lsystem(iterations: int, axiom: str = "F", rules: dict = None) -> str:
    """Expands the L-system string recursively."""
    if rules is None:
        rules = {"F": "F+F-F-F+F"}
    
    result = axiom
    for _ in range(iterations):
        next_result = ""
        for char in result:
            next_result += rules.get(char, char)
        result = next_result
    return result

def evaluate_lsystem_3d(string_instructions: str, step_length: float = 1.0, angle: float = 90.0) -> list[dict]:
    """
    Evaluates L-system instructions onto 3D coordinates.
    F: move forward
    +: positive yaw rotation
    -: negative yaw rotation
    """
    points = [{"x": 0.0, "y": 0.0, "z": 0.0}]
    x, y, z = 0.0, 0.0, 0.0
    current_angle = 0.0
    
    for char in string_instructions:
        if char == "F":
            rad = math.radians(current_angle)
            x += step_length * math.cos(rad)
            y += step_length * math.sin(rad)
            points.append({"x": x, "y": y, "z": z})
        elif char == "+":
            current_angle += angle
        elif char == "-":
            current_angle -= angle
    return points
