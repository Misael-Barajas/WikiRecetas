document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.btn-opciones').forEach(button => {
        button.addEventListener('click', function(event) {
            event.stopPropagation(); 
            
            let menu = this.nextElementSibling;
            
            document.querySelectorAll('.opciones-menu.mostrar').forEach(openMenu => {
                if (openMenu !== menu) {
                    openMenu.classList.remove('mostrar');
                }
            });
            
            menu.classList.toggle('mostrar');
        });
    });
    
    window.addEventListener('click', function() {
        document.querySelectorAll('.opciones-menu.mostrar').forEach(menu => {
            menu.classList.remove('mostrar');
        });
    });
    });
    
    let idParaEliminar = null;
    const modal = document.getElementById('modalConfirmar');
    const btnCancelar = document.getElementById('btnCancelarModal');
    const btnEliminar = document.getElementById('btnEliminarModal');
    
    function abrirModalConfirmacion(event, idReceta) {
    event.stopPropagation();
    
    let menu = event.currentTarget.closest('.opciones-menu');
    if (menu) {
        menu.classList.remove('mostrar');
    }
    
    idParaEliminar = idReceta;
    modal.classList.add('mostrar');
    }
    
    function cerrarModal() {
    idParaEliminar = null;
    modal.classList.remove('mostrar');
    }
    
    if (btnCancelar) btnCancelar.addEventListener('click', cerrarModal);
    
    if (modal) {
    modal.addEventListener('click', (e) => {
        if (e.target === modal) cerrarModal();
    });
    }
    
    if (btnEliminar) {
    btnEliminar.addEventListener('click', function() {
        if (!idParaEliminar) return;
    
        const url = `/eliminar_receta/${idParaEliminar}`;
    
        fetch(url, { method: 'POST' })
        .then(response => {
            if (response.ok || response.redirected) {
                window.location.reload(); 
            } else {
                alert('Error al eliminar. Verifica permisos.');
                cerrarModal();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            cerrarModal();
        });
    });
    }