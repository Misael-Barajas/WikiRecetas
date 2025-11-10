
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
  
  let idParaEliminar = null;
  
  const modal = document.getElementById('modalConfirmar');
  const btnCancelarModal = document.getElementById('btnCancelarModal');
  const btnEliminarModal = document.getElementById('btnEliminarModal');

  if (btnCancelarModal) {
    btnCancelarModal.addEventListener('click', cerrarModalConfirmacion);
  }

  if (btnEliminarModal) {
    btnEliminarModal.addEventListener('click', ejecutarEliminacion);
  }

  if (modal) {
    modal.addEventListener('click', function(event) {
        if (event.target === modal) {
            cerrarModalConfirmacion();
        }
    });
  }

});


function abrirModalConfirmacion(event, idReceta) {
  event.stopPropagation();
  
  let menu = event.currentTarget.closest('.opciones-menu');
  if (menu) {
      menu.classList.remove('mostrar');
  }

  idParaEliminar = idReceta;
  const modal = document.getElementById('modalConfirmar');
  if (modal) {
    modal.classList.add('mostrar');
  }
}

function cerrarModalConfirmacion() {
  idParaEliminar = null;
  const modal = document.getElementById('modalConfirmar');
  if (modal) {
    modal.classList.remove('mostrar');
  }
}

function ejecutarEliminacion() {
  if (!idParaEliminar) return;

  const url = `/eliminar_receta/${idParaEliminar}`;

  fetch(url, {
    method: 'POST'
  })
  .then(response => {
    if (response.ok || response.redirected) {
      window.location.reload();
    } else {
      alert('Hubo un error al eliminar la receta.');
      cerrarModalConfirmacion();
    }
  })
  .catch(error => {
    console.error('Error en el fetch:', error);
    alert('Hubo un error de red.');
    cerrarModalConfirmacion();
  });
}