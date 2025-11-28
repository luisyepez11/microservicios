<?php
namespace App\Services;

use Illuminate\Support\Facades\DB;

class ProductsService{
    public function createProduct($name, $category_id, $price, $description, $image_url){
        if (DB::table('Products')->where('name', $name)->exists()) {
            return "Product already exists";
        }

        $product_id = random_int(1, 9999);
        while (true){
            if (!DB::table('Products')->where('product_id', $product_id)->exists()) {
                break;
            }
            $product_id = random_int(1, 9999);
        }

        $productData = [
            'product_id' => $product_id,
            'name' => $name,
            'category_id' => $category_id,
            'price' => $price,
            'description' => $description,
            'image_url' => $image_url,
        ];

        // If we take this route we need to delete or coment the $product_id logistics above
        // $id = $this->loadCategoryToDB($productData);
        // return $id;

        $this->loadProductToDB($productData);
        return $product_id;
    }

    private function loadProductToDB(array $product){
        return DB::table('Products')->insertGetId($product);
    }

    //Will extract product list from the products table
    public function getProducts(){
        return DB::table('Products');
    }

    //Will extract product details from the products table
    public function getProduct($id){
        return DB::table('Products')->where('product_id', $id)->first();
    }

    public function updateProduct($id, $name, $category_id, $price, $description, $image_url){
        return DB::table('Products')->where('product_id', $id)->update([
            'name' => $name,
            'category_id' => $category_id,
            'price' => $price,
            'description' => $description,
            'image_url' => $image_url,
        ]);
    }

    public function getProductsByCategory($category_id){
        return DB::table('Products')->where('category_id', $category_id)->get();
    }

    public function getProductsByName($name){
        return DB::table('Products')->where('name', 'like', '%' . $name . '%')->get();
    }

    public function deleteProduct($id){
        return DB::table('Products')->where('product_id', $id)->delete();
    }
}
?>
