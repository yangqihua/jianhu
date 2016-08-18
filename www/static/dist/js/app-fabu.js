/*
 ///获取父类元素
 jQuery.parent(expr) 找父亲节点，可以传入expr进行过滤，比如$("span").parent()或者$("span").parent(".class")
 jQuery.parents(expr),类似于jQuery.parents(expr),但是是查找所有祖先元素，不限于父元素


 ///获取兄弟元素
 $('#id').siblings()   当前元素所有的兄弟节点
 $('#id').prev()       当前元素前一个兄弟节点
 $('#id').prevaAll()   当前元素之前所有的兄弟节点
 $('#id').next()       当前元素之后第一个兄弟节点
 $('#id').nextAll()    当前元素之后所有的兄弟节点
 这三个方法都可以添加选择器，给出选择条件，就能找到你指定的兄弟节点了。


 //获取子孙元素
 jQuery.children(expr).返回所有子节点，这个方法只会返回直接的孩子节点，不会返回所有的子孙节点

 jQuery.contents(),返回下面的所有内容，包括节点和文本。这个方法和children()的区别就在于，
 包括空白文本，也会被作为一个 jQuery对象返回，children()则只会返回节点

 Query.find(expr),跟jQuery.filter(expr)完全不一样。jQuery.filter()是从初始的jQuery对象
 集合中筛选出一部分，而jQuery.find()的返回结果，不会有初始集合中的内容，
 比如$("p"),find("span"),是从元素开始找,等同于$("p span")
 */




// $('body').on('click',function(event){
// 	$('.jian-skill-clear').css('display','none');
// });

// var skills = [];
// skills[1] = '<img src="http://res.jian-hu.cn/static/img/add@2x.png" height="16px">';
//编辑技能
$(".weui-row").on('click', '.jian-form-edit-btn', function (event) {

    var _this = $(event.target);
    if (_this.html() == '确定') {
        $('.jian-skill-clear').css('display', 'none');
        _this.html('编辑');
        $('.jian-form-cancel-btn').css('display', 'none');
    } else {
        $('.jian-skill-clear').css('display', 'block');
        _this.html('确定');
    }
    ;
});


//删除技能要求
$(".weui-row").on('click', '.jian-skill-clear', function (event) {
    var _this = $(event.target);
    var skill = _this.prev();
    var curr_id = skill.attr('id');
    for (var i = parseInt(curr_id); i <= 6; i++) {
        if ($('#' + i).hasClass('jian-add-skill')) {
            for (var j = i; j <= 6; j++) {
                $('#' + j).removeClass('jian-form-edit').removeClass('jian-add-skill').html('');
            }
            $('#' + (i - 1)).addClass('jian-add-skill');
            $('#' + (i - 1)).next().remove();
        }
        if ($('#6').text().trim() !== '') {  //说明已经有6条技能了
            if (i == 6) {
                $('#6').html('<img src="http://res.jian-hu.cn/static/img/add@2x.png" height="16px">').addClass('jian-add-skill');
                $('#6').next().remove();
            } else {
                $('#' + i).html($('#' + (i + 1)).html());
            }
        } else {
            $('#' + i).html($('#' + (i + 1)).html());
        }
    }
});


//给动态添加的元素添加事件要使用委托
$(".weui-row").on('click', '.jian-add-skill', function (event) {
    var _this = $(event.target);
    if (_this.attr('id') === undefined) { //如果点击的是'.jian-add-skill'的子元素，也就是+这个符号
        _this = _this.parent();
    }
    ;
    if ($('.weui-col-50 .jian-form-edit-btn').text() == '确定') {
        $.toptip('请先确定', 'warning');
    } else {
        myPrompt(_this);
    }
});


function myPrompt(_this) {
    $.prompt("技能要求不能超过16个字符或不为空", "输入技能要求", function (_text) {
        if (!isLimit(_text, 16) || (_text.trim()) == '') {
            myPrompt(_this);
            $('.weui-prompt-text').css('color', 'red');
        }
        else {
            curr_id = parseInt(_this.attr('id'));
            _this.removeClass('jian-add-skill');
            if (curr_id <= 6) {
                $('#' + (curr_id + 1)).addClass('jian-add-skill').addClass('jian-form-edit').html(_this.html());
            }
            _this.html(_text);
            _this.after('<img src="http://res.jian-hu.cn/static/img/close@2x.png" class="jian-skill-clear">');
            $(".skill"+curr_id).val(_text);
        }
    }, function () {
        //取消操作
    });
}

