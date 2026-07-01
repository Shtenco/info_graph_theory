# SIGT Balanced Engine 445 v12

This is the controlled finite hypothesis-space engine scaled to all 445 constants.

## Hypothesis Space

```text
x
x^2
sqrt(abs(x))
log(abs(x)+eps)
exp(-abs(x))
x/(1+abs(x))
-x
1/x
sign(x)
```

## Summary

| Engine | Test pass <=1% | Median test rel error % | Avg abs error | Complexity penalty | Collapse penalty | Final score | Verdict |
|:--|--:|--:|--:|--:|--:|--:|:--|
| `LEAKY_VALUE_ENGINE` | 80/80 | `0` | `0` | `3.65` | `7.28` | `10.93` | `TRIVIAL_TARGET_LEAKAGE: identity hypothesis sees the answer` |
| `BIP39_PRIOR_ENGINE` | 46/80 | `0.847129739209` | `1.69549061207e+48` | `3.65` | `7.28` | `121.982056609` | `FAIL_BALANCED_TEST: finite hypothesis space does not predict held-out constants` |

## Interpretation

`LEAKY_VALUE_ENGINE` reproduces the target because x is the observed value.
`BIP39_PRIOR_ENGINE` uses the BIP39 sparse prior as x and is therefore the honest falsification mode.

## Worst BIP39 Prior Test Rows

