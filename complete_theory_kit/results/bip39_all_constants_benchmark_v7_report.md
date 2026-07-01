# BIP39 All-Constants Benchmark v7

This benchmark tests the BIP39 model against the full SciPy/CODATA physical-constants catalog.
Only frozen v6 formulas count as no-fit predictions.
Sparse-search rows are diagnostic only and do not count as proof.

## Summary

| Metric | Value |
|:--|:--|
| `catalog_source` | `scipy.constants.physical_constants` |
| `catalog_total_positive_constants` | `387` |
| `dimensionless_constants` | `80` |
| `dimensional_constants` | `307` |
| `frozen_registry_hash` | `d388fa65f2b74ffde9e313ee8334b11028eca6c02255da5a5b831fd9f8a0cbdb` |
| `frozen_no_fit_predictions_available` | `4/387` |
| `frozen_no_fit_predictions_pass_1_percent` | `3/4` |
| `missing_frozen_formulas` | `383` |
| `sparse_search_candidate_count_per_constant` | `101635` |
| `sparse_diagnostic_pass_1_percent_all_constants` | `200/387` |
| `sparse_diagnostic_pass_1_percent_dimensionless` | `58/80` |
| `scientific_verdict` | `FROZEN_BIP39_MODEL_DOES_NOT_COVER_300_PLUS_CONSTANTS; sparse search is diagnostic only` |

## Frozen No-Fit Coverage

| Constant | Unit | Frozen key | Observed | Predicted | Rel error % | Pass <=1% |
|:--|:--|:--|--:|--:|--:|:--|
| `proton mass energy equivalent in MeV` | `MeV` | `proton_mass_MeV` | `938.27208943` | `924.681915252` | `1.44842571055` | `False` |
| `Fermi coupling constant` | `GeV^-2` | `G_F_GeV_minus2` | `1.1663787e-05` | `1.15713955249e-05` | `0.792122447985` | `True` |
| `weak mixing angle` | `` | `sin2_thetaW` | `0.22305` | `0.223969933654` | `0.412433828069` | `True` |
| `fine-structure constant` | `` | `alpha` | `0.0072973525643` | `0.00728622367155` | `0.152505893727` | `True` |

## Missing Frozen Formulas

The frozen BIP39 registry has no formula for `383` catalog constants.
First 80 missing constants:

