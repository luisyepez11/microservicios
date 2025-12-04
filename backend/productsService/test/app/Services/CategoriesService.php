<?php

namespace App\Services;

use Illuminate\Support\Facades\DB;

class CategoriesService{
    public function createCategory($name){
        if (DB::table('categories')->where('name', $name)->exists()) {
            return "category already exists";
        }

        $category_id = random_int(1, 9999);
        while (true){
            if (!DB::table('categories')->where('category_id', $category_id)->exists()) {
                break;
            }
            $category_id = random_int(1, 9999);
        }

        $categoryData = [
            'category_id' => $category_id,
            'name' => $name,
        ];

        $this->loadCategoryToDB($categoryData);
        return $category_id;
    }

    private function loadCategoryToDB(array $category){
        return DB::table('categories')->insert($category);
    }

    public function getCategories(){
        return DB::table('categories')
        ->select('category_id', 'name')
        ->get();
    }

    public function editCategory($id, $name){
        return DB::table('categories')->where('category_id', $id)->update([
            'name' => $name,
        ]);
    }

    public function deleteCategory($id){
        return DB::table('categories')->where('category_id', $id)->delete();
    }
}
?>
