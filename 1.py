from  flask import Flask, render_template
app=Flask(__name__)

@app.route("/")# end point
def home():
    return render_template('index.html')
@app.route("/about")# end point ut
def about():

    return render_template('about.html')#name2 can be any word which is used in html file about
@app.route("/bootstrap")# end point ut
def bootstrap():
    name="utkarsh"
    return render_template('bootstrap.html')

app.run(debug=True)