document.addEventListener("DOMContentLoaded", function(e) {
    const updateCart = document.getElementsByClassName('update-cart');

    for(let i=0;i<updateCart.length;i++){
    
        updateCart[i].addEventListener('click',()=>{
            let productId = updateCart[i].dataset.product;
            let action = updateCart[i].dataset.action;
            console.log("productId:",productId," action:",action);      
            console.log("User : ",user);
            if(user=="AnonymousUser"){
                addCookieItem(productId,action);
            }else{
              updateUserOrder(productId, action);
            }
            
        })
        
    }
  });

const addCookieItem = (productId,action) => {
    console.log("Not logged in");
    if(action=='add'){
        if(cart[productId]==undefined){
            cart[productId] = {'quantiy':1}
        }else{
            cart[productId]['quantiy'] += 1
        }
    }else if(action=='remove'){
        if(cart[productId]!=undefined){
            cart[productId]['quantiy'] -= 1
            if(cart[productId]<=0){
                console.log("Removing item")
                delete cart[productId]
            }
        }
    }
    document.cookie = 'cart='+JSON.stringify(cart)+"; path=/";
    location.reload();
}

const updateUserOrder = (productId,action)=>{
    let url = '/update-cart/';
    let requestOptions = {
        method : "POST",
        headers : {
            'Content-Type' : "application/json",
            'X-CSRFToken' : csrftoken,
        },
        body : JSON.stringify({
            "productId" : productId,
            'action' : action
        })
    }
     fetch(url, requestOptions)
    .then(response=>response.json())
    .then(data=>{
         location.reload();
    })
}