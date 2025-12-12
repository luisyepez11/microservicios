<?php

namespace App\Services;

use Illuminate\Support\Facades\DB;

class CartService{
    public function addToCart($product_id, $quantity, $user_id){
        if (!DB::table('cart')->where('user_id', $user_id)->exists()){
            DB::table('cart')->insert([
                'cart_id' => random_int(1, 9999),
                'user_id' => $user_id,
                'last_check' => now()->toTimeString(),
            ]);
        }

        DB::table('cart_products')->insert([
            'cart_id' => DB::table('cart')->where('user_id', $user_id)->value('cart_id'),
            'product_id' => $product_id,
            'quantity' => $quantity,
        ]);
        return "Product added to cart";
    }

    public function getCartItems($user_id)
{

    DB::table('cart')->where('user_id', $user_id)->update([
        'last_check' => now()->toTimeString(),
    ]);
    
    $cart = DB::table('cart')->where('user_id', $user_id)->first();
    
    
    $cart_id = isset($cart->id) ? $cart->id : $cart->cart_id;

    return DB::table('cart_products')
        ->join('products', 'cart_products.product_id', '=', 'products.product_id')
        ->where('cart_products.cart_id', $cart_id)
        ->select(
            'cart_products.*', 
            'products.name as product_name',
            'products.description',
            'products.image_url',
            'products.price'
        )
        ->get();
}

    public function updateCartItem($product_id, $quantity, $user_id){
        DB::table('cart')->where('user_id', $user_id)->update([
            'last_check' => now()->toTimeString(),
        ]);

        $cart = DB::table('cart')->where('user_id',$user_id)->first();
        
        DB::table('cart_products')
        ->where('cart_id',$cart->cart_id)
        ->where('product_id', $product_id)
        ->update([
            'quantity' => $quantity,
        ]);
        return "Cart item updated";
    }

    public function removeFromCart($product_id, $user_id){
        DB::table('cart')->where('user_id', $user_id)->update([
            'last_check' => now()->toTimeString(),
        ]);
        DB::table('cart_products')->where('cart_id', DB::table('cart')
        ->where('user_id', $user_id)
        ->value('cart_id'))
        ->where('product_id', $product_id)
        ->delete();
        return "Product removed from cart";
    }

    public function deleteCart($user_id){
        // Validate if last check was more than 14 days ago, if so, delete cart
        if (strtotime(DB::table('cart')
        ->where('user_id', $user_id)
        ->value('last_check')) < strtotime('-14 days')){
            DB::table('cart')->where('user_id', $user_id)->delete();
            foreach (DB::table('cart_products')->where('cart_id', DB::table('cart')
            ->where('user_id', $user_id)
            ->value('cart_id'))
            ->get() as $item){
                DB::table('cart_products')
                ->where('cart_id', DB::table('cart'))
                ->where('user_id', $user_id)
                ->value('cart_id')
                ->where('product_id', $item->product_id)
                ->delete();
            }
            return "Cart cleared";
        }
    }
}
?>
