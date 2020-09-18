var viz = new Viz();

viz.renderSVGElement('digraph { a -> b; }')
    .then(function (element) {
        console.log("Hello World")
        var elm = document.getElementById('render');
        elm.appendChild(element);
    });

