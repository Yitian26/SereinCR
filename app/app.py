from flask import Flask
from flask import render_template, request, redirect, url_for, session
import time
import os
from dbop import DbOperation as db
import aiml

# aiml初始化
k = aiml.Kernel()
k.learn("aiml/cn-startup.xml")
k.respond("load aiml b")
# flask实例
app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/static')  # 自定义素材文件夹位置
app.config['SECRET_KEY'] = os.urandom(24)


@app.route('/')
def index():
    return redirect('/login')


@app.route("/login", methods=['GET', 'POST'])  # 登录页面
def login():
    info = ''
    if request.method == 'POST':
        session['id'] = request.form.get('id', 'None')
        session['password'] = request.form.get('password', 'None')
        if request.form.get('login-button', 'None') == 'login':
            if session['id'] != 'None' and session['password'] != 'None':
                data = db.seekfromid(session['id'], 'Sereincr.db')
                if len(data) != 0:
                    if data[0][2] == session['password']:
                        session['name'] = data[0][1]
                        session['lastlogin'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        db.change([session['id'], session['password'], session['name'],
                                   time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())], 'Sereincr.db')
                        return redirect(url_for('chatroom'))  # 跳转到聊天室
                    else:
                        info = '用户名或密码错误'
                else:
                    info = '用户不存在'
        elif request.form.get('signup-button', 'None') == 'signup':
            return redirect(url_for('signup'))
    return render_template("login.html", info=info)


@app.route('/signup', methods=['GET', 'POST'])  # 注册页面
def signup():
    info = ''
    if request.method == 'POST':
        idd = request.form.get('id', 'None')
        password = request.form.get('password', 'None')
        name = request.form.get('name', 'None')
        if db.dblength('Sereincr.db'):
            if 0 < len(idd) <= 20 and 8 <= len(password) <= 50 and 0 < len(name) <= 10:
                if not '0' <= idd[0] <= '9':
                    data = db.seekfromid(idd, 'Sereincr.db')
                    if len(data) == 0:
                        data = db.seekfromname(name, 'Sereincr.db')
                        if len(data) == 0:
                            db.addacc([idd, name, password, ''], 'Sereincr.db')
                            return redirect(url_for('login'))  # 跳转到登录
                        else:
                            info = '昵称已被使用'
                    else:
                        info = '用户名已被注册'
                else:
                    info = '用户名不得以数字开头'
            else:
                info = '输入格式错误'
        else:
            info = '用户注册已达上限'
    return render_template('signup.html', info=info)


@app.route('/chatroom', methods=['GET', 'POST'])  # 聊天室
def chatroom():
    servertime = ''
    session['msgs'] = db.getmsgs('Sereincr.db')
    if servertime != time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()):
        servertime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if request.form.get('sendcheck') == 'sendcheck':  # 聊天功能实现
        text = request.form.get('text', 'None')
        if 0 < len(text) <= 40:
            if len(session['msgs']) == 0:
                idd = 1
            else:
                idd = session['msgs'][0][0] + 1
            db.addmsg([idd, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), session['name'], text], 'Sereincr.db')
            if len(text) > 4:
                if text[:4] == 'bot/':
                    ans = k.respond(text[4:])
                    db.addmsg([idd + 1, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 'bot', ans],
                              'Sereincr.db')
            session['msgs'] = db.getmsgs('Sereincr.db')
    # 导航栏跳转
    if request.form.get('search', 'None') == 'search':
        return redirect('chatroom/se')
    elif request.form.get('account', 'None') == 'account':
        return redirect('chatroom/acc')
    elif request.form.get('info', 'None') == 'info':
        return redirect('chatroom/inf')
    elif request.form.get('logout', 'None') == 'logout':
        session.clear()
        return redirect('/')
    elif request.form.get('admin') == 'admin':
        return redirect('chatroom/control')
    return render_template('chatroom.html', name=session['name'], servertime=servertime,
                           msgs=session['msgs'][::-1], admin=session['name'] == 'Serein')


