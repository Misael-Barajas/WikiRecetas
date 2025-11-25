let idParaEliminar = null;
const modal = document.getElementById('modalConfirmar');
const btnCancelar = document.getElementById('btnCancelarModal');
const btnEliminar = document.getElementById('btnEliminarModal');
const nombreSpan = document.getElementById('nombreCategoriaModal');

function abrirModalCategoria(event, idCategoria, nombreCategoria) {
    event.stopPropagation();
    idParaEliminar = idCategoria;
    if(nombreSpan) nombreSpan.textContent = nombreCategoria;
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

        const url = `/categoria/eliminar/${idParaEliminar}`;

        fetch(url, { method: 'POST' })
        .then(response => {
            if (response.ok || response.redirected) {
                window.location.reload(); 
            } else {
                alert('Error al eliminar la categoría.');
                cerrarModal();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            cerrarModal();
        });
    });
}

window.abrirModalCategoria = abrirModalCategoria;
