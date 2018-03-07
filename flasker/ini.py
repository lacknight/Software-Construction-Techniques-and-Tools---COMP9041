import os, re, sqlite3

conn = sqlite3.connect('data.db', detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
c = conn.cursor()
c.execute("DROP TABLE IF EXISTS STUDENT")
c.execute('''CREATE TABLE STUDENT
        (ID      INT PRIMARY KEY   NOT NULL ,
        ZID           CHAR(50)      NOT NULL ,
        PASSWORD      CHAR(50)      NOT NULL ,
        FULL_NAME     CHAR(50)      NOT NULL ,
        EMAIL         CHAR(50)      NOT NULL ,
        PROGRAM       CHAR(50)      NOT NULL ,
        HOME_LONGITUDE CHAR(50)     NOT NULL ,
        HOME_SUBURB   CHAR(50)      NOT NULL ,
        HOME_LATITUDE CHAR(50)      NOT NULL ,
        BRITHDAY      CHAR(50)      NOT NULL ,
        COURSES       CHAR(50)      NOT NULL ,
        FRIENDS       CHAR(50)      NOT NULL );''')

c.execute("DROP TABLE IF EXISTS MESSAGE")
c.execute('''CREATE TABLE MESSAGE
        (MID      INT PRIMARY KEY  NOT NULL ,
        MFROM        CHAR(50)      NOT NULL , 
        LONGITUDE   CHAR(50)               ,
        LATITUDE    CHAR(50)               ,
        MESSAGE     CHAR(50)       NOT NULL ,
        TIME        CHAR(50)       NOT NULL );''')
# FROM == ZID

c.execute("DROP TABLE IF EXISTS COMMENT")
c.execute('''CREATE TABLE COMMENT
        (CID      INT PRIMARY KEY NOT NULL ,
        MID         INT      NOT NULL ,
        CFROM        CHAR(50)     ,
        MESSAGE     CHAR(50)      ,
        TIME        CHAR(50)      );''')

c.execute("DROP TABLE IF EXISTS REPLY")
c.execute('''CREATE TABLE REPLY
        (RID      INT PRIMARY KEY NOT NULL ,
        CID         INT      NOT NULL ,
        MID         INT      NOT NULL ,
        RFROM       CHAR(50)      ,
        MESSAGE     CHAR(50)      ,
        TIME        CHAR(50)      );''')

c.execute("DROP TABLE IF EXISTS IMG")
c.execute('''CREATE TABLE IMG
        (IID      INT PRIMARY KEY NOT NULL ,
        ZID         CHAR(50)      NOT NULL ,
        PATH        CHAR(50)      );''')


# c.execute("INSERT INTO MESSAGE (MFROM, MESSAGE, TIME) VALUES (?,?,?)",(1,2,3))

student_list = []
message_list = []
comment_list = []
reply_list = []
img_list = []
zid = ''
password = ''
full_name = ''
email = ''
program = ''
home_longitude = ''
home_suburb = ''
home_latitude = ''
brithday = ''
courses = ''
friends = ''
longitude = ''
latitude = ''
message = ''
time = ''
mfrom = ''
cfrom = ''
rfrom = ''
img_path = ''


path = "dataset-medium"
data_dic = os.listdir(path)
student_id = 0
message_id = 0
comment_id = 0
reply_id = 0
img_id = 0
for student_dic in data_dic:
    z_path = path + "/" + student_dic
    if os.path.isdir(z_path):
        z_dic = os.listdir(z_path)
        img_id += 1
        img_current = (img_id, student_dic, './templates/not found.png')
        for file in z_dic:
            f_path = z_path + "/" + file
            if re.match(r'student.txt$', file):
                student_id += 1
                f = open(f_path, 'r')
                for line in f:
                    if re.match(r'^email: ', line):
                        email = line.strip('email:').strip(' \n')
                    elif re.match(r'^password: ', line):
                        password = line.strip('password:').strip(' \n')
                    elif re.match(r'^program: ', line):
                        program = line.strip('program:').strip(' \n')
                    elif re.match(r'^full_name: ', line):
                        full_name = line.strip('full_name:').strip(' \n')
                    elif re.match(r'^zid: ', line):
                        zid = line.strip('zid:').strip(' \n')
                    elif re.match(r'^home_longitude: ', line):
                        home_longitude = line.strip('home_longitude:').strip(' \n')
                    elif re.match(r'^home_suburb: ', line):
                        home_suburb = line.strip('home_suburb:').strip(' \n')
                    elif re.match(r'^birthday: ', line):
                        brithday = line.strip('birthday:').strip(' \n')
                    elif re.match(r'^home_latitude: ', line):
                        home_latitude = line.strip('home_latitude:').strip(' \n')
                    elif re.match(r'^courses: ', line):
                        courses = line.strip('courses:').strip(' \n')
                    elif re.match(r'^friends: ', line):
                        friends = line.strip('friends:').strip(' \n')
                student_current = (student_id, zid, password, full_name, email, program, home_longitude, home_suburb, home_latitude,brithday, courses, friends)
                student_list.append(student_current)

            elif re.match(r'^\d+.txt$', file):
                message_id += 1
                n_file = file.strip('.txt')
                f = open(f_path, 'r')
                for line in f:
                    if re.match(r'^message: ', line):
                        message = line.strip('message:').strip(' \n')
                        if re.match(r'.*\\n', message):
                            print(message)
                            message = re.sub(r'\\n', '<br/>', message)
                            print(message)
                    elif re.match(r'from: ', line):
                        mfrom = line.strip('from:').strip(' \n')
                    elif re.match(r'^time: ', line):
                        time = line.strip('time:').strip(' \n')
                    elif re.match(r'^longitude: ', line):
                        longitude = line.strip('longitude:').strip(' \n')
                    elif re.match(r'^latitude: ', line):
                        latitude = line.strip('latitude:').strip(' \n')
                message_current = (message_id, mfrom, longitude, latitude, message, time)
                message_list.append(message_current)

            elif re.match(r'^\d+-\d+.txt$', file):
                comment_id += 1
                n_file = file.strip('.txt')
                # post_id, comment_id = n_file.split('-')
                f = open(f_path, 'r')
                for line in f:
                    if re.match(r'^message: ', line):
                        message = line.strip('message:').strip(' \n')
                        if re.match(r'.*\\n', message):
                            print(message)
                            message = re.sub(r'\\n', '<br/>', message)
                            print(message)
                    elif re.match(r'from: ', line):
                        cfrom = line.strip('from:').strip(' \n')
                    elif re.match(r'^time: ', line):
                        time = line.strip('time:').strip(' \n')
                comment_current = (comment_id, message_id, cfrom, message, time)
                comment_list.append(comment_current)

            elif re.match(r'^\d+-\d+-\d+.txt$', file):
                reply_id += 1
                n_file = file.strip('.txt')
                # post_id, comment_id, reply_id = n_file.split('-')
                f = open(f_path, 'r')
                for line in f:
                    if re.match(r'^message: ', line):
                        message = line.strip('message:').strip(' \n')
                        if re.match(r'.*\\n', message):
                            print(message)
                            message = re.sub(r'\\n', '<br/>', message)
                            print(message)
                    elif re.match(r'^time: ', line):
                        time = line.strip('time:').strip(' \n')
                    elif re.match(r'from: ', line):
                        rfrom = line.strip('from:').strip(' \n')
                reply_current = (reply_id, comment_id, message_id, rfrom, message, time)
                reply_list.append(reply_current)

            elif re.match(r'^img.jpg$', file):
                img_current = (img_id, student_dic, f_path)
        img_list.append(img_current)
                # print("find jpg")
                # pass
c.executemany("INSERT INTO STUDENT VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",student_list)
c.executemany("INSERT INTO MESSAGE VALUES (?,?,?,?,?,?)",message_list)
c.executemany("INSERT INTO COMMENT VALUES (?,?,?,?,?)",comment_list)
c.executemany("INSERT INTO REPLY VALUES (?,?,?,?,?,?)",reply_list)
c.executemany("INSERT INTO IMG VALUES (?,?,?)",img_list)

conn.commit()
# zid = ('z5190009',)
# for row in c.execute('SELECT * FROM STUDENT WHERE ZID=?', zid):
#     print(row)

# L = []
# for row in c.execute('SELECT * FROM IMG'):
    # L.append(row)
    # L = [row[0],row[1]]
    # print(row)
# if not L:
    # print(1)
# img_path = ''
# zid = ('z5190009','%z5190009','%z5190009','%z5190009')
# zid = ('%z5190009',)
# sql = 'select message.mid, student.full_name, message.mfrom, message.message, message.time from message, student where message.mid in(select mid from message where mfrom="'+zid+'" UNION select mid from comment where message like "%'+zid+'%" UNION select mid from message where message like "%'+zid+'%") and message.mfrom = student.zid '

# for row in c.execute('SELECT MESSAGE.MID, MESSAGE.MFROM, STUDENT.FULL_NAME, MESSAGE.MESSAGE, MESSAGE.TIME FROM MESSAGE, STUDENT WHERE MESSAGE.MID IN (SELECT MID FROM MESSAGE WHERE MFROM=? UNION SELECT MID FROM COMMENT WHERE MESSAGE LIKE ? UNION SELECT MID FROM MESSAGE WHERE MESSAGE LIKE ? UNION SELECT MID FROM REPLY WHERE MESSAGE LIKE ?) AND MESSAGE.MFROM=STUDENT.ZID ORDER BY MESSAGE.TIME DESC', zid):
#     each_message = [row[0],row[1],row[2],row[3],row[4]]
# for row in c.execute('SELECT * FROM COMMENT WHERE MESSAGE LIKE ?', zid):
    # img_path = row[2]
    # print(img_path)
# tuple = ('%let me blow you%',)
for row in c.execute('SELECT MAX(CID) FROM COMMENT'):
#     student_detail = [row[1], row[2], row[3], row[4], row[5], row[7], row[9], row[11]]
    print(row)
    # break
#     print(student_detail)
# mtuple = (421,'z5190009','','','test1','2017-1--29T23:01:21+0000')
# c.execute('INSERT INTO MESSAGE VALUES (?,?,?,?,?,?)', mtuple)
# for row in c.execute('SELECT MID FROM MESSAGE'):
#     print(row)
conn.commit()
conn.close()

# COMMMENT