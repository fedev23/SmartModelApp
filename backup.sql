PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE project (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    created_date TEXT
, is_last_selected BOOLEAN DEFAULT 0);
INSERT INTO project VALUES(57,'auth0_670fc1b2ead82aaae5c1e9ba','Proyecto_prueba_De_Datos','2024-11-13 12:22:35',0);
INSERT INTO project VALUES(63,'auth0_670fc1b2ead82aaae5c1e9ba','test test','2024-11-19 10:44:33',0);
INSERT INTO project VALUES(67,'auth0_670d225413861ad9fa6849d3','ProyectoA','2024-12-27 13:12:10',0);
INSERT INTO project VALUES(69,'auth0_670d225413861ad9fa6849d3','proximo_delete','2025-01-10 09:41:57',0);
INSERT INTO project VALUES(71,'auth0_670d225413861ad9fa6849d3','b','2025-01-10 10:48:25',0);
INSERT INTO project VALUES(72,'auth0_670d225413861ad9fa6849d3','c','2025-01-10 10:50:39',0);
INSERT INTO project VALUES(81,'auth0_670d225413861ad9fa6849d3','proyecto sin version','2025-01-13 12:32:34',0);
INSERT INTO project VALUES(82,'auth0_670d225413861ad9fa6849d3','proyecto prueba','2025-01-14 10:53:30',0);
INSERT INTO project VALUES(83,'auth0_670d225413861ad9fa6849d3','proyecto_prueba','2025-01-14 10:55:58',0);
INSERT INTO project VALUES(84,'auth0_670d225413861ad9fa6849d3','F1','2025-01-15 13:38:08',1);
CREATE TABLE execution_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    project_id INTEGER,
    execution_date TEXT,
    model_name TEXT, dataset_name TEXT,
    FOREIGN KEY (project_id) REFERENCES project(id)
);
INSERT INTO execution_log VALUES(1,'auth0_670fc1b2ead82aaae5c1e9ba',1,'2024-10-31 11:29:36','Nuevo Proyecto',NULL);
INSERT INTO execution_log VALUES(2,'auth0_670fc1b2ead82aaae5c1e9ba',2,'2024-10-31 11:31:17','Nuevo Proyecto',NULL);
INSERT INTO execution_log VALUES(3,'auth0_670fc1b2ead82aaae5c1e9ba',3,'2024-10-31 11:34:37','Nuevo Proyecto',NULL);
INSERT INTO execution_log VALUES(4,'auth0_670fc1b2ead82aaae5c1e9ba',4,'2024-10-31 11:35:20','banco provincia',NULL);
INSERT INTO execution_log VALUES(5,'auth0_670d225413861ad9fa6849d3',5,'2024-10-31 11:35:49','federico',NULL);
INSERT INTO execution_log VALUES(6,'auth0_670fc1b2ead82aaae5c1e9ba',6,'2024-10-31 17:31:50','banco 1',NULL);
INSERT INTO execution_log VALUES(7,'auth0_670fc1b2ead82aaae5c1e9ba',7,'2024-11-01 11:03:57','hola',NULL);
INSERT INTO execution_log VALUES(8,'auth0_670fc1b2ead82aaae5c1e9ba',8,'2024-11-01 11:04:36','fede',NULL);
INSERT INTO execution_log VALUES(9,'auth0_670fc1b2ead82aaae5c1e9ba',9,'2024-11-01 11:26:44','messi',NULL);
INSERT INTO execution_log VALUES(10,'auth0_670fc1b2ead82aaae5c1e9ba',10,'2024-11-01 11:27:47','prueba',NULL);
INSERT INTO execution_log VALUES(11,'auth0_670d225413861ad9fa6849d3',11,'2024-11-01 11:42:20','pepe',NULL);
INSERT INTO execution_log VALUES(12,'auth0_670d225413861ad9fa6849d3',12,'2024-11-01 12:03:19','prueba2',NULL);
INSERT INTO execution_log VALUES(13,'auth0_670d225413861ad9fa6849d3',13,'2024-11-01 12:04:49','h',NULL);
INSERT INTO execution_log VALUES(14,'auth0_670d225413861ad9fa6849d3',14,'2024-11-01 12:18:09','f',NULL);
INSERT INTO execution_log VALUES(15,'auth0_670d225413861ad9fa6849d3',15,'2024-11-01 13:00:19','a',NULL);
INSERT INTO execution_log VALUES(16,'auth0_670d225413861ad9fa6849d3',16,'2024-11-01 13:00:38','verificar proyecto',NULL);
INSERT INTO execution_log VALUES(17,'auth0_670fc1b2ead82aaae5c1e9ba',17,'2024-11-04 10:46:00','Hola',NULL);
INSERT INTO execution_log VALUES(18,'auth0_670fc1b2ead82aaae5c1e9ba',18,'2024-11-04 10:47:25','prueba_eliminar',NULL);
INSERT INTO execution_log VALUES(19,'auth0_670d225413861ad9fa6849d3',19,'2024-11-04 11:50:16','ver lista',NULL);
INSERT INTO execution_log VALUES(20,'auth0_670d225413861ad9fa6849d3',20,'2024-11-04 11:58:08','proyecto',NULL);
INSERT INTO execution_log VALUES(21,'auth0_670d225413861ad9fa6849d3',21,'2024-11-04 11:59:56','verificar',NULL);
INSERT INTO execution_log VALUES(22,'auth0_670d225413861ad9fa6849d3',22,'2024-11-04 12:21:56','Proyecto',NULL);
INSERT INTO execution_log VALUES(23,'auth0_670fc1b2ead82aaae5c1e9ba',23,'2024-11-04 16:03:27','prueba de estado',NULL);
INSERT INTO execution_log VALUES(24,'auth0_670fc1b2ead82aaae5c1e9ba',24,'2024-11-06 11:38:30','a',NULL);
INSERT INTO execution_log VALUES(25,'auth0_670fc1b2ead82aaae5c1e9ba',25,'2024-11-07 14:10:24','Hola',NULL);
INSERT INTO execution_log VALUES(26,'auth0_670fc1b2ead82aaae5c1e9ba',26,'2024-11-08 09:26:39','fede',NULL);
INSERT INTO execution_log VALUES(27,'auth0_670fc1b2ead82aaae5c1e9ba',27,'2024-11-11 15:35:19','Prueba de all',NULL);
INSERT INTO execution_log VALUES(28,'auth0_670fc1b2ead82aaae5c1e9ba',28,'2024-11-12 10:32:10','Proyecto_pueda_id',NULL);
INSERT INTO execution_log VALUES(29,'auth0_670fc1b2ead82aaae5c1e9ba',29,'2024-11-12 10:38:52','pruebo de nuevo',NULL);
INSERT INTO execution_log VALUES(30,'auth0_670fc1b2ead82aaae5c1e9ba',30,'2024-11-12 10:39:36','pruebo id y name',NULL);
INSERT INTO execution_log VALUES(31,'auth0_670fc1b2ead82aaae5c1e9ba',31,'2024-11-12 10:40:08','a',NULL);
INSERT INTO execution_log VALUES(32,'auth0_670fc1b2ead82aaae5c1e9ba',32,'2024-11-12 10:52:06','Proyecto',NULL);
INSERT INTO execution_log VALUES(33,'auth0_670fc1b2ead82aaae5c1e9ba',33,'2024-11-12 11:11:50','Pruebo version y proyecto',NULL);
INSERT INTO execution_log VALUES(34,'auth0_670fc1b2ead82aaae5c1e9ba',34,'2024-11-12 11:26:59','Proyecto_prubea de version',NULL);
INSERT INTO execution_log VALUES(35,'auth0_670fc1b2ead82aaae5c1e9ba',35,'2024-11-12 11:29:15','a',NULL);
INSERT INTO execution_log VALUES(36,'auth0_670fc1b2ead82aaae5c1e9ba',36,'2024-11-12 11:37:52','proyecto22',NULL);
INSERT INTO execution_log VALUES(37,'auth0_670fc1b2ead82aaae5c1e9ba',37,'2024-11-12 11:47:29','practicar version',NULL);
INSERT INTO execution_log VALUES(38,'auth0_670fc1b2ead82aaae5c1e9ba',38,'2024-11-12 11:49:09','check',NULL);
INSERT INTO execution_log VALUES(39,'auth0_670fc1b2ead82aaae5c1e9ba',39,'2024-11-12 11:49:15','ver',NULL);
INSERT INTO execution_log VALUES(40,'auth0_670fc1b2ead82aaae5c1e9ba',40,'2024-11-12 11:51:23','proy',NULL);
INSERT INTO execution_log VALUES(41,'auth0_670fc1b2ead82aaae5c1e9ba',41,'2024-11-12 11:59:09','proyecto?',NULL);
INSERT INTO execution_log VALUES(42,'auth0_670fc1b2ead82aaae5c1e9ba',42,'2024-11-12 13:30:07','Proyecto2',NULL);
INSERT INTO execution_log VALUES(43,'auth0_670fc1b2ead82aaae5c1e9ba',43,'2024-11-12 13:34:42','prueba de datao',NULL);
INSERT INTO execution_log VALUES(44,'auth0_670fc1b2ead82aaae5c1e9ba',44,'2024-11-12 13:37:33','aa',NULL);
INSERT INTO execution_log VALUES(45,'auth0_670fc1b2ead82aaae5c1e9ba',45,'2024-11-12 14:00:42','hola',NULL);
INSERT INTO execution_log VALUES(46,'auth0_670fc1b2ead82aaae5c1e9ba',46,'2024-11-12 14:45:42','proyecto prueba',NULL);
INSERT INTO execution_log VALUES(47,'auth0_670fc1b2ead82aaae5c1e9ba',47,'2024-11-12 14:56:51','aa',NULL);
INSERT INTO execution_log VALUES(48,'auth0_670fc1b2ead82aaae5c1e9ba',48,'2024-11-12 15:04:11','aa',NULL);
INSERT INTO execution_log VALUES(49,'auth0_670fc1b2ead82aaae5c1e9ba',49,'2024-11-12 15:06:30','ver',NULL);
INSERT INTO execution_log VALUES(50,'auth0_670fc1b2ead82aaae5c1e9ba',50,'2024-11-12 15:08:00','pp',NULL);
INSERT INTO execution_log VALUES(51,'auth0_670fc1b2ead82aaae5c1e9ba',51,'2024-11-12 15:11:53','aaaa',NULL);
INSERT INTO execution_log VALUES(52,'auth0_670fc1b2ead82aaae5c1e9ba',52,'2024-11-13 11:08:06','Proyecto pueba de folder1',NULL);
INSERT INTO execution_log VALUES(53,'auth0_670fc1b2ead82aaae5c1e9ba',53,'2024-11-13 11:20:06','pRUEBA DATA 2',NULL);
INSERT INTO execution_log VALUES(54,'auth0_670fc1b2ead82aaae5c1e9ba',54,'2024-11-13 11:22:02','prueba_3',NULL);
INSERT INTO execution_log VALUES(55,'auth0_670fc1b2ead82aaae5c1e9ba',55,'2024-11-13 11:36:54','prueba g',NULL);
INSERT INTO execution_log VALUES(56,'auth0_670fc1b2ead82aaae5c1e9ba',56,'2024-11-13 11:37:41','prueba gg',NULL);
INSERT INTO execution_log VALUES(57,'auth0_670fc1b2ead82aaae5c1e9ba',57,'2024-11-13 12:22:35','Proyecto_prueba_De_Datos',NULL);
INSERT INTO execution_log VALUES(58,'auth0_670fc1b2ead82aaae5c1e9ba',58,'2024-11-15 10:36:40','Beso',NULL);
INSERT INTO execution_log VALUES(59,'auth0_670fc1b2ead82aaae5c1e9ba',59,'2024-11-19 10:29:27','Ver data set',NULL);
INSERT INTO execution_log VALUES(60,'auth0_670fc1b2ead82aaae5c1e9ba',60,'2024-11-19 10:29:39','a',NULL);
INSERT INTO execution_log VALUES(61,'auth0_670fc1b2ead82aaae5c1e9ba',61,'2024-11-19 10:41:26','test',NULL);
INSERT INTO execution_log VALUES(62,'auth0_670fc1b2ead82aaae5c1e9ba',62,'2024-11-19 10:43:16','test now',NULL);
INSERT INTO execution_log VALUES(63,'auth0_670fc1b2ead82aaae5c1e9ba',63,'2024-11-19 10:44:33','test test',NULL);
INSERT INTO execution_log VALUES(64,'auth0_670fc1b2ead82aaae5c1e9ba',64,'2024-11-19 10:46:30','a?',NULL);
INSERT INTO execution_log VALUES(65,'auth0_670fc1b2ead82aaae5c1e9ba',65,'2024-11-19 10:56:16','xd',NULL);
INSERT INTO execution_log VALUES(66,'auth0_670fc1b2ead82aaae5c1e9ba',66,'2024-11-19 11:00:18','pp',NULL);
INSERT INTO execution_log VALUES(67,'auth0_670d225413861ad9fa6849d3',67,'2024-12-27 13:12:10','ProyectoA',NULL);
INSERT INTO execution_log VALUES(68,'auth0_670d225413861ad9fa6849d3',68,'2025-01-09 12:36:57','pepe_eliminar',NULL);
INSERT INTO execution_log VALUES(69,'auth0_670d225413861ad9fa6849d3',69,'2025-01-10 09:41:57','proximo_delete',NULL);
INSERT INTO execution_log VALUES(70,'auth0_670d225413861ad9fa6849d3',70,'2025-01-10 09:48:47','A',NULL);
INSERT INTO execution_log VALUES(71,'auth0_670d225413861ad9fa6849d3',71,'2025-01-10 10:48:25','b',NULL);
INSERT INTO execution_log VALUES(72,'auth0_670d225413861ad9fa6849d3',72,'2025-01-10 10:50:39','c',NULL);
INSERT INTO execution_log VALUES(73,'auth0_670d225413861ad9fa6849d3',73,'2025-01-10 10:53:29','d',NULL);
INSERT INTO execution_log VALUES(74,'auth0_670d225413861ad9fa6849d3',74,'2025-01-10 10:56:00','e',NULL);
INSERT INTO execution_log VALUES(75,'auth0_670d225413861ad9fa6849d3',75,'2025-01-10 11:14:05','proyecto234',NULL);
INSERT INTO execution_log VALUES(76,'auth0_670d225413861ad9fa6849d3',76,'2025-01-13 10:18:02','probando con espacios',NULL);
INSERT INTO execution_log VALUES(77,'auth0_670d225413861ad9fa6849d3',77,'2025-01-13 11:40:45','pp',NULL);
INSERT INTO execution_log VALUES(78,'auth0_670d225413861ad9fa6849d3',78,'2025-01-13 11:44:28','aa',NULL);
INSERT INTO execution_log VALUES(79,'auth0_670d225413861ad9fa6849d3',79,'2025-01-13 12:17:19','proyecto prueba',NULL);
INSERT INTO execution_log VALUES(80,'auth0_670d225413861ad9fa6849d3',80,'2025-01-13 12:20:59','proyecto con espacios',NULL);
INSERT INTO execution_log VALUES(81,'auth0_670d225413861ad9fa6849d3',81,'2025-01-13 12:32:34','proyecto sin version',NULL);
INSERT INTO execution_log VALUES(82,'auth0_670d225413861ad9fa6849d3',82,'2025-01-14 10:53:30','proyecto prueba',NULL);
INSERT INTO execution_log VALUES(83,'auth0_670d225413861ad9fa6849d3',83,'2025-01-14 10:55:58','proyecto_prueba',NULL);
INSERT INTO execution_log VALUES(84,'auth0_670d225413861ad9fa6849d3',84,'2025-01-15 13:38:08','F1',NULL);
CREATE TABLE version (
    version_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    nombre_version TEXT NOT NULL,
    execution_date TEXT, is_last_selected BOOLEAN DEFAULT 0,
    FOREIGN KEY (project_id) REFERENCES project(id)
);
INSERT INTO version VALUES(4,25,'version hola?','2024-11-07 15:58:55',0);
INSERT INTO version VALUES(5,23,'a','2024-11-08 09:17:07',0);
INSERT INTO version VALUES(19,33,'version?','2024-11-12 11:12:40',0);
INSERT INTO version VALUES(20,33,'version23','2024-11-12 11:13:21',0);
INSERT INTO version VALUES(21,34,'prueba de la prueba','2024-11-12 11:27:15',0);
INSERT INTO version VALUES(22,34,'a','2024-11-12 11:27:41',0);
INSERT INTO version VALUES(23,35,'a','2024-11-12 11:29:20',0);
INSERT INTO version VALUES(24,36,'vers','2024-11-12 11:38:27',0);
INSERT INTO version VALUES(25,37,'version 2=','2024-11-12 11:47:40',0);
INSERT INTO version VALUES(26,38,'ver','2024-11-12 11:49:22',0);
INSERT INTO version VALUES(27,40,'version','2024-11-12 11:51:31',0);
INSERT INTO version VALUES(28,41,'version prueba','2024-11-12 11:59:18',0);
INSERT INTO version VALUES(29,43,'v2','2024-11-13 10:44:03',0);
INSERT INTO version VALUES(30,57,'Inicial','2024-11-13 14:26:24',0);
INSERT INTO version VALUES(56,57,'SmartModel','2024-12-06 09:58:10',0);
INSERT INTO version VALUES(59,57,'c','2024-12-12 12:50:41',0);
INSERT INTO version VALUES(67,57,'dataOk','2024-12-26 11:24:42',0);
INSERT INTO version VALUES(69,67,'version22','2024-12-27 13:12:24',0);
INSERT INTO version VALUES(79,67,'version_prueba32','2025-01-09 12:20:30',0);
INSERT INTO version VALUES(82,82,'prueba','2025-01-14 10:54:34',0);
INSERT INTO version VALUES(83,83,'prueba','2025-01-14 11:04:49',0);
INSERT INTO version VALUES(84,83,'version prueba 22','2025-01-14 12:20:21',0);
INSERT INTO version VALUES(85,83,'version prueba 23','2025-01-14 12:24:58',0);
INSERT INTO version VALUES(94,83,'porcentaje6','2025-01-14 16:15:16',0);
INSERT INTO version VALUES(95,83,'porcentaje7','2025-01-14 16:22:27',0);
INSERT INTO version VALUES(98,83,'10','2025-01-14 17:25:16',0);
INSERT INTO version VALUES(106,83,'prueba2','2025-01-15 11:04:57',0);
INSERT INTO version VALUES(108,83,'version234','2025-01-15 11:47:46',0);
INSERT INTO version VALUES(110,83,'F1V2','2025-01-15 13:53:36',0);
INSERT INTO version VALUES(116,84,'fd2','2025-01-17 11:27:21',0);
INSERT INTO version VALUES(119,84,'f','2025-01-17 12:20:55',0);
INSERT INTO version VALUES(124,84,'g','2025-01-17 15:59:25',0);
INSERT INTO version VALUES(125,84,'gg','2025-01-17 16:08:23',0);
INSERT INTO version VALUES(129,84,'fede3','2025-01-20 12:19:08',0);
INSERT INTO version VALUES(131,84,'fd3','2025-01-20 14:43:40',1);
INSERT INTO version VALUES(132,84,'ver','2025-01-20 15:13:57',0);
CREATE TABLE json_versions (
                id_jsons INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_version TEXT NOT NULL,
                fecha_de_carga TEXT NOT NULL,
                version_id INTEGER,
                FOREIGN KEY (version_id) REFERENCES version(version_id)
            );
