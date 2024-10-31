function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

function doThis() {
    var phone = $('#phone').val();
    var csrfToken = getCSRFToken();

    $.ajax({
        type: 'POST',
        url: '/getDetails', 
        data: { phone: phone, csrfmiddlewaretoken: csrfToken },
        success: function(response) {
            $("#user-info-form").fadeOut(500, function() {
                window.location = "/dashboard";
            });
        },
        error: function(error) {
            console.log(error);  
            let data = JSON.parse(error.responseText)
            
            let errorMessage = error.responseText ? error.responseText : "An unknown error occurred!";
            $("#error").text(data.message);
            $("#error").show();
        }
    });
}

function onNextButtonClick(){
    var phone = $('#phone').val();
    if (!(phone.length==10)) {
        $("#error").text("Phone number must be 10 digits.");
        $("#error").show();

    }
    else{
        doThis();
    }

}


function login(){
    var r=document.getElementById("rules");
    var l=document.getElementById("login");

    l.style.visibility="visible"
    r.style.transform="translateX(100%)";
    setTimeout(function (){r.style.display="none"},500);
    
}
function bodhiet(){
    let bodheight=document.body.offsetHeight;
    let margin = document.getElementById("reg").style;
    let back = document.getElementById("login").style;
    margin.marginTop=bodheight-700+"px";
    back.height=bodheight+"px";
}