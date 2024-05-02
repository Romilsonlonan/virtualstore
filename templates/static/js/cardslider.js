const pictures = [
    'img/brinquedos.png',
    'img/esportes.jpg',
    'img/eletroeletronicos.png',
    'img/lojadevariedades.webp',
    'img/moveis.jpg',
    'img/saude.jpeg',
]

const template = document.createElement('template')
template.innerHTML = `
    <div class="container-script">
      <button class="direita">
        <img id="direitaIcon" src="img/direita.png">
      </button>
      <div class="scroll">
        
      </div>
      <button class="esquerda">
        <img id="esquerdaIcon" src="img/esquerda.png">
      </button>
    </div>
  `

class cardView extends HTMLElement {
  constructor () {
    super()

    this.attachShadow({mode: 'open'})
    
    const importCss = document.createElement('style')
    importCss.innerHTML = `@import 'img/home.css/'`

    const importScript = document.createElement('script')
    importScript.src = 'cardslider.js'

    this.shadowRoot.appendChild(template.content.cloneNode(true))
    this.shadowRoot.appendChild(importCss)
    this.shadowRoot.appendChild(importScript)
    
    let card = ''
    let i = 0
    pictures.forEach(component)
    
    function component (model) {
      i += 1
      if (i == 1) {
        list += `
        <section id="${i}" class="active">
          <img src="${model}">
        </section>
        `
      } else {
        card += `
        <section id="${i}">
          <img src="${model}">
        </section>
        `
      }
    }

    const scroll = this.shadowRoot.querySelector('.scroll')
    scroll.innerHTML = list
  }
}

window.customElements.define('card-view', cardView)