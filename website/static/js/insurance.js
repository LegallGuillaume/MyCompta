function add_insurance_fn()
{
    socket = io.connect();
    var form = $('#newInsurance');
    var data = {
        insurance_name: form.find('#insurance-name').val(),
        insurance_type: form.find('#insurance-type').val(),
        insurance_region: form.find('#insurance-region').val(),
        insurance_contract: form.find('#insurance-contract').val()
    };
    socket.emit('v3-insurance-add', data);
    form.find('#insurance-name').val('');
    form.find('#insurance-type').val('');
    form.find('#insurance-region').val('');
    form.find('#insurance-contract').val('');
    $('.modal').modal('hide');
}

function del_insurance_fn()
{
    socket = io.connect();
    var form = $('#deleteInsurance');
    var data = {
        insurance_name: form.find('#insurance-name').val().split(' -- ')[0]
    };
    socket.emit('v3-insurance-delete', data);
    form.find('#insurance-name').val('');
    $('.modal').modal('hide');
}

function sel_insurance_fn()
{
    socket = io.connect();
    var form = $('#selInsurance');
    var data = {
        insurance_name: form.find('#insurance-name').val().split(' -- ')[0]
    };
    socket.emit('v3-insurance-sel', data);
    form.find('#insurance-name').val('');
    $('.modal').modal('hide');
}

function add_card_insurance(data)
{
    var itb = document.getElementById('container-insurance');
    var html_line = '<div id="'+ data['name'].replace(' ', '-') +'" class="col-3">'
    html_line += '    <div class="card mb-3 shadow-gray border-gray" style="max-width: 18rem; background-color: transparent;">'
    html_line += '    <div class="card-header text-md text-center font-weight-bold co-gray bg-light">'+ data['name'] +' -- ' + data['id'] +'</div>'
    html_line += '        <div class="card-body text-info">'
    html_line += '            <h5 class="card-title text-right font-weight-bold">' + data['type'] + ', ' + data['region'] + '</h5>'
    html_line += '            <p class="card-text text-right sel-insurance">' + (data['sel'] ? data['SELECT'] : data['NOTSELECT']) + '</p>'
    html_line += '        </div>'
    html_line += '    </div>'
    html_line += '</div>'
    itb.insertAdjacentHTML('afterbegin', html_line);

    var dinsurance = $('#deleteInsurance');
    select = dinsurance.find('#insurance-name')[0];
    select.insertAdjacentHTML('afterbegin', '<option id="op_'+ data['name'].replace(' ', '-') +'">'+ data['name'] +' -- ' + data['id'] +'</option>')

    var sinsurance = $('#selInsurance');
    select2 = sinsurance.find('#insurance-name')[0];
    select2.insertAdjacentHTML('afterbegin', '<option id="op_'+ data['name'].replace(' ', '-') +'">'+ data['name'] +' -- ' + data['id'] +'</option>')

}

function del_card_insurance(data)
{
    var itb = document.getElementById(data['name']);
    itb.remove();

    var ito = $('#op_' + data['name'].replace(' ', '-'));
    ito.remove();
}

function sel_card_insurance(data)
{
    var itb = $('#' + data['name']);
    itb.find('.sel-insurance').text(data['SELECT'])
}
