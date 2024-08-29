
    const menu = document.getElementById('menu')
    const menuX = document.getElementById('menu-x')
    const menuContent = document.getElementById('content')
    menu.addEventListener('click', () => {
        menuContent.classList.toggle('hidden')
        menu.classList.toggle('hidden')
        menuX.classList.toggle('hidden')
    })

    menuX.addEventListener('click', () => {
        menuContent.classList.toggle('hidden')
        menu.classList.toggle('hidden')
        menuX.classList.toggle('hidden')
    })
