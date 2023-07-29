
$(document).ready(function(){

      // place the cart item quantity on load

      $('.item-qty').each(function(){
        let i_id = $(this).attr('id')
        let qty = $(this).attr('data-qty')

        $('#'+i_id).html(qty)
    })

    $(".add-to-cart").on('click', function(e){
        e.preventDefault();
        product_id = $(this).attr('data-id')
        url = $(this).attr('data-url')

        $.ajax({
            type: 'GET',
            url: url, 
            success: function(res){
                console.log(res)
            if(res.status == 'login-required'){
                swal({
                    'title':res.status, 
                    'text': res.message,
                     'icon':'info',
                }).then(() => window.location = '/accounts/login/')
            }
            if(res.status == 'failed'){
                swal({
                    'title':res.status,
                    'text':res.message,
                    'icon':'error',
                })
            }
            $('#cart-counter').html(res.cart_counter['cart_count'])
            $('#qty-'+product_id).html(res.qty)

                // subtotal, tax and grandtotal
                updateCartAmounts(
                    subtotal=res.amounts['subtotal'],
                    gst=res.amounts['gst'],
                    total=res.amounts['total']
                )
            }
        })
    })

    // decrease cart
    $(".decrease-cart").on('click', function(e){
        e.preventDefault();
        product_id = $(this).attr('data-id')
        cart_id = $(this).attr('cart-id')
        url = $(this).attr('data-url')
        $.ajax({
            type: 'GET',
            url: url, 
            success: function(res){

            if(res.status == 'login-required'){
                    swal({
                        'title':res.status,
                        'text': res.message,
                        'icon': 'info'
                    }).then(() => window.location = '/accounts/login/')
                }
            else if(res.status == 'failed'){
                swal({
                    'title': res.status,
                    'text': res.message,
                    'icon': 'error'
                })
            } else{
                $('#cart-counter').html(res.cart_counter['cart_count'])
                $('#qty-'+product_id).html(res.qty)

                updateCartAmounts(
                    subtotal=res.amounts['subtotal'],
                    gst=res.amounts['gst'],
                    total=res.amounts['total']
                )
                if(checkCart){
                    removeCartItem(res.qty, cart_id)
                    checkCartEmpty()
                }  

            }
            
            }
        })
    })
    // delete cart item
    $(".delete-cart").on('click', function(e){
        e.preventDefault();
        cart_id = $(this).attr('data-id')
        url = $(this).attr('data-url')
        $.ajax({
            type: 'GET',
            url: url, 
            success: function(res){
            if(res.status == 'failed'){
                swal({
                    'title': res.status,
                    'text': res.message,
                    'icon': 'error',
                })
            } else {
                $('#cart-counter').html(res.cart_counter['cart_count'])

                swal({
                    'title': res.status,
                    'text': res.message,
                    'icon': 'success'
                }).then(() => removeCartItem(0, cart_id))
                updateCartAmounts(
                    subtotal=res.amounts['subtotal'],
                    gst=res.amounts['gst'],
                    total=res.amounts['total']
                )
                checkCartEmpty()
            }
            }
         })
        })


    // delete the cart from fronted
    function removeCartItem(cart_item_qty, cart_id){
            if(cart_item_qty <= 0){
                document.getElementById("cart-item-" + cart_id).remove()
            }
        
    
        
    }
    function checkCartEmpty(){
        let cart_counter = document.getElementById('cart-counter').innerHTML
        if(cart_counter == 0){
            const empty_cart = document.getElementById('empty-cart')
            empty_cart.classList.remove('d-none')
        
    }
    }

    //updating cart amount
    function updateCartAmounts(subtotal, gst, total){
        if(checkCart){
            $('#subtotal').html(subtotal)
            $('#gst').html(gst)
            $('#total').html(total)
        }
       
    }

    const checkCart = function(){
        if(window.location.pathname == '/marketplace/cart/'){
            return true
        }
        return false
    }

  

});




let autocomplete;

function initAutoComplete(){
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('id_address'),
        {
            types: ['geocode', 'establishment'],
            componentRestrictions: {'country': ['au']},
        }
    )
    // function to specify what should happen when prediction is clicked
    autocomplete.addListener('place_changed', onPlaceChanged);

}

function onPlaceChanged(){
    const place = autocomplete.getPlace();

    //user did not select the prediction. Reset the input filed or alert()

    if (!place.geometry){
        document.getElementById('id_address').placeholder = 'Start typing...';
    } else {
        console.log('place name=>', place.name)
    }
    // get the address components and assign them to the fields
    handleAddressForm()
    fillFormFileds(place['address_components'])

}

function handleAddressForm(){    
    // this function will update the longitude and latitude from the google map api to the form fields
    const geocoder = new google.maps.Geocoder()
    let address = document.getElementById('id_address').value

    geocoder.geocode({'address': address}, function(results, status){

        if (status == google.maps.GeocoderStatus.OK){
            let latitude = results[0].geometry.location.lat();
            let longitude = results[0].geometry.location.lng();

            $('#id_latitude').val(latitude)
            $('#id_longitude').val(longitude)

            $('#id_address').val(address);
        }
    });

}

function fillFormFileds(addressComponents){
    // get the value from addressComponents and fill it the the form
    addressComponents.forEach(function(component, index){
        if(component.types[0] === 'country'){
            $('#id_country').val(component.long_name)
        }
        if(component.types[0] === 'administrative_area_level_1'){
            $('#id_state').val(component.long_name)
        }
        if(component.types[0] === 'postal_code'){
            $('#id_post_code').val(component.long_name)
        }
    })
}






















   
