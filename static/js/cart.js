// Sélectionner tous les boutons "Ajouter au panier" ou "Mettre à jour le panier"
var updateBtns = document.getElementsByClassName('update-cart');

// Boucle pour ajouter un écouteur d'événement à chaque bouton
for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product; // Récupérer l'ID du produit
        var action = this.dataset.action; // Récupérer l'action (ajouter/supprimer)
        console.log('productId:', productId, 'Action:', action);

        // Vérifier si l'utilisateur est authentifié
        if (user.is_authenticated === "false") { // Correction : Vérifier si l'utilisateur est non connecté
            console.log('User is not authenticated');
            addCookieItem(productId, action); // Appeler addCookieItem pour les utilisateurs non connectés
        } else {
            // Mettre à jour la commande de l'utilisateur
            updateUserOrder(productId, action);
        }
    });
}

// Fonction pour mettre à jour la commande de l'utilisateur via une requête AJAX
function updateUserOrder(productId, action) {
    console.log('User is authenticated, sending data...');

    var url = '/update_item/'; // URL de l'endpoint Django
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken // Token CSRF pour la sécurité
        },
        body: JSON.stringify({ 'productId': productId, 'action': action }) // Données à envoyer
    })
    .then((response) => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then((data) => {
        console.log('Success:', data);
        location.reload(); // Recharger la page (optionnel)
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

// Fonction pour ajouter ou mettre à jour un article dans le cookie du panier
function addCookieItem(productId, action) {
    console.log('User is not authenticated...');

    // Récupérer le cookie 'cart' ou créer un nouvel objet si le cookie n'existe pas
    var cart = JSON.parse(getCookie('cart') || '{}');

    if (action == 'add') {
        if (cart[productId] == undefined) {
            cart[productId] = {'quantity': 1};
        } else {
            cart[productId]['quantity'] += 1;
        }
    }

    if (action == 'remove') {
        cart[productId]['quantity'] -= 1;

        if (cart[productId]['quantity'] <= 0) {
            console.log('Item should be deleted');
            delete cart[productId];
        }
    }

    console.log('CART:', cart);
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"; // Définir le cookie
    location.reload(); // Recharger la page pour mettre à jour l'affichage
}