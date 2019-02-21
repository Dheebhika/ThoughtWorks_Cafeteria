function myFunction() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    ul = document.getElementById("myUL");
    li = ul.getElementsByTagName("li");
    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByTagName("a")[0];
        txtValue = a.textContent || a.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}


var item_cart = [];
    function display_item_cart(){
        var ordered_items_list=document.getElementById("ordered_items_list");

        while(ordered_items_list.rows.length>0) {
            ordered_items_list.deleteRow(0);
        }
        for(var items in item_cart){
            var row=ordered_items_list.insertRow();
            var cellName = row.insertCell(0);
            var cellQuantity = row.insertCell(1);

            cellName.innerHTML = item_cart[items].Name;
            cellQuantity.innerHTML = item_cart[items].Quantity;

        }

    }


    function AddtoCart(name,quantity){

       var singleProduct = {};

       singleProduct.Name=name;
       singleProduct.Quantity=quantity;


       item_cart.push(singleProduct);

       display_item_cart();

    }
