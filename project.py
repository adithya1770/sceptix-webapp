from flask import Flask,render_template,request
import numpy as np
import pymysql

app=Flask(__name__)

@app.route("/",methods=['POST','GET'])
def home():
    name,feed="",""
    if request.method=="POST":
        name=request.form['name']
        feed=request.form['feed']
        mydb=pymysql.connect(host='localhost',user='root',password='root',database='openmath')
        cur=mydb.cursor()
        q="INSERT INTO feedback VALUES('{}','{}')".format(name,feed)
        cur.execute(q)
        mydb.commit()
        cur.close()

    return render_template("buttons.html")

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