@app.route('/chatroom/se', methods=['GET', 'POST'])  # 聊天室_se
def chatroom_se():
    servertime = ''
    msg1 = []
    if servertime != time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()):
        servertime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if request.form.get('searchmsg') == 'searchmsg':  # 搜索功能实现
        name = request.form.get('text')
        try:
            msg1 = db.getmsgbyname(name, 'Sereincr.db')
        except Exception as error:
            print(error)
    # 导航栏跳转
    if request.form.get('search', 'None') == 'search':
        return redirect('se')
    elif request.form.get('account', 'None') == 'account':
        return redirect('acc')
    elif request.form.get('info', 'None') == 'info':
        return redirect('inf')
    elif request.form.get('home', 'None') == 'home':
        return redirect('/chatroom')
    elif request.form.get('logout', 'None') == 'logout':
        session.clear()
        return redirect('/')
    return render_template('chatroom_se.html', name=session['name'], servertime=servertime, msgs=msg1[::-1])


@app.route('/chatroom/acc', methods=['GET', 'POST'])  # 聊天室_acc
def chatroom_acc():
    servertime = ''
    info = ''
    if servertime != time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()):
        servertime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # 导航栏跳转
    if request.form.get('search', 'None') == 'search':
        return redirect('se')
    elif request.form.get('account', 'None') == 'account':
        return redirect('acc')
    elif request.form.get('info', 'None') == 'info':
        return redirect('inf')
    elif request.form.get('home', 'None') == 'home':
        return redirect('/chatroom')
    elif request.form.get('logout', 'None') == 'logout':
        session.clear()
        return redirect('/')
    if request.method == 'POST':  # 账户信息更改
        password = request.form.get('password', 'None')
        name = request.form.get('name', 'None')
        if password == session['password']:
            info = '新密码不得与原密码相同'
        elif name == session['name']:
            info = '新昵称不得与原昵称相同'
        else:
            if len(name) == 0:
                name = session['name']
            if len(password) == 0:
                password = session['password']
            if 0 < len(name) <= 20 and 8 <= len(password) <= 50:
                data = db.seekfromname(name, 'Sereincr.db')
                if len(data) == 0 or data[0][0] == session['id']:
                    info = '修改成功'
                    session['name'] = name
                    session['password'] = password
                    db.change([session['id'], password, name, session['lastlogin']], 'Sereincr.db')
                else:
                    info = '该昵称已被使用'
            else:
                info = '呢称或密码格式错误'
    return render_template('chatroom_acc.html', info=info, name=session['name'], id=session['id'],
                           password=session['password'], servertime=servertime)


@app.route('/chatroom/inf', methods=['GET', 'POST'])  # 聊天室_info
def chatroom_inf():
    servertime = ''
    if servertime != time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()):
        servertime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # 导航栏跳转
    if request.form.get('search', 'None') == 'search':
        return redirect('se')
    elif request.form.get('account', 'None') == 'account':
        return redirect('acc')
    elif request.form.get('info', 'None') == 'info':
        return redirect('inf')
    elif request.form.get('home', 'None') == 'home':
        return redirect('/chatroom')
    elif request.form.get('logout', 'None') == 'logout':
        session.clear()
        return redirect('/')
    return render_template('chatroom_inf.html', name=session['name'], servertime=servertime)


@app.route('/chatroom/control', methods=['GET', 'POST'])
def control():
    servertime = ''
    accounts = db.getaccounts('Sereincr.db')
    if servertime != time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()):
        servertime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # 导航栏跳转
    if request.form.get('search', 'None') == 'search':
        return redirect('se')
    elif request.form.get('account', 'None') == 'account':
        return redirect('acc')
    elif request.form.get('info', 'None') == 'info':
        return redirect('inf')
    elif request.form.get('home', 'None') == 'home':
        return redirect('/chatroom')
    elif request.form.get('logout', 'None') == 'logout':
        session.clear()
        return redirect('/')
    if request.form.get('delcheck') == 'delcheck':  # 删除账户
        idd = request.form.get('text')
        try:
            db.delacc(idd, 'Sereincr.db')
            accounts = db.getaccounts('Sereincr.db')
        except Exception as err:
            print(err)
    return render_template('chatroom_admin.html', name=session['name'], servertime=servertime,
                           accounts=accounts)


# 主程序入口
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
