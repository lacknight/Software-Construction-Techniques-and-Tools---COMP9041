from flask import Flask
from flask import request,render_template

app = Flask(__name__)

# @app.route('/', methods=['GET', 'POST'])
# def home():
#     return '<h1>Home</h1>'
@app.route('/', methods =['GET','POST'])
def init():
    return render_template('login.html')

@app.route('/login', methods =['POST'])
def login():

    # zid = request.form.get('zid', '')
    # password = request.form.get('password', '')
    zid = request.form['zid']
    password = request.form['password']

    # sql = 'select * from students where zid="'+zid+'"'
    # cur = query(sql)
    # s_tuple = cur.fetchone()
    # sql = 'SELECT * FROM STUDENT WHERE ZID = '
    student_detail = c.execute('SELECT * FROM STUDENT WHERE ZID = "+ zid +"')
    if not student_detail:
        flash('Bad username or password.')
        return render_template('login.html')
    else:
        for row in student_detail:
            student_password = row[2]
        if password != student_password:
            flash('Bad username or password.')
            return render_template('login.html')
        else:
            return render_template('index.html',student_info = zid)


# @app.route('/signin', methods=['GET'])
# def signin_form():
#     return '''<form action="/signin" method="post">
#               <p><input name="username"></p>
#               <p><input name="password" type="password"></p>
#               <p><button type="submit">Sign In</button></p>
#               </form>'''
#
# @app.route('/signin', methods=['POST'])
# def signin():
#     # 需要从request对象读取表单内容：
#     if request.form['username']=='admin' and request.form['password']=='password':
#         return '<h3>Hello, admin!</h3>'
#     return '<h3>Bad username or password.</h3>'

if __name__ == '__main__':
    app.run(debug=True)
