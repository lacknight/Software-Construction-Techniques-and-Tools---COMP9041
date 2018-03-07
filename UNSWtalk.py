import os
from flask import Flask, render_template, session, request, flash, jsonify, redirect, url_for, g
import collections, operator, re, uuid, sqlite3
from datetime import datetime
global login_zid

def current_time():
    now = datetime.now()
    current_time = now.strftime('%Y-%m-%dT%H:%M:%S+0000')
    return current_time

students_dir = "dataset-medium"

app = Flask(__name__, static_folder='', static_url_path='')


@app.route('/', methods=['GET', 'POST'])
def init():
    return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    login_zid = ''
    return 'You are logout'
    # return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        zid = request.form['zid']
        password = request.form['password']
        student_detail = get_student_detail(zid)
        if student_detail and student_detail[1] == password:
            login_zid = zid
            img_path = get_student_img(zid)
            message_list = get_message(zid)
            friend_list = get_friend_list(student_detail[-1])
            return render_template('index.html', student_info=student_detail, img=img_path, friend_list=friend_list, message_list=message_list)
        else:
            print("wrong")
            # flash('Bad username or password.')
            return render_template('login.html')

@app.route('/guide', methods=['GET','POST'])
def guide():
    zid = request.args.get('zid')
    student_detail = get_student_detail(zid)
    img_path = get_student_img(zid)
    message_list = get_message(zid)
    friend_list = get_friend_list(student_detail[-1])
    return render_template('guide.html', student_info=student_detail, img=img_path, friend_list=friend_list, message_list=message_list)

@app.route('/search_friend', methods=['GET','POST'])
def search_friend():
    friend_id = request.form['search']
    print(friend_id)
    friend_list = get_search_friend(friend_id)
    print(friend_list)
    return render_template('search_friend.html', friend_list=friend_list)

@app.route('/search_message', methods=['GET','POST'])
def search_message():
    message_word = request.form['search_message']
    # print(friend_id)
    message_list = get_search_message(message_word)
    return render_template('search_message.html', message_list=message_list)

@app.route('/post', methods=['GET','POST'])
def post():
    new_message = request.form.get('new_message', '')
    new_comment = request.form.get('new_comment', '')
    new_reply = request.form.get('new_reply','')
    zid = request.form.get('zid', '')
    mid = request.form.get('mid', '')
    cid = request.form.get('cid', '')
    print(new_message)
    print(zid)
    if new_message:
        add_new_message(zid, new_message)
        student_detail = get_student_detail(zid)
        img_path = get_student_img(zid)
        message_list = get_message(zid)
        friend_list = get_friend_list(student_detail[-1])
        return render_template('index.html', student_info=student_detail, img=img_path, friend_list=friend_list, message_list=message_list)
    if new_comment:
        add_new_comment(login_zid, mid, new_comment)
        student_detail = get_student_detail(zid)
        img_path = get_student_img(zid)
        message_list = get_message(zid)
        friend_list = get_friend_list(student_detail[-1])
        if zid != login_zid:
            return render_template('guide.html', student_info=student_detail, img=img_path, friend_list=friend_list, message_list=message_list)
        else:
            return render_template('index.html', student_info=student_detail, img=img_path, friend_list=friend_list, message_list=message_list)

    if new_reply:
        add_new_reply(login_zid, cid, mid, new_reply)
        student_detail = get_student_detail(zid)
        img_path = get_student_img(zid)
        message_list = get_message(zid)
        friend_list = get_friend_list(student_detail[-1])
        if zid != login_zid:
            return render_template('guide.html', student_info=student_detail, img=img_path, friend_list=friend_list, message_list=message_list)
        else:
            return render_template('index.html', student_info=student_detail, img=img_path, friend_list=friend_list, message_list=message_list)

