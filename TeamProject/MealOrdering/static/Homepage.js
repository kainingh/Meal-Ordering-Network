
    function toggleclass() {
        $(".right").toggleClass("click-right");
        $(".container").toggleClass("active-right");
    };
    
    function rlogin() {
        $(".right .login").css("display", "block");
        $(".right .register").css("display", "none");
        $(".right .bottombox").animate({
            left: "-=50%",
        }, 200, function () {
            // Animation complete.
        });

    };
    function rregister() {
        $(".right .login").css("display", "none");
        $(".right .register").css("display", "block");

        $(".right .bottombox").animate({
            left: "+=50%",
        }, 200, function () {
            // Animation complete.
        });

    };

    function llogin() {
        $(".left .login").css("display", "block");
        $(".left .register").css("display", "none");
        $(".left .bottombox").animate({
            left: "-=50%",
        }, 200, function () {
            // Animation complete.
        });

    };
    function lregister() {
        $(".left .login").css("display", "none");
        $(".left .register").css("display", "block");

        $(".left .bottombox").animate({
            left: "+=50%",
        }, 200, function () {
            // Animation complete.
        });

    };

    function toggleclassleft() {
        $(".left").toggleClass("click-left");
        $(".container").toggleClass("active-left");
    };
