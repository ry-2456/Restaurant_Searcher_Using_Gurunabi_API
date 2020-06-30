// Callback function executed when succeed in getting the current position.
function successCallback(pos) {
  let lat = pos.coords.latitude;  // 緯度
  let lng = pos.coords.longitude; // 経度
  alert(lat);
  alert(lng);

  document.getElementById("geolocation-result").innerHTML = 
    '<table>' + 
    '<td>緯度</dt><dd>' + lat + '</dd>' + 
    '<td>経度</dt><dd>' + lng + '</dd>' + 
    '</table>';
}

// Callback function executed when failed to get the current position.
function errorCallback(error) {
  let errorMsgs = {
    0: "原因不明のエラーが発生しました",
    1: "位置情報の取得が許可されませんでした",
    2: "電場状況などの問題で位置情報が取得できませんでした",
    3: "位置情報の取得に時間がかかりすぎてタイムアウトしました"
  };
  alert(errorMsgs[error.code]);
  alert(error.message);
}

let optionObj = {
  "enableHighAccuracy": false,
};

// Get current position.
if (navigator.geolocation) {
  navigator.geolocation.getCurrentPosition(successCallback, errorCallback, optionObj);
} else {
  let errorMsg = "あなたの端末では現在位置を取得できません";
  alert(errorMsg);
}
