from flask import Flask, request, render_template, current_app, send_from_directory
import utils
import time
import json

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/predict", methods=['POST'])
def result():
    global name
    classification_type = request.form['radio1']
    sub_type = request.form['radio2']

    if sub_type == 'Sequence':
        seq = request.form['seq']
        name = utils.save_seq(seq, type=classification_type)
    elif sub_type == 'Fasta':
        if request.files.get('fasta'):
            fasta = request.files['fasta']
            name = utils.save_fasta(fasta, type=classification_type)
            if not name:
                return render_template("home.html", alert=True)

    if utils.transfer(name):
        with open(utils.DIR_RESPONSES + name + '.json') as json_file:
            data = json.load(json_file)
        if sub_type == 'Sequence':
            data = data[0]
            data['tfaverage'] = utils.floor(data['tfaverage'])
            data['tfpmmedian'] = utils.floor(data['tfpmmedian'])
            return render_template("result.html", seq=True, result=data, name=name, type=int(classification_type))
        elif sub_type == 'Fasta':
            return render_template("result.html", seq=False, name=name)


@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(utils.DIR_RESPONSES, filename + '.json', as_attachment=True)


if __name__ == "__main__":
    app.run()
