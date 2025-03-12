# Calculates and prints the Fibonacci sequence up to 10 numbers
def fibonacci(n):
    # Initialize the first two numbers in the sequence
    a, b = 0, 1
    # Create an empty list to store the sequence
    fib_sequence = []
    # Generate the sequence
    for i in range(n):
        fib_sequence.append(a)
        a, b = b, a + b
    # Return the generated sequence
    return fib_sequence

# Generate and print the Fibonacci sequence
fib_sequence = fibonacci(10)
print("Fibonacci sequence:", fib_sequence)
