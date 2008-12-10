function geoController(){

    if($('#id_city option:selected').val() == null){$('#id_city').attr('disabled', 'disabled');   }

    $('#id_country').change(function(){
        $('#id_city').removeAttr('disabled');
        $.getJSON('/cities/' + $(this).val() + '/', function(data){
            $('#id_city').empty();
            options = '';
            $(data).each(function(){
                options += '<option value="' + this.id + '">' + this.name + '</option>'
            });
            $('#id_city').append(options)
        });
    });
}

	$(function(){
        	geoController();
		$('.wrote-smth').click(function(){
		var _t = this;
		 $.get($(_t).attr('href'), function(data){
			$('body').append(data);
			$('#write-smth').dialog({
				width: 450,
				height:	$('#write-smth').height(),
				modal: true,
				overlay: {
					opacity: 0.5,
					background: "black"
				},
				close: function(){
					$('#write-smth').remove();
				}
			});
			$('#write-smth').show();
			geoController();
			
			$('select#id_city').change(function(){
				$('select#id_type').removeAttr('disabled');
				if($('select#id_type').val() == 2 && $('select#id_city').val() > 0){ /* проверяем что университет и что город установлен */

				$("input#id_title").autocomplete("/places/template/", {parameters: {'city': $('select#city').val()}});
			}});
		});





			return false;
		});
		$('.b-setlang a').click(function(){
			var _t = this;
			$.post('/i18n/setlang/', {'language': $(_t).attr('rel')}, function(){window.location.reload()});
			return false;
		});
});


function createCookie(name,value,days) {
	if (days) {
		var date = new Date();
		date.setTime(date.getTime()+(days*24*60*60*1000));
		var expires = "; expires="+date.toGMTString();
	}
	else var expires = "";
	document.cookie = name+"="+value+expires+"; path=/";
}

function readCookie(name) {
	var nameEQ = name + "=";
	var ca = document.cookie.split(';');
	for(var i=0;i < ca.length;i++) {
		var c = ca[i];
		while (c.charAt(0)==' ') c = c.substring(1,c.length);
		if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
	}
	return null;
}





function Get_Cookie( check_name ) {
	// first we'll split this cookie up into name/value pairs
	// note: document.cookie only returns name=value, not the other components
	var a_all_cookies = document.cookie.split( ';' );
	var a_temp_cookie = '';
	var cookie_name = '';
	var cookie_value = '';
	var b_cookie_found = false; // set boolean t/f default f

	for ( i = 0; i < a_all_cookies.length; i++ )
	{
		// now we'll split apart each name=value pair
		a_temp_cookie = a_all_cookies[i].split( '=' );


		// and trim left/right whitespace while we're at it
		cookie_name = a_temp_cookie[0].replace(/^\s+|\s+$/g, '');

		// if the extracted name matches passed check_name
		if ( cookie_name == check_name )
		{
			b_cookie_found = true;
			// we need to handle case where cookie has no value but exists (no = sign, that is):
			if ( a_temp_cookie.length > 1 )
			{
				cookie_value = unescape( a_temp_cookie[1].replace(/^\s+|\s+$/g, '') );
			}
			// note that in cases where cookie is initialized but no value, null is returned
			return cookie_value;
			break;
		}
		a_temp_cookie = null;
		cookie_name = '';
	}
	if ( !b_cookie_found )
	{
		return null;
	}
}


function Set_Cookie( name, value, expires, path, domain, secure )
{
// set time, it's in milliseconds
var today = new Date();
today.setTime( today.getTime() );

/*
if the expires variable is set, make the correct
expires time, the current script below will set
it for x number of days, to make it for hours,
delete * 24, for minutes, delete * 60 * 24
*/
if ( expires )
{
expires = expires * 1000 * 60 * 60 * 24;
}
var expires_date = new Date( today.getTime() + (expires) );

document.cookie = name + "=" +escape( value ) +
( ( expires ) ? ";expires=" + expires_date.toGMTString() : "" ) +
( ( path ) ? ";path=" + path : "" ) +
( ( domain ) ? ";domain=" + domain : "" ) +
( ( secure ) ? ";secure" : "" );
}


