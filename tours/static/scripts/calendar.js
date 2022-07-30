let buttons_block = document.getElementById("buttons")

function countActiveButtons() {
    let buttons = document.querySelectorAll("#buttons .usual-button")
    let count = 0
    for (let button of buttons) {
        if (button.classList.contains("active")) {
            count++
        }
    }
    return count
}

function toggleAllMonths(key) {
    let value = key ? "inherit" : "none"
    let months = document.querySelectorAll(".month")
    for (let month of months) {
        month.style.display = value
    }
}

function toggleMonth(month, key) {
    let value = key ? "inherit" : "none"
    month.style.display = value
}

buttons_block.onclick = event => {
    if (event.target.id == "buttons") return
    let classList = event.target.classList

    let active_buttons = countActiveButtons()
    if (active_buttons == 1 && classList.contains("active")) { // if it's the only active button
        toggleAllMonths(true)
        classList.toggle("active")
        return
    }

    else if (active_buttons == 0) {
        toggleAllMonths(false)
    }

    classList.toggle("active")
    let month_num = Number(event.target.dataset.month)
    let month = document.querySelectorAll(".month")[month_num]
    toggleMonth(month, classList.contains("active"))
}

