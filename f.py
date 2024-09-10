from flask import Flask, render_template, request, session
import math
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Helper function for combinations (nCr)
def comb(n, r):
    return math.comb(n, r)

# Helper function to check if a number is prime
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

# Toggle between degrees and radians
deg_mode = True

# Evaluates the mathematical expression safely
def evaluate_expression(expression):
    global deg_mode
    try:
        # Handle Degrees/Radians toggle
        if 'Deg/Rad' in expression:
            deg_mode = not deg_mode
            return 'Deg' if deg_mode else 'Rad'

        # Replace certain symbols with Python functions
        new_expression = expression.replace('√', 'math.sqrt')
        new_expression = new_expression.replace('∛', 'math.pow(, 1/3)')
        new_expression = new_expression.replace('²', '**2')
        new_expression = new_expression.replace('^', '**')
        new_expression = new_expression.replace('π', 'math.pi')
        new_expression = new_expression.replace('!', 'math.factorial')
        new_expression = new_expression.replace('sin', 'math.sin' if not deg_mode else 'math.sin(math.radians')
        new_expression = new_expression.replace('cos', 'math.cos' if not deg_mode else 'math.cos(math.radians')
        new_expression = new_expression.replace('tan', 'math.tan' if not deg_mode else 'math.tan(math.radians')
        new_expression = new_expression.replace('asin', 'math.asin')
        new_expression = new_expression.replace('acos', 'math.acos')
        new_expression = new_expression.replace('atan', 'math.atan')
        new_expression = new_expression.replace('sinh', 'math.sinh')
        new_expression = new_expression.replace('cosh', 'math.cosh')
        new_expression = new_expression.replace('tanh', 'math.tanh')
        new_expression = new_expression.replace('log', 'math.log')  # log with base e
        new_expression = new_expression.replace('log10', 'math.log10')  # log base 10
        new_expression = new_expression.replace('10^', '10**')
        new_expression = new_expression.replace('abs', 'abs')
        new_expression = new_expression.replace('C', 'comb')  # nCr
        new_expression = new_expression.replace('%', '/100')  # percentage calculation

        # Custom base logarithm (log(x, b))
        if 'log(' in new_expression and ',' in new_expression:
            args = new_expression.split('log(')[1].split(')')[0].split(',')
            base = float(args[1].strip())
            number = float(args[0].strip())
            return math.log(number, base)

        # Additional operations for prime check and random number
        if 'is_prime' in expression:
            number = int(expression.split('(')[1].split(')')[0])
            return is_prime(number)
        if 'rand' in expression:
            return random.random()

        # Safely evaluate the expression
        result = eval(new_expression, {"__builtins__": None}, {
            'math': math, 'comb': comb
        })

        # Handle scientific notation toggle
        if 'Sci' in expression:
            return "{:.6e}".format(result)
        return result
    except Exception as e:
        return "Error"

# Home route to render the calculator interface
@app.route('/')
def calculator():
    history = session.get('history', [])
    return render_template('calculator.html', history=history)

# Route to handle form submission and calculation
@app.route('/calculate', methods=['POST'])
def calculate():
    expression = request.form['expression']
    result = evaluate_expression(expression)

    # Get history from the session or initialize it
    history = session.get('history', [])
    
    # Add the current calculation and result to the history
    history.insert(0, {'expression': expression, 'result': result})

    # Keep only the last 5 entries in the history
    if len(history) > 5:
        history = history[:5]

    # Update the session with the new history
    session['history'] = history

    return render_template('calculator.html', expression=expression, result=result, history=history)

# Route to handle graph plotting
@app.route('/plot_graph', methods=['POST'])
def plot_graph():
    # This would plot the graph based on the input (using a default equation y=sin(x) here)
    return render_template('calculator.html', graph=True)


if __name__ == "__main__":
    app.run(debug=True)
