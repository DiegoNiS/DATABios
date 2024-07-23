$(document).ready(function() {
    // Inicializar DataTables
    const table = $('#myTable').DataTable({
        "paging": true,     
        "lengthChange": true,   
        "searching": true,      
        "ordering": true,   
        "info": true,
        "language": {
            "url": "https://cdn.datatables.net/plug-ins/1.10.24/i18n/Spanish.json"
        }
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