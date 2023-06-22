from website import create_app

app = create_app()

# This if statement means we only run the server when we run this file instead of just importing this file
if __name__ == '__main__':
    # The argument debug True means it automatically rerun the webserver every time we make a change to our code
    # We turn debug=False in actual production
    app.run()

