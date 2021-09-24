document.addEventListener("DOMContentLoaded", () => {

    menuButton = document.querySelector("#menu");
    inventoryButton = document.querySelector("#inventory");
    purchasesButton = document.querySelector("#purchases");
    financesButton = document.querySelector("#finances");

    menuButton.onclick = () => loadMenu();
    inventoryButton.onclick = () => loadInventory();
    purchasesButton.onclick = () => loadPurchases();
    financesButton.onclick = () => loadFinances();

    // By default, load the menu
    loadMenu();

    // Page-history features
    window.onpopstate = event => {
        window[`load${event.state.section}`](pop=false);
    }
})

function loadInventory(pop=true) {
    fetch("app/inventory")
    .then(response => response.json())
    .then(data => {
            const ingredients = document.querySelector("#ingredients-view > ul");
            ingredients.innerHTML = "";
            document.querySelector("#menu-view").style.display = "none";
            document.querySelector("#purchases-view").style.display = "none";
            document.querySelector("#finances-view").style.display = "none";
            document.querySelector("#ingredients-view").style.display = "block";
            console.log(data);
            JSON.parse(data).forEach(result => {
                let ingredient = document.createElement("li");
                ingredient.innerHTML = `<strong>${result.name}</strong> | <em>${result.quantity} ${result.unit} in stock</em> | <span class="text-success">$${result.unit_price}</span> per unit`;
                let deleteButton = document.createElement("button");
                deleteButton.innerHTML = "<button>Delete Ingredient</button";
                deleteButton.addEventListener("click", () => deleteIngredient(ingredient, result.id));
                ingredients.append(ingredient);
            })
            if (pop) history.pushState({section: "Inventory"}, "", "#inventory");
        })
    .catch(error => console.log(error));
}

function loadMenu(pop=true) {
    fetch("app/menu")
    .then(response => response.json())
    .then(data => {
        document.querySelector("#ingredients-view").style.display = "none";
        document.querySelector("#purchases-view").style.display = "none";
        document.querySelector("#finances-view").style.display = "none";
        const menu = document.querySelector("#menu-view");
        menu.innerHTML = "";
        menu.style.display = "flex";
        menu.style.flexWrap = "wrap";
        menu.style.justifyContent = "space-between";
        menu.style.gap = "10px";
        JSON.parse(data).forEach(result => {
            let recipe = document.createElement("div");
            recipe.className = "card";
            recipe.style.width = "15rem";
            recipe.innerHTML = `
                <img src="${result.recipe_image}" class="card-img-top" alt="">
                <div class="card-body">
                    <h5 class="card-title">${result.name}</h5>
                    <h6 class="card-subtitle my-2 text-success">$${result.price}</h6>
                    <a class="recipe-button btn my-4" style="width: 100%" href="${result.recipe_link}">View Recipe</a>
                </div>
            `;
            menu.append(recipe);
        })
        if (pop) history.pushState({section: "Menu"}, "", "#menu");
    })
}

function loadPurchases(pop=true) {
    fetch("app/purchases")
    .then(response => response.json())
    .then(data => {
        const purchases = document.querySelector("#purchases-view > ul");
        purchases.innerHTML = "";
        document.querySelector("#menu-view").style.display = "none";
        document.querySelector("#ingredients-view").style.display = "none";
        document.querySelector("#finances-view").style.display = "none";
        document.querySelector("#purchases-view").style.display = "block";
        data.forEach(result => {
            let purchase = document.createElement("li");
            purchase.innerHTML = `<strong>${result.menu_item}</strong> was purchased on ${result.timestamp}`;
            purchases.append(purchase);
        })
        if (pop) history.pushState({section: "Purchases"}, "", "#purchases");
    })
}

function loadFinances(pop=true) {
    fetch("app/finances")
    .then(response => response.json())
    .then(data => {
        console.log(data);
        document.querySelector("#menu-view").style.display = "none";
        document.querySelector("#ingredients-view").style.display = "none";
        document.querySelector("#purchases-view").style.display = "none";
        document.querySelector("#finances-view").style.display = "flex";
        document.querySelector("#revenue > h1").innerHTML = `$${data.revenue}`;
        document.querySelector("#cost > h1").innerHTML = `$${data.cost}`;
        document.querySelector("#profit > h1").innerHTML = `$${data.profit}`;
        if (pop) history.pushState({section: "Finances"}, "", "#purchases");
    })
}

function deleteIngredient(ingredient, ingredientId) {
    fetch(`app/modify_ingredient`, {
        method: "PUT",
        body: JSON.stringify({
            ingredient_id: ingredientId,
            remove: true
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
        ingredient.remove();
    })
    .catch(error => console.log(error))
}
