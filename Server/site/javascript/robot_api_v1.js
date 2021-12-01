
function sendGetRequest(iUrl, iCallback) {
  var wXhttp = new XMLHttpRequest();
  wXhttp.open("GET", iUrl, true);
  wXhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      if (null != iCallback){
        iCallback(this.responseText)
      }
    }
  };

  wXhttp.send();
}

function sendPostRequest(iUrl, iJSONData, iCallback) {
  var wXhttp = new XMLHttpRequest();
  wXhttp.open("POST", iUrl, true);
  wXhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      if (null != iCallback){
        iCallback(this.responseText);
      }
    }
  };

  wXhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  wXhttp.send(JSON.stringify(iJSONData));
}


function sendKillProcess() {
  sendPostRequest("/cmd/killprocess",{}, null);
  
}

function getRobotBehaviorMenu(iCallback) {
  sendGetRequest("/robot_api/getBehaviorMenu", function(iResponseText){
    var wObj = JSON.parse(iResponseText);
    if (null != iCallback) iCallback(wObj);
  });
}

function getCurrentRobotBehavior(iCallback) {
  sendGetRequest("/robot_api/getCurrentBehavior", function(iResponseText){
    var wObj = JSON.parse(iResponseText);
    if (null != iCallback) iCallback(wObj);
  });
}

function setRobotBehavior(iType, iName, iCallback) {
  sendPostRequest("/robot_api/setBehavior", {Type: iType, Name:iName}, function(iResponseText){
    if (null != iCallback) iCallback(iResponseText);
  });
}


function getRobotBehaviorForm(iType, iName, iCallback) {
  sendGetRequest("/robot_api/getBehaviorForm/"+iType+"/"+iName, function(iResponseText){
    var wObj = JSON.parse(iResponseText);
    if (null != iCallback) iCallback(wObj);
  });
}