INSERT INTO json_versions VALUES(30,'ver 2','2024-11-19 16:54:08',38);
INSERT INTO json_versions VALUES(32,'cheack 2','2024-11-19 17:10:09',38);
INSERT INTO json_versions VALUES(33,'chiki','2024-11-19 17:14:01',39);
INSERT INTO json_versions VALUES(34,'ee','2024-11-20 09:52:07',38);
INSERT INTO json_versions VALUES(35,'version dos carpetas right?','2024-11-21 09:35:25',40);
INSERT INTO json_versions VALUES(36,'check now en','2024-11-21 09:56:34',40);
INSERT INTO json_versions VALUES(37,'now?','2024-11-21 09:58:41',40);
INSERT INTO json_versions VALUES(51,'c','2024-12-13 15',30);
INSERT INTO json_versions VALUES(52,'d','2024-12-15 13',59);
INSERT INTO json_versions VALUES(56,'beso','2024-12-17 14',56);
INSERT INTO json_versions VALUES(57,'a','2024-12-17 15',59);
INSERT INTO json_versions VALUES(59,'a','2024-12-17 16',56);
INSERT INTO json_versions VALUES(61,'dinosaurio','2024-12-26 09',30);
INSERT INTO json_versions VALUES(62,'dataOk','2024-12-26 11',30);
INSERT INTO json_versions VALUES(63,'version_De_prueba','2024-12-27 15',68);
INSERT INTO json_versions VALUES(64,'besame','2025-01-06 15',74);
INSERT INTO json_versions VALUES(65,'version_prueba_de_22','2025-01-08 10',69);
INSERT INTO json_versions VALUES(68,'prueba_execucion','2025-01-10 15',69);
INSERT INTO json_versions VALUES(72,'version niveles sc','2025-01-14 12',85);
INSERT INTO json_versions VALUES(73,'versionb','2025-01-15 11',83);
INSERT INTO json_versions VALUES(74,'versionb','2025-01-15 11',83);
INSERT INTO json_versions VALUES(75,'a','2025-01-16 11',110);
INSERT INTO json_versions VALUES(76,'b','2025-01-16 11',110);
INSERT INTO json_versions VALUES(78,'fd23456','2025-01-20 16',131);
INSERT INTO json_versions VALUES(80,'fdd3','2025-01-22 13',131);
INSERT INTO json_versions VALUES(81,'NVN&S','2025-01-22 15',131);
CREATE TABLE IF NOT EXISTS "model_execution_temp" (
            execution_id INTEGER PRIMARY KEY AUTOINCREMENT,
            version_id INTEGER,  -- Relación con la tabla 'versions'
            json_version_id INTEGER,  -- Relación con la tabla 'json_versions'
            execution_date TEXT,
            model_name TEXT,
            dataset_name TEXT,
            execution_state TEXT DEFAULT NULL,
            FOREIGN KEY (version_id) REFERENCES versions(version_id),
            FOREIGN KEY (json_version_id) REFERENCES json_versions(id_jsons)
        );
