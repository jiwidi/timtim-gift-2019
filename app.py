from flask import Flask, flash, redirect, render_template, request, session, abort
from random import randint
import datetime
from datetime import timedelta 


app = Flask(__name__, template_folder='templates')




hints = {
    "1": "What is 1+1",
    "2": "What is 2+2",
    "3": "What is 1+1",
    "4": "What is 2+2",
    "5": "What is 1+1",
    "6": "What is 2+2",
    "7": "What is 1+1",
    "8": "What is 2+2",
}

hintsAnswers = {
    "1": "2",
    "2": "4",
    "3": "2",
    "4": "4",
    "5": "2",
    "6": "4",
    "7": "2",
    "8": "4",
}


CurrentDate = datetime.datetime.now()
def gethintn():
    try:
        f = open("demofile.txt", "r")
        hintnumber = f.readline()
        if(hintnumber==''):
            hintnumber = "1"
        f.close()
        return hintnumber
    except:
        return "1"
def increasehitn(currentN):
    try:
        f = open("demofile.txt", "w+")
        hintnumber = str(int(currentN) + 1)
        if (hintnumber in hintsAnswers.keys()):
            f.write(hintnumber)
        else: 
            hintnumber = str(int(hintnumber) - 1)
            f.write(hintnumber)
        f.close()
        return hintnumber
    except:
        f = open("demofile.txt", "w+")
        f.write(currentN)
        f.close()
    return currentN

def checkAnswer(text,hitn):
    hintn = hitn
    result = False
    try:
        if (text==hintsAnswers[hintn]):
            result=True
    except:
         pass
    return result





hintnumber = gethintn()
maxhit = hintnumber
hint = hints[hintnumber]
nextbutton="Validate"

@app.route('/')
def index():
    #Retrieve current hint
    maxhit = gethintn()
    #Default values for strings
    puzzlecount = "Solved {}/14 puzzles".format(maxhit)
    return render_template('index.html',hint=hint,hintnumber=hintnumber, backbutton="none", nextbutton="Start!", hintsolved=puzzlecount,textENABLED="none", bigtextL="TimTim christmas puzzle", mediumtextL="Solve the hints and find your christmas gift :) ")

@app.route('/goback')
def goback():
    #Retrieve current hint
    maxhit = gethintn()
    #Default values for strings
    puzzlecount = "Solved {}/14 puzzles".format(maxhit)
    return render_template('index.html',hint=hint,hintnumber=hintnumber, backbutton="none", nextbutton="Start!", hintsolved=puzzlecount,textENABLED="none", bigtextL="TimTim christmas puzzle", mediumtextL="Solve the hints and find your christmas gift :) ")



@app.route('/start' ,methods=['GET', 'POST'])
def start():
    #Retrieve current hint
    maxhit = gethintn()
    puzzlecount = "Solved {}/14 puzzles".format(maxhit)
    #Default values for strings
    bigtext = "Puzzle n{}".format(int(maxhit))
    mediumtext = hints[maxhit]
    return render_template('index.html', hint=hint,hintnumber=hintnumber, backbutton="",nextbutton="Validate", hintsolved=puzzlecount, bigtextL=bigtext, mediumtextL=mediumtext)

@app.route('/next', methods=['GET', 'POST'])
def next():
    text = request.form['text']
    hitn = request.args.get("hintnumber")
    #Default values for strings
    maxhit = gethintn()
    puzzlecount = "Solved {}/14 puzzles".format(maxhit)
    bigtext = "Puzzle n{}".format(int(hitn))
    mediumtext = hints[hitn]
    resultText = ""
    nextbutton = "Next" if (int(hitn)+1)<=int(maxhit) else "Validate"

    #Checks is okay to solve hint today
    basedate = "22/11/2019 4:00"
    basedate = datetime.datetime.strptime(basedate, "%d/%m/%Y %H:%M")
    CurrentDate = datetime.datetime.now()
    basedate = basedate + timedelta(days=int(hitn)) 

    
    if(CurrentDate<basedate):
        resultText = "Too soon to solve the hint, wait {0} hours".format( str(round((basedate-CurrentDate).seconds/60/60, 2)) )
        return render_template('index.html', hint=hint,hintnumber=int(hitn), backbutton="",nextbutton=nextbutton, hintsolved=puzzlecount, bigtextL=bigtext, mediumtextL=mediumtext, result=resultText)

    #processing
    processed_text = text.lower().strip()
    result = checkAnswer(processed_text,hitn)
    resultText = "WRONG ANSWER TIMTIM"
    if(result):
        hitn = increasehitn(hitn)
        bigtext = "Puzzle n{}".format(int(hitn))
        mediumtext = hints[hitn]
        resultText = "CORRECT ANSWER TIMTIM"
    elif(int(hitn)<int(maxhit)):
        result=True
        hitn = str(int(hitn)+1)
        bigtext = "Puzzle n{}".format(int(hitn))
        mediumtext = hints[hitn]
        hintnumber=int(hitn)
        resultText=""
        return render_template('index.html', hint=hint,hintnumber=hitn, backbutton="",nextbutton=nextbutton, hintsolved=puzzlecount, bigtextL=bigtext, mediumtextL=mediumtext, result=resultText)
        
    return render_template('index.html', hint=hint,hintnumber=hitn, backbutton="",nextbutton=nextbutton, hintsolved=puzzlecount, bigtextL=bigtext, mediumtextL=mediumtext, result=resultText)

@app.route('/previous', methods=['GET', 'POST'])
def previous():
    hintnumber = request.args.get("hintnumber")
    newhint = int(hintnumber) - 1
    newhint = newhint if newhint>=1 else 1
    maxhit = gethintn()
    puzzlecount = "Solved {}/14 puzzles".format(maxhit)
    nextbutton = "Next" if int(newhint)<int(maxhit) else "Validate"
    hintnumber = str(newhint)
    #Default values for strings
    bigtext = "Puzzle n{}".format(int(hintnumber))
    mediumtext = hints[hintnumber]
    resultText = ""
    return render_template('index.html', hint=hint,hintnumber=hintnumber, backbutton="",nextbutton=nextbutton, hintsolved=puzzlecount, bigtextL=bigtext, mediumtextL=mediumtext, result=resultText)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80,debug=True)