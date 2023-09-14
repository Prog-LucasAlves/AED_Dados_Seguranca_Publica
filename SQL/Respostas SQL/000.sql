SELECT fmun, sum(hom_doloso), round(sum(hom_doloso) / 40.281 / 10, 5) FROM data
GROUP BY fmun
ORDER BY 2 DESC







