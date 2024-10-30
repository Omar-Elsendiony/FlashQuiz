
setTimeout(() => {

    $("#username").focusout(function(){
        $.ajax({
            type: 'GET',
            url: "/checkUserNameExists",
            data: {'username': $("#username").val()},
            dataType: "text",
            // success: function(data){
            //     alert("User Exists");
            // },
            // fail: function(data){
            //     alert("User does not exist");
            // }
        }).done(function(data){
            dataParsed = JSON.parse(data);
            if (dataParsed["exists"] == true)
            {
                $(".username_taken").css("display", "block")
                $("#username").css("border-color", "red")
            }
            else{
                $(".username_taken").css("display", "none")
                $("#username").css("border-color", "#f318a2")
            }
        });
    });


    $("#submit").click(function() {
        cond1 = $("#username").val().length < 1 ? alert("Username cannot be empty") : null
        cond2 = $("#username").val().length > 8 ? alert("Username length must be between 1 and 8") : null
        // console.log(!cond1, cond2)

        if (cond1 || cond2)
        {
            return false;
        }

        pass = $("#password").val()
        retypedPass = $("#Re-type").val()

        if (pass != retypedPass)
        {
            alert("Passwords do not match")
            return false;
        }


        $('.form_content').submit();
    });

}, 50);

