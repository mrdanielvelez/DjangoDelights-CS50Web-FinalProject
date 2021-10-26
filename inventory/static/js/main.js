document.addEventListener("DOMContentLoaded", () => {

    const menuButton = document.querySelector("#menu");
    const inventoryButton = document.querySelector("#inventory");
    const purchasesButton = document.querySelector("#purchases");
    const financesButton = document.querySelector("#finances");

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

    // Add an ingredient then load inventory
    document.querySelector("#new-ingredient").onsubmit = () => {
        const ingredientName = document.querySelector("#ingredient_name").value;
        const quantity = document.querySelector("#quantity").value;
        const unit = document.querySelector("#unit").value;
        const unitPrice = document.querySelector("#unit_price").value;
        addIngredient(ingredientName, quantity, unit, unitPrice);
        return false;
    }

    // Add a purchase then load purchases
    document.querySelector("#new-purchase").onsubmit = () => {
        const purchasedItem = document.querySelector("#purchased_item").value;
        const dateTime = document.querySelector("#date_time").value;
        addPurchase(purchasedItem, dateTime);
        return false;
    }
})

function loadMenu(pop=true) {
    fetch("app/menu")
    .then(response => response.json())
    .then(data => {
        document.querySelector("#inventory-view").style.display = "none";
        document.querySelector("#purchases-view").style.display = "none";
        document.querySelector("#finances-view").style.display = "none";
        document.querySelector("#recipe-view").style.display = "none";
        const menu = document.querySelector("#menu-view");
        menu.innerHTML = "";
        menu.style.display = "flex";
        menu.style.flexWrap = "wrap";
        menu.style.justifyContent = "space-between";
        menu.style.gap = "10px";
        let itemForm = document.createElement("form");
        itemForm.method = "POST";
        itemForm.id = "new-item";
        itemForm.action = "/new_item/"
        itemForm.innerHTML = `
            <input required type="text" name="item_name" placeholder="Item">
            <input required type="number" name="price" placeholder="Price">
            <input required type="url" name="image_url" placeholder="Image URL">
            <input required type="url" name="recipe_url" placeholder="Recipe URL">
            <button type="submit">Add</button>
        `;
        menu.append(itemForm);
        JSON.parse(data).forEach(result => {
            let recipe = document.createElement("div");
            recipe.className = "card";
            recipe.style.width = "15rem";
            recipe.innerHTML = `
                <img src="${result.recipe_image}" class="card-img-top" alt="">
                <div class="card-body">
                    <h5 class="card-title">${result.name}</h5>
                    <h6 class="card-subtitle my-2 text-success">$${result.price}</h6>
                    <a class="recipe-button btn my-4" style="width: 100%">View Recipe</a>
                </div>
            `;
            recipe.querySelector("img").addEventListener("click", () => loadRecipe(result.id));
            recipe.querySelector(".recipe-button").addEventListener("click", () => loadRecipe(result.id));
            menu.append(recipe);
        })
        if (pop) history.pushState({section: "Menu"}, "", "#menu");
    })
    .catch(error => console.log(error))
}

function loadInventory(pop=true) {
    fetch("app/inventory")
    .then(response => response.json())
    .then(data => {
            const ingredients = document.querySelector("#inventory-view > ul");
            ingredients.innerHTML = "";
            document.getElementById("new-ingredient").reset();
            document.querySelector("#menu-view").style.display = "none";
            document.querySelector("#purchases-view").style.display = "none";
            document.querySelector("#finances-view").style.display = "none";
            document.querySelector("#recipe-view").style.display = "none";
            document.querySelector("#inventory-view").style.display = "block";
            JSON.parse(data).forEach(result => {
                let ingredient = document.createElement("li");
                ingredient.innerHTML = `<strong>${result.name}</strong> | <em>${result.quantity} ${result.unit} in stock</em> | <span class="text-success">$${result.unit_price}</span> per unit`;
                let deleteButton = document.createElement("button");
                deleteButton.className = "del-button";
                deleteButton.innerHTML = "Delete";
                deleteButton.addEventListener("click", () => deleteIngredient(ingredient, result.id));
                ingredient.append(deleteButton);
                ingredients.append(ingredient);
            })
            if (pop) history.pushState({section: "Inventory"}, "", "#inventory");
        })
    .catch(error => console.log(error));
}

