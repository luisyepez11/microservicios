<?php

namespace App\Services;

use Illuminate\Support\Facades\DB;

class CartService{
    public function addToCart($product_id, $quantity){
        DB::table('cart')->insert([
            'product_id' => $product_id,
            'quantity' => $quantity,
        ]);
        return "Product added to cart";
    }

    public function getCartItems(){
        return DB::table('cart')->get();
    }

    public function updateCartItem($product_id, $quantity){
        DB::table('cart')->where('product_id', $product_id)->update([
            'quantity' => $quantity,
        ]);
        return "Cart item updated";
    }

    public function removeFromCart($product_id){
        DB::table('cart')->where('product_id', $product_id)->delete();
        return "Product removed from cart";
    }
}
?>
