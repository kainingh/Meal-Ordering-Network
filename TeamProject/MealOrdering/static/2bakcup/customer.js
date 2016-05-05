var Tabs = new Array();

Tabs[0] = $(".profile");  //profileTab
Tabs[1] = $(".address"); //addressTab
Tabs[2] = $(".payment"); //paymentTab
Tabs[3] = $(".order");   //orderTab


var initial = function () {
    for (var i = 0; i<4;i++)
    {
        Tabs[i].addClass("inactive");
    }
}
function show(i) {
    initial();
    Tabs[i].removeClass("inactive");
}

function toggle(i) {
    Tabs[i].find(".showPart").toggle("inactive");
    Tabs[i].find(".formPart").toggle("inactive");
}