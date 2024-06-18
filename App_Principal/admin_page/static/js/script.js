document.addEventListener('DOMContentLoaded', (event) => {
    const logo = document.getElementById("logo");
    const barralateral = document.querySelector(".barra-lateral");
    const spans = document.querySelectorAll("span");
    const palanca = document.querySelector(".switch");
    const circulo = document.querySelector(".circulo");
    const menu = document.querySelector(".menu");
    const main = document.querySelector("main");
    const body = document.body;
    const opciones = document.querySelectorAll('.opcion');

    if (localStorage.getItem('darkMode') === 'enabled') {
        body.classList.add('dark-mode');
        circulo.classList.add('prendido');
    }

    body.classList.remove('preload');

    menu.addEventListener("click", () => {
        barralateral.classList.toggle("max-barra-lateral");
        if (barralateral.classList.contains("max-barra-lateral")) {
            menu.children[0].style.display = "none";
            menu.children[1].style.display = "block";
        } else {
            menu.children[0].style.display = "block";
            menu.children[1].style.display = "none";
        }
        if (window.innerWidth <= 320) {
            barralateral.classList.add("mini-barra-lateral");
            main.classList.add("min-main");
            spans.forEach((span) => {
                span.classList.add("oculto");
            });
        }
    });

    palanca.addEventListener("click", () => {
        body.classList.toggle("dark-mode");
        circulo.classList.toggle("prendido");

        // Guarda la preferencia en localStorage
        if (body.classList.contains('dark-mode')) {
            localStorage.setItem('darkMode', 'enabled');
        } else {
            localStorage.setItem('darkMode', 'disabled');
        }
    });

    logo.addEventListener("click", () => {
        barralateral.classList.toggle("mini-barra-lateral");
        main.classList.toggle("min-main");
        spans.forEach((span) => {
            span.classList.toggle("oculto");
        });
    });
    
    opciones.forEach((opcion) => {
        opcion.addEventListener('click', () => {
            // Remover la clase 'activo' de todas las opciones
            opciones.forEach((opcion) => {
                opcion.classList.remove('activo');
            });

            // Agregar la clase 'activo' a la opción seleccionada
            opcion.classList.add('activo');
        });
    });

    // Obtener la URL actual
    const urlActual = window.location.href;

    // Comparar la URL actual con la URL de cada opción y marcar la opción correspondiente como activa
    opciones.forEach((opcion) => {
        if (opcion.href === urlActual) {
            opcion.classList.add('activo');
        }
    });
});
