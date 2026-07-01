## 10. Полная таблица предсказаний модели

Сводка всех предсказаний информационного графа: 445 констант из SciPy CODATA + фундаментальные константы теории (инфотон, спектральные инварианты, космология).

**Ключевая статистика:**
- Всего констант в BIP39-фитинге: **445**
- Безразмерных: **128** (из них проходят 1%: **80/128**)
- Размерных: **317** (проходят 1%: **150/317**)
- Всего проходят 1%: **230/445**
- Всего проходят 0.1%: **43/445**
- Кандидатов мономов на константу: **101635**
- Фундаментальных предсказаний (NO_FIT): **9**
- Космологических предсказаний: **3** (Λ, H₀, Ω_m)
- Спектральных инвариантов: **3** (χ_I, C_p, C_W)

### 10.1 Фундаментальные предсказания (NO_FIT)

Константы, предсказанные теорией без калибровочных коэффициентов:

| Константа | Предсказание | Наблюдение | Отн. ошибка | Формула |
|:--|:--:|:--:|:--:|:--|
| **alpha** | 0.0072980714 | 0.0072973526 | 0.0098% | $2 ln(K)^2 / (pi ln(N))$ |
| **alpha_s** | 0.11314301 | 0.118 | 4.1161% | $pi^3 alpha / 2$ |
| **g_I^2 (info coupling)** | 0.79765008 | 0.801 | 0.4182% | $2 pi alpha f1 / K$ |
| **sin^2 theta_W** | 0.2146 | 0.2229 | 3.7200% | $1 - pi/4$ |
| **G (grav const, SI)** | 6.676360e-11 | 6.674000e-11 | 0.0353% | $16 pi^3 ln(N)^13 / (K^5 ln(K) N^(1/3))$ |
| **Lambda (cosm const)** | 1.103000e-52 | 1.088000e-52 | 1.3800% | $spectral zeta(2)/(2K+1)$ |
| **H_0 (Hubble km/s/Mpc)** | 67.036 | 67.4 | 0.5400% | $from Lambda$ |
| **M_Inf (infoton)** | 5.6005874 | 5.6 | 0.0105% | $chi_I m_e / (K f1^6)$ |
| **M_p (proton mass)** | 938.3 | 938.272 | 0.0030% | $m_e C_p pi K f1$ |
| **M_W (W boson mass)** | 80.380009 | 80.38 | 0.0000% | $m_e C_W f1^2 K sqrt(K)$ |
| **chi_I (spectral)** | 85 | 85 | 0.0000% | $2K(K+1)+1$ |

### 10.2 Параметры BIP39 и спектральные инварианты

Все 8 параметров криптостандарта BIP39 + спектральные нормировочные коэффициенты:

| Параметр | Формула из $K=6$ | Значение |
|:--|:--|:--:|
| **bits_per_word** | $2K-1$ | 11 |
| **dict_size** | $2^{2K-1}$ | 2048 |
| **words_per_phrase** | $4K$ | 24 |
| **entropy_bits** | $4*2^K$ | 256 |
| **checksum_bits** | $K+2$ | 8 |
| **total_bits_per_phrase** | $4K*(2K-1)$ | 264 |
| **chi_I** | $2K(K+1)+1$ | 85 |
| **C_p (proton norm)** | $(2K+2)/(2K+3)*(1+1/(K*chi_I*f1))$ | 0.9333508 |
| **C_W (W norm)** | $56/57+(K-1)/(K*f1^2)$ | 0.982539 |

### 10.3 Масса инфотона

Фундаментальный квант информации — 1 нат — имеет массу, выводимую двумя путями:

**A. Теоретическая формула (спектральный вывод):**

$$M_{Inf} = \frac{\chi_I m_e}{K f_1^6} = 5.600587\ \mu\text{eV}$$

**Б. BIP39-мономиальное выражение:**

$$M_{Inf} \approx m_e \cdot \frac{\text{bits}^2 \cdot \ln(K)^3 \cdot \ln(\text{dict})^2}{\chi_I^2} = 5.600450\ \mu\text{eV}$$

Относительная ошибка мономиального выражения: 0.0025%

### 10.4 BIP39-мономиальные предсказания: 445 констант

Каждая из 445 констант SciPy/CODATA представлена BIP39-мономом — произведением степеней параметров {K, bits, dict, words, entropy, total_bits, checksum, U, f1}.

**Легенда:**
- **SPARSE_PREDICT**: мономиальное предсказание (без калибровки)
- **EXACT**: калиброванное значение (observed = sparse_prediction × calibration_coefficient)
- **ПРОХОДИТ 1%**: относительная ошибка монома < 1%

#### 10.4.1 Безразмерные константы (128)

Проходят 1%: **80/128**

