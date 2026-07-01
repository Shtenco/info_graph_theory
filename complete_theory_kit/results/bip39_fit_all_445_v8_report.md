# BIP39 Fit All 445 Constants v8

This report fits every SciPy/CODATA physical-constants entry with a signed BIP39 sparse monomial.
It includes negative constants by fitting the magnitude and restoring the sign.
Exact 445/445 agreement is obtained only by adding a target-specific calibration coefficient.

## Summary

| Metric | Value |
|:--|:--|
| `catalog_source` | `scipy.constants.physical_constants` |
| `catalog_total_constants` | `445` |
| `negative_constants_included` | `58` |
| `dimensionless_constants` | `128` |
| `dimensional_constants` | `317` |
| `candidate_monomials_per_constant` | `101635` |
| `sparse_fit_pass_1_percent` | `230/445` |
| `sparse_fit_pass_0_1_percent` | `43/445` |
| `sparse_fit_pass_1_percent_dimensionless` | `80/128` |
| `target_calibrated_exact_pass` | `445/445` |
| `mean_sparse_relative_error_percent` | `2.7182256022e+39` |
| `median_sparse_relative_error_percent` | `0.94642382576` |
| `max_sparse_relative_error_percent` | `6.04805236572e+41` |
| `mean_exact_calibration_deviation_percent` | `1.14948638973e+25` |
| `median_exact_calibration_deviation_percent` | `0.937550623283` |
| `scientific_verdict` | `ALL_445_FITTED_DIAGNOSTICALLY; EXACT_445_REQUIRES_TARGET_SPECIFIC_COEFFICIENTS` |

## Best Sparse Fits

