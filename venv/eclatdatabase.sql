-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 01, 2024 at 08:49 AM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.1.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `eclatdatabase`
--

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE `transactions` (
  `id` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `dataset` varchar(255) NOT NULL,
  `rule` varchar(255) NOT NULL,
  `id_user` int(100) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `transactions`
--

INSERT INTO `transactions` (`id`, `name`, `dataset`, `rule`, `id_user`, `created_at`) VALUES
(32, 'cobain2', 'cobain2.csv', 'cobain2_rule.csv', 15, '2023-12-24 05:25:33'),
(33, 'cobain', 'cobain.csv', 'cobain_rule.csv', 14, '2023-12-24 05:25:33'),
(36, 'datafix', 'datafix.csv', 'datafix_rule.csv', 14, '2023-12-24 06:11:58'),
(57, 'datafix', 'datafix.csv', 'datafix_rule.csv', 10, '2023-12-28 01:22:54');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(100) NOT NULL,
  `name` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `username`, `password`, `role`) VALUES
(10, 'nabila', 'lala', '$2b$12$fhvUZSow6zcEuHF0tWdkO.ViLnTcYvOztEcQ07zpRfM/oSiitkQ6e', ''),
(12, 'admin', 'admin', '$2b$12$pcdu2/BGDZk4eML05zZgiOkYO2PbiE2pgOFrIJdcrqAwc5asTjAMu', 'admin'),
(14, 'shilna paradisa', 'shilna', '$2b$12$5Q8HNbYHtvko.UPWYQfWzOAVZEJVc3abXhZVJU4NBy0azLaOe6Pj.', 'user'),
(15, 'Nur Hasna Amatullah', 'hasnay', '$2b$12$3bI0dvYzqE.blOzE9BE6m.r5fmSqpKCFbEQ9IPt/G4DMxyFcWo4Py', 'user'),
(16, 'rere', 'rere', '$2b$12$shS8m2QNBhBLBJWHCpriruzR1sV4tKvhHHD95Cnh8hkvX0fTy24Y2', 'user'),
(34, 'shilna', 'shilnay', '$2b$12$GrdGLFRmMf8WJoaaoIR/mOo6gZZLSf9WZ465Ydk3nutT9rmEOh2V2', 'user'),
(36, 'nana', 'nana', '$2b$12$jyknEdNGOX9D8nWgf.TS2e9PHGAqHBinKllyVMkcqS2oKtFUpcviO', 'user');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_user` (`id_user`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `transactions`
--
ALTER TABLE `transactions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=58;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `transactions`
--
ALTER TABLE `transactions`
  ADD CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
