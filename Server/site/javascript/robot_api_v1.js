
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

function setRobotBehavior(iType, iName, iBehaviorFormDom, iCallback) {
  
  var wParameters = {};
  if (null != iBehaviorFormDom)
  {
    var wInputList = iBehaviorFormDom.getElementsByTagName("input");
    for( var wi = 0; wi < wInputList.length; ++wi){
      if (null != wInputList[wi].behaviorInputLabel){
        var wType = wInputList[wi].behaviorInputType;
        if ("integer" == wType)
        {
          wParameters[wInputList[wi].behaviorInputLabel] = parseInt(wInputList[wi].value);
        }
        else if ("float" == wType)
        {
          wParameters[wInputList[wi].behaviorInputLabel] = parseFloat(wInputList[wi].value);
        }
        else if ("boolean" == wType)
        {
          wParameters[wInputList[wi].behaviorInputLabel] = wInputList[wi].checked;
        }
        else if ("string" == wType)
        {
          wParameters[wInputList[wi].behaviorInputLabel] = wInputList[wi].value;
        }
      }
    }
  }

  sendPostRequest("/robot_api/setBehavior", {Type: iType, Name:iName, Parameters : wParameters}, function(iResponseText){
    if (null != iCallback) iCallback(iResponseText);
  });
}


function getRobotBehaviorForm(iType, iName, iBehaviorFormDom) {
  sendGetRequest("/robot_api/getBehaviorForm/"+iType+"/"+iName, function(iResponseText){
    var wObj = JSON.parse(iResponseText);
    if (null != iBehaviorFormDom){
      iBehaviorFormDom.innerHTML = "";

      for (const iInput in wObj) {
        var wInputType = wObj[iInput]["type"];
        var wInputValue = wObj[iInput]["value"];

        var wInputDom = null;
        if (("integer" == wInputType) || ("float" == wInputType))
        {
          wInputDom = document.createElement("input");
          wInputDom.type = "number";
          wInputDom.value = wInputValue;
        }
        else if ("boolean" == wInputType)
        {
          wInputDom = document.createElement("input");
          wInputDom.type = "checkbox";  
          wInputDom.checked = wInputValue
        }
        else if ("string" == wInputType)
        {
          if (0 <= iInput.toLowerCase().indexOf("color")){
            wInputDom = document.createElement("input");
            wInputDom.type = "color";  
            wInputDom.value = wInputValue;  

          }
          else {
            wInputDom = document.createElement("input");
            wInputDom.type = "text";  
            wInputDom.value = wInputValue;  
          }
        }

        if (null != wInputDom){
          
          wInputDom.behaviorInputType = wInputType;
          wInputDom.behaviorInputLabel = iInput;
          
          var wLabel = document.createElement("span");
          wLabel.innerText = iInput;

          var wInputWrapper = document.createElement("span");
          wInputWrapper.appendChild(wLabel);
          wInputWrapper.appendChild(wInputDom);
          
          iBehaviorFormDom.appendChild(wInputWrapper)
        }
      }
    }
  });
}
