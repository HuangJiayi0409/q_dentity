# FQI-SRC-GR2-11.6.6-p0 · 多底数有限双边求和

家族：A · 超几何型有限求和；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\sum_{k=-m}^n\frac{(1-ad(rst/q)^k)(1-br^k/(dq^k))(1-cs^k/(dq^k))(1-adt^k/(bcq^k))}{(1-ad)(1-b/d)(1-c/d)(1-ad/(bc))}\frac{(a;rst/q^2)_k(b;r)_k(c;s)_k(ad^2/(bc);t)_kq^k}{(dq;q)_k(adst/(bq);st/q)_k(adrt/(cq);rt/q)_k(bcrs/(dq);rs/q)_k}=\frac{(1-a)(1-b)(1-c)(1-ad^2/(bc))}{d(1-ad)(1-b/d)(1-c/d)(1-ad/(bc))}\left[\frac{(arst/q^2;rst/q^2)_n(br;r)_n(cs;s)_n(ad^2t/(bc);t)_n}{(dq;q)_n(adst/(bq);st/q)_n(adrt/(cq);rt/q)_n(bcrs/(dq);rs/q)_n}-\frac{(c/(ad);rt/q)_{m+1}(d/(bc);rs/q)_{m+1}(1/d;q)_{m+1}(b/(ad);st/q)_{m+1}}{(1/c;s)_{m+1}(bc/(ad^2);t)_{m+1}(1/a;rst/q^2)_{m+1}(1/b;r)_{m+1}}\right].
$$

代表来源：`GR2-11.6.6-p0`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-11.6.6-p0**（GR；Chapter 11, 11.6.6-p0, 印刷p326）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。m,n≥0；abcdqrst非零，负指标用有限倒积。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
