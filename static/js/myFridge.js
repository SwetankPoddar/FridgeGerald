$(document).ready( function () {
    loadTable();
} );

function loadTable() {
    if ($.fn.dataTable.isDataTable('#fridgeTable')) {
        $('#fridgeTable').DataTable().destroy();
    }
    $('#fridgeTable').DataTable( {
        "createdRow": function(row, data, dataIndex){
            console.log(data);
            if(data['best_before'] <= 2){
                $(row).addClass('table-danger');
                // very-close-to-expiry
            }
            else if(data['best_before'] <= 5){
                $(row).addClass('table-warning');
                // close-to-expiry
            }
            
        },
        ajax: {
            url: '/ajax/get-fridge',
            dataSrc: ''
        },
        columns: [       
            { data: 'name' },
            { data: 'category' },
            { data: 'quantity' },
            { 
                data: 'best_before',
                render: function(str){
                    str = parseInt(str)
                    result = '<span style="color: '
                    if(str < 3) {
                        result += 'red';
                    } else if (str < 5){
                        result += 'orange';
                    } else {
                        result += 'green';
                    }
                    result += ';">'+str+'</span>';
                    return result;
                },
                className: 'text-center'
            },
            {
                data: 'id',
                render: function(id){
                    id = parseInt(id);
                    return "<a class='btn delete-consume-btn' href='/delete?id="+id+"'> Consumed / Delete </a>";
                },
                bSortable: false,
                className: 'text-center'
            }
        ],
        order: [[ 3, "asc" ]]
    } );
}

function submitForm(formId, url) {
    var form = $('#formModal_'+formId).find('form');
    $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(),
        success: function(){
            loadTable();
            $.get('/ajax/my_fridge_forms', '', function(data){
                $('#forms').html(data);
            });
        },
    });

}