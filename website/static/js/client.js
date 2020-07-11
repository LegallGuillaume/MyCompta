function add_client_fn()
{
    socket = io.connect();
    var form = $('#newClient');
    var data = {
        client_name: form.find('#client-name').val(),
        client_address: form.find('#client-address').val(),
        client_comp: form.find('#client-comp').val(),
        client_zipcode: form.find('#client-zipcode').val(),
        client_city: form.find('#client-city').val(),
        client_country: form.find('#client-country').val()
    };
    socket.emit('v3-client-add', data);
    form.find('#client-name').val('');
    form.find('#client-address').val('');
    form.find('#client-comp').val('');
    form.find('#client-zipcode').val('');
    form.find('#client-city').val('');
    form.find('#client-country').val('');
    $('.modal').modal('hide');
}

function del_client_fn()
{
    socket = io.connect();
    var form = $('#deleteClient');
    var data = {
        client_name: form.find('#client-name').val()
    };
    socket.emit('v3-client-delete', data);
    form.find('#client-name').val('');
    $('.modal').modal('hide');
}

function add_card_client(data)
{
    var itb = document.getElementById('container-client');
    var html_line = '<div id="'+ data['name'] +'" class="col-3">'
    html_line += '    <div class="card mb-3 shadow-gray border-gray" style="max-width: 18rem; background-color: transparent;">'
    html_line += '    <div class="card-header text-md text-center font-weight-bold co-gray bg-light">'+ data['name'] +' -- ' + data['id'] +'</div>'
    html_line += '        <div class="card-body text-info">'
    html_line += '            <h5 class="card-title text-right font-weight-bold">' + data['city'] + ', ' + data['country'] + '</h5>'
    html_line += '            <p class="card-text text-right">' + data['address'] + ', ' + data['comp_address'] + '</p>'
    html_line += '        </div>'
    html_line += '    </div>'
    html_line += '</div>'
    itb.insertAdjacentHTML('afterbegin', html_line);
}

function del_card_client(data)
{
    var itb = document.getElementById(data['name']);
    itb.remove();
}