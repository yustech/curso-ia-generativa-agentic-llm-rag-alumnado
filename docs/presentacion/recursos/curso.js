/* Comportamiento de las presentaciones del curso. */
(function () {
  "use strict";
  var parametros = new URLSearchParams(location.search);
  var esProfesor = document.body.classList.contains("profesor");
  var modoClase = esProfesor && parametros.has("clase");
  var imprimir = parametros.has("print-pdf");
  if (imprimir) { document.body.classList.add("imprimir"); }

  // Modo clase: la versión del profesor sin sus diapositivas privadas.
  if (modoClase) {
    document.querySelectorAll(".slides > section.profe").forEach(function (s) { s.remove(); });
    document.querySelectorAll(".insignia").forEach(function (s) { s.remove(); });
    document.body.classList.add("modo-clase");
  }

  var deck = new Reveal({
    width: 1280, height: 720, margin: 0.075, minScale: 0.2, maxScale: 2.5,
    hash: true, center: false, controls: true, controlsTutorial: false, progress: true,
    slideNumber: "c/t", transition: "slide", transitionSpeed: "default", backgroundTransition: "fade",
    navigationMode: "linear", overview: true, touch: true, pdfSeparateFragments: false,
    plugins: [RevealNotes, RevealSearch, RevealZoom]
  });

  function $(selector, raiz) { return (raiz || document).querySelector(selector); }
  function $$(selector, raiz) { return Array.prototype.slice.call((raiz || document).querySelectorAll(selector)); }

  var aviso = document.createElement("div");
  aviso.className = "aviso";
  $(".reveal").appendChild(aviso);
  var temporizador;
  function avisar(texto) {
    aviso.textContent = texto;
    aviso.classList.add("visible");
    clearTimeout(temporizador);
    temporizador = setTimeout(function () { aviso.classList.remove("visible"); }, 1600);
  }

  // Ajuste: si el contenido no cabe en la diapositiva, se reduce lo justo.
  function ajustar(seccion) {
    if (!seccion || seccion.classList.contains("sin-ajuste")) { return; }
    var cuerpo = $(".cuerpo", seccion);
    if (!cuerpo) { return; }
    cuerpo.style.transform = "";
    cuerpo.style.width = "";
    // Una línea de código demasiado larga reduce la letra de su bloque antes que obligar a desplazar.
    $$("pre", cuerpo).forEach(function (pre) {
      pre.style.fontSize = "";
      if (pre.scrollWidth > pre.clientWidth + 2) {
        var base = parseFloat(getComputedStyle(pre).fontSize);
        pre.style.fontSize = Math.max(13, Math.floor(base * pre.clientWidth / pre.scrollWidth * 10) / 10) + "px";
      }
    });
    var disponible = cuerpo.clientHeight;
    var necesario = cuerpo.scrollHeight;
    if (disponible > 0 && necesario > disponible + 2) {
      var escala = Math.max(0.6, disponible / necesario);
      cuerpo.style.transform = "scale(" + escala + ")";
      cuerpo.style.width = (100 / escala) + "%";
      seccion.dataset.escala = escala.toFixed(2);
    } else {
      delete seccion.dataset.escala;
    }
  }

  // Cifras que cuentan hasta su valor.
  function contar(seccion) {
    $$("[data-cuenta]", seccion).forEach(function (el) {
      var fin = parseInt(el.dataset.cuenta, 10);
      if (imprimir || !isFinite(fin)) { return; }
      var inicio = performance.now();
      var duracion = 900;
      function paso(ahora) {
        var t = Math.min(1, (ahora - inicio) / duracion);
        el.textContent = Math.round(fin * (1 - Math.pow(1 - t, 3)));
        if (t < 1) { requestAnimationFrame(paso); }
      }
      requestAnimationFrame(paso);
    });
  }

  // Índice lateral.
  var menu = $(".menu ol");
  var entradas = [];
  function construirMenu() {
    $$(".slides > section[data-menu]").forEach(function (seccion) {
      var li = document.createElement("li");
      if (seccion.classList.contains("profe")) { li.className = "profe"; }
      var boton = document.createElement("button");
      boton.type = "button";
      boton.textContent = seccion.dataset.menu;
      boton.addEventListener("click", function () {
        var indices = deck.getIndices(seccion);
        deck.slide(indices.h, indices.v);
        document.body.classList.remove("menu-abierto");
      });
      li.appendChild(boton);
      menu.appendChild(li);
      entradas.push({ seccion: seccion, li: li });
    });
  }
  function marcarMenu(actual) {
    var posicion = deck.getIndices(actual).h;
    var activa = null;
    entradas.forEach(function (e) {
      e.li.classList.remove("actual");
      if (deck.getIndices(e.seccion).h <= posicion) { activa = e; }
    });
    if (activa) { activa.li.classList.add("actual"); }
    var donde = $(".pie-curso .donde");
    var ante = $(".antetitulo", actual);
    donde.textContent = ante ? ante.textContent : (activa && posicion > 0 ? activa.seccion.dataset.menu : "");
  }

  function alCambiar(seccion) {
    ajustar(seccion);
    contar(seccion);
    marcarMenu(seccion);
  }

  deck.initialize().then(function () {
    construirMenu();
    alCambiar(deck.getCurrentSlide());
    if (imprimir) { $$(".slides section").forEach(ajustar); }
  });
  deck.on("slidechanged", function (e) { alCambiar(e.currentSlide); });
  deck.on("resize", function () { ajustar(deck.getCurrentSlide()); });
  deck.on("overviewshown", function () { $$(".slides > section").forEach(ajustar); });

  // Resultados del intérprete.
  function alternarResultados() {
    var ver = document.body.classList.toggle("ver-resultados");
    var boton = $('[data-accion="resultados"]');
    if (boton) { boton.classList.toggle("activo", ver); }
    avisar(ver ? "Resultados visibles" : "Resultados ocultos: haz clic para descubrirlos");
  }

  function copiar(texto, boton) {
    function hecho() {
      boton.classList.add("hecho");
      var antes = boton.textContent;
      boton.textContent = "Copiado";
      setTimeout(function () { boton.classList.remove("hecho"); boton.textContent = antes; }, 1400);
    }
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(texto).then(hecho, function () { copiaClasica(texto); hecho(); });
    } else {
      copiaClasica(texto);
      hecho();
    }
  }
  function copiaClasica(texto) {
    var area = document.createElement("textarea");
    area.value = texto;
    area.style.position = "fixed";
    area.style.opacity = "0";
    document.body.appendChild(area);
    area.select();
    try { document.execCommand("copy"); } catch (error) { /* sin portapapeles */ }
    area.remove();
  }
  // De una sesión del intérprete solo se copian las instrucciones.
  function textoDe(bloque) {
    var codigo = $("pre code", bloque);
    if (!bloque.classList.contains("consola")) { return codigo.textContent; }
    var copia = codigo.cloneNode(true);
    $$(".salida", copia).forEach(function (s) { s.remove(); });
    return copia.textContent.split("\n")
      .filter(function (l) { return /^(>>>|\.\.\.)/.test(l); })
      .map(function (l) { return l.replace(/^(>>>|\.\.\.) ?/, ""); })
      .join("\n");
  }

  document.addEventListener("click", function (evento) {
    var objetivo = evento.target;
    var salida = objetivo.closest(".salida");
    if (salida) { salida.classList.toggle("vista"); return; }

    var boton = objetivo.closest("button");
    if (boton && boton.classList.contains("copiar")) { copiar(textoDe(boton.closest(".codigo")), boton); return; }
    if (boton && boton.classList.contains("revelar")) {
      var salidas = $$(".salida", boton.closest(".codigo"));
      var ocultar = salidas.every(function (s) { return s.classList.contains("vista"); });
      salidas.forEach(function (s, i) {
        setTimeout(function () { s.classList.toggle("vista", !ocultar); }, ocultar ? 0 : i * 140);
      });
      boton.textContent = ocultar ? "Ver resultados" : "Ocultar resultados";
      return;
    }
    if (boton && boton.classList.contains("pregunta")) { boton.classList.toggle("vuelta"); return; }
    if (boton && boton.classList.contains("pestana")) {
      var solucion = boton.closest(".solucion");
      $$(".pestana", solucion).forEach(function (p) { p.classList.toggle("activa", p === boton); });
      $$(".panel", solucion).forEach(function (p) { p.classList.toggle("activo", p.dataset.panel === boton.dataset.panel); });
      return;
    }
    if (boton && boton.classList.contains("dia")) { mostrarDia(boton); return; }
    if (boton && boton.dataset.accion) {
      var accion = boton.dataset.accion;
      if (accion === "menu") { document.body.classList.toggle("menu-abierto"); }
      if (accion === "resultados") { alternarResultados(); }
      if (accion === "general") { deck.toggleOverview(); }
      if (accion === "pantalla") { pantallaCompleta(); }
      if (accion === "modo") {
        if (modoClase) { parametros.delete("clase"); } else { parametros.set("clase", "1"); }
        var consulta = parametros.toString();
        location.href = location.pathname + (consulta ? "?" + consulta.replace("clase=1", "clase") : "") + "#/";
      }
      return;
    }

    // Clic en una fila de una tabla: la destaca y atenúa las demás.
    var fila = objetivo.closest(".tabla tbody tr");
    if (fila && !objetivo.closest("a")) {
      var tabla = fila.closest("table");
      var yaEstaba = fila.classList.contains("foco");
      $$("tr.foco", tabla).forEach(function (f) { f.classList.remove("foco"); });
      fila.classList.toggle("foco", !yaEstaba);
      tabla.classList.toggle("enfocada", !yaEstaba);
      return;
    }
    if (document.body.classList.contains("menu-abierto") && !objetivo.closest(".menu")) {
      document.body.classList.remove("menu-abierto");
    }
  });

  function mostrarDia(boton) {
    var seccion = boton.closest("section");
    $$(".dia", seccion).forEach(function (d) { d.classList.toggle("activo", d === boton); });
    var detalle = $(".detalle-dia", seccion);
    detalle.textContent = boton.querySelector(".s").textContent + ", " + boton.querySelector(".f").textContent + ". " + boton.dataset.detalle + ".";
    detalle.classList.remove("cambia");
    void detalle.offsetWidth;
    detalle.classList.add("cambia");
  }
  document.addEventListener("mouseover", function (evento) {
    var dia = evento.target.closest && evento.target.closest(".dia");
    if (dia && !dia.classList.contains("activo")) { mostrarDia(dia); }
  });

  function pantallaCompleta() {
    if (document.fullscreenElement) { document.exitFullscreen(); }
    else if (document.documentElement.requestFullscreen) { document.documentElement.requestFullscreen(); }
  }

  var botonModo = $('[data-accion="modo"]');
  if (botonModo) { botonModo.textContent = modoClase ? "Modo profesor" : "Modo clase"; botonModo.classList.toggle("activo", modoClase); }

  deck.addKeyBinding({ keyCode: 77, key: "M", description: "Índice de la presentación" }, function () {
    document.body.classList.toggle("menu-abierto");
  });
  deck.addKeyBinding({ keyCode: 82, key: "R", description: "Mostrar u ocultar los resultados" }, alternarResultados);
  deck.addKeyBinding({ keyCode: 72, key: "H", description: "Índice del curso" }, function () { location.href = "index.html"; });

  window.cursoDeck = deck;
  window.cursoAjustar = ajustar;
}());
