

def is_number(string):
    try:
        # Try to convert the string to an integer or a float
        int(string)
        return True  # It's an integer
    except ValueError:
        try:
            float(string)
            return True  # It's a float
        except ValueError:
            return False  # It's neither an integer nor a float
   