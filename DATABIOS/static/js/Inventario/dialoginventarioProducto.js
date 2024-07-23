document.addEventListener('DOMContentLoaded', function() {
    // Dialog Crear Productos
    const DialogAdd = document.getElementById('DiaInvProAdd')
    const openDialogAdd = document.getElementById('openDiaInvProAdd')
    const closeDialogAdd = document.getElementById('closeDiaInvPraAdd')
    const cancelDialogAdd = document.getElementById('cancelDiaInvProAdd') 
    // Dialog Editar Productos
    const editarDialog = document.getElementById('editarProductoDialog');

    // Eliminar Productos
    const eliminarDialog = document.getElementById('eliminarProductoDialog');

    /* ADD dialog */
    openDialogAdd.addEventListener('click', function() {
        DialogAdd.showModal();
    });

    closeDialogAdd.addEventListener('click', function() {
        DialogAdd.close();
    });

    cancelDialogAdd.addEventListener('click', function() {
        DialogAdd.close();
    });
    
    /* All delete Buttons */
});
