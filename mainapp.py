from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random
import json


app = Flask(__name__)
# Path to your JSON file
file_path = "./questions.json"
# Read and parse the JSON file 
with open(file_path, "r") as file: 
    questions = json.load(file)
    data = questions['questions']


store = []


def rand_check(rand):
    if rand['question'] in store:
        row_count = len(data)
        rand = data[(int(row_count * random.random()))]
        rand_check(rand)
    store.append(rand['question'])
    return rand


fl = ['false']


def flip_lifeline_chek(fl_uon, numQues, score):
    if fl_uon != "flun":
        if fl[0] == 'false':
            fl[0] = 'true'
            numQues -= 1
            score -= 100
    return numQues,score


@app.route('/result/<name> <score> <exqu> <ffqu> <flqu>')
def result(name,score,exqu,ffqu,flqu):
    return render_template("resultscreen.html",name=name, score=score, exQuesUsed=exqu, ffQuesUsed=ffqu, flQuesUsed=flqu)


@app.route('/gmscreen/<name> <score> <numQues> <ex_uon> <ff_uon> <fl_uon>', methods=['GET', 'POST'])
def gmscreen(name, score, numQues, ex_uon, ff_uon, fl_uon):
    numQues,score = flip_lifeline_chek(fl_uon,int(numQues),int(score))
    numQues += 1
    score += 100
    row_count = len(data)
    rand = data[(int(row_count * random.random()))]
    f_rand = rand_check(rand)
    return render_template('gamescreen.html', name=name.title(), quiz=f_rand, score=score, numQues=numQues,ex_uon=ex_uon,ff_uon=ff_uon,fl_uon=fl_uon)


@app.route('/', methods=['GET', 'POST'])
def entry():
    if request.method == 'POST':
        user = request.form['usrname']
        score = -100
        numQues = 0
        ex_uon = "exun"
        ff_uon = "ffun"
        fl_uon = "flun"
        return redirect(url_for('gmscreen', name=user, score=score,
                numQues=numQues,ex_uon=ex_uon,ff_uon=ff_uon,fl_uon=fl_uon))

    return render_template('userlogin.html')


app.run(debug=True)
