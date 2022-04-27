from crypt import methods
import mysql.connector
from flask import *

app = Flask(__name__)

conn = mysql.connector.connect(host="localhost",user="onkar",password="***********",database="dbms_mini_project")
mycursor = conn.cursor()
######################## Functions
def check_login(token,page):
    if token!='1':
        return '<script>function Redirect(){window.location = "{}";}document.write("Please login to your account. Redirecting to login page");setTimeout(\'Redirect()\', 5000);</script>'.format(page)
    else:
        return 1


def write_file(data, dir):
    data1 = ""
    for x in data:
        for i in x:
            data1 = data1 +  str(i) +" "
        data1 = data1 + '\n'
    return render_template("sql_output.html",output=data1)
    

######################## Employee Code
@app.route("/")
def index():
    return render_template("index.html")#Explain about project details

@app.route("/register.html", methods=['GET', 'POST'])
def register():                                        
    if request.method == 'GET':
        return render_template("register.html")
    if request.method == 'POST':
        comp_email = request.form['email']
        comp_id = request.form['company_id']
        emp_id = request.form['employee_id']
        password = request.form['password']
        query = 'insert into Employee values("'+emp_id+'","'+comp_email+'","'+comp_id+'","'+password+'");'
        try:
            mycursor.execute(query)
            conn.commit()
            query = 'update Company set employee_count = employee_count+1 where company_id = "'+comp_id+'";'
            mycursor.execute(query)
            conn.commit()
            return """<script>function Redirect() {
               window.location = "/login.html";
            }            
            document.write("You will be redirected to login page in 10 sec.");
            setTimeout('Redirect()', 5000);</script>"""
        except mysql.connector.errors.IntegrityError or mysql.connector.errors.get_mysql_exception:
            return render_template("register.html",error="Please chack your credentials. Something went wrong!!!")

