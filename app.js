function test(items){
    // console.log(items)
    items = JSON.parse(items)
    console.log(items)
    items.forEach( item => {
        let marker = new mapboxgl.Marker()
        .setLngLat([item.item_lon, item.item_lat]) // Marker 1 coordinates
        .addTo(map);        
    })
}


/* Dialog */
document.querySelectorAll('.item').forEach((item) => {
        item.addEventListener('click', function (event) {
            /* prevent default from button and form  */
            if (event.target.tagName !== 'FORM' && event.target.tagName !== 'BUTTON') {
                const dialogId = this.getAttribute('data-dialog-id');
                showDialog(dialogId);
            }
        });
    });

    document.querySelectorAll('.btn_close').forEach((closeBtn) => {
        closeBtn.addEventListener('click', function () {
            console.log('close');   
            const dialogId = this.getAttribute('data-dialog-id');
            closeDialog('dialog-' + dialogId);
        });
    });

function showDialog(dialogId) {
    const dialog = document.querySelector(`#${dialogId}`);
    if(dialog) {
        dialog.showModal();
    } else {
        console.error(`Dialog with id ${dialogId} not found`);
    }
}

function closeDialog(dialogId) {
    const dialog = document.querySelector(`#${dialogId}`);
    if(dialog) {
        dialog.close();
    } else {
        console.error(`Dialog with id ${dialogId} not found`);
    }
}