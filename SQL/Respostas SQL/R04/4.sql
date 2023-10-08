-- Quantidade de Homicídios dolosos por data e município.
-- Ordenado por ano
SELECT rank()
    OVER(ORDER BY ano) AS Rank, 
    ano AS Ano,
    sum(hom_doloso) AS Qtd_Homicidio_Doloso, 
    printf('%.2f', percent_rank()
    OVER(ORDER BY ano)) AS '(%)Percent_Acum'
    FROM data
    GROUP BY ano