INSERT INTO model_execution_temp VALUES(1,59,NULL,'2024-12-19 16','desarollo','Muestra_Desarrollo.txt','Exito');
INSERT INTO model_execution_temp VALUES(2,59,NULL,'2024-12-20 11','desarollo','Muestra_Desarrollo.txt','Error');
INSERT INTO model_execution_temp VALUES(3,59,NULL,'2024-12-20 11','desarollo','Muestra_Desarrollo.txt','Error');
INSERT INTO model_execution_temp VALUES(4,59,NULL,'2024-12-20 11','desarollo','Muestra_Desarrollo.txt','Error');
INSERT INTO model_execution_temp VALUES(5,59,NULL,'2024-12-20 12','desarollo','Muestra_Desarrollo.txt','Error');
INSERT INTO model_execution_temp VALUES(6,59,NULL,'2024-12-20 12','desarollo','Muestra_Desarrollo.txt','Error');
INSERT INTO model_execution_temp VALUES(7,59,NULL,'2024-12-20 12','desarollo','Muestra_Desarrollo.txt','Error');
INSERT INTO model_execution_temp VALUES(8,59,NULL,'2024-12-20 12','desarollo','Muestra_Desarrollo.txt','Error');
INSERT INTO model_execution_temp VALUES(9,59,NULL,'2024-12-20 12','desarollo','Muestra_Desarrollo.txt','Error');
INSERT INTO model_execution_temp VALUES(10,59,NULL,'2024-12-20 12','desarollo','Muestra_Desarrollo.txt','Error');
INSERT INTO model_execution_temp VALUES(11,59,NULL,'2024-12-20 12','desarollo','Muestra_Desarrollo.txt','Error');
INSERT INTO model_execution_temp VALUES(12,59,NULL,'2024-12-20 12','desarollo','Muestra_Desarrollo.txt','Error');
INSERT INTO model_execution_temp VALUES(13,59,NULL,'2024-12-20 12','desarollo','Muestra_Desarrollo.txt','Error');
INSERT INTO model_execution_temp VALUES(14,59,NULL,'2024-12-20 14:56:50','desarollo','Muestra_Desarrollo.txt','Exito');
INSERT INTO model_execution_temp VALUES(15,59,NULL,'2024-12-20 15:15:53','desarollo','Modeling_App.db','Exito');
INSERT INTO model_execution_temp VALUES(16,59,NULL,'2024-12-20 15:17:44','desarollo','Modeling_App.db','Exito');
INSERT INTO model_execution_temp VALUES(17,59,NULL,'2024-12-20 15:17:44','desarollo','Modeling_App.db','Error');
INSERT INTO model_execution_temp VALUES(18,59,57,'2024-12-20 17:03:07','in_sample','Muestra_Desarrollo.txt','Exito');
INSERT INTO model_execution_temp VALUES(19,59,52,'2024-12-20 17:04:27','in_sample','Muestra_Desarrollo.txt','Exito');
INSERT INTO model_execution_temp VALUES(20,56,52,'2024-12-20 17:04:40','in_sample','Muestra_Desarrollo.txt','Exito');
INSERT INTO model_execution_temp VALUES(21,56,59,'2024-12-20 17:04:42','in_sample','Muestra_Desarrollo.txt','Exito');
INSERT INTO model_execution_temp VALUES(22,59,59,'2024-12-20 17:04:48','in_sample','Muestra_Desarrollo.txt','Exito');
INSERT INTO model_execution_temp VALUES(23,59,57,'2024-12-20 17:04:49','in_sample','Muestra_Desarrollo.txt','Exito');
INSERT INTO model_execution_temp VALUES(24,59,52,'2024-12-20 17:05:01','in_sample','Muestra_Desarrollo.txt','Exito');
INSERT INTO model_execution_temp VALUES(25,59,52,'2024-12-21 10:53:47','in_sample','Muestra_Desarrollo.txt','Exito');
INSERT INTO model_execution_temp VALUES(26,59,NULL,'2024-12-23 11:56:45','of_sample','Modeling_App.db','Exito');
INSERT INTO model_execution_temp VALUES(27,59,57,'2024-12-23 12:17:54','in_sample','Muestra_Desarrollo.txt','Exito');
INSERT INTO model_execution_temp VALUES(28,59,57,'2024-12-23 12:21:38','in_sample','Muestra_Desarrollo.txt','Exito');
INSERT INTO model_execution_temp VALUES(29,59,52,'2024-12-23 12:22:15','in_sample','Muestra_Desarrollo.txt','Exito');
INSERT INTO model_execution_temp VALUES(30,59,57,'2024-12-23 12:22:30','in_sample','Muestra_Desarrollo.txt','Exito');
INSERT INTO model_execution_temp VALUES(31,NULL,57,'2024-12-23 12:32:25','in_sample','Muestra_Desarrollo.txt','Exito');
INSERT INTO model_execution_temp VALUES(32,NULL,52,'2024-12-23 12:32:54','in_sample','Muestra_Desarrollo.txt','Exito');
INSERT INTO model_execution_temp VALUES(33,NULL,57,'2024-12-23 12:33:02','in_sample','Muestra_Desarrollo.txt','Exito');
INSERT INTO model_execution_temp VALUES(34,NULL,52,'2024-12-23 12:33:17','in_sample','Muestra_Desarrollo.txt','Exito');
INSERT INTO model_execution_temp VALUES(35,NULL,57,'2024-12-23 12:38:54','in_sample','Muestra_Desarrollo.txt','Exito');
INSERT INTO model_execution_temp VALUES(36,NULL,52,'2024-12-23 12:39:01','in_sample','Muestra_Desarrollo.txt','Exito');
INSERT INTO model_execution_temp VALUES(37,NULL,57,'2024-12-23 12:39:26','in_sample','Muestra_Desarrollo.txt','Exito');
INSERT INTO model_execution_temp VALUES(38,NULL,51,'2024-12-23 12:41:04','in_sample','Muestra_Desarrollo.txt','Exito');
INSERT INTO model_execution_temp VALUES(39,NULL,57,'2024-12-23 12:41:07','in_sample','Muestra_Desarrollo.txt','Exito');
INSERT INTO model_execution_temp VALUES(40,NULL,57,'2024-12-23 12:48:07','in_sample','Muestra_Desarrollo.txt','Exito');
INSERT INTO model_execution_temp VALUES(41,NULL,52,'2024-12-23 12:49:05','in_sample','Muestra_Desarrollo.txt','Exito');
INSERT INTO model_execution_temp VALUES(42,NULL,57,'2024-12-23 12:49:08','in_sample','Muestra_Desarrollo.txt','Exito');
INSERT INTO model_execution_temp VALUES(43,NULL,57,'2024-12-23 12:57:06','in_sample','Muestra_Desarrollo.txt','Exito');
INSERT INTO model_execution_temp VALUES(44,NULL,52,'2024-12-23 13:00:15','in_sample','Muestra_Desarrollo.txt','Exito');
INSERT INTO model_execution_temp VALUES(45,NULL,57,'2024-12-23 13:00:05','in_sample','Muestra_Desarrollo.txt','Exito');
INSERT INTO model_execution_temp VALUES(46,NULL,59,'2024-12-23 13:01:34','in_sample','Muestra_Desarrollo.txt','Exito');
INSERT INTO model_execution_temp VALUES(47,56,NULL,'2024-12-23 13:02:33','desarollo','Modeling_App.db','Error');
INSERT INTO model_execution_temp VALUES(48,59,NULL,'2024-12-23 13:03:22','desarollo','Modeling_App.db','Error');
INSERT INTO model_execution_temp VALUES(49,NULL,57,'2024-12-23 13:03:24','in_sample','Muestra_Desarrollo.txt','Exito');
INSERT INTO model_execution_temp VALUES(50,NULL,52,'2024-12-23 13:03:48','in_sample','Muestra_Desarrollo.txt','Exito');
INSERT INTO model_execution_temp VALUES(51,NULL,57,'2024-12-23 13:03:56','in_sample','Muestra_Desarrollo.txt','Exito');
INSERT INTO model_execution_temp VALUES(52,NULL,52,'2024-12-23 13:08:12','in_sample','Muestra_Desarrollo.txt','Exito');
INSERT INTO model_execution_temp VALUES(53,NULL,57,'2024-12-23 13:20:00','in_sample','Muestra_Desarrollo.txt','Exito');
INSERT INTO model_execution_temp VALUES(54,30,NULL,'2024-12-26 09:45:11','desarollo','Modeling_App.db','Exito');
INSERT INTO model_execution_temp VALUES(55,67,NULL,'2024-12-27 11:40:52','desarollo','Modeling_App.db','Exito');
INSERT INTO model_execution_temp VALUES(56,68,NULL,'2024-12-27 15:05:45','desarollo','Modeling_App.db','Exito');
INSERT INTO model_execution_temp VALUES(57,NULL,63,'2024-12-27 15:17:52','in_sample','Muestra_Desarrollo.txt','Error');
INSERT INTO model_execution_temp VALUES(58,NULL,63,'2024-12-27 15:24:18','in_sample','Muestra_Desarrollo.txt','Error');
INSERT INTO model_execution_temp VALUES(59,NULL,63,'2024-12-27 15:27:28','in_sample','Muestra_Desarrollo.txt','Error');
INSERT INTO model_execution_temp VALUES(60,NULL,63,'2024-12-27 15:28:08','in_sample','Muestra_Desarrollo.txt','Error');
INSERT INTO model_execution_temp VALUES(61,NULL,63,'2024-12-27 15:30:49','in_sample','Muestra_Desarrollo.txt','Exito');
INSERT INTO model_execution_temp VALUES(62,68,NULL,'2024-12-27 16:53:47','of_sample','Modeling_App.db','Exito');
INSERT INTO model_execution_temp VALUES(63,68,NULL,'2024-12-30 10:02:56','produccion','Modeling_App.db','Exito');
INSERT INTO model_execution_temp VALUES(64,68,NULL,'2024-12-30 10:13:32','produccion','Modeling_App.db','Exito');
INSERT INTO model_execution_temp VALUES(65,NULL,63,'2024-12-30 10:49:57','in_sample','Muestra_Desarrollo.txt','Exito');
INSERT INTO model_execution_temp VALUES(67,NULL,63,'2025-01-02 13:44:33','in_sample','Muestra_Desarrollo.txt','Exito');
INSERT INTO model_execution_temp VALUES(68,68,NULL,'2025-01-06 09:43:00','produccion','Modeling_App.db','Error');
INSERT INTO model_execution_temp VALUES(69,68,NULL,'2025-01-06 10:38:32','of_sample','Modeling_App.db','Error');
INSERT INTO model_execution_temp VALUES(70,68,NULL,'2025-01-06 10:41:51','of_sample','Modeling_App.db','Error');
INSERT INTO model_execution_temp VALUES(71,68,NULL,'2025-01-06 10:50:19','of_sample','Modeling_App.db','Error');
INSERT INTO model_execution_temp VALUES(72,68,NULL,'2025-01-06 10:51:31','of_sample','Modeling_App.db','Error');
INSERT INTO model_execution_temp VALUES(73,68,NULL,'2025-01-06 10:52:06','of_sample','Modeling_App.db','Error');
INSERT INTO model_execution_temp VALUES(74,68,NULL,'2025-01-06 10:53:03','of_sample','Modeling_App.db','Error');
INSERT INTO model_execution_temp VALUES(75,68,NULL,'2025-01-06 10:53:54','of_sample','Modeling_App.db','Error');
INSERT INTO model_execution_temp VALUES(76,68,NULL,'2025-01-06 11:01:01','of_sample','Modeling_App.db','Exito');
INSERT INTO model_execution_temp VALUES(77,73,NULL,'2025-01-06 12:14:46','of_sample','Modeling_App.db','Error');
INSERT INTO model_execution_temp VALUES(78,73,NULL,'2025-01-06 12:22:56','of_sample','Modeling_App.db','Error');
INSERT INTO model_execution_temp VALUES(79,74,NULL,'2025-01-06 12:57:52','of_sample','Modeling_App.db','Error');
INSERT INTO model_execution_temp VALUES(80,74,NULL,'2025-01-06 14:41:45','desarollo','Modeling_App.db','Error');
INSERT INTO model_execution_temp VALUES(81,74,NULL,'2025-01-06 14:44:22','desarollo','Modeling_App.db','Error');
INSERT INTO model_execution_temp VALUES(82,74,NULL,'2025-01-06 14:46:24','desarollo','Modeling_App.db','Error');
INSERT INTO model_execution_temp VALUES(83,74,NULL,'2025-01-06 14:48:22','desarollo','Modeling_App.db','Error');
INSERT INTO model_execution_temp VALUES(84,74,NULL,'2025-01-06 14:52:12','desarollo','Modeling_App.db','Error');
INSERT INTO model_execution_temp VALUES(85,74,NULL,'2025-01-06 15:04:39','desarollo','Modeling_App.db','Exito');
INSERT INTO model_execution_temp VALUES(86,NULL,'','2025-01-06 15:39:43','in_sample','Muestra_Desarrollo.txt','Error');
INSERT INTO model_execution_temp VALUES(87,NULL,64,'2025-01-06 15:50:58','in_sample','Muestra_Desarrollo.txt','Exito');
INSERT INTO model_execution_temp VALUES(88,NULL,'','2025-01-06 15:59:25','in_sample','Muestra_Desarrollo.txt','Error');
INSERT INTO model_execution_temp VALUES(89,77,NULL,'2025-01-07 14:31:06','desarollo','Modeling_App.db','Error');
INSERT INTO model_execution_temp VALUES(90,77,NULL,'2025-01-07 14:34:17','desarollo','Modeling_App.db','Exito');
INSERT INTO model_execution_temp VALUES(91,77,NULL,'2025-01-07 14:58:30','desarollo','Modeling_App.db','Exito');
INSERT INTO model_execution_temp VALUES(92,77,NULL,'2025-01-07 15:06:38','desarollo','Modeling_App.db','Exito');
INSERT INTO model_execution_temp VALUES(93,77,NULL,'2025-01-07 15:10:02','desarollo','Modeling_App.db','Exito');
INSERT INTO model_execution_temp VALUES(94,77,NULL,'2025-01-07 15:13:08','desarollo','Modeling_App.db','Exito');
INSERT INTO model_execution_temp VALUES(95,69,NULL,'2025-01-08 16:41:53','desarollo','Modeling_App.db','Exito');
INSERT INTO model_execution_temp VALUES(96,NULL,66,'2025-01-10 14:02:46','in_sample','Muestra_Desarrollo.txt','Error');
CREATE TABLE user_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT, -- Nueva clave primaria
            hash_user_id VARCHAR(255) NOT NULL, -- ID único del usuario
            mail_user TEXT, -- Email del usuario
            UNIQUE(hash_user_id) -- Índice único en 'hash_user_id'
        );
