# SQL

Note: l'extrait des données donne des valeurs de l'année 2020 mais les
questions parlent de filtrer sur l'année 2019.

Il y a également une typo sur `prop_id` (à la place de `prod_id`).

## Première partie du test

```
SELECT
  date AS date,
  SUM(prod_price * prod_qty) AS ventes
FROM
  `my_dataset.TRANSACTION`
WHERE
  date BETWEEN DATE("2019-01-01") AND DATE("2019-12-31")
GROUP BY
  date
ORDER BY
  date ASC
```

## Seconde partie du test

```
WITH transaction_ventes AS (
  -- Filter before JOIN because it reduces the cost of the query in BigQuery (less data has to be shuffled)
  SELECT
    client_id AS client_id,
    prop_id AS prop_id,
    prod_price * prod_qty AS vente
  FROM
    `my_dataset.TRANSACTION`
  WHERE
    date BETWEEN DATE("2019-01-01") AND DATE("2019-12-31")
)
SELECT
  transaction_ventes.client_id AS client_id,
  SUM(IF(nomenclature.product_type = "MEUBLE", transaction_ventes.vente, 0)) AS ventes_meuble,
  SUM(IF(nomenclature.product_type = "DECO", transaction_ventes.vente, 0)) AS ventes_deco
FROM
  transaction_ventes
INNER JOIN
  `my_dataset.PRODUCT_NOMENCLATURE` AS nomenclature
ON
  transaction_ventes.prop_id = nomenclature.product_id
GROUP BY
  client_id
```
