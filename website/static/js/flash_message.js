var socket;
$(document).ready(function()
{
    socket = io.connect();

    socket.on('alert', receive_alert);
    if ('/' != window.location.pathname && '/profile' != window.location.pathname)
    {
        socket.on('invoice-name', function(data)
        {
            var form = $('#newInvoice');
            form.find('#invoice-name').val(data['name']);
        });
    
        socket.on('add-invoice', add_line_table_invoice);
        socket.on('delete-invoice', remove_line_table_invoice);
        socket.on('bill-invoice', bill_line_table_invoice);
        socket.on('add-client', add_card_client);
        socket.on('delete-client', del_card_client);
        socket.on('add-insurance', add_card_insurance);
        socket.on('delete-insurance', del_card_insurance);
        socket.on('sel-insurance', sel_card_insurance);
    }

});

function receive_alert(data)
{
    var type = '';
    var type2 = '';
    var icon = '';
    switch (data['type']) {
        case 'danger':
            type = 'border-brown alert-bg-red'
            type2 = 'bg-red-2';
            icon = 'minus-circle'
            break;
        case 'info':
            type = 'border-brown alert-bg-blue'
            type2 = 'bg-blue-2';
            icon = 'info-circle'
            break;
        case 'warning':
            type = 'border-brown alert-bg-cream'
            type2 = 'bg-cream-2';
            icon = 'exclamation-triangle'
            break;
        case 'success':
            type = 'border-brown alert-bg-green'
            type2 = 'bg-green-2';
            icon = 'check-square'
            break;
        default:
            type = 'border-brown alert-bg-light'
            type2 = 'bg-light-2';
            icon = 'question'
            break;
    }
    var html_alert = '<div class="mx-auto mb-1 alert '+ type + ' alert-dismissible" role="alert" style="width:45%; padding:0;">'
    html_alert += '    <div class="row" style="margin-left:0px;">'
    html_alert += '        <div class="col-1 '+ type2 +' p-0 pt-1">'
    html_alert += '            <button type="button" style="background-color: transparent; border:none;" data-dismiss="alert" aria-label="Close"><span class="fas fa-'+ icon +' fa-2x co-brown"></span></button>'
    html_alert += '        </div>'
    html_alert += '        <div class="col">'
    html_alert += '            <p class="text-left" style="margin-left: 5px; margin-top: 5px; color: black;">'+ data['message'] +'</p>'
    html_alert += '        </div>'
    html_alert += '    </div>'
    html_alert += '</div>'

    var calert = document.getElementById('container-alert');
    if ('append' in data)
    {
        if (!data['append'])
            $('.alert').alert('close')
    }
    calert.insertAdjacentHTML('beforeend', html_alert);
    goTo('page-top');
}
