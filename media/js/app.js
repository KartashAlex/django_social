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

