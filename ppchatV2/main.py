from flask import Flask, session, redirect, url_for, escape, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for("index"))
    html = render_template('main.html', pagetitle="主页" )
    return html

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/idgen')
def idgen():
    html = render_template('main.html', pagetitle="身份生成" )
    return html

@app.route('/chatroom')
def chatroom():
    html = render_template('main.html', pagetitle="聊天" )
    return html

# set the secret key.  keep this really secret:
app.secret_key = b'b\xd1\x10#\xe3\xca\xfd\\A\x10\xffh\xff\xbc\x92\x10<\x92\x11G[*\xa5['

if __name__ == "__main__":
    app.run(host='192.168.0.107')