| Constant | Unit | Value |
|:--|:--|--:|
| `alpha particle mass` | `kg` | `6.644657345e-27` |
| `alpha particle mass energy equivalent` | `J` | `5.9719201997e-10` |
| `alpha particle mass energy equivalent in MeV` | `MeV` | `3727.3794118` |
| `alpha particle mass in u` | `u` | `4.00150617913` |
| `alpha particle molar mass` | `kg mol^-1` | `0.0040015061833` |
| `alpha particle relative atomic mass` | `` | `4.00150617913` |
| `alpha particle rms charge radius` | `m` | `1.6785e-15` |
| `alpha particle-electron mass ratio` | `` | `7294.29954171` |
| `alpha particle-proton mass ratio` | `` | `3.97259969025` |
| `Angstrom star` | `m` | `1.00001495e-10` |
| `atomic mass constant` | `kg` | `1.66053906892e-27` |
| `atomic mass constant energy equivalent` | `J` | `1.49241808768e-10` |
| `atomic mass constant energy equivalent in MeV` | `MeV` | `931.49410372` |
| `atomic mass unit-electron volt relationship` | `eV` | `931494103.72` |
| `atomic mass unit-hartree relationship` | `E_h` | `34231776.922` |
| `atomic mass unit-hertz relationship` | `Hz` | `2.25234272185e+23` |
| `atomic mass unit-inverse meter relationship` | `m^-1` | `7.5130066209e+14` |
| `atomic mass unit-joule relationship` | `J` | `1.49241808768e-10` |
| `atomic mass unit-kelvin relationship` | `K` | `1.08095402067e+13` |
| `atomic mass unit-kilogram relationship` | `kg` | `1.66053906892e-27` |
| `atomic unit of 1st hyperpolarizability` | `C^3 m^3 J^-2` | `3.2063612996e-53` |
| `atomic unit of 1st hyperpolarizablity` | `C^3 m^3 J^-2` | `3.20636151e-53` |
| `atomic unit of 2nd hyperpolarizability` | `C^4 m^4 J^-3` | `6.2353799735e-65` |
| `atomic unit of 2nd hyperpolarizablity` | `C^4 m^4 J^-3` | `6.2353808e-65` |
| `atomic unit of action` | `J s` | `1.05457181765e-34` |
| `atomic unit of charge` | `C` | `1.602176634e-19` |
| `atomic unit of charge density` | `C m^-3` | `1.08120238677e+12` |
| `atomic unit of current` | `A` | `0.00662361823751` |
| `atomic unit of electric dipole mom.` | `C m` | `8.4783536198e-30` |
| `atomic unit of electric dipole moment` | `C m` | `8.47835309e-30` |
| `atomic unit of electric field` | `V m^-1` | `514220675112` |
| `atomic unit of electric field gradient` | `V m^-2` | `9.7173624424e+21` |
| `atomic unit of electric polarizability` | `C^2 m^2 J^-1` | `1.64877727212e-41` |
| `atomic unit of electric polarizablity` | `C^2 m^2 J^-1` | `1.648777274e-41` |
| `atomic unit of electric potential` | `V` | `27.211386246` |
| `atomic unit of electric quadrupole mom.` | `C m^2` | `4.4865515185e-40` |
| `atomic unit of electric quadrupole moment` | `C m^2` | `4.48655124e-40` |
| `atomic unit of energy` | `J` | `4.35974472221e-18` |
| `atomic unit of force` | `N` | `8.2387235038e-08` |
| `atomic unit of length` | `m` | `5.29177210544e-11` |
| `atomic unit of mag. dipole mom.` | `J T^-1` | `1.85480201315e-23` |
| `atomic unit of mag. flux density` | `T` | `235051.757077` |
| `atomic unit of magn. dipole moment` | `J T^-1` | `1.8548019e-23` |
| `atomic unit of magn. flux density` | `T` | `235051.757077` |
| `atomic unit of magnetizability` | `J T^-2` | `7.8910365794e-29` |
| `atomic unit of mass` | `kg` | `9.1093837139e-31` |
| `atomic unit of mom.um` | `kg m s^-1` | `1.992851882e-24` |
| `atomic unit of momentum` | `kg m s^-1` | `1.99285191545e-24` |
| `atomic unit of permittivity` | `F m^-1` | `1.1126500562e-10` |
| `atomic unit of time` | `s` | `2.41888432659e-17` |
| `atomic unit of velocity` | `m s^-1` | `2187691.26216` |
| `Avogadro constant` | `mol^-1` | `6.02214076e+23` |
| `Bohr magneton` | `J T^-1` | `9.2740100657e-24` |
| `Bohr magneton in eV/T` | `eV T^-1` | `5.7883817982e-05` |
| `Bohr magneton in Hz/T` | `Hz T^-1` | `13996244917.1` |
| `Bohr magneton in inverse meter per tesla` | `m^-1 T^-1` | `46.686447719` |
| `Bohr magneton in inverse meters per tesla` | `m^-1 T^-1` | `46.68644814` |
| `Bohr magneton in K/T` | `K T^-1` | `0.67171381472` |
| `Bohr radius` | `m` | `5.29177210544e-11` |
| `Boltzmann constant` | `J K^-1` | `1.380649e-23` |
| `Boltzmann constant in eV/K` | `eV K^-1` | `8.61733326215e-05` |
| `Boltzmann constant in Hz/K` | `Hz K^-1` | `20836619123.3` |
| `Boltzmann constant in inverse meter per kelvin` | `m^-1 K^-1` | `69.5034800486` |
| `Boltzmann constant in inverse meters per kelvin` | `m^-1 K^-1` | `69.503457` |
| `characteristic impedance of vacuum` | `ohm` | `376.730313412` |
| `classical electron radius` | `m` | `2.8179403205e-15` |
| `Compton wavelength` | `m` | `2.42631023538e-12` |
| `Compton wavelength over 2 pi` | `m` | `3.8615926764e-13` |
| `conductance quantum` | `S` | `7.74809172986e-05` |
| `conventional value of ampere-90` | `A` | `1.00000008887` |
| `conventional value of coulomb-90` | `C` | `1.00000008887` |
| `conventional value of farad-90` | `F` | `0.999999982206` |
| `conventional value of henry-90` | `H` | `1.00000001779` |
| `conventional value of Josephson constant` | `Hz V^-1` | `4.835979e+14` |
| `conventional value of ohm-90` | `ohm` | `1.00000001779` |
| `conventional value of volt-90` | `V` | `1.00000010667` |
| `conventional value of von Klitzing constant` | `ohm` | `25812.807` |
| `conventional value of watt-90` | `W` | `1.00000019554` |
| `Copper x unit` | `m` | `1.00207697e-13` |
| `Cu x unit` | `m` | `1.00207697e-13` |

