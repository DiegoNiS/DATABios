$(document).ready(function() {
    // Inicializar DataTables
    let table = $('#myTable').DataTable({
        "paging": true,     
        "lengthChange": true,   
        "searching": true,      
        "ordering": true,   
        "info": true,
        "language": {
            url: "//cdn.datatables.net/plug-ins/2.1.0/i18n/es-MX.json",
        },
    });

    // Filtro personalizado para categorías
    $('#categoryFilter').on('change', function() {
        var selectedCategory = $(this).val();

        if (selectedCategory) {
            table.column(0).search('^' + selectedCategory + '$', true, false).draw();
        } else {
            table.column(0).search('').draw();
        }
    });
});