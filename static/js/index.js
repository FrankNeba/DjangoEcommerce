
    // const menu = document.getElementById('menu')
    // const menuX = document.getElementById('menu-x')
    // const menuContent = document.getElementById('content')
    // menu.addEventListener('click', () => {
    //     menuContent.classList.toggle('hidden')
    //     menu.classList.toggle('hidden')
    //     menuX.classList.toggle('hidden')
    // })

    // menuX.addEventListener('click', () => {
    //     menuContent.classList.toggle('hidden')
    //     menu.classList.toggle('hidden')
    //     menuX.classList.toggle('hidden')
    // })

    const amount = document.getElementById('amount')
    const total = document.getElementById('total')
    const itemprice = document.getElementById('itemprice')

    amount.addEventListener('change', ()=> {
        let price = Number(amount.value) * Number(itemprice)
        total.textContent = amount.value
        console.log('iteminputed')
    })


