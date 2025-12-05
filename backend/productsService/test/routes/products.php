<?php
use Illuminate\Support\Facades\Route;
use App\Services\ProductsService;

Route::get('/products', function () {
    $productsService = new ProductsService();
    return $productsService->getProducts();
});

// receives product id as a route parameter
Route::get('/products/{id}', function ($id) {
    $productsService = new ProductsService();
    return $productsService->getProduct($id);
})->whereNumber('id');

Route::get('/products/category/{category_id}', function ($category_id) {
    $productsService = new ProductsService();
    return $productsService->getProductsByCategory($category_id);
})->whereNumber('category_id');

Route::post('/newProduct', function () {
    $productsService = new ProductsService();
    $name = request('name');
    $category_id = request('category_id');
    $price = request('price');
    $description = request('description');
    $image_url = request('image_url');

    return $productsService->createProduct($name, $category_id, $price, $description, $image_url);
});

Route::put('/updateProduct/{id}', function ($id) {
    $productsService = new ProductsService();
    $name = request('name');
    $category_id = request('category_id');
    $price = request('price');
    $description = request('description');
    $image_url = request('image_url');

    return $productsService->updateProduct($id, $name, $category_id, $price, $description, $image_url);
})->whereNumber('id');

Route::delete('/deleteProduct/{id}', function ($id) {
    $productsService = new ProductsService();
    return $productsService->deleteProduct($id);
})->whereNumber('id');
?>