INSERT INTO user_info VALUES(2,'auth0_670d225413861ad9fa6849d3','gloria2002@gmail.com.ar');
CREATE TABLE user_configurations (
            user_id INTEGER PRIMARY KEY, -- Clave primaria y referencia a user_info
            valor_min_seg INTEGER NOT NULL,
            valor_max_seg INTEGER NOT NULL,
            num_select_filas INTEGER NOT NULL,
            value_dark_or_light TEXT, -- Columna adicional
            FOREIGN KEY (user_id) REFERENCES user_info(id)
        );
INSERT INTO user_configurations VALUES(2,4,8,5,'light');
CREATE TABLE IF NOT EXISTS "name_files" (
                id_files INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_archivo TEXT NOT NULL,
                fecha_de_carga TEXT NOT NULL,
                project_id INTEGER,
                is_last_selected BOOLEAN DEFAULT 0,
                FOREIGN KEY (project_id) REFERENCES project(id)
            );
INSERT INTO name_files VALUES(6,'Muestra_Desarrollo.txt','2024-12-16 14:57',57,0);
INSERT INTO name_files VALUES(7,'Muestra_Scoring.txt','2024-12-17 10:08',57,0);
INSERT INTO name_files VALUES(11,'set_Cliente_Conocido.txt','2024-12-17 13:24',57,0);
INSERT INTO name_files VALUES(27,'Muestra_Desarrollo.txt','2024-12-27 14:42',57,0);
INSERT INTO name_files VALUES(30,'Muestra_Desarrollo.txt','2025-01-06 14:18',NULL,0);
INSERT INTO name_files VALUES(31,'Muestra_Desarrollo.txt','2025-01-06 16:30',NULL,0);
INSERT INTO name_files VALUES(32,'Muestra_Desarrollo.txt','2025-01-06 17:27',NULL,0);
INSERT INTO name_files VALUES(36,'Muestra_Desarrollo.txt','2025-01-08 09:14',67,0);
INSERT INTO name_files VALUES(38,'Muestra_Desarrollo.txt','2025-01-13 11:44',NULL,0);
INSERT INTO name_files VALUES(39,'Muestra_Desarrollo.txt','2025-01-13 11:45',NULL,0);
INSERT INTO name_files VALUES(40,'Muestra_Desarrollo.txt','2025-01-13 11:46',NULL,0);
INSERT INTO name_files VALUES(41,'Muestra_Desarrollo.txt','2025-01-13 11:51',NULL,0);
INSERT INTO name_files VALUES(42,'Muestra_Desarrollo.txt','2025-01-13 11:52',NULL,0);
INSERT INTO name_files VALUES(43,'Muestra_Desarrollo.txt','2025-01-13 11:56',NULL,0);
INSERT INTO name_files VALUES(44,'Muestra_Desarrollo.txt','2025-01-13 11:58',NULL,0);
INSERT INTO name_files VALUES(45,'Muestra_Desarrollo.txt','2025-01-13 11:59',NULL,0);
INSERT INTO name_files VALUES(48,'Muestra_Desarrollo.txt','2025-01-13 12:09',NULL,0);
INSERT INTO name_files VALUES(49,'Muestra_Desarrollo.txt','2025-01-13 12:32',81,0);
INSERT INTO name_files VALUES(50,'Muestra_Desarrollo.txt','2025-01-14 10:53',82,0);
INSERT INTO name_files VALUES(55,'Muestra_Desarrollo1.txt','2025-01-15 14:06',83,0);
INSERT INTO name_files VALUES(56,'Muestra_Desarrollo1.txt','2025-01-16 14:52',67,0);
INSERT INTO name_files VALUES(57,'Muestra_Desarrollo.txt','2025-01-16 15:15',84,0);
INSERT INTO name_files VALUES(58,'Muestra_Desarrollo1.txt','2025-01-16 16:39',84,1);
INSERT INTO name_files VALUES(59,'Muestra_Desarrollo3.txt','2025-01-21 16:50',84,0);
INSERT INTO name_files VALUES(60,'Muestra_Desarrollo4.txt','2025-01-21 16:54',84,0);
CREATE TABLE name_files_new (
                id_files INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_archivo TEXT NOT NULL,
                fecha_de_carga TEXT NOT NULL,
                project_id INTEGER,
                is_last_selected BOOLEAN DEFAULT 0,
                FOREIGN KEY (project_id) REFERENCES project(id)
            );
