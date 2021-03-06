(function () {
'use strict';
var website = openerp.website;
var _t = openerp._t;	

website.if_dom_contains('div.o_website_service', function () {
	
    var empty_sign = false;
    $('#modelaccept').on('shown.bs.modal', function (e) {
        $("#signature").empty().jSignature({'decor-color' : '#D1D0CE'});
        empty_sign = $("#signature").jSignature("getData",'image');
    });

    $('#sign_clean').on('click', function (e) {
        $("#signature").jSignature('reset');
    });


    $('form.js_accept_json').submit(function(ev){
        ev.preventDefault();
        var $link = $(ev.currentTarget);
        var href = $link.attr("action");
        var order_id = href.match(/accept\/([0-9]+)/);
        var token = href.match(/token=(.*)/);
        if (token)
            token = token[1];

        var signer_name = $("#name").val();
        var sign = $("#signature").jSignature("getData",'image');
        var is_empty = sign?empty_sign[1]==sign[1]:false;
        $('#signer').toggleClass('has-error', ! signer_name);
        $('#drawsign').toggleClass('panel-danger', is_empty).toggleClass('panel-default', ! is_empty);

        if (is_empty || ! signer_name)
            return false;

        openerp.jsonRpc("/service/order/accept", 'call', {
            'order_id': parseInt(order_id[1]),
            'token': token,
            'signer': signer_name,
            'sign': sign?JSON.stringify(sign[1]):false,
        }).then(function (data) {
            $('#modelaccept').modal('hide');
            window.location.href = '/service/order/'+order_id[1]+'/'+token+'?message=3';
        });
        return false;
    });


});






}());
