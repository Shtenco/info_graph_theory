# CAS-верификация TeX-формул README

Статус: `PASS_CAS_RECOGNIZED_FORMULAS`

## Сводка

- CAS-проверок: `51`
- Пройдено: `51`
- Ошибок: `0`
- Display-формул найдено: `128`
- Inline-формул найдено: `1148`
- Всего TeX-фрагментов: `1276`
- Распознанных упоминаний формульных семейств: `1276`
- Нераспознанных TeX-фрагментов: `0`

## Проверки

| Группа | Проверка | Статус | Деталь |
|:--|:--|:--|:--|
| structural | f2*f5=K | PASS | `simplify -> 0` |
| infoton | chi_I(K=6)=85 | PASS | `simplify -> 0` |
| bip39 | bits_per_word=2K-1 at K=6 | PASS | `simplify -> 0` |
| bip39 | dictionary_size=2^(2K-1) at K=6 | PASS | `simplify -> 0` |
| bip39 | words_per_phrase=4K at K=6 | PASS | `simplify -> 0` |
| bip39 | sha256_entropy=4*2^K at K=6 | PASS | `simplify -> 0` |
| bip39 | checksum=K+2 at K=6 | PASS | `simplify -> 0` |
| bip39 | phrase_bits=4K(2K-1) at K=6 | PASS | `simplify -> 0` |
| 11d | Deff=2K-1=11 at K=6 | PASS | `simplify -> 0` |
| 11d | 2^Deff=2^11=2048 at K=6 | PASS | `simplify -> 0` |
| 11d | Deff=D_Mtheory | PASS | `simplify -> 0` |
| t13 | chi_I = (D-C)/W at K=6 | PASS | `simplify -> 0` |
| t13 | D = chi*W + C at K=6 | PASS | `simplify -> 0` |
| t13 | E = D/C at K=6 | PASS | `simplify -> 0` |
| convergence | ratio_limit | PASS | `lim a_(n+1)/a_n = exp(-sigma), < 1 for sigma>0` |
| lenr | barrier_factor_positive | PASS | `exp(-S_G)>0 for real S_G: exp(-S_G)` |
| lenr | barrier_suppression | PASS | `for S_G>0, exp(-S_G)<1, therefore 0<B_eff<B0` |
| graph | tr(L)=K*N | PASS | `simplify -> 0 (identity for K-regular graph)` |
| spectral | chi_I_numeric | PASS | `85 matches 85` |
| spectral | Cp_spectral | PASS | `0.933350867734 matches 0.933350796` |
| spectral | Cw_spectral | PASS | `0.982532641399 matches 0.982539` |
| spectral | Cn_minus_Cp_near_eta_D | PASS | `0.001293143 matches 0.00128` |
| structural | U | PASS | `3.00004731619564 matches 3.00004731619564` |
| structural | f1_formula | PASS | `104.198258823183 matches 104.198258823183` |
| structural | f3 | PASS | `5.36807227969222e-21 matches 5.36807227969222e-21` |
| structural | f4 | PASS | `2.08216211714244e+41 matches 2.08216211714244e+41` |
| structural | f5 | PASS | `3.34866375930748 matches 3.34866375930748` |
| structural | f1_working_in_range | PASS | `104.37 matches 104` |
| structural | f6_approx_1 | PASS | `1 matches 1` |
| structural | f2=lnK | PASS | `1.79175946922805 matches 1.79175946922805` |
| structural | Kp_appx_Nneg1_3 | PASS | `2.88162e-41 matches 2.87738055568357e-41` |
| structural | f3_sq_eq_Kp | PASS | `2.88162e-41 matches 2.88162e-41` |
| structural | f4_eq_1_over_p | PASS | `2.08216211714244e+41 matches 2.08216211714244e+41` |
| structural | f5_eq_K_over_lnK | PASS | `3.34866375930748 matches 3.34866375930748` |
| structural | f2_times_f5_eq_K | PASS | `6 matches 6` |
| bip39 | 2^K_states | PASS | `64.0 matches 64` |
| bip39 | 4_times_2K | PASS | `256.0 matches 256` |
| bip39 | K_plus_2 | PASS | `8.0 matches 8` |
| bip39 | words_per_phrase_num | PASS | `24.0 matches 24` |
| bip39 | checksum_bits | PASS | `8.0 matches 8` |
| bip39 | bits_per_word_num | PASS | `11.0 matches 11` |
| ew | sin2_theta_W_0 | PASS | `1-pi/4 = 0.214602` |
| infoton | bip39_monomial_micro_eV | PASS | `M_Inf(BIP39)=5.600450 matches 5.600587 (theoretical M_Inf) with error 0.0025%` |
| structural | f1_working_near_formula | PASS | `working=104.370000, formula=104.198259, diff=0.171741` |
| constants | alpha | PASS | `0.00729807144137314 matches 0.00729807144137314` |
| constants | alpha_s | PASS | `0.113143011171905 matches 0.113143011171905` |
| constants | g_I^2 | PASS | `0.797650077694323 matches 0.797650077694323` |
| mass | infoton_micro_eV | PASS | `5.60058744215342 matches 5.60058744215342` |
| mass | proton_MeV | PASS | `938.300000353144 matches 938.300000353144` |
| mass | W_GeV | PASS | `80.3800085651086 matches 80.3800085651086` |
| mass | neutron_MeV_formula | PASS | `939.60000039874 matches 939.6` |

## Нераспознанные примеры

Это не ошибки. Это формулы, которые требуют расширения TeX->SymPy парсера или ручной спецификации.


## Граница CAS-слоя

CAS-слой доказывает распознанные алгебраические и численные формулы. Он не доказывает физическую истинность модели и не интерпретирует произвольный TeX/русский текст без формальной спецификации.
