import decimal

# Configure high precision for arbitrary mathematical calculations.
# The default precision is 28, but for mathematical visualization
# we might need thousands of digits of accuracy.
decimal.getcontext().prec = 1000
