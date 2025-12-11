<?php
use Illuminate\Support\Facades\Route;
use App\Services\CartService;

Route::post('{user_id}/cart/add', function ($user_id) {
    $data = request()->validate([
        'product_id' => 'required|integer',
        'quantity' => 'required|integer',
    ]);
    $cartService = new CartService();
    return $cartService->addToCart($data['product_id'], $data['quantity'], $user_id);
});

Route::get('{user_id}/cart/items', function ($user_id) {
    $cartService = new CartService();
    return $cartService->getCartItems($user_id);
});

Route::put('{user_id}/cart/update', function ($user_id) {
    $data = request()->validate([
        'product_id' => 'required|integer',
        'quantity' => 'required|integer',
    ]);
    $cartService = new CartService();
    return $cartService->updateCartItem($data['product_id'], $data['quantity'], $user_id);
});

Route::delete('{user_id}/cart/remove', function ($user_id) {
    $data = request()->validate([
        'product_id' => 'required|integer',
    ]);
    $cartService = new CartService();
    return $cartService->removeFromCart($data['product_id'], $user_id);
});

Route::delete('{user_id}/cart/delete', function ($user_id) {
    $cartService = new CartService();
    return $cartService->deleteCart($user_id);
});
?>