function loadPurchases(pop=true) {
    fetch("app/purchases")
    .then(response => response.json())
    .then(data => {
        const purchases = document.querySelector("#purchases-view > ul");
        purchases.innerHTML = "";
        document.getElementById("new-purchase").reset();
        document.querySelector("#menu-view").style.display = "none";
        document.querySelector("#inventory-view").style.display = "none";
        document.querySelector("#finances-view").style.display = "none";
        document.querySelector("#recipe-view").style.display = "none";
        document.querySelector("#purchases-view").style.display = "block";
        data.forEach(result => {
            let purchase = document.createElement("li");
            purchase.innerHTML = `<strong>${result.menu_item}</strong> was purchased on ${result.timestamp}`;
            purchases.append(purchase);
        })
        if (pop) history.pushState({section: "Purchases"}, "", "#purchases");
    })
    .catch(error => console.log(error))
}

function loadFinances(pop=true) {
    fetch("app/finances")
    .then(response => response.json())
    .then(data => {
        document.querySelector("#menu-view").style.display = "none";
        document.querySelector("#inventory-view").style.display = "none";
        document.querySelector("#purchases-view").style.display = "none";
        document.querySelector("#recipe-view").style.display = "none";
        document.querySelector("#finances-view").style.display = "flex";
        document.querySelector("#profit > h2").innerHTML = `$${data.profit}`;
        document.querySelector("#revenue > h2").innerHTML = `$${data.revenue}`;
        document.querySelector("#expenses > h2").innerHTML = `$${data.expenses}`;
        if (pop) history.pushState({section: "Finances"}, "", "#finances");
    })
    .catch(error => console.log(error))
}

function loadRecipe(recipeId, pop=true) {
    fetch(`recipes/${recipeId}`)
    .then(response => response.json())
    .then(data => {
        document.querySelector("#menu-view").style.display = "none";
        document.querySelector("#inventory-view").style.display = "none";
        document.querySelector("#purchases-view").style.display = "none";
        document.querySelector("#finances-view").style.display = "none";
        const recipe = document.querySelector("#recipe-view");
        recipe.style.display = "flex";
        recipe.innerHTML = "";
        const recipeTitle = document.createElement("h3");
        recipeTitle.innerHTML = `${data.recipe_name}`;
        const recipeImage = document.createElement("img");
        recipeImage.src = `${data.recipe_image}`;
        const recipeMain = document.createElement("div");
        recipeMain.id = "recipe-main";
        recipeMain.append(recipeTitle, recipeImage);
        recipe.append(recipeMain);
        const recipeInfo = document.createElement("div");
        recipeInfo.id = "recipe-info";
        const instructionsButton = document.createElement("a");
        instructionsButton.className = "recipe-button btn my-3";
        instructionsButton.style = "width: 100%";
        instructionsButton.innerHTML = "View Instructions";
        instructionsButton.href = data.recipe_link;
        recipeInfo.append(instructionsButton);
        data.recipe_requirements.forEach(requirement => {
            req = document.createElement("li");
            req.innerHTML = `${requirement.quantity} ${requirement.unit} of ${requirement.name}`
            recipeInfo.append(req);
        })
        recipe.append(recipeInfo);
        if (pop) history.pushState({section: "Recipes", recipeId: recipeId}, "", `#${data.recipe_name.replace(/\s+/g, '-').toLowerCase()}`);
    })
    .catch(error => console.log(error))
}

function addIngredient(ingredientName, quantity, unit, unitPrice) {
    fetch("new_ingredient/", {
        method: "POST",
        body: JSON.stringify({
          ingredient_name: ingredientName,
          quantity: quantity,
          unit: unit,
          unit_price: unitPrice
        })
    })
    .then(response => response.json())
    .then(result => {
        if (!("error" in result)) loadInventory();
    })
    .catch(error => console.log(error))
}

function deleteIngredient(ingredient, ingredientId) {
    fetch("delete_ingredient/", {
        method: "PUT",
        body: JSON.stringify({
            ingredient_id: ingredientId,
            remove: true
        })
    })
    .then(response => response.json())
    .then(result => {
        if (!("error" in result)) ingredient.remove();
    })
    .catch(error => console.log(error))
}

function addPurchase(purchasedItem, dateTime) {
    fetch("new_purchase/", {
        method: "POST",
        body: JSON.stringify({
          purchased_item: purchasedItem,
          date_time: dateTime,
        })
    })
    .then(response => response.json())
    .then(result => {
        if (!("error" in result)) loadPurchases();
    })
    .catch(error => console.log(error))
}
