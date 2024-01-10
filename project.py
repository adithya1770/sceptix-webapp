from flask import Flask,render_template,request,redirect,url_for
import numpy as np
import pymysql
from flask_bcrypt import Bcrypt
import random

app=Flask(__name__)
bcrypt=Bcrypt(app)

@app.route("/",methods=['POST','GET'])
def auth():
    n,p="",""
    sign_n,sign_p="",""
    credential=""
    if request.method=="POST":
        n=request.form['n']
        p=request.form['p']
        sign_n=request.form['sign_n']
        sign_p=request.form['sign_p']
        mydb=pymysql.connect(host='adithya69.mysql.pythonanywhere-services.com',user='adithya69',password='mnadi123',database='adithya69$openmath')
        cur=mydb.cursor()
        if bool(sign_n) and bool(sign_p):
            q="insert into creds values('{}','{}')".format(sign_n,sign_p)
            cur.execute(q)
            mydb.commit()
            return "<h1><big><center>Sign Up Successful, Credentials stored in database, Return to Authorisation Page to login</center></big></h1>"
        else:
            q="select * from creds;"
            cur.execute(q)
            credential=cur.fetchall()
            pw_hash = bcrypt.generate_password_hash(p).decode('utf-8')
            user_hash = bcrypt.generate_password_hash(n).decode('utf-8')
        if (n,p) in credential:
                if bcrypt.check_password_hash(pw_hash,p)==True and bcrypt.check_password_hash(user_hash,n)==True:
                    q1="insert into login values('{}')".format(n)
                    cur.execute(q1)
                    mydb.commit()
                    return redirect(url_for('home',user_hash=user_hash,pw_hash=pw_hash))
        else:
            return render_template("errorinpsw.html")
    return render_template('auth.html',n=n,p=p)

@app.route("/num",methods=['POST','GET'])
def num():
    try:
        Rand_no=0
        if request.method=="POST":
            Rand_no+=random.randrange(int(request.form['start']),int(request.form['end']))
        return render_template("numgen.html",Rand_no=Rand_no)
    except:
        return render_template("error.html")

@app.route("/eign",methods=['GET','POST'])
def eign():
        r=""
        evalue=""
        evect=""
        if request.method=="POST":
             r=np.array(eval(request.form['e']))
             evalue,evect=np.linalg.eig(r)
        return render_template("eigen.html",evalue=evalue,r=r,evect=evect)

@app.route("/learn",methods=['POST','GET'])
def learn():
    return render_template("vids.html")

@app.route("/rules",methods=['POST','GET'])
def rules():
    return render_template("rules.html")

@app.route("/info",methods=['POST','GET'])
def info():
    return render_template("terms.html")

@app.route("/reset",methods=['POST','GET'])
def delete():
    use=""
    new=""
    if request.method=="POST":
        use=request.form['use']
        new=request.form['new']
        mydb=pymysql.connect(host='adithya69.mysql.pythonanywhere-services.com',user='adithya69',password='mnadi123',database='adithya69$openmath')
        cur=mydb.cursor()
        q="UPDATE creds SET password =%s WHERE user =%s;"
        r=(new,use)
        cur.execute(q,r)
        mydb.commit()
        if bool(use) and bool(new):
            return "<h1><center><i>Password Updated Successfully!</i></center></h1>"
    return render_template("reset.html",use=use,new=new)


@app.route("/delete",methods=['POST','GET'])
def reset():
    use=""
    if request.method=="POST":
        use=request.form['use']
        mydb=pymysql.connect(host='adithya69.mysql.pythonanywhere-services.com',user='adithya69',password='mnadi123',database='adithya69$openmath')
        cur=mydb.cursor()
        q="DELETE FROM creds WHERE user=%s;"
        r=(use)
        cur.execute(q,r)
        mydb.commit()
        if bool(use):
            return "<h1><center><i>Account Deleted Successfully!</i></center></h1>"
    return render_template("delete.html",use=use)

@app.route("/forgot",methods=['POST','GET'])
def forgot():
    use=""
    data=""
    r=""
    single_data=""
    if request.method=='POST':
        use=request.form['use']
        mydb=pymysql.connect(host='adithya69.mysql.pythonanywhere-services.com',user='adithya69',password='mnadi123',database='adithya69$openmath')
        cur=mydb.cursor()
        q="SELECT password FROM creds WHERE user=%s;"
        r=(use,)
        cur.execute(q,r)
        mydb.commit()
        single_data=cur.fetchone()
        data=single_data[0]
    return render_template("forgotpassword.html",data=data,use=use,r=r)

@app.route("/calc",methods=['POST','GET'])
def calc():
    exp1=""
    result=""
    try:
        if request.method=="POST":
            exp1=request.form['exp']
            result=eval(exp1)
        return render_template("calc.html",exp1=exp1,result=result)
    except:
        return render_template("error.html")

@app.route("/home",methods=['POST','GET'])
def home():
    comments,nam="",""
    name,feed="",""
    count=""
    nu=""
    count=""
    name_User=""
    name_1=""
    mydb=pymysql.connect(host='adithya69.mysql.pythonanywhere-services.com',user='adithya69',password='mnadi123',database='adithya69$openmath')
    cur=mydb.cursor()
    if request.method=="POST":
        name=request.form['name']
        feed=request.form['feed']
        q="INSERT INTO feedback VALUES('{}','{}')".format(name,feed)
        cur.execute(q)
        mydb.commit()
        q1="SELECT * from feedback;"
        cur.execute(q1)
        comments=cur.fetchall()
        for i in comments:
                nam=i[0]
                comments=i[1]
    cur.execute("SELECT COUNT(*) FROM login;")
    mydb.commit()
    nu=cur.fetchone()
    count=nu[0]
    cur.execute("select * from login;")
    mydb.commit()
    name_1=cur.fetchall()
    length=len(name_1)
    name_User=name_1[length-1][0]
    cur.close()
    return render_template("buttons.html",comments=comments,nam=nam,count=count,nu=nu,name_User=name_User,name_1=name_1)

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
    try:
        if request.method=="POST":
            mat1=np.array(eval(request.form['mat1']))
            mat2=np.array(eval(request.form['mat2']))
            result=np.dot(mat1,mat2)
        return render_template("multi.html",result=result)
    except:
        return render_template('error.html')

@app.route("/rank",methods=["POST","GET"])
def rank():
    mat=""
    result=""
    try:
        if request.method=="POST":
            mat=np.array(eval(request.form['mat1']))
            result=np.linalg.matrix_rank(mat)
        return render_template("rank.html",result=result)
    except:
        return render_template("error.html")

@app.route("/inverse",methods=["POST","GET"])
def inverse():
    mat=""
    result=""
    try:
        if request.method=="POST":
            mat=np.array(eval(request.form['mat1']))
            result=np.linalg.inv(mat)
        return render_template("inverse.html",matrix=mat,result=result)
    except:
        return render_template("error.html")

@app.route("/deter",methods=["POST","GET"])
def deter():
    mat=""
    det=""
    result=""
    try:
        if request.method=="POST":
            mat=np.array(eval(request.form['mat1']))
            result=np.linalg.det(mat)
        return render_template("front.html",matrix=mat,result=result)
    except:
        return render_template("error.html")

if __name__=="__main__":
    app.run(debug=True)
