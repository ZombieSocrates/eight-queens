from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/status")
def hello():
    return '''
        <h1> Time to move some 
            <a href = "https://youtu.be/HgzGwKwLmgM?t=35">Queens</a>
        </h1>  
    '''

if __name__ == "__main__":
    app.run()