CREATE TABLE IF NOT EXISTS "old_validation_scoring2" (
                id_validacion_sc INTEGER PRIMARY KEY,
                nombre_archivo_validation_sc TEXT NOT NULL,
                fecha_de_carga TEXT NOT NULL,
                json_versiones_id INTEGER NOT NULL,
                FOREIGN KEY (json_versiones_id) REFERENCES json_versions(id_jsons) ON DELETE CASCADE
            );
CREATE TABLE validation_scoring (
                id_validacion_sc INTEGER PRIMARY KEY,
                nombre_archivo_validation_sc TEXT NOT NULL,
                fecha_de_carga TEXT NOT NULL,
                json_versiones_id INTEGER NOT NULL, ultima_vez_usado TEXT, nombre_modelo TEXT DEFAULT 'validacion',
                FOREIGN KEY (json_versiones_id) REFERENCES json_versions(id_jsons) ON DELETE CASCADE
            );
INSERT INTO validation_scoring VALUES(1,'Muestra_Scoring15.txt','2025-01-22 17:48',81,NULL,'validacion');
INSERT INTO validation_scoring VALUES(2,'Muestra_Validación12.txt','2025-01-23 12:18',81,NULL,'validacion');
INSERT INTO validation_scoring VALUES(3,'Muestra_Scoring15.txt','2025-01-23 12:20:15',80,'2025-01-23 12:20:15','produccion');
CREATE TABLE scoring (
                id_score INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_archivo_score TEXT NOT NULL,
                fecha_de_carga TEXT NOT NULL,
                json_versiones_id INTEGER NOT NULL,
                ultima_vez_usado TEXT,
                nombre_modelo TEXT DEFAULT 'validacion',
                FOREIGN KEY (json_versiones_id) REFERENCES json_versions(id_jsons) ON DELETE CASCADE
            );
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('project',84);
INSERT INTO sqlite_sequence VALUES('execution_log',84);
INSERT INTO sqlite_sequence VALUES('version',132);
INSERT INTO sqlite_sequence VALUES('json_versions',81);
INSERT INTO sqlite_sequence VALUES('model_execution_temp',96);
INSERT INTO sqlite_sequence VALUES('user_info',2);
INSERT INTO sqlite_sequence VALUES('name_files',60);
COMMIT;
