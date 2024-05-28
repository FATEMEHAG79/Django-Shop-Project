//Add to cart



$(document).ready(function (){
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


    $("#delete-item-product").on("click",function () {
    let item_id = $(this).attr("data-product")
    let this_val = $(this)

    console.log("item_id:", item_id);

    $.ajax(
        {
            url: "/delete-product/",
            data: {
                "id_item": item_id
            },
            dataType: "json",
            beforeSend: function () {
                this_val.hide()
            },
            success: function (response) {
                this_val.show()
                $(".cart-items-count").text(response.totalcartitems)
                $("#cart-list").html(response.data)

            }
        })
    })
})
