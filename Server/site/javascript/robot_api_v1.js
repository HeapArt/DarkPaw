
function sentPostRequest(iUrl, iJSONData) {
  var wXhttp = new XMLHttpRequest();
  wXhttp.open("POST", iUrl, true);
  wXhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
    }
  };

  wXhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  wXhttp.send(JSON.stringify(iJSONData));
}


function sendKillProcess() {
  sentPostRequest("/cmd/killprocess",{});
  
}