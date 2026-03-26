import engine.math_core.precision  # This initializes the decimal context

def generate_fibonacci(n: int) -> list[str]:
    """
    Generate the Fibonacci sequence up to n elements.
    Returns strings to preserve arbitrary precision explicitly.
    """
    if n <= 0:
        return []
    
    # Initialize first numbers as Python's arbitrary-precision integers
    seq = [0, 1]
    
    # Calculate sequence up to n
    for i in range(2, n):
        seq.append(seq[-1] + seq[-2])
    
    # Slice to n if n < 2, then stringify all elements
    result = seq[:n]
    return [str(num) for num in result]

if __name__ == "__main__":
    print(generate_fibonacci(5))
