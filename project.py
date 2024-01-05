from flask import Flask,render_template,request,redirect,url_for
import numpy as np
import pymysql

app=Flask(__name__)


@app.route("/",methods=['POST','GET'])
def auth():
    n,p="",""
    if request.method=="POST":
        n=request.form['n']
        p=request.form['p']
        mydb=pymysql.connect(host='adithya69.mysql.pythonanywhere-services.com',user='adithya69',password='mnadi123',database='adithya69$openmath')
        cur=mydb.cursor()
        q="select * from creds;"
        cur.execute(q)
        credential=cur.fetchall()
        for k in credential:
            user_name=k[0]
            passwd=k[1]
        if n==user_name and p==passwd:
            return redirect(url_for('home',n=n,p=p))
        else:
            return "<h1>Enter correct password and user user:user,password:passwd</h1>"
    return render_template('auth.html',n=n,p=p)

@app.route("/learn",methods=['POST','GET'])
def learn():
    return render_template("vids.html")

@app.route("/home",methods=['POST','GET'])
def home():
    comments,nam="",""
    name,feed="",""
    if request.method=="POST":
        name=request.form['name']
        feed=request.form['feed']
        mydb=pymysql.connect(host='adithya69.mysql.pythonanywhere-services.com',user='adithya69',password='mnadi123',database='adithya69$openmath')
        cur=mydb.cursor()
        q="INSERT INTO feedback VALUES('{}','{}')".format(name,feed)
        cur.execute(q)
        mydb.commit()
        q1="SELECT * from feedback;"
        cur.execute(q1)
        comments=cur.fetchall()
        for i in comments:
                nam=i[0]
                comments=i[1]
        cur.close()
    return render_template("buttons.html",comments=comments,nam=nam)

@app.route("/quiz",methods=['POST','GET'])
def quiz():
    marks=0
    a=list()
    if request.method=="POST":
        q1_ans=request.form['yes']
        q2_ans=request.form['ans']
        q3_ans=request.form['idn']
        q1a=q1_ans
        q2a=q2_ans
        q3a=q3_ans
        if q1a in ["no","No"]:
            marks+=1
        else:
            marks-=1
        if q2a in ["-2"]:
            marks+=1
        else:
            marks-=1
        if q3a in ["1"]:
            marks+=1
        else:
            marks-=1
    return render_template("quiz.html",marks=marks)

@app.route("/multi",methods=["POST","GET"])
def multi():
    mat1=""
    mat2=""
    result=""
    if request.method=="POST":
        mat1=np.array(eval(request.form['mat1']))
        mat2=np.array(eval(request.form['mat2']))
        result=np.dot(mat1,mat2)
    return render_template("multi.html",result=result)

@app.route("/rank",methods=["POST","GET"])
def rank():
    mat=""
    result=""
    if request.method=="POST":
        mat=np.array(eval(request.form['mat1']))
        result=np.linalg.matrix_rank(mat)
    return render_template("rank.html",result=result)

@app.route("/inverse",methods=["POST","GET"])
def inverse():
    mat=""
    result=""
    if request.method=="POST":
        mat=np.array(eval(request.form['mat1']))
        result=np.linalg.inv(mat)
    return render_template("inverse.html",matrix=mat,result=result)

@app.route("/deter",methods=["POST","GET"])
def deter():
    mat=""
    det=""
    result=""
    if request.method=="POST":
        mat=np.array(eval(request.form['mat1']))
        result=np.linalg.det(mat)
    return render_template("front.html",matrix=mat,result=result)

if __name__=="__main__":
    app.run(debug=True)