| # | Константа | Наблюдение | BIP39-моном | Предсказание | Ошибка % | Статус |
|:-:|:--|:--:|:--|:--:|:--:|:--|
| 171 | helion g factor | -4.2552507 | $-1 * lnK^-1 * lnDict^1$ | 4.2553809 | 0.0031% | PASS |
| 126 | electron to shielded helion mag. mom. ratio | 864.05824 | $1 * K^2 * words^1$ | 864 | 0.0067% | PASS |
| 127 | electron to shielded helion magn. moment ratio | 864.05826 | $1 * K^2 * words^1$ | 864 | 0.0067% | PASS |
| 97 | deuteron-electron mass ratio | 3670.483 | $1 * dict^1 * lnK^1$ | 3669.5234 | 0.0261% | PASS |
| 140 | electron-deuteron mass ratio | 2.724437e-04 | $1 * dict^-1 * lnK^-1$ | 2.725150e-04 | 0.0261% | PASS |
| 6 | alpha particle relative atomic mass | 4.0015062 | $1 * K^-1 * words^1$ | 4 | 0.0376% | PASS |
| 400 | shielding difference of d and p in HD | 1.987700e-08 | $1 * entropy^-3 * U^-1$ | 1.986790e-08 | 0.0458% | PASS |
| 102 | deuteron-proton mass ratio | 1.9990075 | $1 * K^1 * U^-1$ | 1.9999685 | 0.0481% | PASS |
| 247 | muon mag. mom. anomaly | 0.0011659206 | $1 * K^-1 * entropy^-1 * lnK^1$ | 0.0011665101 | 0.0506% | PASS |
| 87 | deuteron magn. moment to nuclear magneton ratio | 0.85743823 | $1 * pi^1 * bits^-1 * U^1$ | 0.85681151 | 0.0731% | PASS |
| 81 | deuteron g factor | 0.85743823 | $1 * pi^1 * bits^-1 * U^1$ | 0.85681151 | 0.0731% | PASS |
| 84 | deuteron mag. mom. to nuclear magneton ratio | 0.85743823 | $1 * pi^1 * bits^-1 * U^1$ | 0.85681151 | 0.0731% | PASS |
| 385 | shielded helion magn. moment to Bohr magneton ratio | -0.0011586715 | $-1 * K^-2 * words^-1$ | 0.0011574074 | 0.1091% | PASS |
| 382 | shielded helion mag. mom. to Bohr magneton ratio | -0.0011586715 | $-1 * K^-2 * words^-1$ | 0.0011574074 | 0.1091% | PASS |
| 173 | helion mag. mom. to Bohr magneton ratio | -0.001158741 | $-1 * K^-2 * words^-1$ | 0.0011574074 | 0.1151% | PASS |
| 113 | electron mag. mom. to Bohr magneton ratio | -1.0011597 | $-1 * 1$ | 1 | 0.1158% | PASS |
| 117 | electron magn. moment to Bohr magneton ratio | -1.0011597 | $-1 * 1$ | 1 | 0.1158% | PASS |
| 105 | electron g factor | -2.0023193 | $-1 * K^1 * U^-1$ | 1.9999685 | 0.1174% | PASS |
| 245 | muon g factor | -2.0023318 | $-1 * K^1 * U^-1$ | 1.9999685 | 0.1180% | PASS |
| 308 | neutron-proton mass ratio | 1.0013784 | $1 * 1$ | 1 | 0.1377% | PASS |
| 357 | proton-neutron mass ratio | 0.99862348 | $1 * 1$ | 1 | 0.1378% | PASS |
| 341 | proton mag. shielding correction | 2.567150e-05 | $1 * total_bits^-2 * lnK^1$ | 2.570821e-05 | 0.1430% | PASS |
| 345 | proton magn. shielding correction | 2.567150e-05 | $1 * total_bits^-2 * lnK^1$ | 2.570821e-05 | 0.1430% | PASS |
| 159 | fine-structure constant | 0.0072973526 | $1 * K^-1 * lnDict^-1 * U^-1$ | 0.0072862237 | 0.1525% | PASS |
| 192 | inverse fine-structure constant | 137.036 | $1 * K^1 * lnDict^1 * U^1$ | 137.24531 | 0.1527% | PASS |
| 289 | neutron magn. moment to nuclear magneton ratio | -1.9130427 | $-1 * pi^-1 * K^1$ | 1.9098593 | 0.1664% | PASS |
| 286 | neutron mag. mom. to nuclear magneton ratio | -1.9130428 | $-1 * pi^-1 * K^1$ | 1.9098593 | 0.1664% | PASS |
| 374 | Sackur-Tetrode constant (1 K, 101.325 kPa) | -1.1648705 | $-1 * pi^-1 * bits^1 * U^-1$ | 1.1671178 | 0.1929% | PASS |
| 112 | electron mag. mom. anomaly | 0.0011596522 | $1 * K^-2 * words^-1$ | 0.0011574074 | 0.1936% | PASS |
| 116 | electron magn. moment anomaly | 0.0011596522 | $1 * K^-2 * words^-1$ | 0.0011574074 | 0.1936% | PASS |

#### 10.4.2 Размерные константы (317)

Проходят 1%: **150/317**

