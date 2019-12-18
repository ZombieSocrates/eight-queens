# Eight Queens
An application for solving the [Eight Queens puzzle](https://en.wikipedia.org/wiki/Eight_queens_puzzle). What began as getting nerd sniped by a Constraint Satisfaction Problem from Chapter 6 of [Artificial Intelligence: A Modern Approach](http://aima.cs.berkeley.edu/) matured into a way for people to interact with the problem, track their progress, and solve it themselves. There's a front end written in vanilla JS (with some help from the [JSBoard library](https://github.com/danielborowski/jsboard.git)) supported by a Flask back end that actually handles the solutions.

# Setup
Assuming that you've already cloned the repo and want to run the app locally... 

## back-end
To get the back end running, you're going to need a Python 3.7.0 virtual environment.
```
pyenv virtualenv 3.7.0 <YOUR-ENV-NAME>
pyenv activate <YOUR-ENV-NAME>
pip install -r back-end/requirements.txt
``` 

From there, just run the following commands:
```
cd back-end
export FLASK_APP=api.py
export FLASK_DEBUG=1
flask run
```

In a browser, head to `localhost:5000/status` and you should see a message that says **Time to Move Some Queens**, which means you're good to go!

## front-end
At current state, I'm just using [lite-server](https://github.com/johnpapa/lite-server), which comes with its own setup instructions...
```
npm init -y
npm install lite-server --save-dev
```
Then add the following to the resulting `package.json` file
```
  "scripts": {
    "dev": "lite-server"
  },
```
The only other thing you'll then need to do is pull down the JSBoard submodule with
```
git submodule update --init
```

From there you are ready to serve up some queens.
```
cd front-end
npm run dev
```

Head to `localhost:3000` and you are ready for the app in all its glory.

# Next Steps
The core functionality of "a website that solves the Eight Queens puzzle for basically any initial configuration" is done. With that handled, I think I'd like to take this in more of an explorable explanation direction. Something that actually onboards people to the problem domain and provides hints/additional context if desired rather than "Click. Boom. Solve." A not-so-scientific laundry list of things I'm hoping will serve this goal...

## front-end
- Organize the page better with a clearer hierarchy of information
- Make buttons look like buttons, interactables look like interactables, and static displays look like static displays
- More information about which queens are conflicted
- More information about which moves actually represent improvements
- A hint button that lets people get clues if they want
- An actual onboarding hierarchy
- **Top Priority for all of the above:** Refactor the front end into an actual framework that other devs can make sense of
- Handle boards with arbitrary dimensionality.

## back-end
Admittedly less here toward the main goal, but somethings that might be interesting
- Move the things that are sort of like unit tests out of `__main__` blocks in `solvers.py` and `chess_board.py` into an actual test harness.
- Dig into some strange behavior about one of the tests in `solvers.py`
- Handle edge case if somebody makes a solve request for an already solved board.
- I think the feature of hinting could potentially involve an API call? Uncertain.
- Handle boards with arbitrary dimensionality


