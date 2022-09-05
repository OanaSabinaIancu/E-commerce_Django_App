var btn = document.getElementsByClassName('update-cart')

for( var i = 0; i < btn.length; i++){
    btn[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId', productId, 'action', action)

        console.log('user', user)
      
            updateOrder(productId, action)
        
    })
}

function updateOrder(productId, action){
    console.log("User logged in sendiing data")
    var url = '/update_item/'
    
    fetch(url,  {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken' : csrftoken,
        },
        body:JSON.stringify({'productId': productId, 'action': action})
    })
    
    .then((response) => {
        return response.json()
    })

    .then((data) => {
        location.reload()
    })
}