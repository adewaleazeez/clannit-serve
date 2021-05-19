//Jquery to update re-put field by 30%
$('#selectreput').change(function(){
    var amount = $('#selectreput').val();
    var increase_percent = Number((amount * 0.33335).toPrecision(2)) ;
    var sum = $('#reput_increase_value').val(increase_percent);
});
$('#selectreputfresh').change(function(){
    var amount = $('#selectreput').val();
    var increase_percent = Number((amount * 0.33335).toPrecision(2))
    var new_put = $('#selectreputfresh').val();
    var reput_value = increase_percent + Number(new_put);
    $('#reput_increase_value').val(reput_value);
    });
//Ajax post request for reput out amount
$('#reputbtn').click(function(){
$('#reputbtn').attr('disabled', true);
var reput_amount = $('#reput_increase_value').val();
var former_put_id = $('#selectreput :selected').data('reput');
var reput_sub = $('#reputbtn').val();


var data = {reput_amount: reput_amount,former_put_id: former_put_id, reput_sub: reput_sub };

if(confirm("Are you sure you want to proceed with this put order?"))
 {
 if(former_put_id){
  $.ajax({
  type: "POST",
  url: "/dashboard",
  data: data,

  success: function(data){
  window.location.href= "/dashboard";
  }
  });

  }else{
  alert('Kindly Select an amount before proceeding')
  }
  }
  return false;
  });












//Jquery to update put field by 50%
$('#selectput').change(function(){
    var amount = $('#selectput').val();
    var increase_percent = '$'+(Number(amount)+ Number(amount * 0.5)) ;
    $('#increase_value').val(increase_percent);
});


//Jquery to sum the addition of out amount and commissions
$('#selectout, #commission').change(function(){

    var sum = 0;
    $('#selectout :selected').each(function() {
        sum += Number($(this).val());
    });
    $('#commission :selected').each(function() {
        sum += Number($(this).val());
    });
    $("#sum").val(sum);
    $('#outbtn').click(function(){
    });
});


//Ajax post request for out amount
$("#outbtn").click(function(){
$('#outbtn').attr('disabled', true);
var out = $('#selectout :selected').map(function(i,el){
                return $(el).data('id')}).get();
var commission = $('#commission :selected').map(function(i,el){
                return $(el).data('commission')}).get();

var data = {out_amount: $('#sum').val(), out_sub: $('#outbtn').val(), out: out, commission: commission};

if(confirm("Are you sure you want to proceed with this out order?"))
 {
 if($('#sum').val() && $('#sum').val() != '0' ){
  $.ajax({
  type: "POST",
  url: "/dashboard",
  data: data,

  success: function(data){
  window.location.href= "/dashboard";
  }
  });

  }else{
  alert('Kindly Select an amount before proceeding')
  }
  }
  return false;
  });


//Ajax post request for put amount
$("#putbtn").click(function(){
$('#putbtn').attr('disabled', true);
var put_amount = $('#selectput').val();
var put_sub = $('#putbtn').val();

var data = {put_amount: put_amount, put_sub: put_sub};


if(confirm("Are you sure you want to proceed with this Put order?"))
 {
 if(put_amount && put_amount != '' ){
  $.ajax({
  type: "POST",
  url: "/dashboard",
  data: data,

  success: function(data){
  window.location.href= "/dashboard";
  }
  });

  }else{
  alert('Kindly Select an amount before proceeding')
  }
  }
  return false;
  });



//
//$('#selectout').change(function(){
//var selected = $('#selectout').val();
//
//var total = 0;
//for (var i = 0; i < selected.length; i++) {
//    total += selected[i] << 0;
//}
//var sum_total = total;
//
//$('#subbut').click(function(){
//confirm(sum_total);
//});
//
//console.log(selected);
//});


