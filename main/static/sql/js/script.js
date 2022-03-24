$('#sql-form').on('submit', function(event){
    event.preventDefault();
    $.ajax({
        url : 'post/',
        type : 'POST',
        data : { 'qrybox' : $('#sql-qry').val() },
        dataType : 'json',
        success : function(result){
            $('#sql-qry').val('');
            $('#qry-list').append('<li class="text-right list-group-item">'+ result.qry +'</li>');
            var output=JSON.parse(result.output)
            var s='<table style="border: 1px solid #ddd;padding: 8px;border-collapse: collapse;width: 20%;">'
            
            output.forEach(element => {
                s+='<tr>'
                element.forEach(e=>{
                    s+='<td>'+e+'</td>'
                })
                s+='</tr>'
            })
            s+='</table>'
            console.log(s)
            $('#qry-list').append(s)
                            
                             
                                
            // var sqllist = document.getElementById('qry-list-div');
            // sqllist.scrollTop = sqllist.scrollHeight;
        
        },

    });
});

// function getQueries(){
//     if (!scrolling) {
//         $.get('/queries/', function(queries1){
//             $('#qry-list').html(queries1);
//         });
//     }
//     scrolling = false;
// }

var scrolling = false;
// $(function(){
//     $('#qry-list-div').on('scroll', function(){
//         scrolling = true;
//     });
//     refreshTimer = setInterval(getQueries, 500);
// });


// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ready(function() {
    $('#send').attr('disabled','disabled');
    $('#sql-qry').keyup(function() {
        if($(this).val() != '') {
            $('#send').removeAttr('disabled');
        }
        else {
            $('#send').attr('disabled','disabled');
        }
    });

});