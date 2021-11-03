import os, sys, threading
from flask import Flask, render_template, request, send_from_directory, redirect

WebApp = Flask(__name__)
_WebAppStarted = False
_KillProcessCallback = []

def startWebApp(iPort, iBluePrintList=[], iDebugMode = False):
  global _WebAppStarted
  if False == _WebAppStarted:
    _WebAppStarted = True

    for wBluePrint in iBluePrintList:
      WebApp.register_blueprint(wBluePrint)

    WebApp.run(host='0.0.0.0', port=iPort, debug=iDebugMode)
    return True
  return False


def subscribeToKillProcessCallback(iKillCallback):
  global _KillProcessCallback
  _KillProcessCallback.append(iKillCallback)


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


@WebApp.route('/cmd/killprocess', methods=["POST"])
def kill_process():
    print("Kill Service invoked")

    for wCallBack in _KillProcessCallback:
      if None != wCallBack:
        wCallBack()

    wDelayCall = threading.Timer(5, os.kill, [os.getpid(), 9])
    wDelayCall.setDaemon(True)
    wDelayCall.start()
    return "Killing Service in 5 seconds"


def main():
  port = int(os.environ.get('PORT', 5000))
  startWebApp(port, True)

if __name__ == '__main__':
  main()