from engine.math_core.fractals import generate_lsystem, evaluate_lsystem_3d

def test_generate_lsystem():
    result = generate_lsystem(1, axiom="F", rules={"F": "F+F-F"})
    assert result == "F+F-F"
    
    result2 = generate_lsystem(2, axiom="F", rules={"F": "F+F"})
    assert result2 == "F+F+F+F"

def test_evaluate_lsystem_3d():
    instr = "F+F"
    points = evaluate_lsystem_3d(instr, step_length=1.0, angle=90.0)
    assert len(points) == 3
    assert abs(points[0]["x"]) < 1e-9
    assert abs(points[1]["x"] - 1.0) < 1e-9
    assert abs(points[1]["y"]) < 1e-9
    assert abs(points[2]["x"] - 1.0) < 1e-9
    assert abs(points[2]["y"] - 1.0) < 1e-9