| Constant | Unit | Value | Sparse predicted | Rel error % | Complexity | Formula |
|:--|:--|--:|--:|--:|--:|:--|
| `electron mass energy equivalent in MeV` | `MeV` | `0.51099895069` | `0.51099895069` | `0` | 0 | `sign(1) * m_e[MeV] * 1` |
| `conventional value of henry-90` | `H` | `1.00000001779` | `1` | `1.77936675559e-06` | 0 | `sign(1) * 1 * 1` |
| `conventional value of ohm-90` | `ohm` | `1.00000001779` | `1` | `1.77936675559e-06` | 0 | `sign(1) * 1 * 1` |
| `conventional value of farad-90` | `F` | `0.999999982206` | `1` | `1.7793667856e-06` | 0 | `sign(1) * 1 * 1` |
| `conventional value of ampere-90` | `A` | `1.00000008887` | `1` | `8.88714298663e-06` | 0 | `sign(1) * 1 * 1` |
| `conventional value of coulomb-90` | `C` | `1.00000008887` | `1` | `8.88714298663e-06` | 0 | `sign(1) * 1 * 1` |
| `conventional value of volt-90` | `V` | `1.00000010667` | `1` | `1.06665095814e-05` | 0 | `sign(1) * 1 * 1` |
| `conventional value of watt-90` | `W` | `1.00000019554` | `1` | `1.95536516047e-05` | 0 | `sign(1) * 1 * 1` |
| `helion g factor` | `` | `-4.2552506995` | `-4.25538087958` | `0.00305928108941` | 2 | `sign(-1) * 1 * lnK^-1 * lnDict^1` |
| `electron to shielded helion mag. mom. ratio` | `` | `864.05823986` | `864` | `0.00674027019399` | 3 | `sign(1) * 1 * K^2 * words^1` |
| `electron to shielded helion magn. moment ratio` | `` | `864.058255` | `864` | `0.00674202227256` | 3 | `sign(1) * 1 * K^2 * words^1` |
| `neutron mass energy equivalent` | `J` | `1.50534976514e-10` | `1.50516779736e-10` | `0.0120880732083` | 4 | `sign(1) * 1 * K^-1 * dict^-2 * total_bits^-1` |
| `deuteron-electron mass ratio` | `` | `3670.48296765` | `3669.52339298` | `0.0261430085468` | 2 | `sign(1) * 1 * dict^1 * lnK^1` |
| `deuteron mass energy equivalent in MeV` | `MeV` | `1875.612945` | `1875.12260334` | `0.0261430086949` | 2 | `sign(1) * m_e[MeV] * dict^1 * lnK^1` |
| `electron-deuteron mass ratio` | `` | `0.000272443710763` | `0.000272514954371` | `0.026149844908` | 2 | `sign(1) * 1 * dict^-1 * lnK^-1` |
| `nuclear magneton in MHz/T` | `MHz T^-1` | `7.6225932188` | `7.62461898616` | `0.0265758292651` | 1 | `sign(1) * 1 * lnDict^1` |
| `deuteron molar mass` | `kg mol^-1` | `0.00201355321466` | `0.00201416015625` | `0.0301428134892` | 3 | `sign(1) * 1 * checksum^-2 * bip_density^1` |
| `Bohr magneton in K/T` | `K T^-1` | `0.67171381472` | `0.671920398366` | `0.0307547114847` | 3 | `sign(1) * 1 * checksum^-1 * lnK^1 * U^1` |
| `neutron-proton mass difference energy equivalent in MeV` | `MeV` | `1.29333251` | `1.29292929293` | `0.031176597479` | 2 | `sign(1) * 1 * K^-1 * bip_density^-1` |
| `alpha particle mass in u` | `u` | `4.00150617913` | `4` | `0.0376403049646` | 2 | `sign(1) * 1 * K^-1 * words^1` |
| `alpha particle relative atomic mass` | `` | `4.00150617913` | `4` | `0.0376403049646` | 2 | `sign(1) * 1 * K^-1 * words^1` |
| `Compton wavelength` | `m` | `2.42631023538e-12` | `2.42531920473e-12` | `0.0408451746088` | 5 | `sign(1) * 1 * K^-1 * dict^-3 * checksum^-1` |
| `shielding difference of d and p in HD` | `` | `1.9877e-08` | `1.98679015673e-08` | `0.0457736716255` | 4 | `sign(1) * 1 * entropy^-3 * U^-1` |
| `deuteron-proton mass ratio` | `` | `1.99900750127` | `1.99996845637` | `0.048071610365` | 2 | `sign(1) * 1 * K^1 * U^-1` |
| `standard atmosphere` | `Pa` | `101325` | `101376` | `0.0503330866025` | 4 | `sign(1) * 1 * K^2 * bits^1 * entropy^1` |
| `luminous efficacy` | `lm W^-1` | `683` | `682.655899773` | `0.0503807066916` | 2 | `sign(1) * 1 * dict^1 * U^-1` |
| `muon mag. mom. anomaly` | `` | `0.00116592062` | `0.00116651007111` | `0.0505567104572` | 3 | `sign(1) * 1 * K^-1 * entropy^-1 * lnK^1` |
| `hertz-kelvin relationship` | `K` | `4.79924307337e-11` | `4.79669240497e-11` | `0.0531473059417` | 5 | `sign(1) * 1 * pi^1 * dict^-3 * lnDict^-1` |
| `Boltzmann constant in Hz/K` | `Hz K^-1` | `20836619123.3` | `20847699113.8` | `0.0531755673231` | 5 | `sign(1) * 1 * pi^-1 * dict^3 * lnDict^1` |
| `kelvin-hertz relationship` | `Hz` | `20836619123.3` | `20847699113.8` | `0.0531755673231` | 5 | `sign(1) * 1 * pi^-1 * dict^3 * lnDict^1` |
| `molar volume of ideal gas (273.15 K, 100 kPa)` | `m^3 mol^-1` | `0.0227109546415` | `0.0227272727273` | `0.0718511662973` | 2 | `sign(1) * 1 * K^1 * total_bits^-1` |
| `deuteron magn. moment to nuclear magneton ratio` | `` | `0.8574382329` | `0.856811509907` | `0.0730924944208` | 3 | `sign(1) * 1 * pi^1 * bits^-1 * U^1` |
| `deuteron g factor` | `` | `0.8574382335` | `0.856811509907` | `0.0730925643456` | 3 | `sign(1) * 1 * pi^1 * bits^-1 * U^1` |
| `deuteron mag. mom. to nuclear magneton ratio` | `` | `0.8574382335` | `0.856811509907` | `0.0730925643456` | 3 | `sign(1) * 1 * pi^1 * bits^-1 * U^1` |
| `Bohr magneton in Hz/T` | `Hz T^-1` | `13996244917.1` | `13985253560.8` | `0.0785307513656` | 4 | `sign(1) * 1 * dict^1 * entropy^2 * f1^1` |
| `atomic unit of mag. flux density` | `T` | `235051.757077` | `234849.497151` | `0.0860491020597` | 4 | `sign(1) * 1 * dict^1 * checksum^2 * lnK^1` |
| `atomic unit of magn. flux density` | `T` | `235051.757077` | `234849.497151` | `0.0860491020597` | 4 | `sign(1) * 1 * dict^1 * checksum^2 * lnK^1` |
| `hertz-hartree relationship` | `E_h` | `1.51982984606e-16` | `1.51848184619e-16` | `0.0886941308063` | 6 | `sign(1) * 1 * bits^-1 * dict^-3 * total_bits^-2` |
| `hartree-hertz relationship` | `Hz` | `6.5796839205e+15` | `6.58552489456e+15` | `0.088772867132` | 6 | `sign(1) * 1 * bits^1 * dict^3 * total_bits^2` |
| `quantum of circulation times 2` | `m^2 s^-1` | `0.00072738950934` | `0.000726695083506` | `0.0954682222837` | 3 | `sign(1) * 1 * entropy^-1 * lnK^-1 * U^-1` |
| `Boltzmann constant in eV/K` | `eV K^-1` | `8.61733326215e-05` | `8.608815427e-05` | `0.0988453723306` | 3 | `sign(1) * 1 * K^1 * total_bits^-2` |
| `kelvin-electron volt relationship` | `eV` | `8.61733326215e-05` | `8.608815427e-05` | `0.0988453723306` | 3 | `sign(1) * 1 * K^1 * total_bits^-2` |
| `electron volt-kelvin relationship` | `K` | `11604.5181216` | `11616` | `0.0989431730784` | 3 | `sign(1) * 1 * K^-1 * total_bits^2` |
| `nuclear magneton in K/T` | `K T^-1` | `0.00036582677706` | `0.0003662109375` | `0.105011569434` | 3 | `sign(1) * 1 * K^1 * dict^-1 * checksum^-1` |
| `electron molar mass` | `kg mol^-1` | `5.4857990962e-07` | `5.47988941771e-07` | `0.107726848729` | 5 | `sign(1) * 1 * entropy^-1 * total_bits^-1 * U^-3` |
| `shielded helion magn. moment to Bohr magneton ratio` | `` | `-0.001158671474` | `-0.00115740740741` | `0.109096203795` | 3 | `sign(-1) * 1 * K^-2 * words^-1` |
| `shielded helion mag. mom. to Bohr magneton ratio` | `` | `-0.00115867149457` | `-0.00115740740741` | `0.109097977168` | 3 | `sign(-1) * 1 * K^-2 * words^-1` |
| `shielded helion mag. mom.` | `J T^-1` | `-1.07455311035e-26` | `-1.07338079464e-26` | `0.109097977336` | 3 | `sign(-1) * mu_B[J/T] * K^-2 * words^-1` |
| `helion mag. mom. to Bohr magneton ratio` | `` | `-0.00115874098083` | `-0.00115740740741` | `0.115088138303` | 3 | `sign(-1) * 1 * K^-2 * words^-1` |
| `helion mag. mom.` | `J T^-1` | `-1.07461755198e-26` | `-1.07338079464e-26` | `0.115088138707` | 3 | `sign(-1) * mu_B[J/T] * K^-2 * words^-1` |
| `electron mag. mom. to Bohr magneton ratio` | `` | `-1.00115965218` | `-1` | `0.115830894497` | 0 | `sign(-1) * 1 * 1` |
| `electron mag. mom.` | `J T^-1` | `-9.2847646917e-24` | `-9.2740100657e-24` | `0.115830894558` | 0 | `sign(-1) * mu_B[J/T] * 1` |
| `electron magn. moment to Bohr magneton ratio` | `` | `-1.00115965219` | `-1` | `0.115830895039` | 0 | `sign(-1) * 1 * 1` |
| `electron g factor` | `` | `-2.00231930436` | `-1.99996845637` | `0.117406249279` | 2 | `sign(-1) * 1 * K^1 * U^-1` |
| `muon g factor` | `` | `-2.00233184123` | `-1.99996845637` | `0.118031627638` | 2 | `sign(-1) * 1 * K^1 * U^-1` |
| `atomic unit of current` | `A` | `0.00662361823751` | `0.00663145596216` | `0.118329957631` | 3 | `sign(1) * 1 * pi^-1 * K^-1 * checksum^-1` |
| `tau mass in u` | `u` | `1.90754` | `1.9098593171` | `0.121586813527` | 2 | `sign(1) * 1 * pi^-1 * K^1` |
| `proton mass energy equivalent` | `J` | `1.50327761802e-10` | `1.50516779736e-10` | `0.125737210193` | 4 | `sign(1) * 1 * K^-1 * dict^-2 * total_bits^-1` |
| `atomic mass unit-kelvin relationship` | `K` | `1.08095402067e+13` | `1.07952050727e+13` | `0.132615575835` | 7 | `sign(1) * 1 * bits^-1 * dict^3 * words^3` |
| `kelvin-atomic mass unit relationship` | `u` | `9.2510872884e-14` | `9.2633719625e-14` | `0.132791678633` | 7 | `sign(1) * 1 * bits^1 * dict^-3 * words^-3` |
| `deuteron mass energy equivalent` | `J` | `3.00506323491e-10` | `3.00096884893e-10` | `0.136249578014` | 4 | `sign(1) * 1 * dict^-2 * lnDict^-1 * f1^-1` |
| `neutron-proton mass ratio` | `` | `1.00137841946` | `1` | `0.137652203524` | 0 | `sign(1) * 1 * 1` |
| `proton-neutron mass ratio` | `` | `0.99862347797` | `1` | `0.137841945475` | 0 | `sign(1) * 1 * 1` |
| `proton mag. shielding correction` | `` | `2.56715e-05` | `2.57082109336e-05` | `0.143002682345` | 3 | `sign(1) * 1 * total_bits^-2 * lnK^1` |
| `proton magn. shielding correction` | `` | `2.56715e-05` | `2.57082109336e-05` | `0.143002682345` | 3 | `sign(1) * 1 * total_bits^-2 * lnK^1` |
| `fine-structure constant` | `` | `0.0072973525643` | `0.00728622367155` | `0.152505893727` | 3 | `sign(1) * 1 * K^-1 * lnDict^-1 * U^-1` |
| `inverse fine-structure constant` | `` | `137.035999177` | `137.245306359` | `0.152738829876` | 3 | `sign(1) * 1 * K^1 * lnDict^1 * U^1` |
| `elementary charge over h-bar` | `A J^-1` | `1.51926744788e+15` | `1.51684489985e+15` | `0.159455007653` | 7 | `sign(1) * 1 * dict^3 * total_bits^3 * f1^-1` |
| `natural unit of action in eV s` | `eV s` | `6.58211956951e-16` | `6.59263185113e-16` | `0.159709672724` | 7 | `sign(1) * 1 * dict^-3 * total_bits^-3 * f1^1` |
| `reduced Planck constant in eV s` | `eV s` | `6.58211956951e-16` | `6.59263185113e-16` | `0.159709672724` | 7 | `sign(1) * 1 * dict^-3 * total_bits^-3 * f1^1` |
| `Planck constant over 2 pi in eV s` | `eV s` | `6.582119514e-16` | `6.59263185113e-16` | `0.159710517402` | 7 | `sign(1) * 1 * dict^-3 * total_bits^-3 * f1^1` |
| `proton charge to mass quotient` | `C kg^-1` | `95788331.43` | `95941422.9069` | `0.1598226784` | 4 | `sign(1) * 1 * dict^2 * lnDict^1 * U^1` |
| `neutron magn. moment to nuclear magneton ratio` | `` | `-1.91304273` | `-1.9098593171` | `0.166405739262` | 2 | `sign(-1) * 1 * pi^-1 * K^1` |
| `neutron mag. mom. to nuclear magneton ratio` | `` | `-1.91304276` | `-1.9098593171` | `0.166407304835` | 2 | `sign(-1) * 1 * pi^-1 * K^1` |
| `molar volume of silicon` | `m^3 mol^-1` | `1.205883199e-05` | `1.20798329925e-05` | `0.174154532874` | 3 | `sign(1) * 1 * lnDict^-1 * f1^-2` |
| `helion mass energy equivalent` | `J` | `4.4995394185e-10` | `4.49161836704e-10` | `0.176041383941` | 5 | `sign(1) * 1 * bits^-2 * total_bits^-3` |
| `atomic unit of electric potential` | `V` | `27.211386246` | `27.162443621` | `0.179860829293` | 3 | `sign(1) * 1 * pi^-1 * bits^1 * bip_density^-1` |
| `Hartree energy in eV` | `eV` | `27.211386246` | `27.162443621` | `0.179860829293` | 3 | `sign(1) * 1 * pi^-1 * bits^1 * bip_density^-1` |
| `hartree-electron volt relationship` | `eV` | `27.211386246` | `27.162443621` | `0.179860829293` | 3 | `sign(1) * 1 * pi^-1 * bits^1 * bip_density^-1` |
| `electron volt-hartree relationship` | `E_h` | `0.0367493221757` | `0.0368155389093` | `0.180184911368` | 3 | `sign(1) * 1 * pi^1 * bits^-1 * bip_density^1` |

