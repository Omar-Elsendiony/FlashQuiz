
setTimeout(() => {
    var areUserSettingsDisplayed = false;
    $(".username").click(function() {
        if (areUserSettingsDisplayed) {
            $(".userSettings").css("display", "none");
            areUserSettingsDisplayed = false;
            // $(".usernameInput").hide();
        }
        else {
            $(".userSettings").css("display", "block");
            // $(".usernameInput").show();
            // $(".usernameInput").focus();
            areUserSettingsDisplayed = true;
        }
    });

    $(document).click(function(e) {
        e.stopPropagation();
        $(".dropdownSearch").html("");
    });


    // $(".search").focusout(function(){
    //     $(".dropdownSearch").html("");
    // });


    $("#searchText").keyup(function(){

        $.ajax({
            type: 'POST',
            url: "/search_question/",
            data: {'search_value': $("#searchText").val()},
            dataType: "text",

        }).done(function(data){
            dataParsed = JSON.parse(data);
            // console.log(dataParsed);
            dataParsed = dataParsed['questions_list']
            $(".dropdownSearch").html("");
            for (var i = 0; i < dataParsed.length; i++)
            {
                $(".dropdownSearch").append("<li><a href='/question/" + dataParsed[i]["id"] + "'>" + dataParsed[i]["title"] + "</a></li>");
            }
        });
    });


}, 50);
