-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:4306
-- Generation Time: Mar 31, 2025 at 05:24 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `xerowaste`
--

-- --------------------------------------------------------

--
-- Table structure for table `dishes`
--

CREATE TABLE `dishes` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `image_url` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `dishes`
--

INSERT INTO `dishes` (`id`, `name`, `price`, `image_url`) VALUES
(1, 'Tomato Soup', 150.00, 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSMhp7w14vM1xnA1TUVWmBM9b8pMKE1bJ2bKg&s'),
(2, 'Pasta Alfredo', 250.00, 'https://www.justspices.co.uk/media/recipe/chicken-alfredo.jpg'),
(3, 'Garlic Bread', 120.00, 'https://www.mygingergarlickitchen.com/wp-content/rich-markup-images/16x9/16x9-garlic-bread.jpg'),
(4, 'Veggie Pizza', 350.00, 'https://kristineskitchenblog.com/wp-content/uploads/2024/12/veggie-pizza-recipe-09-2.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `dish_ingredients`
--

CREATE TABLE `dish_ingredients` (
  `id` int(11) NOT NULL,
  `dish_id` int(11) NOT NULL,
  `ingredient_id` int(11) NOT NULL,
  `quantity_used` int(11) NOT NULL,
  `unit` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `dish_ingredients`
--

INSERT INTO `dish_ingredients` (`id`, `dish_id`, `ingredient_id`, `quantity_used`, `unit`) VALUES
(1, 1, 1, 300, 'grams'),
(2, 1, 2, 100, 'grams'),
(3, 1, 3, 50, 'grams'),
(4, 1, 4, 10, 'grams'),
(5, 1, 5, 20, 'grams'),
(6, 1, 6, 5, 'grams'),
(7, 2, 8, 200, 'grams'),
(8, 2, 5, 30, 'grams'),
(9, 2, 7, 200, 'ml'),
(10, 2, 9, 50, 'grams'),
(11, 3, 5, 50, 'grams'),
(12, 3, 4, 20, 'grams'),
(13, 3, 6, 5, 'grams'),
(14, 4, 1, 100, 'grams'),
(15, 4, 3, 50, 'grams'),
(16, 4, 9, 100, 'grams'),
(17, 4, 5, 30, 'grams');

-- --------------------------------------------------------

--
-- Table structure for table `ingredients`
--

CREATE TABLE `ingredients` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `stock` int(11) NOT NULL CHECK (`stock` >= 0),
  `unit` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ingredients`
--

INSERT INTO `ingredients` (`id`, `name`, `stock`, `unit`) VALUES
(1, 'Tomato', 4700, 'grams'),
(2, 'Carrot', 2900, 'grams'),
(3, 'Onion', 1950, 'grams'),
(4, 'Garlic', 490, 'grams'),
(5, 'Butter', 1950, 'grams'),
(6, 'Salt', 995, 'grams'),
(7, 'Milk', 4800, 'ml'),
(8, 'Pasta', 2800, 'grams'),
(9, 'Cheese', 950, 'grams');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `dish_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL CHECK (`quantity` > 0),
  `order_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `table_number` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `dish_id`, `quantity`, `order_date`, `table_number`) VALUES
(1, 1, 1, '2025-03-30 19:45:16', 0),
(2, 2, 1, '2025-03-30 19:46:40', 0);

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `category` varchar(50) NOT NULL,
  `stock` int(11) DEFAULT 0,
  `expiry_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `name`, `category`, `stock`, `expiry_date`) VALUES
(1, 'Whole Wheat Bread', 'Bakery', 120, '2025-04-05'),
(2, 'Croissant', 'Bakery', 90, '2025-03-30'),
(3, 'Bagel', 'Bakery', 150, '2025-04-07'),
(4, 'Chocolate Cake', 'Bakery', 50, '2025-04-02'),
(5, 'Apple Pie', 'Bakery', 30, '2025-03-28'),
(6, 'Milk', 'Food', 200, '2025-04-01'),
(7, 'Cheese', 'Food', 80, '2025-04-15'),
(8, 'Yogurt', 'Food', 100, '2025-03-30'),
(9, 'Eggs', 'Food', 250, '2025-04-10'),
(10, 'Avocado', 'Food', 40, '2025-03-25'),
(11, 'Bananas', 'Food', 120, '2025-03-29'),
(12, 'Organic Carrots', 'Food', 150, '2025-04-12'),
(13, 'Lettuce', 'Food', 180, '2025-03-31'),
(14, 'Olive Oil', 'Food', 60, '2025-06-10'),
(15, 'Garlic', 'Food', 200, '2025-05-01'),
(16, 'Tomatoes', 'Food', 130, '2025-03-27');

-- --------------------------------------------------------

--
-- Table structure for table `product_purchases`
--

CREATE TABLE `product_purchases` (
  `id` int(11) NOT NULL,
  `product_id` int(11) DEFAULT NULL,
  `quantity` int(11) NOT NULL,
  `price_per_unit` float NOT NULL,
  `purchase_date` date DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tables`
--

CREATE TABLE `tables` (
  `id` int(11) NOT NULL,
  `number` int(11) NOT NULL,
  `status` enum('Occupied','Available') DEFAULT 'Available'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `waste_entries`
--

CREATE TABLE `waste_entries` (
  `id` int(11) NOT NULL,
  `waste_type` varchar(100) NOT NULL,
  `quantity` float NOT NULL,
  `unit` varchar(20) NOT NULL,
  `source` varchar(100) DEFAULT NULL,
  `waste_date` date NOT NULL DEFAULT curdate(),
  `reason` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `waste_entries`
--

INSERT INTO `waste_entries` (`id`, `waste_type`, `quantity`, `unit`, `source`, `waste_date`, `reason`) VALUES
(1, 'Plastic', 10, 'g', 'Kitchen', '2025-03-27', ''),
(2, 'Metal', 100, 'kg', 'Manufacturing', '2025-03-08', '');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `dishes`
--
ALTER TABLE `dishes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `dish_ingredients`
--
ALTER TABLE `dish_ingredients`
  ADD PRIMARY KEY (`id`),
  ADD KEY `dish_id` (`dish_id`),
  ADD KEY `ingredient_id` (`ingredient_id`);

--
-- Indexes for table `ingredients`
--
ALTER TABLE `ingredients`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `dish_id` (`dish_id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `product_purchases`
--
ALTER TABLE `product_purchases`
  ADD PRIMARY KEY (`id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `tables`
--
ALTER TABLE `tables`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `number` (`number`);

--
-- Indexes for table `waste_entries`
--
ALTER TABLE `waste_entries`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `dishes`
--
ALTER TABLE `dishes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `dish_ingredients`
--
ALTER TABLE `dish_ingredients`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `ingredients`
--
ALTER TABLE `ingredients`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT for table `product_purchases`
--
ALTER TABLE `product_purchases`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=54;

--
-- AUTO_INCREMENT for table `tables`
--
ALTER TABLE `tables`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `waste_entries`
--
ALTER TABLE `waste_entries`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `dish_ingredients`
--
ALTER TABLE `dish_ingredients`
  ADD CONSTRAINT `dish_ingredients_ibfk_1` FOREIGN KEY (`dish_id`) REFERENCES `dishes` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `dish_ingredients_ibfk_2` FOREIGN KEY (`ingredient_id`) REFERENCES `ingredients` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`dish_id`) REFERENCES `dishes` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `product_purchases`
--
ALTER TABLE `product_purchases`
  ADD CONSTRAINT `product_purchases_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