## Worst Sparse Fits

| Constant | Unit | Value | Sparse predicted | Rel error % | Complexity | Exact coefficient |
|:--|:--|--:|--:|--:|--:|--:|
| `atomic unit of 2nd hyperpolarizability` | `C^4 m^4 J^-3` | `6.2353799735e-65` | `3.77119045999e-25` | `6.04805236572e+41` | 9 | `1.6534248375e-40` |
| `atomic unit of 2nd hyperpolarizablity` | `C^4 m^4 J^-3` | `6.2353808e-65` | `3.77119045999e-25` | `6.04805156405e+41` | 9 | `1.65342505666e-40` |
| `atomic unit of 1st hyperpolarizability` | `C^3 m^3 J^-2` | `3.2063612996e-53` | `3.77119045999e-25` | `1.17615892522e+30` | 9 | `8.502252362e-29` |
| `atomic unit of 1st hyperpolarizablity` | `C^3 m^3 J^-2` | `3.20636151e-53` | `3.77119045999e-25` | `1.17615884804e+30` | 9 | `8.50225291991e-29` |
| `hertz-kilogram relationship` | `kg` | `7.37249732381e-51` | `3.77119045999e-25` | `5.11521441698e+27` | 9 | `1.95495226296e-26` |
| `Planck time` | `s` | `5.391247e-44` | `3.77119045999e-25` | `6.99502445351e+20` | 9 | `1.42958756849e-19` |
| `inverse meter-kilogram relationship` | `kg` | `2.2102190943e-42` | `3.77119045999e-25` | `1.70625186874e+19` | 9 | `5.86079944185e-18` |
| `atomic unit of electric polarizability` | `C^2 m^2 J^-1` | `1.64877727212e-41` | `3.77119045999e-25` | `2.28726494704e+18` | 9 | `4.37203394952e-17` |
| `atomic unit of electric polarizablity` | `C^2 m^2 J^-1` | `1.648777274e-41` | `3.77119045999e-25` | `2.28726494443e+18` | 9 | `4.37203395451e-17` |
| `kelvin-kilogram relationship` | `kg` | `1.53617918724e-40` | `3.77119045999e-25` | `2.45491573595e+17` | 9 | `4.07345957076e-16` |
| `atomic unit of electric quadrupole moment` | `C m^2` | `4.48655124e-40` | `3.77119045999e-25` | `8.40554416579e+16` | 9 | `1.18969097095e-15` |
| `atomic unit of electric quadrupole mom.` | `C m^2` | `4.4865515185e-40` | `3.77119045999e-25` | `8.40554364402e+16` | 9 | `1.1896910448e-15` |
| `Newtonian constant of gravitation over h-bar c` | `(GeV/c^2)^-2` | `6.70883e-39` | `3.77119045999e-25` | `5.62123419432e+15` | 9 | `1.77896875567e-14` |
| `electron volt-kilogram relationship` | `kg` | `1.78266192163e-36` | `3.77119045999e-25` | `2.1154827027e+13` | 9 | `4.72705354063e-12` |
| `Planck length` | `m` | `1.616255e-35` | `3.77119045999e-25` | `2.33328927665e+12` | 9 | `4.2857952075e-11` |
| `hartree-kilogram relationship` | `kg` | `4.85087020954e-35` | `3.77119045999e-25` | `777425553891` | 9 | `1.28629679699e-10` |
| `Planck constant over 2 pi` | `J s` | `1.0545718e-34` | `3.77119045999e-25` | `357603954414` | 9 | `2.79638965782e-10` |
| `atomic unit of action` | `J s` | `1.05457181765e-34` | `3.77119045999e-25` | `357603948430` | 9 | `2.79638970462e-10` |
| `natural unit of action` | `J s` | `1.05457181765e-34` | `3.77119045999e-25` | `357603948430` | 9 | `2.79638970462e-10` |
| `reduced Planck constant` | `J s` | `1.05457181765e-34` | `3.77119045999e-25` | `357603948430` | 9 | `2.79638970462e-10` |
| `hertz-joule relationship` | `J` | `6.62607015e-34` | `3.77119045999e-25` | `56914435977.8` | 9 | `1.75702347052e-09` |
| `Planck constant` | `J Hz^-1` | `6.62607015e-34` | `3.77119045999e-25` | `56914435977.8` | 9 | `1.75702347052e-09` |
| `atomic unit of mass` | `kg` | `9.1093837139e-31` | `3.77119045999e-25` | `41398863.7327` | 9 | `2.41551939912e-06` |
| `electron mass` | `kg` | `9.1093837139e-31` | `3.77119045999e-25` | `41398863.7327` | 9 | `2.41551939912e-06` |
| `natural unit of mass` | `kg` | `9.1093837139e-31` | `3.77119045999e-25` | `41398863.7327` | 9 | `2.41551939912e-06` |
| `neutron-proton mass difference` | `kg` | `2.30557461e-30` | `3.77119045999e-25` | `16356735.4875` | 9 | `6.1136520005e-06` |
| `atomic unit of electric dipole moment` | `C m` | `8.47835309e-30` | `3.77119045999e-25` | `4447922.41657` | 9 | `2.24819010865e-05` |
| `atomic unit of electric dipole mom.` | `C m` | `8.4783536198e-30` | `3.77119045999e-25` | `4447922.13862` | 9 | `2.24819024914e-05` |
| `Thomson cross section` | `m^2` | `6.6524587051e-29` | `3.77119045999e-25` | `566786.714697` | 9 | `0.000176402087767` |
| `atomic unit of magnetizability` | `J T^-2` | `7.8910365794e-29` | `3.77119045999e-25` | `477808.120441` | 9 | `0.00020924524134` |
| `muon mass` | `kg` | `1.883531627e-28` | `3.77119045999e-25` | `200119.12061` | 9 | `0.000499452797991` |
| `atomic mass constant` | `kg` | `1.66053906892e-27` | `3.77119045999e-25` | `22610.639759` | 9 | `0.00440322250106` |
| `atomic mass unit-kilogram relationship` | `kg` | `1.66053906892e-27` | `3.77119045999e-25` | `22610.639759` | 9 | `0.00440322250106` |
| `unified atomic mass unit` | `kg` | `1.66053906892e-27` | `3.77119045999e-25` | `22610.639759` | 9 | `0.00440322250106` |
| `proton mass` | `kg` | `1.67262192595e-27` | `3.77119045999e-25` | `22446.5803209` | 9 | `0.0044352624024` |
| `neutron mass` | `kg` | `1.67492750056e-27` | `3.77119045999e-25` | `22415.5444563` | 9 | `0.0044413760544` |
| `tau mass` | `kg` | `3.16754e-27` | `3.77119045999e-25` | `11805.7390277` | 9 | `0.00839931059862` |
| `deuteron mass` | `kg` | `3.3435837768e-27` | `3.77119045999e-25` | `11178.887301` | 9 | `0.0088661228126` |
| `deuteron magn. moment` | `J T^-1` | `4.33073482e-27` | `3.77119045999e-25` | `8607.96900927` | 9 | `0.011483734025` |
| `helion mass` | `kg` | `5.0064127862e-27` | `3.77119045999e-25` | `7432.7197757` | 9 | `0.0132754175089` |
| `triton mass` | `kg` | `5.0073567512e-27` | `3.77119045999e-25` | `7431.2997403` | 9 | `0.0132779206044` |
| `nuclear magneton` | `J T^-1` | `5.0507837393e-27` | `3.77119045999e-25` | `7366.54510398` | 9 | `0.0133930751917` |
| `alpha particle mass` | `kg` | `6.644657345e-27` | `3.77119045999e-25` | `5575.52285119` | 9 | `0.0176195220461` |
| `neutron magn. moment` | `J T^-1` | `-9.6623645e-27` | `-3.77119045999e-25` | `3802.96853321` | 9 | `0.0256215235017` |
| `shielded helion magn. moment` | `J T^-1` | `-1.074553024e-26` | `-3.77119045999e-25` | `3409.54338759` | 9 | `0.0284937352117` |
| `shielded proton magn. moment` | `J T^-1` | `1.41057047e-26` | `3.77119045999e-25` | `2573.52148666` | 9 | `0.0374038512498` |
| `proton magn. moment` | `J T^-1` | `1.41060671e-26` | `3.77119045999e-25` | `2573.45280102` | 9 | `0.0374048122195` |
| `muon magn. moment` | `J T^-1` | `-4.49044799e-26` | `-3.77119045999e-25` | `739.824994831` | 9 | `0.119072426536` |
| `atomic unit of mom.um` | `kg m s^-1` | `1.992851882e-24` | `5.59264144657e-24` | `180.635078657` | 9 | `0.356334640981` |
| `atomic unit of momentum` | `kg m s^-1` | `1.99285191545e-24` | `5.59264144657e-24` | `180.635073947` | 9 | `0.356334646962` |
| `joule-kelvin relationship` | `K` | `7.24297051604e+22` | `1.63038863168e+23` | `125.099443394` | 9 | `0.444248099828` |
| `kilogram-hertz relationship` | `Hz` | `1.35639248965e+50` | `2.65168256711e+24` | `100` | 9 | `5.11521441698e+25` |
| `kilogram-inverse meter relationship` | `m^-1` | `4.52443833544e+41` | `2.65168256711e+24` | `100` | 9 | `1.70625186874e+17` |
| `kilogram-kelvin relationship` | `K` | `6.50965726073e+39` | `2.65168256711e+24` | `100` | 9 | `2.45491573595e+15` |
| `kilogram-electron volt relationship` | `eV` | `5.6095886038e+35` | `2.65168256711e+24` | `99.9999999995` | 9 | `211548270271` |
| `kilogram-hartree relationship` | `E_h` | `2.06148578874e+34` | `2.65168256711e+24` | `99.9999999871` | 9 | `7774255539.91` |
| `joule-hertz relationship` | `Hz` | `1.50919017964e+33` | `2.65168256711e+24` | `99.9999998243` | 9 | `569144360.778` |
| `Planck temperature` | `K` | `1.416784e+32` | `2.65168256711e+24` | `99.9999981284` | 9 | `53429623.0467` |
| `kilogram-atomic mass unit relationship` | `u` | `6.0221407537e+26` | `2.65168256711e+24` | `99.5596777499` | 9 | `227.106397591` |
| `Loschmidt constant (273.15 K, 101.325 kPa)` | `m^-3` | `2.6867801118e+25` | `2.65168256711e+24` | `90.1306305065` | 9 | `10.1323595257` |
| `Loschmidt constant (273.15 K, 100 kPa)` | `m^-3` | `2.65164580488e+25` | `2.65168256711e+24` | `89.9998613607` | 9 | `9.99986136265` |
| `inverse meter-joule relationship` | `J` | `1.98644585715e-25` | `3.77119045999e-25` | `89.84612374` | 9 | `0.52674238499` |
| `Avogadro constant` | `mol^-1` | `6.02214076e+23` | `1.7880638506e+23` | `70.3085012147` | 9 | `3.36796740115` |
| `natural unit of mom.um` | `kg m s^-1` | `2.730924488e-22` | `4.57682848122e-22` | `67.5926412954` | 9 | `0.596684909475` |
| `natural unit of momentum` | `kg m s^-1` | `2.730924488e-22` | `4.57682848122e-22` | `67.5926412954` | 9 | `0.596684909475` |
| `atomic unit of mag. dipole mom.` | `J T^-1` | `1.85480201315e-23` | `6.1335069478e-24` | `66.9317430954` | 9 | `3.02404811625` |
| `atomic unit of magn. dipole moment` | `J T^-1` | `1.8548019e-23` | `6.1335069478e-24` | `66.9317410781` | 9 | `3.02404793177` |
| `Boltzmann constant` | `J K^-1` | `1.380649e-23` | `6.1335069478e-24` | `55.5751900172` | 9 | `2.25099443394` |
| `kelvin-joule relationship` | `J` | `1.380649e-23` | `6.1335069478e-24` | `55.5751900172` | 9 | `2.25099443394` |
| `joule-inverse meter relationship` | `m^-1` | `5.03411656754e+24` | `2.65168256711e+24` | `47.325761501` | 9 | `1.8984612374` |
| `electron magn. moment` | `J T^-1` | `-9.28476412e-24` | `-6.1335069478e-24` | `33.9400886385` | 9 | `1.51377738691` |
| `Bohr magneton` | `J T^-1` | `9.2740100657e-24` | `6.1335069478e-24` | `33.8634861905` | 9 | `1.51202405812` |
| `hertz-atomic mass unit relationship` | `u` | `4.439821659e-24` | `5.59264144657e-24` | `25.9654525815` | 9 | `0.793868461159` |
| `atomic mass unit-hertz relationship` | `Hz` | `2.25234272185e+23` | `1.7880638506e+23` | `20.6131538838` | 9 | `1.25965452581` |
| `natural unit of time` | `s` | `1.28808866644e-21` | `1.47645734189e-21` | `14.6238904481` | 8 | `0.872418477589` |
| `Planck mass energy equivalent in GeV` | `GeV` | `1.22089e+19` | `1.293448966e+19` | `5.94312067459` | 9 | `0.943902722171` |
| `molar Planck constant times c` | `J m mol^-1` | `0.119626565582` | `0.125` | `4.49184041342` | 1 | `0.957012524656` |
| `muon Compton wavelength` | `m` | `1.17344411e-14` | `1.22490868926e-14` | `4.38577166291` | 6 | `0.957984966792` |
| `molar gas constant` | `J mol^-1 K^-1` | `8.31446261815` | `8` | `3.78211596582` | 1 | `1.03930782727` |
| `molar Planck constant` | `J Hz^-1 mol^-1` | `3.99031271289e-10` | `4.13921144274e-10` | `3.73150528681` | 4 | `0.964027271401` |

## Calibration Meaning

The column `exact_calibration_coefficient` in the CSV/JSON is the number that makes the sparse BIP39 formula exact.
Therefore `target_calibrated_exact_pass = 445/445` is mathematically trivial after fitting and is not a physical proof.
The useful result is the visible distribution of how much calibration each constant needs.

## Scientific Status

This v8 layer satisfies the request to fit all 445 catalog constants.
It should be cited as a diagnostic fit table, not as a no-fit derivation of all constants.
A proof-level version would need one frozen rule that selects the formula for a new constant before its value is known, plus a declared unit basis for dimensional constants.
