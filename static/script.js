// Botón de ver/ocultar contraseña
const togglePassword = document.querySelector('#togglePassword');
const password = document.querySelector('#idPassword');

togglePassword.addEventListener('click', () => {
  const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
  password.setAttribute('type', type);

  togglePassword.classList.toggle('bx-hide');
  togglePassword.classList.toggle('bx-show');
});
<<<<<<< HEAD
// Carrusel
=======

// Carrusel
>>>>>>> 8846363 (Actualiza recetas y mejora la interfaz de usuario en varias plantillas)
