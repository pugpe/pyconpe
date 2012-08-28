/* Clear forms */
(function($){
	$.fn.clearDefault = function(){
		return this.each(function(){
			var default_value = $(this).val();
			$(this).focus(function(){
				if ($(this).val() === default_value) $(this).val("");
			});
			$(this).blur(function(){
				if ($(this).val() === "") $(this).val(default_value);
			});
		});
	};
})(jQuery);

$(function(){
	$('.sign-in').jqTransform({imgPath:'../img/'});
});

$(document).ready(function(){
	$('a[rel=external]').attr('target','_blank');
	$('.clear-text').clearDefault();
    $('.btn-ok').click(function () {
        $(this).parent().parent().hide();
    });
});