$(".jian-fabu-btn").on('click', '', function (event) {
    if ($('.jian-upload-label .jian-form-edit-btn').text() == '确定') {
        $.toptip('请先确定图片添加', 'warning');
        return;
    }
    if ($('.weui-col-50 .jian-form-edit-btn').text() == '确定') {
        $.toptip('请先确定技能标签', 'warning');
        return;
    }
    if($("#company_name").val()==''){
        $.toptip('请先填写公司名称', 'warning');
        return;
    }
    if($("#job_title").val()==''){
        $.toptip('请先填写职位名称', 'warning');
        return;
    }
    $.confirm("确认后不可撤回哦！", "确认发送?", function () {
        $('.myform').submit();
    }, function () {
        //取消操作
    });
});


//编辑图片
$(".jian-upload-label").on('click', '.jian-form-edit-btn', function (event) {
    var _this = $(event.target);
    if (_this.html() == '确定') {
        $('.jian-img-clear').css('display', 'none');
        _this.html('编辑');
        $('.jian-form-cancel-btn').css('display', 'none');
    } else {
        $('.jian-img-clear').css('display', 'block');
        _this.html('确定');
    }
    ;
});


//删除图片
$(".weui-row").on('click', '.jian-img-clear', function (event) {
    var _this = $(event.target);
    var imgdiv = _this.parent();
    var curr_id = imgdiv.attr('id').substring(6, 7);
    var imgdiv7 = '';
    if ($('#imgdiv6').find('.mimg').length !== 0) {
        imgdiv7 = '<div class="weui_uploader_input_wrp" style="margin:0"><div class="weui_uploader_input"></div></div>';
    }

    for (var i = parseInt(curr_id); i <= 6; i++) {
        if (i == 6) {
            $('#imgdiv' + i).html(imgdiv7);
            formatUpload("imgdiv6");
        }
        else {
            $('#imgdiv' + i).html($('#imgdiv' + (i + 1)).html());
        }
    }
});


//添加图片
$(".weui-row").on('click', '.weui_uploader_input', function (event) {
    var _this = $(event.target);
    if ($('.jian-upload-label .jian-form-edit-btn').text() == '确定') {
        $.toptip('请先确定', 'warning');
    } else {
        addImg(_this, 'http://res.jian-hu.cn/static/img/tencent2.jpg');
    }
});

function addImg(_this, img_src) {
    var imgdiv = _this.parent().parent();
    var dom = '<img src="' + img_src + '" class="mimg" ><img src="http://res.jian-hu.cn/static/img/close@2x.png" class="jian-img-clear">'
    imgdiv.html(dom);
    var curr_id = imgdiv.attr('id');
    formatUpload(curr_id);//自动缩放图片
    if (curr_id !== 'imgdiv6') { //替换下一个图片div的样式
        id_num = parseInt(curr_id.substring(6, 7));
        var next_id = "imgdiv" + (id_num + 1);
        $("#" + next_id).html('<div class="weui_uploader_input_wrp" style="margin:0"><div class="weui_uploader_input"></div></div>');
        formatUpload(next_id);//自动缩放图片
    }
}

$("#city-picker").cityPicker({
    showDistrict: false
});


function formatUpload(id) {
    var width = $('#' + id).width();
    $('#' + id).height(width);

    $('.weui_uploader_input_wrp').height(width - 2);//去除两个border的宽度2px
    $('.weui_uploader_input_wrp').width(width - 2);

    $('#' + id).each(function (index, el) {
        setImgAutoSize($(this).find('.mimg'));
    });
}
formatUpload("imgdiv1");

function isLimit(val, max) {
    var returnValue = '';
    var byteValLen = 0;
    for (var i = 0; i < val.length; i++) {
        if (val[i].match(/[^\x00-\xff]/ig) != null)
            byteValLen += 2;
        else
            byteValLen += 1;
    }
    if (byteValLen > max) {
        return false;
    } else {
        return true;
    }
}

//传入的img自动等比例缩放
function setImgAutoSize(img) {
    $("<img/>").attr("src", img.attr("src")).load(function () {
        var realWidth = this.width;
        var realHeight = this.height;
        if (realHeight > realWidth) {
            img.css('width', '100%');
        } else {
            img.css('height', '100%');
            img.css('width', 'auto');
        }
    });
}