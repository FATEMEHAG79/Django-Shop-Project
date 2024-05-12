//Add to cart

$("#add-to-cart-btn").on("click",function () {
    let quantity = $("#product-quantity").val()
    let product_name = $(".product-name").val()
    let product_id = $(".product-id").val()
    let product_price = $("#current-product-price").text()
    let this_val = $(this)


    console.log("Quantity:" , quantity);
    console.log("Name:" , product_name);
    console.log("Id:" , product_id);
    console.log("Price:" , product_price);
    console.log("Current Element:" , this_val);

    $.ajax({
        url:"/add-to-cart/",
        data:{
            "id" : product_id ,
            "qty" : quantity ,
            "name" : product_name,
            "price" : product_price,
        },
        dataType: "json" ,
        beforeSend : function (){
            console.log("Adding Product to cart ....");
        },
        success: function (response) {
            this_val.html("Item added to cart.")
            console.log("Aded Product to cart");
            $(".cart-items-count").text(response.totalcartitems)
        }
    })
})
