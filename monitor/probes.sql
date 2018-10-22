SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;


CREATE TABLE `connectedDevices` (
  `id` int(11) NOT NULL,
  `deviceID` int(11) NOT NULL,
  `networkID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `devices` (
  `id` int(11) NOT NULL,
  `MAC` char(17) NOT NULL,
  `firstSeen` datetime NOT NULL,
  `lastSeen` datetime NOT NULL,
  `sessionCount` int(11) NOT NULL,
  `probesSeen` tinyint(1) NOT NULL,
  `connectedSeen` tinyint(1) NOT NULL,
  `manufacturer` varchar(60) DEFAULT NULL,
  `notes` mediumtext
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `ESSIDs` (
  `id` int(11) NOT NULL,
  `ESSID` varchar(32) NOT NULL,
  `firstSeen` datetime NOT NULL,
  `lastSeen` datetime NOT NULL,
  `sessionCount` int(11) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `networks` (
  `id` int(11) NOT NULL,
  `BSSID` char(17) NOT NULL,
  `ESSID` varchar(32) DEFAULT NULL,
  `channel` int(11) NOT NULL,
  `RSSImax` int(11) NOT NULL,
  `latitude` decimal(10,8) NOT NULL,
  `longitude` decimal(11,8) NOT NULL,
  `manufacturer` varchar(60) DEFAULT NULL,
  `notes` mediumtext
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `sessionESSIDs` (
  `id` int(11) NOT NULL,
  `sessionID` int(11) NOT NULL,
  `ESSIDid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `sessions` (
  `id` int(11) NOT NULL,
  `deviceID` int(11) NOT NULL,
  `firstSeen` datetime NOT NULL,
  `lastSeen` datetime NOT NULL,
  `seenCount` int(11) NOT NULL,
  `latitude` decimal(10,8) DEFAULT NULL,
  `longitude` decimal(11,8) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(16) NOT NULL,
  `password` varbinary(128) NOT NULL,
  `salt` char(16) NOT NULL,
  `type` enum('DRONE','VIEWER','ADMIN') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


ALTER TABLE `connectedDevices`
  ADD PRIMARY KEY (`id`),
  ADD KEY `deviceID` (`deviceID`),
  ADD KEY `networkID` (`networkID`);

ALTER TABLE `devices`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `MAC` (`MAC`),
  ADD KEY `firstSeen` (`firstSeen`),
  ADD KEY `lastSeen` (`lastSeen`),
  ADD KEY `sessionCount` (`sessionCount`);

ALTER TABLE `ESSIDs`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ESSID` (`ESSID`),
  ADD KEY `firstSeen` (`firstSeen`),
  ADD KEY `lastSeen` (`lastSeen`),
  ADD KEY `sessionCount` (`sessionCount`);

ALTER TABLE `networks`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `MAC` (`BSSID`),
  ADD KEY `ESSID` (`ESSID`),
  ADD KEY `latitude` (`latitude`),
  ADD KEY `longitude` (`longitude`);

ALTER TABLE `sessionESSIDs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sessionID` (`sessionID`),
  ADD KEY `ESSID` (`ESSIDid`);

ALTER TABLE `sessions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `start` (`firstSeen`),
  ADD KEY `end` (`lastSeen`),
  ADD KEY `seenCount` (`seenCount`),
  ADD KEY `deviceID` (`deviceID`),
  ADD KEY `latitude` (`latitude`),
  ADD KEY `longitude` (`longitude`);

ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);


ALTER TABLE `connectedDevices`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `devices`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `ESSIDs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `networks`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `sessionESSIDs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `sessions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `connectedDevices`
  ADD CONSTRAINT `connectedDevices_ibfk_1` FOREIGN KEY (`deviceID`) REFERENCES `devices` (`id`) ON UPDATE NO ACTION,
  ADD CONSTRAINT `connectedDevices_ibfk_2` FOREIGN KEY (`networkID`) REFERENCES `networks` (`id`) ON UPDATE NO ACTION;

ALTER TABLE `sessionESSIDs`
  ADD CONSTRAINT `sessionESSIDs_ibfk_1` FOREIGN KEY (`ESSIDid`) REFERENCES `ESSIDs` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  ADD CONSTRAINT `sessionESSIDs_ibfk_2` FOREIGN KEY (`sessionID`) REFERENCES `sessions` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION;

ALTER TABLE `sessions`
  ADD CONSTRAINT `sessions_ibfk_1` FOREIGN KEY (`deviceID`) REFERENCES `devices` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
