
function addline(class_copy)
{
    devis_line = $('.' + class_copy + ':last').clone();
    devis_line.removeClass('d-none');
    devis_line.addClass('devis-copy');
    $('.' + class_copy + ':last').after(devis_line);
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
    $('.devis-copy').remove();
    original = $('.devis-line:first');
    original.find('textarea').val('');
    original.find('input').val('');
    original2.find('.devis-end-text:first');
    original2.find('textarea').val('');
}

function remove_devis(devis_id)
{
    $.ajax({
        method: 'POST',
        url: '/quotation-delete',
        data: {devis: devis_id}
    }).done(function()
    {
        clear_modal();
    });
    reload_page();
}

$(document).ready(function()
    {
        $('#btn_new_devis').click(function(e)
        {
            $('#newDevis').modal('hide');
            objs = {
                devis: $('#devis-id').val(),
                client: $('#devis-client').val(),
                date_envoi: $('#devis-dateenvoi').val(),
                date_validite: $('#devis-datevalidite').val(),
                tva: $('#devis-tva').prop('checked'),
                lines: [],
                text_end: []
            }
            $('.devis-line').each(function()
            {
                obj = {}
                obj['description'] = $(this).find('textarea').val();
                obj['quantity'] = $(this).find('input:first').val();
                obj['prix'] = $(this).find('input:last').val();
                objs['lines'].push(obj);
            });
            $('.devis-end-text').each(function()
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
            var recipient = button.data('devisid') // Extract info from data-* attributes
            var modal = $(this);
            modal.find('.modal-body p').text('Etês-vous sùr de vouloir supprimer le devis N° ' + recipient + ' ?');
            modal.find('#btn_supp_devis').data('devisid', recipient);
        });

        $('#btn_supp_devis').click(function()
        {
            var devisid = $(this).data('devisid');
            if(devisid != '')
            {
                remove_devis(devisid);
                $(this).data('devisid', '');
            }

            $('#confirmModel').modal('hide');
            reload_page();
        });

        $(".custom-file-input").on("change", function() {
            var fileName = $(this).val().split('\\').pop();
            $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
        });
    });