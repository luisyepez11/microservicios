<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        // If the table does not exist, create it
        if (!Schema::hasTable('products')) {
            Schema::create('products', function (Blueprint $table) {
                $table->integer('product_id')->primary();
                $table->integer('category_id');
                $table->string('name', 50);
                $table->string('description', 255);
                $table->string('image_url', 255);
                $table->integer('price');
            });
        }
    }


    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('products');
    }
};
