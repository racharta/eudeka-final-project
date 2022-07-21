CREATE TABLE `user` (
  `id` varchar(10) NOT NULL,
  `avatar` varchar(200) NOT NULL,
  `email` varchar(50) NOT NULL,
  `username` varchar(30) NOT NULL,
  `password` varchar(20) NOT NULL,
  `kota` varchar(50) NOT NULL,
  `provinsi` varchar(50) NOT NULL,
  `terakhir_diedit` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `barang` (
  `id` varchar(10) NOT NULL,
  `gambar` varchar(200) NOT NULL,
  `nama` varchar(20) NOT NULL,
  `kategori` varchar(50) NOT NULL,
  `stok` int NOT NULL,
  `harga` int NOT NULL,
  `dari_user` varchar(100) NOT NULL,
  `dari_kota` varchar(30) NOT NULL,
  `berat` int NOT NULL,
  `deskripsi` varchar(300) NOT NULL,
  `yg_sudah_beli` int NOT NULL,
  `terakhir_diedit` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `pesanan` (
  `id` varchar(10) NOT NULL,
  `id_barang` varchar(10) NOT NULL,
  `id_pembeli` varchar(10) NOT NULL,
  `banyak` int NOT NULL,
  `ongkir` int NOT NULL,
  `dari_kota` varchar(30) NOT NULL,
  `ke_kota` varchar(30) NOT NULL,
  `harga_total` int NOT NULL,
  `waktu_dibuat` datetime NOT NULL,
  `terakhir_diedit` datetime NOT NULL,
  `_Pesanan__status` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci