/**
 * Clannit.js v1.0.0
 * https://github.com/olayinkaakeju/clannit.js *
 * 
 * Copyright (C) 2018 Olayinka Akeju (@afshinmeh)
 */

$(document).ready(function(){
    $(function() {
        // Toolbar extra buttons
        var btnFinish = $('<button></button>').text('Close')
        .addClass('btn btn-info')
        .on('click', function(){ alert('Finish Clicked'); });

        var btnCancel = $('<button></button>').text('Refresh')
            .addClass('btn btn-danger')
            .on('click', function(){ $('#smartwizard').smartWizard("reset"); });

        $('#id_building').change(function () {
            var optionSelected = $(this).find(':selected').data('type');
            building_id = document.querySelector('#id_building').value;
            data = {'building_id': building_id, 'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()};
    
            $.ajax({
                url: "/get_details_apartment/",
                type: "POST",
                data: data,
                success : function(result) {
                    $("#id_apartment option").remove();
                    $("#id_apartment").append('<option value="">Select apartment</option>');
                    if(result.length < 1){
                        $("#id_apartment").append('<option value="">No apartment in the selected building</option>');
                    } 
                    for (var i = result.length - 1; i >= 0; i--) {
                        $("#id_apartment").append('<option value="'+result[i].apartment_id+'">'+ result[i].apartment_number +'</option>');
                    }
                },
            });
        });

        $("#role_select").change(function() {
            if ($("#security_select").is(":selected")) {
                $("#select_security").show();
                $("select#id_street option:checked").val("Gate");
                $("select#id_building option:checked").val("Gate");
                $("select#id_apartment option:checked").val("Gate");
                $("#select_resident").hide();
                
            } else {
                $("#select_security").hide();
                $("#select_resident").show();
            }
        }).trigger('change');

        $("#role_select2").change(function() {
            if ($("#security_select").is(":selected")) {
                $("#select_security").show();
                $("select#id_street3 option:checked").val("Gate");
                $("select#building_red option:checked").val("Gate");
                $("select#apartment_red option:checked").val("Gate");
                $("#select_resident").hide();
                
            } else {
                $("#select_security").hide();
                $("#select_resident").show();
            }
        }).trigger('change');

        $('#id_street').change(function () {
            var optionSelected = $(this).find("option:selected");
            var valueSelected  = optionSelected.val();
            var street_name   = optionSelected.text();

            data = {'street_name': valueSelected, 'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()}
            
            $.ajax({
                url: "/get_details/", 
                type: "POST",
                data: data, 
                success : function(result) {
                    $("#id_building option").remove();
                    $("#id_building").append('<option value="">Select building</option>');
                    if(result.length < 1){
                        $("#id_building").append('<option value="">No building in the selected street</option>');
                    } 
                    else{
                        for (var i = result.length - 1; i >= 0; i--) {
                            $("#id_building").append('<option value="'+result[i].building_id+'" data-type="'+result[i].building_type+'">'+ result[i].building_number +'</option>');
                        };
                    }
                    
                },
            });
        });

        $('#password_change').click(function(){
            password1 = document.querySelector('#password1').value;
            password2 = document.querySelector('#password2').value;
            user_id = document.querySelector('#user_id').value;
     
            if(password1.length != 0 && password2.length != 0 && password1 == password2){
                data = {'user_id': user_id, 'password1': password1, 'password2':password1};
                $.ajax({
                    url: "/profile_status/",
                    type: "POST",
                    data: data,
                    success : function(result) {
                        console.log(result);
                        window.location.href = "http://www.clannit.com/estate_manager_dashboard";
                    },
                });
     
            } else{
                alert("PLEASE ENTER A VALID PASSWORD");
            }
        });

        $('#password_change1').click(function(){
            password1 = document.querySelector('#password3').value;
            password2 = document.querySelector('#password4').value;
            user_id = document.querySelector('#user_id').value;
     
            if(password1.length != 0 && password2.length != 0 && password1 == password2){
                data = {'user_id': user_id, 'password1': password1, 'password2':password1};
                $.ajax({
                    url: "/profile_status/",
                    type: "POST",
                    data: data,
                    success : function(result) {
                        console.log(result);
                        window.location.href = "http://www.clannit.com/estate_manager_dashboard";
                    },
                });
     
            } else{
                alert("PLEASE ENTER A VALID PASSWORD");
            }
        });

        $(".del_but").click(function(){
            var check = confirm("Are you sure you want to delete this item?");
            if (check == true) {
                return true;
            }
            else {
                return false;
            }
        });

        $("#site_tour").click(function() {
            $('#first_visit1').modal('toggle');
            introJs().start();
            
 
        });

        $("#smartwizard").on("showStep", function(e, anchorObject, stepNumber, stepDirection, stepPosition) {
            //alert("You are on step "+stepNumber+" now, " +stepPosition);
            if(stepPosition === 'first'){
                $("#prev-btn").addClass('disabled');
            }else if(stepPosition === 'final'){
                $("#next-btn").addClass('disabled');
            }else{
                $("#prev-btn").removeClass('disabled');
                $("#next-btn").removeClass('disabled');
            }
        }); 

        // Smart Wizard 1
        $('#smartwizard').smartWizard({
            selected: 0,
            theme: 'arrows',
            transitionEffect:'fade',
            showStepURLhash: false,
            toolbarSettings: {toolbarPosition: 'bottom'},
            ajaxSettings:{}
        
        });

        /*To save, delete or edit street: Saving is working, others on hold*/ 
        $("#addstreet").click(function(){
            $(".id_street1 option").remove();
            streetname = document.querySelector('#streetname').value;
            estate_id = document.querySelector('#estate_id').value;
            if(streetname.length == 0){
                alert("Please enter a street name");            
            }
            else{
                data = {'estate_id': estate_id, 'streetname': streetname, 'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()};
                $.ajax({
                    beforeSend: function(){
                        $('#loader').show();
                    },
                    url: "/add_street/",
                    type: "POST",
                    data: data,
                    success : function(result) {
                        $("#addstreet").trigger("reset");
                        if(result == 'True'){
                            $('#suc_msg1').html("Street was succesfully created").addClass('bg-success').fadeIn('slow');
                            $('#suc_msg1').delay(5000).fadeOut('slow');
                            
                        }
                        else{
                            $('#suc_msg1').html("Street aleady exists").addClass('bg-danger').fadeIn('slow');
                            $('#suc_msg1').delay(5000).fadeOut('slow');
                        }
                        $('#loader').hide();
                        get_streets(estate_id);
                        
                    },
                });
                
            }
        });

        /*To save, delete or edit building: Saving is working, others on hold*/ 
        $("#addbuilding").click(function(){
            street_id = document.querySelector('#id_street1').value;
            building = document.querySelector('#id_building_number').value;
            building_type = document.querySelector('#id_building_type').value;

            if(street_id.length == 0 || building.length == 0 || building_type.length == 0){
                alert("Ensure to fill all fields");            
            }
            else{
                data = {'street_id': street_id, 'building': building, 'building_type': building_type, 'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()};
                $.ajax({
                    beforeSend: function(){
                        $('.loader').show();
                    },
                    url: "/add_building/",
                    type: "POST",
                    data: data,
                    success : function(result) {
                        if(result == 'True'){
                            $('#suc_msg2').html("Building was succesfully created").addClass('bg-success').fadeIn('slow');
                            $('#suc_msg2').delay(5000).fadeOut('slow');
                        }
                        else{
                            $('#suc_msg2').html("Building aleady exists").addClass('bg-danger').fadeIn('slow');
                            $('#suc_msg2').delay(5000).fadeOut('slow');
                        }
                        $('.loader').hide();
                        
                    },
                });
                
            }
        });

        /*To save, delete or edit apartment: Saving is working, others on hold*/ 
        $("#addapartment").click(function(){
            street_id = document.querySelector('#id_street2').value;
            building = document.querySelector('#id_building2').value;
            apartment = document.querySelector('#id_apartment_number').value;

            if(street_id.length == 0 || building.length == 0 || apartment.length == 0){
                alert("Please ensure to fill all fields");            
            }
            else{
                data = {'street_id': street_id, 'building': building, 'apartment': apartment, 'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()};
                $.ajax({
                    beforeSend: function(){
                        $('.loaderc').show();
                    },
                    url: "/add_apartment/",
                    type: "POST",
                    data: data,
                    success : function(result) {
                        if(result == 'True'){
                            $('#suc_msg3').html("Apartment was succesfully created").addClass('bg-success').fadeIn('slow');
                            $('#suc_msg3').delay(5000).fadeOut('slow');
                        }
                        else{
                            $('#suc_msg3').html("Apartment aleady exists").addClass('bg-danger').fadeIn('slow');
                            $('#suc_msg3').delay(5000).fadeOut('slow');
                        }
                        $('.loader').hide();
                        
                    },
                });
                
            }
        });

        /*To save, delete or edit apartment: Saving is working, others on hold*/ 
        $("#addresident").click(function(){
            data = {};
            data.title_resd = $("#title_resd").val();
            data.first_name = $("#first_name_resd").val();
            data.last_name = $("#last_name_resd").val();
            data.email = $("#user_email").val();
            data.mobile_number = $("#mobile_no").val();

            data.gender = $("#my_gender").val();
            data.role = $("#role_select2").val();
            data.street = $("#id_street3").val();
            data.building = $("#building_red").val();
            data.apartment = $("#apartment_red").val();
            data.csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val()

            if(data.first_name.length == 0 || data.gender.length == 0 || 
                data.last_name.length == 0 || data.role.length == 0 || 
                data.email.length == 0 || data.street.length == 0 || 
                data.mobile_number.length == 0 || data.building.length == 0 || 
                data.apartment.length == 0){
                alert("All fields are required")
            }
            else{
                $.ajax({
                    beforeSend: function(){
                        $('#loaderf').show();
                    },
                    url: "/add_residents/",
                    type: "POST",
                    data: data,
                    success : function(result) {
                        if(result == 'True'){
                            $('#suc_msg4').html("Resident was succesfully created").addClass('bg-success').fadeIn('slow');
                            $('#suc_msg4').delay(5000).fadeOut('slow');
                        }
                        else{
                            $('#suc_msg4').html("Resident aleady exists").addClass('bg-danger').fadeIn('slow');
                            $('#suc_msg4').delay(5000).fadeOut('slow');
                        }
                        $('#loaderf').hide();
                        
                    },
                });
            }
        });

        /*Get streets within an estate */
        function get_streets(estate_id){
            data = {'estate_id': estate_id, 'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()};
            $.ajax({
                url: "/get_all_streets/",
                type: "POST",
                data: data,
                success : function(result) {
                    $(".id_street1 option").remove();
                    
                    if(result.length < 1){
                        $(".id_street1").append('<option value="">No street has been created</option>');
                    }else{
                        $(".id_street1").append('<option value="">Select street name</option>');
                        for (var i = result.length - 1; i >= 0; i--) {
                        $(".id_street1").append('<option value="'+result[i].street_id+'">'+ result[i].street_name +'</option>');
                        }
                    } 
                },
            });
        }

        /*Get buildings from a street as it changes*/
        $('#id_street2').change(function(){
            var optionSelected = $(this).find("option:selected");
            var valueSelected  = optionSelected.val();
            var street_name   = optionSelected.text();

            data = {'street_name': valueSelected, 'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()}
            
            $.ajax({
                url: "/get_details/",
                type: "POST",
                data: data,
                beforeSend: function(){
                    $('#loaderb').show();
                },
                success : function(result) {
                    $("#id_building2 option").remove();
                    $("#id_building2").append('<option value="">Select building</option>');
                    if(result.length < 1){
                        $("#id_building2").append('<option value="">No building in the selected street</option>');
                    } 
                    else{
                        for (var i = result.length - 1; i >= 0; i--) {
                            $("#id_building2").append('<option value="'+result[i].building_id+'" data-type="'+result[i].building_type+'">'+ result[i].building_number +'</option>');
                        }
                    }
                    $('#loaderb').hide();
                },
            });
        });

        /*Get buildings from a street as it changes*/
        $('#id_street3').change(function(){
            var optionSelected = $(this).find("option:selected");
            var valueSelected  = optionSelected.val();
            var street_name   = optionSelected.text();

            data = {'street_name': valueSelected, 'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()}
            
            $.ajax({
                url: "/get_details_build/",
                type: "POST",
                data: data,
                beforeSend: function(){
                    $('#loaderd').show();
                },
                success : function(result) {
                    $("#building_red option").remove();
                    $("#building_red").append('<option value="">Select building</option>');
                    if(result.length < 1){
                        $("#building_red").append('<option value="">No building in the selected street</option>');
                    } 
                    else{
                        for (var i = result.length - 1; i >= 0; i--) {
                            $("#building_red").append('<option value="'+result[i].building_id+'" data-type="'+result[i].building_type+'">'+ result[i].building_number +'</option>');
                        }
                    }
                    $('#loaderd').hide();
                },
            });
        });

        $('#building_red').change(function(){
            var optionSelected = $(this).find("option:selected");
            var valueSelected  = optionSelected.val();
            var optionSelected2 = $(this).find(':selected').data('type');

            if(optionSelected2 == 0){
                $("#apartment_red option").remove();
                $("#apartment_red").append('<option value="1">Single Tenancy</option>');
            }
            else {
                data = {'building_id': valueSelected, 'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()}
            
                $.ajax({
                    url: "/get_details_apartment/",
                    type: "POST",
                    data: data,
                    beforeSend: function(){
                        $('#loadere').show();
                    },
                    success : function(result) {
                        $("#apartment_red option").remove();
                        $("#apartment_red").append('<option value="">Select apartment</option>');
                        if(result.length < 1){
                            $("#apartment_red").append('<option value="">No apartment in the selected building</option>');
                        } 
                        else{
                            for (var i = result.length - 1; i >= 0; i--) {
                                $("#apartment_red").append('<option value="'+result[i].apartment_id+'">'+ result[i].apartment_number +'</option>');
                            }
                        }
                        $('#loadere').hide();
                    },
                });
            }
        });

    });

    

    

    

});



//Checkbox function
// $('input[type="checkbox"]').click(function(){
//     if($(this).is(":checked")){
//         var user_id = $(this).val();
//         data = {'profile_status': 1, 'user_id': user_id}
//         $.ajax({
//             url: "/profile_status/",
//             type: "POST",
//             data: data,
//             success : function(result) {
//                 console.log(result);
//             },
//         });
//     }
// });

