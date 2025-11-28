const modal = document.getElementById('modalConfirmar');
const btnCancelar = document.getElementById('btnCancelarModal');
const nombreSpan = document.getElementById('nombreUsuarioModal');
const formEliminar = document.getElementById('formEliminarUsuario');

function abrirModalUsuario(event, idUsuario, nombreUsuario) {
    event.stopPropagation();
    if(nombreSpan) nombreSpan.textContent = nombreUsuario;
    formEliminar.action = "/admin/usuario/eliminar/" + idUsuario;
    modal.classList.add('mostrar');
}

function cerrarModal() {
    modal.classList.remove('mostrar');
}

if (btnCancelar) btnCancelar.addEventListener('click', cerrarModal);
if (modal) modal.addEventListener('click', (e) => { if (e.target === modal) cerrarModal(); });