@app.route('/delete', methods=['GET','POST'])
def delete():
    old_message = request.form.get('old_message', '')
    old_comment = request.form.get('old_comment', '')
    old_reply = request.form.get('old_reply','')
    zid = request.form.get('zid', '')
    mid = request.form.get('mid', '')
    cid = request.form.get('cid', '')
    rid = request.form.get('rid', '')
    if old_message:
        deleter_message(mid, old_message)
        student_detail = get_student_detail(zid)
        img_path = get_student_img(zid)
        message_list = get_message(zid)
        friend_list = get_friend_list(student_detail[-1])
        if zid != login_zid:
            return render_template('guide.html', student_info=student_detail, img=img_path, friend_list=friend_list, message_list=message_list)
        else:
            return render_template('index.html', student_info=student_detail, img=img_path, friend_list=friend_list, message_list=message_list)
    if old_comment:
        delete_comment(cid, mid, old_comment)
        student_detail = get_student_detail(zid)
        img_path = get_student_img(zid)
        message_list = get_message(zid)
        friend_list = get_friend_list(student_detail[-1])
        if zid != login_zid:
            return render_template('guide.html', student_info=student_detail, img=img_path, friend_list=friend_list, message_list=message_list)
        else:
            return render_template('index.html', student_info=student_detail, img=img_path, friend_list=friend_list, message_list=message_list)

    if old_reply:
        delete_reply(rid, cid, mid, old_reply)
        student_detail = get_student_detail(zid)
        img_path = get_student_img(zid)
        message_list = get_message(zid)
        friend_list = get_friend_list(student_detail[-1])
        if zid != login_zid:
            return render_template('guide.html', student_info=student_detail, img=img_path, friend_list=friend_list, message_list=message_list)
        else:
            return render_template('index.html', student_info=student_detail, img=img_path, friend_list=friend_list, message_list=message_list)

