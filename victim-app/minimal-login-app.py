from flask import Flask, request, render_template_string

app = Flask(__name__)

# Hardcoded credentials (in a real application, never do this!)
VALID_USERNAME = "admin"
VALID_PASSWORD = "password123"

# HTML template for the login form
LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body>
    <h2>Login</h2>
    <form method="POST">
        <input type="text" name="username" placeholder="Username" required><br>
        <input type="password" name="password" placeholder="Password" required><br>
        <input type="submit" value="Login">
    </form>
    {% if error %}
    <p style="color: red;">{{ error }}</p>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username != VALID_USERNAME or password != VALID_PASSWORD:
            error = 'Invalid credentials'
        else:
            return 'Login successful!'
    return render_template_string(LOGIN_TEMPLATE, error=error)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9999)
