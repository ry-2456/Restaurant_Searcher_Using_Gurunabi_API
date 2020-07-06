// レストランの場所を表示する地図
// let restName = "マクドナルド";
// let restLat = 35.6811673;
// let restLng = 139.7670516;
// let restPos = new google.maps.LatLng(restLat, restLng);
// 
// let Options = {
//   zoom: 15,
//   center: restPos,
//   MapTypeId: 'roadmap'
// };
// 
// // マップを作る
// let map = new google.maps.Map(document.getElementById('map-canvas'), Options);
// 
// // Markerを立てる
// let marker = new google.maps.Marker({
//   position: restPos,
//   map: map,
//   title: restName
// });


// 詳細ページの画像切り替え処理
$(document).ready(function(){
  $(".sub-img img").hover(function() {
    // インデックスを取得
    let index = $(".sub-img img").index(this);
    // マウスオーバーした画像のurlを取得
    let imgurl = $(".sub-img img").eq(index).attr("src");
    // 元のメイン画像のURLを保存
    defaultImgurl = $(".main-img img").attr("src");
    // サブをメイン画像領域に表示
    $(".main-img img").attr("src", imgurl);
  }, function(){
    $(".main-img img").attr("src", defaultImgurl);
  });
});
