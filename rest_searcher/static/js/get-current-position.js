// Callback function executed when succeed in getting the current position.
function successCallback(pos) {
  // let lat = pos.coords.latitude;  // 緯度
  // let lng = pos.coords.longitude; // 経度
  lat = pos.coords.latitude;  // 緯度
  lng = pos.coords.longitude; // 経度
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

// Option for geolocation API
let optionObj = {
  enableHighAccuracy: true,
  timeout: 2000,
  maximuAge: 0
};

// Get current position.
function getCurrentPosition() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(successCallback, errorCallback, optionObj);
  } else {
    let errorMsg = "あなたの端末では現在位置を取得できません";
    alert(errorMsg);
  }
}

// pass current position (lat, lng) to Flask
function passCurrentPositionToFlask(options) {
  return new Promise((resolve, reject) => {
    navigator.geolocation.getCurrentPosition(resolve, reject, options);
})};


// pass curent position to Flask
passCurrentPositionToFlask(optionObj).then((position) => {
    let lat = position.coords.latitude;  // 緯度
    let lng = position.coords.longitude; // 経度

    document.getElementById("geolocation-result").innerHTML = 
      '<table>' + 
      '<td>緯度</dt><dd>' + lat + '</dd>' + 
      '<td>経度</dt><dd>' + lng + '</dd>' + 
      '</table>';

    alert(lat);
    alert(lng);

    console.log(lat);
    console.log(lng);
    $.ajax({
      type: "POST",
      contentType: "application/json;charset=utf-8",
      url: "/receive_position",
      data: JSON.stringify({'lat': lat, 'lng': lng}),
      dataType: "json"
     });
  }).catch((err) => {
    console.log(err.message);
});