@app.route('/detail_change', methods=['GET','POST'])
def detail_change():
    zid = request.form.get('zid', '')
    full_name = request.form.get('full_name', '')
    brithday = request.form.get('brithday', '')
    email = request.form.get('email', '')
    program = request.form.get('course', '')
    home = request.form.get('home', '')
    conn = sqlite3.connect('data.db', detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
    c = conn.cursor()
    if full_name:
        c.execute('UPDATE STUDENT SET FULL_NAME=? WHERE ZID=?',(full_name,zid))
    if brithday:
        c.execute('UPDATE STUDENT SET EMAIL=? WHERE ZID=?',(brithday,zid))
    if email:
        c.execute('UPDATE STUDENT SET BRITHDAY=? WHERE ZID=?',(email,zid))
    if program:
        c.execute('UPDATE STUDENT SET PROGRAM=? WHERE ZID=?',(program,zid))
    if home:
        c.execute('UPDATE STUDENT SET HOME_SUBURB=? WHERE ZID=?',(home,zid))
    conn.commit()
    conn.close()
    zid = request.args.get('zid')
    student_detail = get_student_detail(zid)
    img_path = get_student_img(zid)
    message_list = get_message(zid)
    friend_list = get_friend_list(student_detail[-1])
    return render_template('index.html', student_info=student_detail, img=img_path, friend_list=friend_list, message_list=message_list)



def get_student_detail(id):
    conn = sqlite3.connect('data.db', detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
    c = conn.cursor()
    student_detail = []
    zid = (id,)
    for row in c.execute('SELECT * FROM STUDENT WHERE ZID=?', zid):
        student_detail = [row[1],row[2],row[3],row[4],row[5],row[7],row[9],row[11]]
    conn.close()
    return student_detail

def get_student_img(id):
    conn = sqlite3.connect('data.db', detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
    c = conn.cursor()
    img_path = ''
    zid = (id,)
    for row in c.execute('SELECT * FROM IMG WHERE ZID=?', zid):
        img_path = row[2]
    conn.close()
    return img_path

def get_friend_list(friends):
    conn = sqlite3.connect('data.db', detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
    c = conn.cursor()
    friend_list = []
    for friend in friends.strip('()').split(', '):
        friend_detail = get_student_detail(friend)
        friend_img = get_student_img(friend)
        current_friend_detail = [friend_detail[0], friend_detail[2], friend_img]
        friend_list.append(current_friend_detail)
    conn.close()
    return friend_list

def get_message(id):
    conn = sqlite3.connect('data.db', detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
    c = conn.cursor()
    message_list = []
    zid = (id,'%'+id+'%','%'+id+'%', '%'+id+'%')
    for row in c.execute('SELECT MESSAGE.MID, MESSAGE.MFROM, STUDENT.FULL_NAME, MESSAGE.MESSAGE, MESSAGE.TIME FROM MESSAGE, STUDENT WHERE MESSAGE.MID IN (SELECT MID FROM MESSAGE WHERE MFROM=? UNION SELECT MID FROM COMMENT WHERE MESSAGE LIKE ? UNION SELECT MID FROM MESSAGE WHERE MESSAGE LIKE ? UNION SELECT MID FROM REPLY WHERE MESSAGE LIKE ?) AND MESSAGE.MFROM=STUDENT.ZID ORDER BY MESSAGE.TIME DESC',zid):
        each_message = [row[0], row[1], row[2], row[3], row[4]]
        comment_list = get_comment(row[0])
        each_message.append(comment_list)
        message_list.append(each_message)
    conn.close()
    return message_list

def get_comment(id):
    conn = sqlite3.connect('data.db', detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
    c = conn.cursor()
    comment_list = []
    mid = (id,)
    for row in c.execute('SELECT CID, MID, CFROM, MESSAGE, TIME FROM COMMENT WHERE MID=? ORDER BY TIME DESC',mid):
        each_message = [row[0], row[1], row[2],row[3], row[4]]
        reply_list = get_reply(row[0])
        each_message.append(reply_list)
        comment_list.append(each_message)
    conn.close()
    return comment_list

def get_reply(id):
    conn = sqlite3.connect('data.db', detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
    c = conn.cursor()
    reply_list = []
    mid = (id,)
    for row in c.execute('SELECT RID, CID, MID, RFROM, MESSAGE, TIME FROM REPLY WHERE CID=? ORDER BY TIME DESC',mid):
        each_message = [row[0], row[1], row[2],row[3], row[4], row[5]]
        reply_list.append(each_message)
    conn.close()
    return reply_list

def get_search_friend(id):
    conn = sqlite3.connect('data.db', detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
    c = conn.cursor()
    friend_list = []
    zid = ('%'+id+'%',)
    for row in c.execute('SELECT STUDENT.ZID, STUDENT.FULL_NAME, IMG.PATH FROM STUDENT, IMG WHERE STUDENT.FULL_NAME LIKE ? AND STUDENT.ZID = IMG.ZID', zid):
        each_message = [row[0], row[1], row[2]]
        friend_list.append(each_message)
    conn.close()
    return friend_list

def get_search_message(id):
    conn = sqlite3.connect('data.db', detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
    c = conn.cursor()
    message_list = []
    zid = ('%'+id+'%',)
    for row in c.execute('SELECT MESSAGE.MFROM, STUDENT.FULL_NAME, MESSAGE.MESSAGE, MESSAGE.TIME FROM STUDENT, MESSAGE WHERE MESSAGE.MESSAGE LIKE ? AND STUDENT.ZID=MESSAGE.MFROM', zid):
        each_message = [row[0], row[1], row[2], row[3]]
        message_list.append(each_message)
    conn.close()
    return message_list

def add_new_message(id, message):
    conn = sqlite3.connect('data.db', detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
    c = conn.cursor()
    time = current_time()
    if message:
        for row in c.execute('SELECT MAX(MID) FROM MESSAGE'):
            mid = row[0] + 1
        message_tuple = (mid,id,'','',message,time)
        print(message_tuple)
        c.execute('INSERT INTO MESSAGE VALUES (?,?,?,?,?,?)',message_tuple)
        for row in c.execute('SELECT MAX(MID) FROM MESSAGE'):
            print(row)
    conn.commit()
    conn.close()

def add_new_comment(id, mid, message):
    conn = sqlite3.connect('data.db', detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
    c = conn.cursor()
    time = current_time()
    if message:
        for row in c.execute('SELECT MAX(CID) FROM COMMMENT'):
            cid = row[0] + 1
        message_tuple = (cid, mid,id,message,time)
        print(message_tuple)
        c.execute('INSERT INTO COMMENT VALUES (?,?,?,?,?)',message_tuple)
        for row in c.execute('SELECT MAX(CID) FROM COMMENT'):
            print(row)
    conn.commit()
    conn.close()

def add_new_reply(id, cid, mid, message):
    conn = sqlite3.connect('data.db', detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
    c = conn.cursor()
    time = current_time()
    if message:
        for row in c.execute('SELECT MAX(RID) FROM REPLY'):
            rid = row[0] + 1
        message_tuple = (rid, cid, mid,id,message,time)
        print(message_tuple)
        c.execute('INSERT INTO REPLY VALUES (?,?,?,?,?,?)',message_tuple)
        for row in c.execute('SELECT MAX(RID) FROM REPLY'):
            print(row)
    conn.commit()
    conn.close()

def delete_message(id):
    conn = sqlite3.connect('data.db', detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
    c = conn.cursor()
    c.execute('DELETE FROM MESSAGE WHERE MID=?',id)
    c.execute('DELETE FROM COMMENT WHERE MID=?',id)
    c.execute('DELETE FROM REPLY WHERE MID=?',id)
    conn.commit()
    conn.close()

def delete_comment(cid):
    conn = sqlite3.connect('data.db', detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
    c = conn.cursor()
    c.execute('DELETE FROM COMMENT WHERE CID=?',cid)
    c.execute('DELETE FROM REPLY WHERE CID=?',cid)
    conn.commit()
    conn.close()

def delete_reply(rid):
    conn = sqlite3.connect('data.db', detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
    c = conn.cursor()
    c.execute('DELETE FROM REPLY WHERE RID=?',rid)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    app.run(debug=True)

