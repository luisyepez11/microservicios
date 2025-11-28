<?php
use Illuminate\Support\Facades\Route;
use App\Services\CartService;

Route::post('/addToCart', function () {
    $cartService = new CartService();
    $product_id = request('product_id');
    $quantity = request('quantity');

    return $cartService->addToCart($product_id, $quantity);
});

Route::get('/cartItems', function () {
    $cartService = new CartService();
    return $cartService->getCartItems();
});

Route::put('/updateCartItem/{product_id}', function ($product_id) {
    $cartService = new CartService();
    $quantity = request('quantity');

    return $cartService->updateCartItem($product_id, $quantity);
})->whereNumber('product_id');

Route::delete('/removeFromCart/{product_id}', function ($product_id) {
    $cartService = new CartService();
    return $cartService->removeFromCart($product_id);
})->whereNumber('product_id');
?>
