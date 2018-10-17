-- phpMyAdmin SQL Dump
-- version 4.6.6deb4
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Oct 17, 2018 at 07:37 AM
-- Server version: 10.1.26-MariaDB-0+deb9u1
-- PHP Version: 7.0.30-0+deb9u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `probes`
--

-- --------------------------------------------------------

--
-- Table structure for table `devices`
--

CREATE TABLE `devices` (
  `id` int(11) NOT NULL,
  `MAC` char(17) NOT NULL,
  `firstSeen` datetime NOT NULL,
  `lastSeen` datetime NOT NULL,
  `manufacturer` varchar(60) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `ESSIDs`
--

CREATE TABLE `ESSIDs` (
  `id` int(11) NOT NULL,
  `ESSID` varchar(32) NOT NULL,
  `firstSeen` datetime NOT NULL,
  `lastSeen` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `sessionESSIDs`
--

CREATE TABLE `sessionESSIDs` (
  `id` int(11) NOT NULL,
  `sessionID` int(11) NOT NULL,
  `ESSIDid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `sessions`
--

CREATE TABLE `sessions` (
  `id` int(11) NOT NULL,
  `deviceID` int(11) NOT NULL,
  `firstSeen` datetime NOT NULL,
  `lastSeen` datetime NOT NULL,
  `seenCount` int(11) NOT NULL,
  `location` enum('Noervenich','Aachen','','') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `devices`
--
ALTER TABLE `devices`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `MAC` (`MAC`),
  ADD KEY `firstSeen` (`firstSeen`),
  ADD KEY `lastSeen` (`lastSeen`);

--
-- Indexes for table `ESSIDs`
--
ALTER TABLE `ESSIDs`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ESSID` (`ESSID`),
  ADD KEY `firstSeen` (`firstSeen`),
  ADD KEY `lastSeen` (`lastSeen`);

--
-- Indexes for table `sessionESSIDs`
--
ALTER TABLE `sessionESSIDs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sessionID` (`sessionID`),
  ADD KEY `ESSID` (`ESSIDid`);

--
-- Indexes for table `sessions`
--
ALTER TABLE `sessions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `start` (`firstSeen`),
  ADD KEY `end` (`lastSeen`),
  ADD KEY `seenCount` (`seenCount`),
  ADD KEY `location` (`location`),
  ADD KEY `deviceID` (`deviceID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `devices`
--
ALTER TABLE `devices`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;
--
-- AUTO_INCREMENT for table `ESSIDs`
--
ALTER TABLE `ESSIDs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=44;
--
-- AUTO_INCREMENT for table `sessionESSIDs`
--
ALTER TABLE `sessionESSIDs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=44;
--
-- AUTO_INCREMENT for table `sessions`
--
ALTER TABLE `sessions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `sessionESSIDs`
--
ALTER TABLE `sessionESSIDs`
  ADD CONSTRAINT `sessionESSIDs_ibfk_1` FOREIGN KEY (`ESSIDid`) REFERENCES `ESSIDs` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  ADD CONSTRAINT `sessionESSIDs_ibfk_2` FOREIGN KEY (`sessionID`) REFERENCES `sessions` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION;

--
-- Constraints for table `sessions`
--
ALTER TABLE `sessions`
  ADD CONSTRAINT `sessions_ibfk_1` FOREIGN KEY (`deviceID`) REFERENCES `devices` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
