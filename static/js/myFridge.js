$(document).ready( function () {
    loadTable();
} );

function loadTable() {
    $('#fridgeTable').DataTable( {
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
            }
        ],
        order: [[ 3, "asc" ]]
    } );
}