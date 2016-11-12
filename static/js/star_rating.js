$(document).ready(function () {

  $( "#star1" ).click(function() {
    $("#star1").removeClass("btn-default").addClass("btn-warning");
    $("#star2").removeClass("btn-warning").addClass("btn-default");
    $("#star3").removeClass("btn-warning").addClass("btn-default");
    $("#star4").removeClass("btn-warning").addClass("btn-default");
    $("#star5").removeClass("btn-warning").addClass("btn-default");
    $("#rate").val('1');
    $("#rating_numbers").html("1");

  });
  $( "#star2" ).click(function() {
    $("#star1").removeClass("btn-default").addClass("btn-warning");
    $("#star2").removeClass("btn-default").addClass("btn-warning");
    $("#star3").removeClass("btn-warning").addClass("btn-default");
    $("#star4").removeClass("btn-warning").addClass("btn-default");
    $("#star5").removeClass("btn-warning").addClass("btn-default");
    $("#rate").val('2');
    $("#rating_numbers").html("2");

  });
  $( "#star3" ).click(function() {
    $("#star1").removeClass("btn-default").addClass("btn-warning");
    $("#star2").removeClass("btn-default").addClass("btn-warning");
    $("#star3").removeClass("btn-default").addClass("btn-warning");
    $("#star4").removeClass("btn-warning").addClass("btn-default");
    $("#star5").removeClass("btn-warning").addClass("btn-default");
    $("#rate").val('3');
    $("#rating_numbers").html("3");

  });
  $( "#star4" ).click(function() {
    $("#star1").removeClass("btn-default").addClass("btn-warning");
    $("#star2").removeClass("btn-default").addClass("btn-warning");
    $("#star3").removeClass("btn-default").addClass("btn-warning");
    $("#star4").removeClass("btn-default").addClass("btn-warning");
    $("#star5").removeClass("btn-warning").addClass("btn-default");
    $("#rate").val('4');
    $("#rating_numbers").html("4");
  });
  $( "#star5" ).click(function() {
    $("#star1").removeClass("btn-default").addClass("btn-warning");
    $("#star2").removeClass("btn-default").addClass("btn-warning");
    $("#star3").removeClass("btn-default").addClass("btn-warning");
    $("#star4").removeClass("btn-default").addClass("btn-warning");
    $("#star5").removeClass("btn-default").addClass("btn-warning");
    $("#rate").val('5');
    $("#rating_numbers").html("5");

  });
});
