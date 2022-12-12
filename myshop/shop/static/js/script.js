const b_image = document.getElementById('b_image')
const s_image = document.getElementsByClassName('s_image')

for (let i = 0; i < s_image.length; i++) {
    s_image[i].addEventListener('click', () => {
        b_image.src = s_image[i].src
    })
}

const btn = document.getElementById('btn_message')
const flashes = document.getElementById('flashes')


btn.addEventListener('click', () => {
    flashes.remove()
}, 2000)