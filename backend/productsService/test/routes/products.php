<?php
use Illuminate\Support\Facades\Route;
use App\Services\ProductsService;

Route::get('/Products', function () {
    $productsService = new ProductsService();
    return $productsService->getProducts();
});

// receives product id as a route parameter
Route::get('/Products/{id}', function ($id) {
    $productsService = new ProductsService();
    return $productsService->getProduct($id);
})->whereNumber('id');

Route::get('/Products/Category/{category_id}', function () {
    $productsService = new ProductsService();
    return $productsService->getProductsByCategory($category_id);
})->whereNumber('category_id');

Route::get('/Products/Category/id', function () {
    return 'Products by Category';
});

?>
