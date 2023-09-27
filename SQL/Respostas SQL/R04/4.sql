-- Quantidade de Homicídios dolosos por data e município.

SELECT rank()
    OVER(ORDER BY sum(hom_doloso) DESC) AS Rank,
    fmun AS Municipio, 
    sum(hom_doloso) as Qtd_Homicidio_Doloso, 
    printf('%.4f', percent_rank()
    OVER(ORDER BY sum(hom_doloso) DESC)) AS '%Percent_Acum'
    FROM data
    GROUP BY fmun
    LIMIT 10