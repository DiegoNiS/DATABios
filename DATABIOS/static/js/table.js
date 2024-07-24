$(document).ready(function() {
    try {
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
    
        // Filtro personalizado para categorías (lista_usuarios.html)
        const categoryFilter = $('#categoryFilter');
    
        if (categoryFilter.length) { // Verifica si el elemento existe en el DOM
            categoryFilter.on('change', function() {
                var selectedCategory = $(this).val();
    
                try {
                    if (selectedCategory) {
                        table.column(0).search('^' + selectedCategory + '$', true, false).draw();
                    } else {
                        table.column(0).search('').draw();
                    }
                } catch (error) {
                    console.error('Error al aplicar el filtro de categoría:', error);
                }
            });
        } else {
            console.warn('Filtrado no correspondiente.');
        }
    } catch (error) {
        console.error('Error al inicializar DataTables:', error);
    }

});