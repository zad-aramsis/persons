odoo.define("persons.NewPersonForm", function(require){
'use strict';
console.log("Hi this is for the testing purpose log write down.");
var publicWidget = require("web.public.widget");

publicWidget.registry.NewPersonForm = publicWidget.Widget.extend({
    selector:"#new_person_creation",
    events:{
        'submit': "_onSubmitButton",
    },

    _onSubmitButton: function(evt){
        var personName = this.$("input[name='name']").val();
        var $userName = this.$("select[name='user']");
        var user_name = ($userName.val() || '0');
        if(!personName){
            $("#person_client_side_validation_message").html("Please enter Person name.");
            $("#person_client_side_validation_message").show();
            evt.preventDefault();
        }
        if(!user_name || user_name == '0'){
            $("#person_client_side_validation_message").html("Please select User.");
            $("#person_client_side_validation_message").show();
            evt.preventDefault();
        }
        if(!user_name.match(/^[0-9]+$/)){
            $("#person_client_side_validation_message").html("Please select proper User option.");
            $("#person_client_side_validation_message").show();
            evt.preventDefault();
        }
    },
});
});