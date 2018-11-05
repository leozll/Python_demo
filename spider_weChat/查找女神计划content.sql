
 delete from Sheet2content
 
 insert INTO Sheet2content
SELECT DISTINCT 
a.snsid,c.content,c.urlcontent,c.medialist
 FROM [dbo].[Sheet2$] a
INNER JOIN MobileMomentSpider c
ON a.snsid=substring(c.snsid,2,20)

 insert INTO Sheet2content
SELECT DISTINCT 
a.snsid,c.content,c.urlcontent,c.medialist
 FROM [dbo].[Sheet2$] a
INNER JOIN MobileMomentSpidercs c
ON a.snsid=substring(c.snsid,2,20)


 insert INTO Sheet2content
SELECT substring(a.snsid,2,20) AS snsid,a.content,'' AS urlcontent,a.medialist AS medialist
FROM MobileMomentcs a WHERE EXISTS 
(SELECT 1 FROM 
(SELECT snsid FROM [Sheet2$] a WHERE NOT EXISTS 
(SELECT 1 FROM Sheet2content b WHERE b.snsid=a.snsid)) b
where b.snsid=substring(a.snsid,2,20)
)


