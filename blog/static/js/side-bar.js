$('.custom-dropdown-button').on('click', e => {
    const toggleId = `#${e.target.dataset.toggle}`
    $(toggleId).toggle()
})