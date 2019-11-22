from flask import Flask, flash, redirect, render_template, request, session, abort
from random import randint
import datetime
from datetime import timedelta 


app = Flask(__name__, template_folder='templates')




hints = {
    "1": "What is 1+1",
    "2": "What is 2+2"
}

hintsAnswers = {
    "1": "2",
    "2": "4"
}


CurrentDate = datetime.datetime.now()
def gethintn():
    try:
        f = open("demofile.txt", "r")
        hintnumber = f.readline()
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
hint = hints[hintnumber]


@app.route('/')
def index():
    return render_template('index.html',hint=hint,hintnumber=hintnumber)

@app.route('/home')
def home():
    return render_template('home.html', hint=hint,hintnumber=hintnumber)
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/next', methods=['POST'])
def next():
    #Checks textbox to see if the answer is corret
    text = request.form['text']
    hitn = request.args.get("hintnumber")
    
    #Checks is okay to solve hint today
    basedate = "14/12/2019 4:00"
    basedate = datetime.datetime.strptime(basedate, "%d/%m/%Y %H:%M")
    CurrentDate = datetime.datetime.now()
    basedate = basedate + timedelta(days=int(hitn)) 
    if(CurrentDate<basedate and False):
        resultText = "Too soon to solve the hint, wait {0} hours".format( (basedate-CurrentDate).seconds/60 )
        return render_template('home.html',hint=hints[hitn], hintnumber=hitn, result=resultText)

    #processing
    processed_text = text.lower().strip()
    result = checkAnswer(processed_text,hitn)
    maxhit = gethintn()
    resultText = "WRONG ANSWER TIMTIM"
    if(result):
        hitn = increasehitn(hitn)
        resultText = "CORRECT ANSWER TIMTIM"
        return render_template('home.html',hint=hints[hitn], hintnumber=hitn, result=resultText)
    if (hitn<maxhit):
        result=True
        hitn = increasehitn(hitn)
        resultText=""
        return render_template('home.html',hint=hints[hitn], hintnumber=hitn, result=resultText)
    return render_template('home.html',hint=hints[hitn], hintnumber=hitn, result=resultText)
    

@app.route('/previous', methods=['POST'])
def previous():
    hintnumber = request.args.get("hintnumber")
    newhint = int(hintnumber) - 1
    newhint = newhint if newhint>=1 else 1
    hintnumber = str(newhint)
    #text = request.form['text']
    #processed_text = text.upper()
    return render_template('home.html',hint=hints[hintnumber],hintnumber=hintnumber)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80,debug=True)