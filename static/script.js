// Botón de ver/ocultar contraseña
const togglePassword = document.querySelector('#togglePassword');
const password = document.querySelector('#idPassword');

togglePassword.addEventListener('click', () => {
  const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
  password.setAttribute('type', type);

  togglePassword.classList.toggle('bx-hide');
  togglePassword.classList.toggle('bx-show');
});

let next = document.querySelector(".next");
let prev = document.querySelector(".prev");

next.addEventListener("click", function () {
  let items = document.querySelectorAll(".item");
  document.querySelector(".slide").appendChild(items[0]);
});

prev.addEventListener("click", function () {
  let items = document.querySelectorAll(".item");
  document.querySelector(".slide").prepend(items[items.length - 1]);
});
