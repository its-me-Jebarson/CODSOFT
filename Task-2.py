def calculator():
    """Simple calculator with basic arithmetic operations."""
    
    print("=== Simple Calculator ===")
    print("Available operations:")
    print("1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (*)")
    print("4. Division (/)")
    print("5. Modulus (%)")
    print("6. Exponentiation (**)")
    
    try:
        # Get first number
        num1 = float(input("\nEnter the first number: "))
        
        # Get second number
        num2 = float(input("Enter the second number: "))
        
        # Get operation choice
        print("\nChoose an operation:")
        operation = input("Enter operation (+, -, *, /, %, **): ").strip()
        
        # Perform calculation based on operation
        if operation == '+':
            result = num1 + num2
            print(f"\n{num1} + {num2} = {result}")
            
        elif operation == '-':
            result = num1 - num2
            print(f"\n{num1} - {num2} = {result}")
            
        elif operation == '*':
            result = num1 * num2
            print(f"\n{num1} * {num2} = {result}")
            
        elif operation == '/':
            if num2 == 0:
                print("\nError: Division by zero is not allowed!")
            else:
                result = num1 / num2
                print(f"\n{num1} / {num2} = {result}")
                
        elif operation == '%':
            if num2 == 0:
                print("\nError: Modulus by zero is not allowed!")
            else:
                result = num1 % num2
                print(f"\n{num1} % {num2} = {result}")
                
        elif operation == '**':
            result = num1 ** num2
            print(f"\n{num1} ** {num2} = {result}")
            
        else:
            print("\nError: Invalid operation! Please use +, -, *, /, %, or **")
            
    except ValueError:
        print("\nError: Please enter valid numbers!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

def main():
    """Main function to run the calculator with option to repeat."""
    while True:
        calculator()
        
        # Ask if user wants to perform another calculation
        again = input("\nWould you like to perform another calculation? (y/n): ").strip().lower()
        if again not in ['y', 'yes']:
            print("Thank you for using the calculator!")
            break
        print("\n" + "="*30)

if __name__ == "__main__":
    main()