@app.route("/login.html", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    if request.method == 'POST':
        emp_id = request.form['ID']
        comp_id = request.form['comp_id']
        password = request.form['password']
        query = 'select employee_id,pass from Employee where employee_id="'+emp_id+'" and pass="'+password+'" and company_id="'+comp_id+'";'
        mycursor.execute(query)
        data = mycursor.fetchall()
        if len(data)==0:
            return render_template("login.html",error="Wrong Credentials")
        if data[0][0]==emp_id and data[0][1]==password:
            resp = make_response(render_template("redirect.html"))
            resp.set_cookie('Emplaoyee_login','1')
            resp.set_cookie('Company_id',comp_id)
            return resp
        

@app.route("/createbug.html",methods=['GET', 'POST'])
def createbug():
    token = request.cookies.get('Emplaoyee_login')
    val = check_login(token,"/login.html")
    if val != 1:
        return val
    if request.method == 'GET':
        return render_template("createbug.html")
    if request.method == 'POST':
        emp_id = request.form['emp_id']
        comp_id = request.form['comp_id']
        model_id = request.form['model_id']
        bug_id = request.form['bug_id']
        bug_ststus = request.form['bug_status']
        bug_steps = request.form['bug_steps']
        bug_link = request.form['bug_link']
        query = 'insert into Bug_Track values("'+bug_id+'","'+bug_steps+'","'+bug_link+'","'+bug_ststus+'","'+comp_id+'","'+emp_id+'","'+model_id+'");'
        try:
            mycursor.execute(query)
            conn.commit()
            return """<script>function Redirect() {
               window.location = "/dashboard.html";
            }            
            document.write("You will be redirected to dashboard page in 10 sec.");
            setTimeout('Redirect()', 5000);</script>"""
        except mysql.connector.errors.IntegrityError or mysql.connector.errors.get_mysql_exception:
            return render_template("createbug.html",error="Please enter correct details. Something went wrong!!!")

@app.route("/updatebug.html",methods=['GET', 'POST'])
def updatebug():
    token = request.cookies.get('Emplaoyee_login')
    val = check_login(token,"/login.html")
    if val != 1:
        return val
    if request.method == 'GET':
        return render_template("updatebug.html")
    if request.method == 'POST':
        model_id = request.form['model_id']
        bug_id = request.form['bug_id']
        bug_status = request.form['bug_status']
        query = 'update Bug_Track set bug_status="'+bug_status+'" where model_id="'+model_id+'" and bug_id="'+bug_id+'";'
        try:
            mycursor.execute(query)
            conn.commit()
            return """<script>function Redirect() {
               window.location = "/dashboard.html";
            }            
            document.write("You will be redirected to dashboard page in 10 sec.");
            setTimeout('Redirect()', 5000);</script>"""
        except mysql.connector.errors.IntegrityError or mysql.connector.errors.get_mysql_exception:
            return render_template("createbug.html",error="Please enter correct details. Something went wrong!!!")

@app.route("/viewbugsemp.html")
def viewbugsemp():
    token = request.cookies.get('Emplaoyee_login')
    val = check_login(token,"/login.html")
    if val != 1:
        return val
    comp_id = request.cookies.get('Company_id')
    query = 'select * from Bug_Track where company_id="'+comp_id+'";'
    mycursor.execute(query)
    data = mycursor.fetchall()
    return write_file(data,'/dashboard_employee.html')


@app.route("/dashboard.html")
def dashboard():
    return render_template("dashboard_employee.html")




################################ Company code






@app.route("/register_company.html", methods=['GET', 'POST'])
def register_company():
    if request.method == 'GET':
        return render_template("register_company.html")
    if request.method == 'POST':
        comp_email = request.form['email']
        comp_name = request.form['name']
        comp_id = request.form['company_id']
        password = request.form['password']
        query = 'insert into Company values("'+comp_id+'","'+comp_name+'","'+comp_email+'",0,"'+password+'");'
        try:
            mycursor.execute(query)
            conn.commit()
            return """<script>function Redirect() {
               window.location = "/login_company.html";
            }            
            document.write("You will be redirected to login page in 10 sec.");
            setTimeout('Redirect()', 5000);</script>"""
        except mysql.connector.errors.IntegrityError or mysql.connector.errors.get_mysql_exception:
            return render_template("register_company.html",error="Please chack your credentials. Something went wrong!!!")

@app.route("/login_company.html",methods=['GET', 'POST'])
def login_company():
    if request.method == 'GET':
        return render_template("login_company.html")
    if request.method == 'POST':
        comp_id = request.form['ID']
        password = request.form['password']
        query = 'select company_id,password_comp from Company where company_id="'+comp_id+'" and password_comp="'+password+'";'
        mycursor.execute(query)
        data = mycursor.fetchall()
        if len(data)==0:
            return render_template("login_company.html",error="Wrong Credentials")
        if data[0][0]==comp_id and data[0][1]==password:
            resp = make_response(render_template("dashboard_company.html"))
            resp.set_cookie('Company_login','1')
            resp.set_cookie('Company_id',comp_id)
            return resp

@app.route("/dashboard_company.html")
def dashboard_company():
    return render_template("dashboard_company.html")


@app.route("/viewemployee.html", methods=['GET', 'POST'])
def viewemployee():
    token = request.cookies.get('Company_login')
    val = check_login(token,"/login_company.html")
    if val != 1:
        return val
    comp_id = request.cookies.get('Company_id')
    query = 'select employee_id,employee_email from Employee where company_id="'+comp_id+'";'
    mycursor.execute(query)
    data = mycursor.fetchall()
    return write_file(data,"/dashboard_company.html")
    

@app.route("/removeemployee.html", methods=['GET', 'POST'])
def removeemployee():
    token = request.cookies.get('Company_login')
    val = check_login(token,"/login_company.html")
    if val != 1:
        return val
    comp_id = request.cookies.get('Company_id')

    if request.method == 'GET':
        return render_template("removeemployee.html")
    if request.method == 'POST':
        emp_id = request.form['emp_id']
        query = 'delete from Employee where employee_id="'+emp_id+'" and company_id="'+comp_id+'";'
        try:
            mycursor.execute(query)
            conn.commit()
            return render_template("removeemployee.html",error="Employee removed")
        except mysql.connector.errors.IntegrityError or mysql.connector.errors.get_mysql_exception:
            return render_template("removeemployee.html",error="Employee Linked to different tables. Please contact support!!!")

@app.route("/viewbugs.html", methods=['GET', 'POST'])
def viewbugs():
    token = request.cookies.get('Company_login')
    val = check_login(token,"/login_company.html")
    if val != 1:
        return val
    comp_id = request.cookies.get('Company_id')
    query = 'select * from Bug_Track where company_id="'+comp_id+'";'
    mycursor.execute(query)
    data = mycursor.fetchall()
    return write_file(data,"/dashboard_company.html")

@app.route("/addmodel.html", methods=['GET', 'POST'])
def addmodel():
    token = request.cookies.get('Company_login')
    val = check_login(token,"/login_company.html")
    if val != 1:
        return val
    comp_id = request.cookies.get('Company_id')
    if request.method == 'GET':
        return render_template("addmodel.html")
    if request.method == 'POST':
        model_id = request.form['model_id']
        model_name = request.form['model_name']
        query = 'insert into Models values("'+model_id+'","'+model_name+'","'+comp_id+'",0);'
        try:
            mycursor.execute(query)
            conn.commit()
            return render_template("addmodel.html",error="Module added")
        except mysql.connector.errors.IntegrityError or mysql.connector.errors.get_mysql_exception:
            return render_template("addmodel.html",error="Please chack your model id. Contact Support!!!")

@app.route("/viewmodels.html", methods=['GET', 'POST'])
def viewmodels():
    token = request.cookies.get('Company_login')
    val = check_login(token,"/login_company.html")
    if val != 1:
        return val
    comp_id = request.cookies.get('Company_id')
    query = 'select * from Models where company_id="'+comp_id+'";'
    mycursor.execute(query)
    data = mycursor.fetchall()
    return write_file(data,"/dashboard_company.html")

@app.route("/removemodel.html", methods=['GET', 'POST'])
def removemodel():
    token = request.cookies.get('Company_login')
    val = check_login(token,"/login_company.html")
    if val != 1:
        return val
    comp_id = request.cookies.get('Company_id')

    if request.method == 'GET':
        return render_template("removemodel.html")
    if request.method == 'POST':
        model_id = request.form['model_id']
        query = 'delete from Models where model_id="'+model_id+'" and company_id="'+comp_id+'";'
        try:
            mycursor.execute(query)
            conn.commit()
            return render_template("removemodel.html",error="Model removed")
        except mysql.connector.errors.IntegrityError or mysql.connector.errors.get_mysql_exception:
            return render_template("removemodel.html",error="Model Linked to bug table. Please contact support!!!")

if __name__ == "__main__":
    app.run("127.0.0.1",8080)
