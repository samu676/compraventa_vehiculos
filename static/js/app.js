/* Interacciones del lado del navegador: contadores animados, buscador,
   filtros del catálogo y cambio de vista (tarjetas / tabla).
   Todo es opcional: si JavaScript falla, las páginas siguen funcionando. */

// Quita tildes y pasa a minúsculas para que "camion" encuentre "Camión"
const normalizar = t => (t || '').toString().toLowerCase()
  .normalize('NFD').replace(/[̀-ͯ]/g, '');

// ---------------------------------------------------------- contadores animados
function animarContadores() {
  // Si el usuario pidió "reducir movimiento" en su sistema, se muestran los valores directamente
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  document.querySelectorAll('[data-contar]').forEach(el => {
    const final = parseFloat(el.dataset.contar) || 0;
    const esPesos = el.hasAttribute('data-pesos');
    const formato = v => (esPesos ? '$ ' : '') + Math.round(v).toLocaleString('es-CO');
    const inicio = performance.now();
    const duracion = 900;
    function paso(ahora) {
      const t = Math.min((ahora - inicio) / duracion, 1);
      el.textContent = formato(final * (1 - Math.pow(1 - t, 3)));  // desacelera al final
      if (t < 1) requestAnimationFrame(paso);
    }
    requestAnimationFrame(paso);
  });
}

// ---------------------------------------------------------- buscador y filtros
function aplicarFiltros() {
  const buscador = document.querySelector('[data-buscador]');
  if (!buscador) return;
  const texto = normalizar(buscador.value);
  const filtros = [...document.querySelectorAll('select[data-filtro]')]
    .map(s => [s.dataset.filtro, s.value]).filter(([, v]) => v);

  let elementos = document.querySelectorAll('[data-buscable]');
  if (!elementos.length) elementos = document.querySelectorAll('main table tbody tr');

  let visibles = 0;
  elementos.forEach(el => {
    const coincide = normalizar(el.textContent).includes(texto)
      && filtros.every(([campo, valor]) => el.dataset[campo] === valor);
    el.classList.toggle('d-none', !coincide);
    const vista = el.closest('[data-vista-contenido]');
    if (coincide && (!vista || !vista.classList.contains('d-none'))) visibles++;
  });
  const aviso = document.getElementById('sin-resultados');
  if (aviso) aviso.classList.toggle('d-none', visibles > 0);
}

// ---------------------------------------------------------- vista tarjetas / tabla
function cambiarVista(vista) {
  document.querySelectorAll('[data-vista-contenido]').forEach(c =>
    c.classList.toggle('d-none', c.dataset.vistaContenido !== vista));
  document.querySelectorAll('[data-vista]').forEach(b =>
    b.classList.toggle('active', b.dataset.vista === vista));
  try { localStorage.setItem('vista-vehiculos', vista); } catch (e) { /* sin almacenamiento */ }
  aplicarFiltros();
}

document.addEventListener('DOMContentLoaded', () => {
  animarContadores();

  document.querySelectorAll('[data-buscador], select[data-filtro]').forEach(el =>
    el.addEventListener('input', aplicarFiltros));

  const botonesVista = document.querySelectorAll('[data-vista]');
  if (botonesVista.length) {
    botonesVista.forEach(b => b.addEventListener('click', () => cambiarVista(b.dataset.vista)));
    let guardada = null;
    try { guardada = localStorage.getItem('vista-vehiculos'); } catch (e) { /* sin almacenamiento */ }
    cambiarVista(guardada || 'tarjetas');
  }
});
