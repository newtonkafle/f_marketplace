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




















   
