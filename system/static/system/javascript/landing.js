jQuery(document).ready(function($){
    function judgeClient() {
        let client = '';
        if (/(iPhone|iPad|iPod|iOS)/i.test(navigator.userAgent)) {  //判断iPhone|iPad|iPod|iOS
          client = 'iOS';
        } else if (/(Android)/i.test(navigator.userAgent)) {  //判断Android
          client = 'Android';
        } else {
          client = 'PC';
        }
        return client;
      }
    var client = judgeClient()
    if(client == 'iOS')
        $(".get-app").attr("href","https://itunes.apple.com/us/app/apple-store/id1057900220?pt=118033742&amp;ct=Homepage&amp;mt=8");
    else
        $(".get-app").attr("href","https://fir.im/npjf");
})