$('.chonglu1').on('click', function(event) {
  var _this = $(event.target);
    $.confirm("重录将删除之前的录音", "提示", function() {
          $('#luyin1').attr('src','http://res.jian-hu.cn/static/img/luyin@2x.png');
        _this.parent().parent().parent().prev().html("点击开始录音，最多录60秒");
        _this.parent().parent().prev().prev().html("");
        _this.parent().html("");
    }, function() {
      //取消操作
    });
});

$('.chonglu2').on('click', function(event) {
    var _this = $(event.target);
  $.confirm("重录将删除之前的录音", "提示", function() {
        $('#luyin2').attr('src','http://res.jian-hu.cn/static/img/luyin@2x.png');
        _this.parent().parent().parent().prev().html("点击开始录音，最多录60秒");
        _this.parent().parent().prev().prev().html("");
        _this.parent().html("");
    }, function() {
      //取消操作
    });
});

$('.jian-fasong-btn').on('click', function(event) {
  // $.confirm("重录将删除之前的录音", "提示", function() {
    location.href = "/";
    // }, function() {
    //   //取消操作
    // });
});

$('#luyin1').on('click', function(event) {
      var _this = $(event.target);
    //1.更新点击录音图片，实现360度旋转
    _this.attr('src', 'http://res.jian-hu.cn/static/img/luyinzhong@3x.gif');
    //2.更新点击开始录音文本
    var second = 2;
    _this.parent().parent().parent().prev().html('已录 <font style="color: #ff9600;">'+second+'</font> 秒');

    //3.更新将左边空白部分替换成暂停图片按钮
    var start = '<div class="jian-luyin-start-img"><img src="http://res.jian-hu.cn/static/img/stop@2x.png" class="jian-luyin-stop"></div>';
    _this.parent().parent().prev().html(start);
});

//第二个
$('#luyin2').on('click', function(event) {
    var _this = $(event.target);
    //1.更新点击录音图片，实现360度旋转
    _this.attr('src', 'http://res.jian-hu.cn/static/img/luyinzhong@3x.gif');
    //2.更新点击开始录音文本
    var second = 2;
    _this.parent().parent().parent().prev().html('已录 <font style="color: #ff9600;">'+second+'</font> 秒');

    //3.更新将左边空白部分替换成暂停图片按钮
    var start = '<div class="jian-luyin-start-img"><img src="http://res.jian-hu.cn/static/img/stop@2x.png" class="jian-luyin-stop"></div>';
    _this.parent().parent().prev().html(start);
});


//暂停录音
$('.jian-luyin-start').on('click', '.jian-luyin-stop',function(event){
    var _this = $(event.target);
    var img_dom = _this.parent().parent().next().find('.jian-luyin-img');
    img_dom.attr('src','http://res.jian-hu.cn/static/img/bofang@2x.png');
    

    var chonglu = _this.parent().parent().next().next();
    console.log(chonglu);
    chonglu.find('a').html('<div class="jian-luyin-2">重录</div>');

    _this.parent().parent().html('点击试听');
    // console.log(img_dom);
    // alert('stop');
});