| Constant | Unit | Model | Observed | Predicted | Rel error % |
|:--|:--|:--|--:|--:|--:|
| `atomic unit of 1st hyperpolarizablity` | `C^3 m^3 J^-2` | `x` | `3.20636151e-53` | `3.77119045999e-25` | `1.17615884804e+30` |
| `inverse meter-kilogram relationship` | `kg` | `x` | `2.2102190943e-42` | `3.77119045999e-25` | `1.70625186874e+19` |
| `natural unit of action` | `J s` | `x` | `1.05457181765e-34` | `3.77119045999e-25` | `357603948430` |
| `atomic unit of mass` | `kg` | `x` | `9.1093837139e-31` | `3.77119045999e-25` | `41398863.7327` |
| `electron mass` | `kg` | `x` | `9.1093837139e-31` | `3.77119045999e-25` | `41398863.7327` |
| `muon mass` | `kg` | `x` | `1.883531627e-28` | `3.77119045999e-25` | `200119.12061` |
| `unified atomic mass unit` | `kg` | `x` | `1.66053906892e-27` | `3.77119045999e-25` | `22610.639759` |
| `deuteron magn. moment` | `J T^-1` | `x` | `4.33073482e-27` | `3.77119045999e-25` | `8607.96900927` |
| `nuclear magneton` | `J T^-1` | `x` | `5.0507837393e-27` | `3.77119045999e-25` | `7366.54510398` |
| `shielded helion magn. moment` | `J T^-1` | `x` | `-1.074553024e-26` | `-3.77119045999e-25` | `3409.54338759` |
| `muon magn. moment` | `J T^-1` | `x` | `-4.49044799e-26` | `-3.77119045999e-25` | `739.824994831` |
| `kilogram-hertz relationship` | `Hz` | `x` | `1.35639248965e+50` | `2.65168256711e+24` | `100` |
| `joule-inverse meter relationship` | `m^-1` | `x` | `5.03411656754e+24` | `2.65168256711e+24` | `47.325761501` |
| `tau Compton wavelength over 2 pi` | `m` | `x` | `1.11056e-16` | `1.07088526894e-16` | `3.5724977547` |
| `electron volt-hertz relationship` | `Hz` | `x` | `2.41798924208e+14` | `2.36294844163e+14` | `2.2763046044` |
| `natural unit of energy in MeV` | `MeV` | `x` | `0.51099895069` | `0.500007886033` | `2.15089769608` |
| `natural unit of mom.um in MeV/c` | `MeV/c` | `x` | `0.5109989461` | `0.500007886033` | `2.15089681716` |
| `atomic unit of charge` | `C` | `x` | `1.602176634e-19` | `1.63609790577e-19` | `2.11719925551` |
| `proton rms charge radius` | `m` | `x` | `8.4075e-16` | `8.23225367205e-16` | `2.08440473323` |
| `muon mass energy equivalent` | `J` | `x` | `1.692833804e-11` | `1.72467143447e-11` | `1.8807298388` |
| `conductance quantum` | `S` | `x` | `7.74809172986e-05` | `7.89141414141e-05` | `1.84977690698` |
| `helion shielding shift` | `` | `x` | `5.9967029e-05` | `6.103515625e-05` | `1.78119087741` |
| `alpha particle-electron mass ratio` | `` | `x` | `7294.29954171` | `7170.88511595` | `1.69192977415` |
| `joule-hartree relationship` | `E_h` | `x` | `2.2937122784e+17` | `2.33228964569e+17` | `1.6818747344` |
| `atomic unit of energy` | `J` | `x` | `4.35974472221e-18` | `4.28763212086e-18` | `1.65405559132` |
| `shielded helion to proton magn. moment ratio` | `` | `x` | `-0.761766562` | `-0.7734375` | `1.53208851401` |
| `electron-deuteron magn. moment ratio` | `` | `x` | `-2143.923493` | `-2112` | `1.48902202454` |
| `electron-proton mass ratio` | `` | `x` | `0.000544617021489` | `0.00055262133018` | `1.46971328024` |
| `atomic unit of permittivity` | `F m^-1` | `x` | `1.1126500562e-10` | `1.12887584802e-10` | `1.45830144243` |
| `molar volume of ideal gas (273.15 K, 101.325 kPa)` | `m^3 mol^-1` | `x` | `0.022413969545` | `0.0227272727273` | `1.39780319425` |
| `Josephson constant` | `Hz V^-1` | `x` | `4.83597848417e+14` | `4.89832430174e+14` | `1.28920791886` |
| `Faraday constant` | `C mol^-1` | `x` | `96485.3321233` | `95325.0909091` | `1.20250528105` |
| `proton-neutron magn. moment ratio` | `` | `x` | `-1.45989805` | `-1.44269504089` | `1.17837057944` |
| `Wien displacement law constant` | `m K` | `x` | `0.0028977685` | `0.0029296875` | `1.1015027598` |
| `electron to shielded proton magn. moment ratio` | `` | `x` | `-658.2275956` | `-651.898646904` | `0.961513728367` |
| `electron to shielded proton mag. mom. ratio` | `` | `x` | `-658.2275856` | `-651.898646904` | `0.961512223744` |
| `neutron mass in u` | `u` | `x` | `1.00866491606` | `1` | `0.859048026955` |
| `atomic mass constant energy equivalent` | `J` | `x` | `1.49241808768e-10` | `1.50516779736e-10` | `0.854298790908` |
| `proton mag. mom. to Bohr magneton ratio` | `` | `x` | `0.0015210322023` | `0.00153398078789` | `0.851302527722` |
| `Bohr magneton in eV/T` | `eV T^-1` | `x` | `5.7883817982e-05` | `5.73921028466e-05` | `0.849486354726` |
| `neutron magn. moment to Bohr magneton ratio` | `` | `x` | `-0.00104187563` | `-0.0010330741447` | `0.844773123691` |
| `kelvin-hartree relationship` | `E_h` | `x` | `3.16681156346e-06` | `3.19353462153e-06` | `0.843847432664` |
| `nuclear magneton in eV/T` | `eV T^-1` | `x` | `3.15245125417e-08` | `3.12695728841e-08` | `0.808702933045` |
| `neutron-proton mass difference in u` | `u` | `x` | `0.00138844948` | `0.00137741046832` | `0.795060377742` |
| `proton g factor` | `` | `x` | `5.5856946893` | `5.62897838553` | `0.774902651047` |
| `Sackur-Tetrode constant (1 K, 100 kPa)` | `` | `x` | `-1.15170753496` | `-1.16019284641` | `0.736759219776` |
| `proton Compton wavelength over 2 pi` | `m` | `x` | `2.10308910109e-16` | `2.08791253851e-16` | `0.721631935461` |
| `tau molar mass` | `kg mol^-1` | `x` | `0.00190754` | `0.00189396926528` | `0.711425958301` |
| `lattice spacing of ideal Si (220)` | `m` | `x` | `1.920155716e-10` | `1.90674026531e-10` | `0.698664727163` |
| `shielded helion gyromag. ratio` | `s^-1 T^-1` | `x` | `203789460.78` | `202397184` | `0.683193711133` |
| `shielded helion gyromagn. ratio` | `s^-1 T^-1` | `x` | `203789460.78` | `202397184` | `0.683193711133` |
| `electron-triton mass ratio` | `` | `x` | `0.000181920006233` | `0.000183108356701` | `0.65322692831` |
| `electron-helion mass ratio` | `` | `x` | `0.000181954307465` | `0.000183108356701` | `0.634252221106` |
| `helion mass energy equivalent in MeV` | `MeV` | `x` | `2808.39161112` | `2790.69158773` | `0.630254816244` |
| `electron volt-inverse meter relationship` | `m^-1` | `x` | `806554.393735` | `811008` | `0.552176802913` |
| `atomic unit of electric field` | `V m^-1` | `x` | `514220675112` | `516942105988` | `0.529234044461` |
| `electron charge to mass quotient` | `C kg^-1` | `x` | `-175882000838` | `-174992710548` | `0.505617565297` |
| `inverse meter-kelvin relationship` | `K` | `x` | `0.014387768775` | `0.0143226907683` | `0.452314794622` |
| `shielded proton gyromag. ratio` | `s^-1 T^-1` | `x` | `267515319.4` | `268435456` | `0.343956601089` |
| `proton gyromagn. ratio` | `s^-1 T^-1` | `x` | `267522187.08` | `268435456` | `0.341380627143` |
| `reduced Planck constant times c in MeV fm` | `MeV fm` | `x` | `197.326980459` | `198` | `0.341068179897` |
| `electron volt-atomic mass unit relationship` | `u` | `x` | `1.07354410083e-09` | `1.07034154479e-09` | `0.298316206979` |
| `electron-muon magn. moment ratio` | `` | `x` | `206.7669894` | `207.345115137` | `0.279602531625` |
| `shielded proton gyromag. ratio in MHz/T` | `MHz T^-1` | `x` | `42.57638543` | `42.6666666667` | `0.212045329247` |
| `triton-proton mass ratio` | `` | `x` | `2.99371703403` | `3.0000473162` | `0.211452254628` |
| `muon Compton wavelength over 2 pi` | `m` | `x` | `1.867594308e-15` | `1.86381178404e-15` | `0.202534562567` |
| `reduced muon Compton wavelength` | `m` | `x` | `1.867594306e-15` | `1.86381178404e-15` | `0.202534455694` |
| `Hartree energy in eV` | `eV` | `x` | `27.211386246` | `27.162443621` | `0.179860829293` |
| `proton mag. shielding correction` | `` | `x` | `2.56715e-05` | `2.57082109336e-05` | `0.143002682345` |
| `proton-neutron mass ratio` | `` | `x` | `0.99862347797` | `1` | `0.137841945475` |
| `electron mag. mom.` | `J T^-1` | `x` | `-9.2847646917e-24` | `-9.2740100657e-24` | `0.115830894558` |
| `electron volt-kelvin relationship` | `K` | `x` | `11604.5181216` | `11616` | `0.0989431730784` |
| `hertz-hartree relationship` | `E_h` | `x` | `1.51982984606e-16` | `1.51848184619e-16` | `0.0886941308063` |
| `Boltzmann constant in Hz/K` | `Hz K^-1` | `x` | `20836619123.3` | `20847699113.8` | `0.0531755673231` |
| `shielding difference of d and p in HD` | `` | `x` | `1.9877e-08` | `1.98679015673e-08` | `0.0457736716255` |
| `alpha particle mass in u` | `u` | `x` | `4.00150617913` | `4` | `0.0376403049646` |
| `alpha particle relative atomic mass` | `` | `x` | `4.00150617913` | `4` | `0.0376403049646` |
| `Bohr magneton in K/T` | `K T^-1` | `x` | `0.67171381472` | `0.671920398366` | `0.0307547114847` |
| `electron to shielded helion magn. moment ratio` | `` | `x` | `864.058255` | `864` | `0.00674202227256` |
| `conventional value of coulomb-90` | `C` | `x` | `1.00000008887` | `1` | `8.88714298663e-06` |

## Scientific Status

The balanced engine is useful because it exposes leakage.
Perfect performance in leaky mode is not evidence.
The BIP39 prior mode is the actual predictive test.
