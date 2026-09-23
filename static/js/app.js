// JavaScript usado únicamente cuando aporta interacción real en el navegador.

document.addEventListener("DOMContentLoaded", function () {
  // En el formulario de asignación de horarios: si el Gerente marca
  // "Marcar como descanso", deshabilitamos los campos de hora para
  // evitar datos inconsistentes.
  const checkDescanso = document.getElementById("id_es_descanso");
  const entrada = document.getElementById("id_entrada");
  const salida = document.getElementById("id_salida");

  if (checkDescanso && entrada && salida) {
    const actualizar = () => {
      const desactivar = checkDescanso.checked;
      entrada.disabled = desactivar;
      salida.disabled = desactivar;
      entrada.required = !desactivar;
      salida.required = !desactivar;
    };
    checkDescanso.addEventListener("change", actualizar);
    actualizar();
  }

  // Botón "seleccionar todos" en la lista de colaboradores por área
  const seleccionarTodos = document.getElementById("seleccionar-todos");
  if (seleccionarTodos) {
    seleccionarTodos.addEventListener("change", function () {
      document.querySelectorAll(".chk-colaborador").forEach((chk) => {
        chk.checked = seleccionarTodos.checked;
      });
    });
  }
});