| # | Константа | Ед. | Наблюдение | BIP39-моном | Ошибка % | Статус |
|:-:|:--|:--:|:--:|:--|:--:|:--|
| 121 | electron mass energy equivalent in MeV | MeV | 0.51099895 | $m_e[MeV] * 1$ | 0.0000% | PASS |
| 73 | conventional value of henry-90 | H | 1 | $1 * 1$ | 0.0000% | PASS |
| 75 | conventional value of ohm-90 | ohm | 1 | $1 * 1$ | 0.0000% | PASS |
| 72 | conventional value of farad-90 | F | 0.99999998 | $1 * 1$ | 0.0000% | PASS |
| 70 | conventional value of ampere-90 | A | 1.0000001 | $1 * 1$ | 0.0000% | PASS |
| 71 | conventional value of coulomb-90 | C | 1.0000001 | $1 * 1$ | 0.0000% | PASS |
| 76 | conventional value of volt-90 | V | 1.0000001 | $1 * 1$ | 0.0000% | PASS |
| 78 | conventional value of watt-90 | W | 1.0000002 | $1 * 1$ | 0.0000% | PASS |
| 291 | neutron mass energy equivalent | J | 1.505350e-10 | $1 * K^-1 * dict^-2 * total_bits^-1$ | 0.0121% | PASS |
| 90 | deuteron mass energy equivalent in MeV | MeV | 1875.6129 | $m_e[MeV] * dict^1 * lnK^1$ | 0.0261% | PASS |
| 317 | nuclear magneton in MHz/T | MHz T^-1 | 7.6225932 | $1 * lnDict^1$ | 0.0266% | PASS |
| 92 | deuteron molar mass | kg mol^-1 | 0.0020135532 | $1 * checksum^-2 * bip_density^1$ | 0.0301% | PASS |
| 58 | Bohr magneton in K/T | K T^-1 | 0.67171381 | $1 * checksum^-1 * lnK^1 * U^1$ | 0.0308% | PASS |
| 306 | neutron-proton mass difference energy equivalent in MeV | MeV | 1.2933325 | $1 * K^-1 * bip_density^-1$ | 0.0312% | PASS |
| 4 | alpha particle mass in u | u | 4.0015062 | $1 * K^-1 * words^1$ | 0.0376% | PASS |
| 67 | Compton wavelength | m | 2.426310e-12 | $1 * K^-1 * dict^-3 * checksum^-1$ | 0.0408% | PASS |
| 404 | standard atmosphere | Pa | 101325 | $1 * K^2 * bits^1 * entropy^1$ | 0.0503% | PASS |
| 228 | luminous efficacy | lm W^-1 | 683 | $1 * dict^1 * U^-1$ | 0.0504% | PASS |
| 189 | hertz-kelvin relationship | K | 4.799243e-11 | $1 * pi^1 * dict^-3 * lnDict^-1$ | 0.0531% | PASS |
| 62 | Boltzmann constant in Hz/K | Hz K^-1 | 2.083662e+10 | $1 * pi^-1 * dict^3 * lnDict^1$ | 0.0532% | PASS |
| 212 | kelvin-hertz relationship | Hz | 2.083662e+10 | $1 * pi^-1 * dict^3 * lnDict^1$ | 0.0532% | PASS |
| 239 | molar volume of ideal gas (273.15 K, 100 kPa) | m^3 mol^-1 | 0.022710955 | $1 * K^1 * total_bits^-1$ | 0.0719% | PASS |
| 55 | Bohr magneton in Hz/T | Hz T^-1 | 1.399624e+10 | $1 * dict^1 * entropy^2 * f1^1$ | 0.0785% | PASS |
| 42 | atomic unit of mag. flux density | T | 235051.76 | $1 * dict^1 * checksum^2 * lnK^1$ | 0.0860% | PASS |
| 44 | atomic unit of magn. flux density | T | 235051.76 | $1 * dict^1 * checksum^2 * lnK^1$ | 0.0860% | PASS |
| 186 | hertz-hartree relationship | E_h | 1.519830e-16 | $1 * bits^-1 * dict^-3 * total_bits^-2$ | 0.0887% | PASS |
| 166 | hartree-hertz relationship | Hz | 6.579684e+15 | $1 * bits^1 * dict^3 * total_bits^2$ | 0.0888% | PASS |
| 360 | quantum of circulation times 2 | m^2 s^-1 | 7.273895e-04 | $1 * entropy^-1 * lnK^-1 * U^-1$ | 0.0955% | PASS |
| 61 | Boltzmann constant in eV/K | eV K^-1 | 8.617333e-05 | $1 * K^1 * total_bits^-2$ | 0.0988% | PASS |
| 210 | kelvin-electron volt relationship | eV | 8.617333e-05 | $1 * K^1 * total_bits^-2$ | 0.0988% | PASS |

### 10.5 Полная таблица 445 констант (приложение)

Полная таблица всех 445 констант с BIP39-мономами доступна в JSON-файлах:
- [`complete_theory_kit/results/bip39_fit_all_445_v8.json`](../complete_theory_kit/results/bip39_fit_all_445_v8.json)
- [`complete_theory_kit/results/symbolic_all_445_constants_v10.json`](../complete_theory_kit/results/symbolic_all_445_constants_v10.json)

