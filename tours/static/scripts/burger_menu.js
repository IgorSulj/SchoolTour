let burger = document.getElementById('burger')
let burger_menu = document.getElementById('header__menu')
burger_menu.style.height = 0

burger.onclick = () => {
    is_collapsed = burger_menu.style.height == '0px'
    if (is_collapsed)
        burger_menu.style.height = burger_menu.scrollHeight + 'px'
    else
        burger_menu.style.height = '0px'
}