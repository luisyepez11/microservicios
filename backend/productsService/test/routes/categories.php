<?php

use Illuminate\Support\Facades\Route;
use App\Services\CategoriesService;

Route::get('/categories', function () {
    $categoriesService = new CategoriesService();
    return $categoriesService->getCategories();
});

Route::get('/categories/{id}', function ($id) {
    $categoriesService = new CategoriesService();
    return $categoriesService->getCategory($id);
})->whereNumber('id');

Route::post('/categories/new', function () {
    $categoriesService = new CategoriesService();
    $name = request('name');

    return $categoriesService->createCategory($name);
});

Route::put('/categories/update/{id}', function ($id) {
    $categoriesService = new CategoriesService();
    $name = request('name');

    return $categoriesService->editCategory($id, $name);
})->whereNumber('id');

Route::delete('/categories/delete/{id}', function ($id) {
    $categoriesService = new CategoriesService();
    return $categoriesService->deleteCategory($id);
})->whereNumber('id');

?>
