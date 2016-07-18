#!flask-website/bin/python

from app import app


app.secret_key = 'secret'
app.run()
#app.run(debug=True, host='0.0.0.0')
