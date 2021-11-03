import os
from flask import Flask, render_template, request, send_from_directory, redirect

WebApp = Flask(__name__)
_WebAppStarted = False

def startWebApp(iPort, iDebugMode = False):
  global _WebAppStarted
  if False == _WebAppStarted:
    _WebAppStarted = True
    WebApp.run(host='0.0.0.0', port=iPort, debug=iDebugMode)
    return True
  return False


@WebApp.route('/')
def send_index():
      return redirect("/site/index.html", code=302)


@WebApp.route('/site/<path:path>')
def send_site(path):
    print(os.getcwd())
    if path.endswith(".mjs"):
        return send_from_directory('./site/', path, as_attachment=True, mimetype='text/javascript')
    else:
        return send_from_directory('./site/', path)



def main():
    port = int(os.environ.get('PORT', 5000))
    startWebApp(port, True)

if __name__ == '__main__':
    main()