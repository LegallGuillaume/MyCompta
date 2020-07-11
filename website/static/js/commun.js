
function addline(class_copy)
{
    quotation_line = $('.' + class_copy + ':last').clone();
    quotation_line.removeClass('d-none');
    quotation_line.addClass('quotation-copy');
    $('.' + class_copy + ':last').after(quotation_line);
}

function removeline(class_copy)
{
    if ($('.'+ class_copy).length > 1)
    {
        $('.'+ class_copy + ':last').remove();
    }
}

function clear_modal()
{
    $('.quotation-copy').remove();
    original = $('.quotation-line:first');
    original.find('textarea').val('');
    original.find('input').val('');
    original2.find('.quotation-end-text:first');
    original2.find('textarea').val('');
}

function remove_quotation(quotation_id)
{
    $.ajax({
        method: 'POST',
        url: '/quotation-delete',
        data: {quotation: quotation_id}
    }).done(function()
    {
        clear_modal();
    });
    reload_page();
}

$(document).ready(function()
    {
        $('#btn_new_quotation').click(function(e)
        {
            $('#newDevis').modal('hide');
            objs = {
                quotation: $('#quotation-id').val(),
                client: $('#quotation-client').val(),
                date_sent: $('#quotation-datesent').val(),
                date_validity: $('#quotation-datevalidity').val(),
                tax: $('#quotation-tax').prop('checked'),
                lines: [],
                text_end: []
            }
            $('.quotation-line').each(function()
            {
                obj = {}
                obj['description'] = $(this).find('textarea').val();
                obj['quantity'] = $(this).find('input:first').val();
                obj['price'] = $(this).find('input:last').val();
                objs['lines'].push(obj);
            });
            $('.quotation-end-text').each(function()
            {
                objs['text_end'].push({text :$(this).find('textarea').val()});
            });
            $.ajax({
                method: 'POST',
                url: '/quotation-add',
                data: objs
            }).done(function()
            {
                clear_modal();
            });
            reload_page();
        });

        $('#confirmModel').on('show.bs.modal', function (event) {
            var button = $(event.relatedTarget) // Button that triggered the modal
            var recipient = button.data('quotationid') // Extract info from data-* attributes
            var modal = $(this);
            modal.find('.modal-body p').text('Are you sure you want to take out the quotation N° ' + recipient + ' ?');
            modal.find('#btn_del_quotation').data('quotationid', recipient);
        });

        $('#btn_del_quotation').click(function()
        {
            var quotationid = $(this).data('quotationid');
            if(quotationid != '')
            {
                remove_quotation(quotationid);
                $(this).data('quotationid', '');
            }

            $('#confirmModel').modal('hide');
            reload_page();
        });

        $(".custom-file-input").on("change", function() {
            var fileName = $(this).val().split('\\').pop();
            $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
        });
    });

function goTo(elID)
{
    $([document.documentElement, document.body]).animate({
        scrollTop: $('#' + elID).offset().top - 60
    }, 250);
}