## Sparse Search Diagnostic For Dimensionless Constants

These rows show how well a BIP39 monomial search can approximate dimensionless constants.
Because formulas are selected after seeing each target, this is a look-elsewhere diagnostic, not a no-fit proof.

| Constant | Value | Predicted | Rel error % | Complexity | Formula |
|:--|--:|--:|--:|--:|:--|
| `electron to shielded helion mag. mom. ratio` | `864.05823986` | `864` | `0.00674027019399` | 3 | `1 * K^2 * words^1` |
| `electron to shielded helion magn. moment ratio` | `864.058255` | `864` | `0.00674202227256` | 3 | `1 * K^2 * words^1` |
| `deuteron-electron mass ratio` | `3670.48296765` | `3669.52339298` | `0.0261430085468` | 2 | `1 * dict^1 * lnK^1` |
| `electron-deuteron mass ratio` | `0.000272443710763` | `0.000272514954371` | `0.026149844908` | 2 | `1 * dict^-1 * lnK^-1` |
| `alpha particle relative atomic mass` | `4.00150617913` | `4` | `0.0376403049646` | 2 | `1 * K^-1 * words^1` |
| `shielding difference of d and p in HD` | `1.9877e-08` | `1.98679015673e-08` | `0.0457736716255` | 4 | `1 * entropy^-3 * U^-1` |
| `deuteron-proton mass ratio` | `1.99900750127` | `1.99996845637` | `0.048071610365` | 2 | `1 * K^1 * U^-1` |
| `muon mag. mom. anomaly` | `0.00116592062` | `0.00116651007111` | `0.0505567104572` | 3 | `1 * K^-1 * entropy^-1 * lnK^1` |
| `deuteron magn. moment to nuclear magneton ratio` | `0.8574382329` | `0.856811509907` | `0.0730924944208` | 3 | `1 * pi^1 * bits^-1 * U^1` |
| `deuteron g factor` | `0.8574382335` | `0.856811509907` | `0.0730925643456` | 3 | `1 * pi^1 * bits^-1 * U^1` |
| `deuteron mag. mom. to nuclear magneton ratio` | `0.8574382335` | `0.856811509907` | `0.0730925643456` | 3 | `1 * pi^1 * bits^-1 * U^1` |
| `neutron-proton mass ratio` | `1.00137841946` | `1` | `0.137652203524` | 0 | `1 * 1` |
| `proton-neutron mass ratio` | `0.99862347797` | `1` | `0.137841945475` | 0 | `1 * 1` |
| `proton mag. shielding correction` | `2.56715e-05` | `2.57082109336e-05` | `0.143002682345` | 3 | `1 * total_bits^-2 * lnK^1` |
| `proton magn. shielding correction` | `2.56715e-05` | `2.57082109336e-05` | `0.143002682345` | 3 | `1 * total_bits^-2 * lnK^1` |
| `fine-structure constant` | `0.0072973525643` | `0.00728622367155` | `0.152505893727` | 3 | `1 * K^-1 * lnDict^-1 * U^-1` |
| `inverse fine-structure constant` | `137.035999177` | `137.245306359` | `0.152738829876` | 3 | `1 * K^1 * lnDict^1 * U^1` |
| `electron mag. mom. anomaly` | `0.00115965218046` | `0.00115740740741` | `0.193572960101` | 3 | `1 * K^-2 * words^-1` |
| `electron magn. moment anomaly` | `0.0011596521859` | `0.00115740740741` | `0.193573428299` | 3 | `1 * K^-2 * words^-1` |
| `triton-proton mass ratio` | `2.99371703403` | `3.0000473162` | `0.211452254628` | 1 | `1 * U^1` |
| `helion-proton mass ratio` | `2.99315267155` | `3.0000473162` | `0.23034724253` | 1 | `1 * U^1` |
| `electron-muon mass ratio` | `0.0048363317` | `0.00482287706339` | `0.278199210555` | 3 | `1 * pi^-1 * K^-1 * bits^-1` |
| `muon-electron mass ratio` | `206.7682827` | `207.345115137` | `0.27897529998` | 3 | `1 * pi^1 * K^1 * bits^1` |
| `electron-muon magn. moment ratio` | `206.7669894` | `207.345115137` | `0.279602531625` | 3 | `1 * pi^1 * K^1 * bits^1` |
| `electron-muon mag. mom. ratio` | `206.7669881` | `207.345115137` | `0.27960316211` | 3 | `1 * pi^1 * K^1 * bits^1` |
| `weak mixing angle` | `0.22305` | `0.223969933654` | `0.412433828069` | 2 | `1 * checksum^-1 * lnK^1` |
| `muon-tau mass ratio` | `0.0594635` | `0.0592164427062` | `0.415477215041` | 3 | `1 * pi^-1 * lnK^-1 * U^-1` |
| `tau-muon mass ratio` | `16.817` | `16.8872014984` | `0.417443648825` | 3 | `1 * pi^1 * lnK^1 * U^1` |
| `helion relative atomic mass` | `3.01493224693` | `3.0000473162` | `0.493706973067` | 1 | `1 * U^1` |
| `triton relative atomic mass` | `3.01550071597` | `3.0000473162` | `0.512465465271` | 1 | `1 * U^1` |
| `electron-tau mass ratio` | `0.000287585` | `0.000285931616901` | `0.574919797314` | 3 | `1 * entropy^-1 * lnK^-1 * lnDict^-1` |
| `tau-electron mass ratio` | `3477.23` | `3497.33971653` | `0.578325751619` | 3 | `1 * entropy^1 * lnK^1 * lnDict^1` |
| `helion-electron mass ratio` | `5495.88527984` | `5461.24719819` | `0.63025481592` | 3 | `1 * dict^1 * checksum^1 * U^-1` |
| `electron-helion mass ratio` | `0.000181954307465` | `0.000183108356701` | `0.634252221106` | 3 | `1 * dict^-1 * checksum^-1 * U^1` |
| `triton-electron mass ratio` | `5496.92153551` | `5461.24719819` | `0.648987566826` | 3 | `1 * dict^1 * checksum^1 * U^-1` |
| `electron-triton mass ratio` | `0.000181920006233` | `0.000183108356701` | `0.65322692831` | 3 | `1 * dict^-1 * checksum^-1 * U^1` |
| `deuteron relative atomic mass` | `2.01355321254` | `1.99996845637` | `0.674665863921` | 2 | `1 * K^1 * U^-1` |
| `alpha particle-proton mass ratio` | `3.97259969025` | `4` | `0.689732464493` | 2 | `1 * K^-1 * words^1` |
| `triton g factor` | `5.95792493` | `6` | `0.706203426434` | 1 | `1 * K^1` |
| `triton mag. mom. to nuclear magneton ratio` | `2.978962465` | `3.0000473162` | `0.707791771242` | 1 | `1 * U^1` |
| `proton relative atomic mass` | `1.00727646658` | `1` | `0.722390209672` | 0 | `1 * 1` |
| `neutron-electron magn. moment ratio` | `0.00104066882` | `0.0010330741447` | `0.729787917018` | 3 | `1 * bits^-1 * total_bits^-1 * U^1` |
| `neutron-electron mag. mom. ratio` | `0.00104066884` | `0.0010330741447` | `0.729789824833` | 3 | `1 * bits^-1 * total_bits^-1 * U^1` |
| `electron-neutron magn. moment ratio` | `960.9205` | `967.984732882` | `0.735152687623` | 3 | `1 * bits^1 * total_bits^1 * U^-1` |
| `electron-neutron mag. mom. ratio` | `960.92048` | `967.984732882` | `0.735154784261` | 3 | `1 * bits^1 * total_bits^1 * U^-1` |
| `electron relative atomic mass` | `0.000548579909044` | `0.00055262133018` | `0.736706005718` | 3 | `1 * pi^-1 * words^-2` |
| `proton g factor` | `5.5856946893` | `5.62897838553` | `0.774902651047` | 2 | `1 * pi^1 * lnK^1` |
| `W to Z mass ratio` | `0.88145` | `0.888860850325` | `0.840756744589` | 3 | `1 * checksum^1 * U^-2` |
| `proton-tau mass ratio` | `0.528051` | `0.523598775598` | `0.843142878567` | 2 | `1 * pi^1 * K^-1` |
| `tau-proton mass ratio` | `1.89376` | `1.9098593171` | `0.850124466814` | 2 | `1 * pi^-1 * K^1` |
| `proton magn. moment to Bohr magneton ratio` | `0.001521032206` | `0.00153398078789` | `0.851302282395` | 2 | `1 * pi^1 * dict^-1` |
| `proton mag. mom. to Bohr magneton ratio` | `0.0015210322023` | `0.00153398078789` | `0.851302527722` | 2 | `1 * pi^1 * dict^-1` |
| `shielded proton mag. mom. to Bohr magneton ratio` | `0.0015209931551` | `0.00153398078789` | `0.853891599847` | 2 | `1 * pi^1 * dict^-1` |
| `shielded proton magn. moment to Bohr magneton ratio` | `0.001520993132` | `0.00153398078789` | `0.85389313156` | 2 | `1 * pi^1 * dict^-1` |
| `neutron relative atomic mass` | `1.00866491606` | `1` | `0.859048026955` | 0 | `1 * 1` |
| `shielding difference of t and p in HT` | `2.3945e-08` | `2.41568526369e-08` | `0.884746865294` | 4 | `1 * pi^-2 * dict^-2` |
| `neutron-tau mass ratio` | `0.528779` | `0.523598775598` | `0.979657740134` | 2 | `1 * pi^1 * K^-1` |
| `tau-neutron mass ratio` | `1.89115` | `1.9098593171` | `0.989308997316` | 2 | `1 * pi^-1 * K^1` |
| `muon-neutron mass ratio` | `0.1124545168` | `0.111107606291` | `1.19773802572` | 2 | `1 * U^-2` |
| `neutron-muon mass ratio` | `8.89248408` | `9.00028389941` | `1.21225765987` | 2 | `1 * U^2` |
| `muon-proton mass ratio` | `0.1126095262` | `0.111107606291` | `1.33374143382` | 2 | `1 * U^-2` |
| `proton-muon mass ratio` | `8.88024338` | `9.00028389941` | `1.35177060218` | 2 | `1 * U^2` |
| `deuteron mag. mom. to Bohr magneton ratio` | `0.0004669754568` | `0.000473484848485` | `1.3939472814` | 2 | `1 * checksum^-1 * total_bits^-1` |
| `deuteron magn. moment to Bohr magneton ratio` | `0.0004669754567` | `0.000473484848485` | `1.39394730311` | 2 | `1 * checksum^-1 * total_bits^-1` |
| `triton mag. mom. to Bohr magneton ratio` | `0.0016223936648` | `0.0015995148916` | `1.41018630031` | 2 | `1 * K^-1 * f1^-1` |
| `proton-electron mass ratio` | `1836.15267343` | `1809.55736847` | `1.4484255772` | 3 | `1 * pi^1 * words^2` |
| `electron-proton mass ratio` | `0.000544617021489` | `0.00055262133018` | `1.46971328024` | 3 | `1 * pi^-1 * words^-2` |
| `shielded proton magn. moment to nuclear magneton ratio` | `2.792775604` | `2.75` | `1.53165202169` | 3 | `1 * K^1 * bits^1 * words^-1` |
| `shielded proton mag. mom. to nuclear magneton ratio` | `2.792775648` | `2.75` | `1.53165357305` | 3 | `1 * K^1 * bits^1 * words^-1` |
| `proton mag. mom. to nuclear magneton ratio` | `2.79284734463` | `2.75` | `1.53418140495` | 3 | `1 * K^1 * bits^1 * words^-1` |
| `proton magn. moment to nuclear magneton ratio` | `2.792847351` | `2.75` | `1.53418162954` | 3 | `1 * K^1 * bits^1 * words^-1` |
| `neutron-electron mass ratio` | `1838.683662` | `1809.55736847` | `1.58408399086` | 3 | `1 * pi^1 * words^2` |
| `electron-neutron mass ratio` | `0.00054386734416` | `0.00055262133018` | `1.60958110727` | 3 | `1 * pi^-1 * words^-2` |
| `triton-proton mag. mom. ratio` | `1.066639908` | `1.04923275701` | `1.63196134509` | 2 | `1 * checksum^1 * lnDict^-1` |
| `triton to proton mag. mom. ratio` | `1.0666399189` | `1.04923275701` | `1.63196235031` | 2 | `1 * checksum^1 * lnDict^-1` |
| `alpha particle-electron mass ratio` | `7294.29954171` | `7170.88511595` | `1.69192977415` | 3 | `1 * pi^-1 * bits^1 * dict^1` |
| `electron to alpha particle mass ratio` | `0.000137093355473` | `0.000139452798899` | `1.72104870965` | 3 | `1 * pi^1 * bits^-1 * dict^-1` |
| `helion shielding shift` | `5.9967029e-05` | `6.103515625e-05` | `1.78119087741` | 2 | `1 * dict^-1 * checksum^-1` |
| `deuteron-proton mag. mom. ratio` | `0.3070122093` | `0.318309886184` | `3.67987869588` | 1 | `1 * pi^-1` |
| `deuteron-proton magn. moment ratio` | `0.3070122084` | `0.318309886184` | `3.67987899982` | 1 | `1 * pi^-1` |

## Scientific Reading

The frozen BIP39 no-fit model does not yet provide formulas for the 300+ CODATA catalog.
It covers only the small set frozen in v6, with a few aliases visible in the SciPy catalog.
The sparse-search diagnostic can approximate many numbers, but that is exactly the curve-fitting risk unless the formula-selection rule is frozen before the target is known.
Dimensional constants are especially strict: a dimensionless BIP39 monomial cannot predict their SI numerical values without a declared unit basis.
