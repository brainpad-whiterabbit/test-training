document$.subscribe(function() {
  var diagrams = document.querySelectorAll(".mermaid")
  if (!diagrams.length || typeof mermaid === "undefined") {
    return
  }

  diagrams.forEach(function(diagram) {
    var code = diagram.querySelector("code")
    if (code) {
      diagram.textContent = code.textContent
    }
    diagram.removeAttribute("data-processed")
  })

  var palette = document.body.getAttribute("data-md-color-scheme")
  mermaid.initialize({
    startOnLoad: false,
    theme: palette === "slate" ? "dark" : "default"
  })
  mermaid.run({ nodes: diagrams })
})
