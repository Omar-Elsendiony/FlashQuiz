
setTimeout(() => {
    function leftToRight() {
        $(".objectFloating").animate({ left: ['+=10%', 'linear'], top: ['+=2%', 'swing'] }, 1000, function() {
            $(this).animate({ left: ['+=10%', 'linear'], top: ['-=2%', 'swing'] }, 1000, function() {
                $(this).animate({ left: ['+=10%', 'linear'], top: ['+=2%', 'swing'] }, 1000, function() {
                    $(this).animate({ left: ['+=10%', 'linear'], top: ['-=2%', 'swing'] }, 1000, function() {
                        animateElement(); // Call the function again to loop the animation
                    });
                });
            });
        });
    }

    function rightToLeft() {
        $(".objectFloating").animate({ left: ['-=10%', 'linear'], top: ['+=2%', 'swing'] }, 1000, function() {
            $(this).animate({ left: ['-=10%', 'linear'], top: ['-=2%', 'swing'] }, 1000, function() {
                $(this).animate({ left: ['-=10%', 'linear'], top: ['+=2%', 'swing'] }, 1000, function() {
                    $(this).animate({ left: ['-=10%', 'linear'], top: ['-=2%', 'swing'] }, 1000, function() {
                        animateElement(); // Call the function again to loop the animation
                    });
                });
            });
        });
    }
    var start = true
    var direction = "right";
    function animateElement() {
        return
        var element = document.getElementsByClassName('objectFloating')[0];
        var position = element.getBoundingClientRect();
        var x = position.left;
        var y = position.top;
        // console.log(x, y);
        // console.log(screen.width);
        if (start == true) {
            start = false;
            leftToRight();
        }
        else{
            // console.log("else")
            if (x >= 0.2 * screen.width ) {
                direction = "left";
                // rightToLeft();
            }
            if (x <= 0.2 * screen.width) {
                direction = "right"
                // leftToRight();
            }
            if (direction == "right") {
                leftToRight();
            }
            else{
                rightToLeft();
            }

        }
        
    }
    
    // Start the animation
    animateElement();
}, 1000);

