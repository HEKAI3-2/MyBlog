$("#div_digg .action").click(function () {
    if ($(".info").attr("username")) {
        // 有值就ture
        var is_up = $(this).hasClass('diggit');
        //alert(is_up);
        // var article_id = "{{ article.pk }}";
        var article_id = $(".info").attr("article_id");

        $.ajax({
            url: "/blog/up_down/",
            type: "post",
            data: {
                is_up: is_up,
                article_id: article_id,
                csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
            },
            success: function (data) {
                if (data.status) {
                    //点赞或踩完成
                    if (is_up) {
                        //点赞成功
                        val = $("#digg_count").text();
                        val = parseInt(val) + 1;
                        $("#digg_count").text(val);
                    } else {
                        //踩成功
                        val = $("#bury_count").text();
                        val = parseInt(val) + 1;
                        $("#bury_count").text(val);
                    }
                } else {
                    if (data.first_action) {
                        $("#digg_tips").html("已经推荐过了");
                    } else {
                        $("#digg_tips").html("已经踩过了");
                    }
                    setTimeout(function () {
                        $("#digg_tips").html("")
                    }, 1000);
                }

            }
        })
    }else {
        location.href="/login/"
    }

});