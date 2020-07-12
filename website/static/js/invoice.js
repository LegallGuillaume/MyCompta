
function add_invoice_fn()
{
    socket = io.connect();
    var form = $('#newInvoice');
    var data = {
        invoice_name: form.find('#invoice-name').val(),
        invoice_client: form.find('#invoice-client').val(),
        invoice_project: form.find('#invoice-project').val(),
        invoice_day_rate: form.find('#invoice-day_rate').val(),
        invoice_days: form.find('#invoice-days').val(),
        invoice_datesent: form.find('#invoice-datesent').val(),
        invoice_dateexpiry: form.find('#invoice-dateexpiry').val(),
        invoice_delay: form.find('#invoice-delay').val(),
        invoice_tax: form.find('#invoice-tax').val() == "on"
    };
    socket.emit('v3-invoice-add', data);
    form.find('#invoice-project').val('');
    form.find('#invoice-datesent').val('');
    form.find('#invoice-dateexpiry').val('');
    form.find('#invoice-delay').val('');
    $('.modal').modal('hide');
}

function del_invoice_fn()
{
    socket = io.connect();
    var form = $('#deleteInvoice');
    var data = {
        invoice_name: form.find('#invoice-name').val().split(' -- ')[0]
    };
    socket.emit('v3-invoice-delete', data);
    form.find('#invoice-name').val('');
    $('.modal').modal('hide');
}

function bill_invoice_fn()
{
    socket = io.connect();
    var form = $('#billInvoice');
    var data = {
        invoice_name: form.find('#invoice-name').val().split(' -- ')[0]
    };
    socket.emit('v3-invoice-bill', data);
    form.find('#invoice-name').val('');
    $('.modal').modal('hide');
}


function add_line_table_invoice(data)
{
    var itb = document.getElementById('invoice-table-body');
    var html_line = '<tr id="'+ data["name"] +'" class="'+ (data["sold"] ? 'bg-green' : 'bg-red') +' b-none">'
    html_line += '    <td class="co-brown text-left"><a class="co-brown" target="_blank" href="/pdf/'+ data["name"] +'">'+ data["name"] +'</a></td>'
    html_line += '    <td class="co-brown text-left">'+ data["client"] + '</td>'
    html_line += '    <td class="co-brown text-left">'+ data["project"] + '</td>'
    html_line += '    <td class="co-brown text-left">'+ data["date_sent"] +'</td>'
    html_line += '    <td class="co-brown text-left">'+ data["days"] + '</td>'
    html_line += '    <td class="co-brown text-left">'+ data["day_rate"] +' €</td>'
    html_line += '    <td class="co-brown text-left">'+ (data["tax"] ? data["YES"] : data["NO"]) +'</td>'
    html_line += '    <td class="co-brown text-left">'+ data["date_expiry"] + '</td>'
    html_line += '    <td class="co-brown text-left">'+ data["total"] +' €</td>'
    if (data['tax'])
    html_line += '    <td class="co-brown text-left">'+ data["total_tax"] +' €</td>'
    else
    html_line += '    <td class="co-brown text-left">---</td>'
    html_line += '</tr>'
    itb.insertAdjacentHTML('afterbegin', html_line);

    var dinvoice = $('#deleteInvoice');
    select = dinvoice.find('#invoice-name')[0];
    select.insertAdjacentHTML('afterbegin', '<option id="op_'+ data['name'] +'">'+ data['name'] +' -- ' + data['id'] +'</option>')

    var binvoice = $('#billInvoice');
    select2 = binvoice.find('#invoice-name')[0];
    select2.insertAdjacentHTML('afterbegin', '<option id="op_'+ data['name'] +'">'+ data['name'] +' -- ' + data['id'] +'</option>')

}

function remove_line_table_invoice(data)
{
    var itb = document.getElementById(data['name']);
    itb.remove();
    
    var ito = $('#deleteInvoice').find('#op_' + data['name']);
    ito.remove();
    var ito2 = $('#billInvoice').find('#op_' + data['name']);
    ito2.remove();
}

function bill_line_table_invoice(data)
{
    var itb = $('#'+ data['name']);
    itb.removeClass('bg-red');
    itb.addClass('bg-green');
}