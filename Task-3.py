import random
import string

def generate_password(length, include_uppercase=True, include_lowercase=True, 
                     include_numbers=True, include_symbols=True):
    """
    Generate a random password with specified criteria.
    
    Args:
        length (int): Desired length of the password
        include_uppercase (bool): Include uppercase letters
        include_lowercase (bool): Include lowercase letters
        include_numbers (bool): Include numbers
        include_symbols (bool): Include special symbols
    
    Returns:
        str: Generated password
    """
    # Build character pool based on user preferences
    chars = ""
    
    if include_lowercase:
        chars += string.ascii_lowercase
    if include_uppercase:
        chars += string.ascii_uppercase
    if include_numbers:
        chars += string.digits
    if include_symbols:
        chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    # Ensure at least one character type is selected
    if not chars:
        chars = string.ascii_letters + string.digits
        print("No character types selected. Using letters and numbers by default.")
    
    # Generate password
    password = ''.join(random.choice(chars) for _ in range(length))
    return password

def get_user_input():
    """Get user preferences for password generation."""
    print("=== Password Generator ===")
    print()
    
    # Get password length
    while True:
        try:
            length = int(input("Enter desired password length (minimum 4): "))
            if length < 4:
                print("Password length should be at least 4 characters.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
    
    print("\nCharacter types to include:")
    
    # Get character type preferences
    include_uppercase = input("Include uppercase letters (A-Z)? (y/n): ").lower().startswith('y')
    include_lowercase = input("Include lowercase letters (a-z)? (y/n): ").lower().startswith('y')
    include_numbers = input("Include numbers (0-9)? (y/n): ").lower().startswith('y')
    include_symbols = input("Include symbols (!@#$%^&*)? (y/n): ").lower().startswith('y')
    
    return length, include_uppercase, include_lowercase, include_numbers, include_symbols

def check_password_strength(password):
    """
    Check and display password strength.
    
    Args:
        password (str): The generated password
    """
    score = 0
    feedback = []
    
    # Length check
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Consider using at least 8 characters")
    
    # Character type checks
    if any(c.islower() for c in password):
        score += 1
    else:
        feedback.append("Consider adding lowercase letters")
    
    if any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append("Consider adding uppercase letters")
    
    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append("Consider adding numbers")
    
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        score += 1
    else:
        feedback.append("Consider adding special characters")
    
    # Determine strength
    if score >= 4:
        strength = "Strong"
    elif score >= 3:
        strength = "Medium"
    else:
        strength = "Weak"
    
    print(f"\nPassword Strength: {strength}")
    if feedback:
        print("Suggestions for improvement:")
        for suggestion in feedback:
            print(f"  - {suggestion}")

def main():
    """Main function to run the password generator."""
    while True:
        # Get user input
        length, uppercase, lowercase, numbers, symbols = get_user_input()
        
        # Generate password
        password = generate_password(length, uppercase, lowercase, numbers, symbols)
        
        # Display results
        print(f"\n{'='*50}")
        print("GENERATED PASSWORD:")
        print(f"{'='*50}")
        print(f"Password: {password}")
        print(f"Length: {len(password)} characters")
        
        # Check password strength
        check_password_strength(password)
        
        # Ask if user wants to generate another password
        print(f"\n{'='*50}")
        generate_another = input("Generate another password? (y/n): ").lower().startswith('y')
        
        if not generate_another:
            print("Thank you for using the Password Generator!")
            break
        print()

if __name__ == "__main__":
    main()