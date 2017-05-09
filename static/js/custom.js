$(function() {

  // We can attach the `fileselect` event to all file inputs on the page
  $(document).on('change', ':file', function() {
    var input = $(this),
        numFiles = input.get(0).files ? input.get(0).files.length : 1,
        label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
    input.trigger('fileselect', [numFiles, label]);
  });

  // We can watch for our custom `fileselect` event like this
  $(document).ready( function() {
      $(':file').on('fileselect', function(event, numFiles, label) {

          var input = $(this).parents('.input-group').find(':text'),
              log = numFiles > 1 ? numFiles + ' files selected' : label;

          if( input.length ) {
              input.val(log);
          } else {
              if( log ) alert(log);
          }

      });
  });

});

$(document).ready(function(){
  var slider = $('.bxslider').bxSlider({
	  	auto:false,hideControlOnEnd:true,infiniteLoop:false,
  		pager:false,touchEnabled:false, mode: 'fade',
  		speed: 0,captions: true
	  });
	  $('.bx-wrapper .bx-prev').text('PREVIOUS');
	  $( ".banner .banner-detail .banner-box a" ).click(function(e) {
		  $(this).parent().siblings().removeClass('boxexpand');
		  $(this).parent().toggleClass('boxexpand');
		  e.preventDefault();
	});

  $('#slider-next').click(function() {
    slider.goToNextSlide();
  });

  //slider.goToSlide();

	// business profile gallery carousel
  $('#media').carousel({
  	pause: true,
  	interval: false,
  });

	// slim scroll
	$(function(){

      $('#selectbox-detail').slimScroll();
          allowPageScroll: true

    });

	// editable selectfield
	$(function() {
		$('.dropdown-menu a').click(function() {
			console.log($(this).attr('data-value'));
			$(this).closest('.dropdown').find('input.countrycode')
			.val('(' + $(this).attr('data-value') + ')');
		});
	});

	// loginform code
	$( "#loginbtn1" ).click(function(){
		$( "#main-loginform" ).hide();
		$( "#login-form2" ).show();
	});

	$( "#loginbtn2" ).click(function(){
		$( "#login-form2" ).hide();
		$( "#forget-password" ).show();
	});

	$( "#forgetpassword" ).click(function(){
		$( "#forget-password" ).hide();
		$( "#reset-password" ).show();
	});


  $( "#forgot-passwordbtn" ).click(function(){
    $( "#main-loginform" ).hide();
    $( "#login-form2" ).hide();
    $( "#forget-password" ).hide();
    $( "#reset-password" ).show();
  });

	$( "#reset-againbtn" ).click(function(){
    $( "#main-loginform" ).show();
    $( "#login-form2" ).hide();
    $( "#forget-password" ).hide();
    $( "#reset-password" ).hide();

//		$( "#reset-password" ).hide();
//		$( "#reset-again" ).show();
	});

  $( "#member_register_connect").click(function() {

  });

	// tooltip on accounts tab photo view
	$( ".delete_btn" ).click(function(){
		$(this).children('.tooltip').toggleClass( "showTooltip" );
	});

});





	// flexslider for media preview
    function initFlexModal() {
      $('#carousel').flexslider({
        animation: "slide",
        controlNav: false,
        animationLoop: false,
        slideshow: false,
        itemWidth: 169,
        itemMargin: 5,
        asNavFor: '#slider'
      });

	  $('#carousel2').flexslider({
        animation: "slide",
        controlNav: false,
        animationLoop: false,
        slideshow: false,
        itemWidth: 169,
        itemMargin: 5,
        asNavFor: '#slider'
      });

      $('#slider').flexslider({
        animation: "slide",
        controlNav: false,
        animationLoop: false,
        slideshow: false,
        sync: "#carousel",
        start: function(slider){
          $('body').removeClass('loading');
        }
    });
	}


$('#myModal2').on('shown.bs.modal', function () {
    initFlexModal();
})
$( function() {
	$( "#datepicker-from,#datepicker-from2, #datepicker-to,#datepicker-to2" ).datepicker();
});

$("#slider4").responsiveSlides({
		auto: true,
		pager: false,
		nav: true,
		speed: 500,
		namespace: "callbacks"
	  });


 $("#member_register_password_1_text").keyup(function() {
   var pwd1 = $("#member_register_password_1_text").val();
   var pwd2 = $("#member_register_password_2_text").val();

   if (pwd1.length >= 8)
     $('#member_register_password_8_15_chars').attr('checked', true);
   else
     $('#member_register_password_8_15_chars').attr('checked', false);

   if (/[A-Za-z]+/i.test(pwd1))
     $('#member_register_password_1_letter').attr('checked', true);
   else
     $('#member_register_password_1_letter').attr('checked', false);

   if (/[0-9]+/i.test(pwd1))
     $('#member_register_password_1_number').attr('checked', true);
   else
     $('#member_register_password_1_number').attr('checked', false);

   if (pwd1 == pwd2)
     $('#member_register_password_matches').attr('checked', true);
   else
     $('#member_register_password_matches').attr('checked', false);

 });

 $("#member_register_password_2_text").keyup(function() {
   var pwd1 = $("#member_register_password_1_text").val();
   var pwd2 = $("#member_register_password_2_text").val();

   if (pwd1 == pwd2)
     $('#member_register_password_matches').attr('checked', true);
   else
     $('#member_register_password_matches').attr('checked', false);
 });

 $("#member_register_connect").click(function() {

 });
