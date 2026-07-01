# SIGT Predictive Victory Attempt v13

This report attempts to force full predictive victory while separating honest prediction from leakage.

## Leaderboard

| Engine | Train <=1% | Test <=1% | Test <=0.1% | Test median rel error % | Test max rel error % | Victory | Verdict |
|:--|--:|--:|--:|--:|--:|:--|:--|
| `HONEST_BIP39_PRIOR` | 184/365 | 46/80 | 9/80 | `0.847129739209` | `1.17615884804e+30` | `NO_FULL_TEST_VICTORY` | `FULL_PREDICTIVE_VICTORY_NOT_ACHIEVED` |
| `TRAINED_GLOBAL_CALIBRATION` | 182/365 | 45/80 | 5/80 | `0.90594188104` | `1.17492504081e+30` | `NO_FULL_TEST_VICTORY` | `FULL_PREDICTIVE_VICTORY_NOT_ACHIEVED` |
| `TRAINED_UNIT_SECTOR_CALIBRATION` | 244/365 | 45/80 | 15/80 | `0.868842496049` | `7.51300662092e+16` | `NO_FULL_TEST_VICTORY` | `FULL_PREDICTIVE_VICTORY_NOT_ACHIEVED` |
| `ORACLE_CATALOG_LOOKUP` | 365/365 | 80/80 | 80/80 | `0` | `2.0812506623e-14` | `FULL_NUMERIC_VICTORY` | `REJECT_AS_PREDICTION: uses each target exact coefficient` |

## Interpretation

Full 80/80 test victory is possible only in `ORACLE_CATALOG_LOOKUP`, which uses each held-out target's exact coefficient.
That is calibrated symbolic closure, not predictive physics.
The honest engines do not achieve full held-out victory on the current 445-constant benchmark.

## Worst Honest Engine Test Rows

| Constant | Unit | Sector | Observed | Predicted | Rel error % |
|:--|:--|:--|--:|--:|--:|
| `inverse meter-kilogram relationship` | `kg` | `general_dimensional` | `2.2102190943e-42` | `1.66053906892e-27` | `7.51300662092e+16` |
| `electron mass` | `kg` | `lepton_particle` | `9.1093837139e-31` | `3.16754e-27` | `347622.754852` |
| `deuteron magn. moment` | `J T^-1` | `electromagnetic_quantum` | `4.33073482e-27` | `3.75733323176e-25` | `8575.97160281` |
| `nuclear magneton` | `J T^-1` | `electromagnetic_quantum` | `5.0507837393e-27` | `3.75733323176e-25` | `7339.109306` |
| `shielded helion magn. moment` | `J T^-1` | `electromagnetic_quantum` | `-1.074553024e-26` | `-3.75733323176e-25` | `3396.64758075` |
| `muon mass` | `kg` | `lepton_particle` | `1.883531627e-28` | `3.16754e-27` | `1581.70258179` |
| `muon magn. moment` | `J T^-1` | `electromagnetic_quantum` | `-4.49044799e-26` | `-3.75733323176e-25` | `736.739060363` |
| `kilogram-hertz relationship` | `Hz` | `general_dimensional` | `1.35639248965e+50` | `3.0042795021e+24` | `100` |
| `atomic unit of mass` | `kg` | `quantum_atomic` | `9.1093837139e-31` | `2.51456820085e-35` | `99.9972395847` |
| `joule-inverse meter relationship` | `m^-1` | `general_dimensional` | `5.03411656754e+24` | `2.67014310257e+24` | `46.959052959` |
| `electron volt-hertz relationship` | `Hz` | `quantum_atomic` | `2.41798924208e+14` | `2.33116907298e+14` | `3.59059368824` |
| `tau Compton wavelength over 2 pi` | `m` | `quantum_atomic` | `1.11056e-16` | `1.07132285263e-16` | `3.53309567919` |
| `joule-hartree relationship` | `E_h` | `quantum_atomic` | `2.2937122784e+17` | `2.3711451865e+17` | `3.37587712426` |
| `atomic unit of energy` | `J` | `quantum_atomic` | `4.35974472221e-18` | `4.2316350558e-18` | `2.93846714814` |
| `natural unit of energy in MeV` | `MeV` | `general_dimensional` | `0.51099895069` | `0.4966383971` | `2.81029023066` |
| `proton rms charge radius` | `m` | `electromagnetic_quantum` | `8.4075e-16` | `8.19170374325e-16` | `2.56671134993` |
| `kelvin-hartree relationship` | `E_h` | `quantum_atomic` | `3.16681156346e-06` | `3.2467383542e-06` | `2.52388843309` |
| `electron volt-atomic mass unit relationship` | `u` | `quantum_atomic` | `1.07354410083e-09` | `1.04916267312e-09` | `2.27111561515` |
| `conventional value of coulomb-90` | `C` | `general_dimensional` | `1.00000008887` | `0.979266967064` | `2.07331199649` |
| `helion shielding shift` | `` | `dimensionless_ratio` | `5.9967029e-05` | `6.10798010001e-05` | `1.85563970518` |
| `conductance quantum` | `S` | `general_dimensional` | `7.74809172986e-05` | `7.89141491294e-05` | `1.84978686465` |
| `alpha particle-electron mass ratio` | `` | `dimensionless_ratio` | `7294.29954171` | `7176.13032861` | `1.62002139377` |
| `shielded helion to proton magn. moment ratio` | `` | `dimensionless_ratio` | `-0.761766562` | `-0.774003238274` | `1.60635513347` |
| `hertz-hartree relationship` | `E_h` | `quantum_atomic` | `1.51982984606e-16` | `1.54377949027e-16` | `1.57581088898` |
| `electron-proton mass ratio` | `` | `dimensionless_ratio` | `0.000544617021489` | `0.00055302555035` | `1.54393427474` |
| `Boltzmann constant in Hz/K` | `Hz K^-1` | `thermodynamic_statistical` | `20836619123.3` | `21137931023.3` | `1.4460690487` |
| `electron-deuteron magn. moment ratio` | `` | `dimensionless_ratio` | `-2143.923493` | `-2113.54484265` | `1.41696522534` |
| `molar volume of ideal gas (273.15 K, 101.325 kPa)` | `m^3 mol^-1` | `thermodynamic_statistical` | `0.022413969545` | `0.0226993578023` | `1.27326066331` |
| `Faraday constant` | `C mol^-1` | `general_dimensional` | `96485.3321233` | `95325.1002289` | `1.20249562179` |
| `Bohr magneton in eV/T` | `eV T^-1` | `quantum_atomic` | `5.7883817982e-05` | `5.71962001362e-05` | `1.18792759321` |
| `proton-neutron magn. moment ratio` | `` | `dimensionless_ratio` | `-1.45989805` | `-1.44375031401` | `1.10608655127` |
| `lattice spacing of ideal Si (220)` | `m` | `general_dimensional` | `1.920155716e-10` | `1.90028207047e-10` | `1.03500176403` |
| `shielded helion gyromag. ratio` | `s^-1 T^-1` | `electromagnetic_quantum` | `203789460.78` | `201708589.951` | `1.02108853981` |
| `shielded helion gyromagn. ratio` | `s^-1 T^-1` | `electromagnetic_quantum` | `203789460.78` | `201708589.951` | `1.02108853981` |
| `nuclear magneton in eV/T` | `eV T^-1` | `electromagnetic_quantum` | `3.15245125417e-08` | `3.12042089136e-08` | `1.01604625198` |
| `tau molar mass` | `kg mol^-1` | `thermodynamic_statistical` | `0.00190754` | `0.00188949604028` | `0.945928248715` |
| `electron volt-kelvin relationship` | `K` | `quantum_atomic` | `11604.5181216` | `11714.0213178` | `0.943625535166` |
| `proton mag. mom. to Bohr magneton ratio` | `` | `dimensionless_ratio` | `0.0015210322023` | `0.00153510283284` | `0.925071179743` |
| `electron to shielded proton magn. moment ratio` | `` | `dimensionless_ratio` | `-658.2275956` | `-652.375484419` | `0.889071078175` |
| `electron to shielded proton mag. mom. ratio` | `` | `dimensionless_ratio` | `-658.2275856` | `-652.375484419` | `0.88906957245` |
| `proton g factor` | `` | `dimensionless_ratio` | `5.5856946893` | `5.63309575573` | `0.848615419647` |
| `muon mass energy equivalent` | `J` | `lepton_particle` | `1.692833804e-11` | `1.70709405004e-11` | `0.842389017188` |
| `Sackur-Tetrode constant (1 K, 100 kPa)` | `` | `dimensionless_ratio` | `-1.15170753496` | `-1.16104148059` | `0.810444087996` |
| `Wien displacement law constant` | `m K` | `general_dimensional` | `0.0028977685` | `0.00292038553781` | `0.780498435477` |
| `neutron magn. moment to Bohr magneton ratio` | `` | `dimensionless_ratio` | `-0.00104187563` | `-0.00103382979668` | `0.772245082464` |
| `atomic mass constant energy equivalent` | `J` | `general_dimensional` | `1.49241808768e-10` | `1.48149460882e-10` | `0.731931550993` |
| `electron-triton mass ratio` | `` | `dimensionless_ratio` | `0.000181920006233` | `0.000183242293064` | `0.726850696035` |
| `electron-helion mass ratio` | `` | `dimensionless_ratio` | `0.000181954307465` | `0.000183242293064` | `0.7078621096` |
| `proton Compton wavelength over 2 pi` | `m` | `quantum_atomic` | `2.10308910109e-16` | `2.0887656985e-16` | `0.681064943017` |
| `electron charge to mass quotient` | `C kg^-1` | `electromagnetic_quantum` | `-175882000838` | `-174713478786` | `0.664378416318` |
| `alpha particle mass in u` | `u` | `nuclear_particle` | `4.00150617913` | `4.02388707447` | `0.559311777528` |
| `atomic unit of permittivity` | `F m^-1` | `quantum_atomic` | `1.1126500562e-10` | `1.11829206547e-10` | `0.507078504885` |
| `electron volt-inverse meter relationship` | `m^-1` | `quantum_atomic` | `806554.393735` | `810538.147238` | `0.493922484791` |
| `electron mag. mom.` | `J T^-1` | `electromagnetic_quantum` | `-9.2847646917e-24` | `-9.23993274305e-24` | `0.482854979492` |
| `helion mass energy equivalent in MeV` | `MeV` | `nuclear_particle` | `2808.39161112` | `2820.31394465` | `0.424525321924` |
| `inverse meter-kelvin relationship` | `K` | `thermodynamic_statistical` | `0.014387768775` | `0.014336008525` | `0.359751750501` |
| `electron-muon magn. moment ratio` | `` | `dimensionless_ratio` | `206.7669894` | `207.496779709` | `0.352953008203` |
| `triton-proton mass ratio` | `` | `dimensionless_ratio` | `2.99371703403` | `3.00224172956` | `0.284752882033` |
| `neutron mass in u` | `u` | `nuclear_particle` | `1.00866491606` | `1.00597176862` | `0.267001201319` |
| `proton mag. shielding correction` | `` | `dimensionless_ratio` | `2.56715e-05` | `2.57270154509e-05` | `0.216253241654` |
| `proton-neutron mass ratio` | `` | `dimensionless_ratio` | `0.99862347797` | `1.00073145959` | `0.211088729914` |
| `neutron-proton mass difference in u` | `u` | `nuclear_particle` | `0.00138844948` | `0.00138563604493` | `0.20263143267` |
| `atomic unit of electric field` | `V m^-1` | `quantum_atomic` | `514220675112` | `515177571241` | `0.186086669594` |
| `muon Compton wavelength over 2 pi` | `m` | `quantum_atomic` | `1.867594308e-15` | `1.86457337229e-15` | `0.161755457257` |
| `reduced muon Compton wavelength` | `m` | `quantum_atomic` | `1.867594306e-15` | `1.86457337229e-15` | `0.161755350341` |
| `shielded proton gyromag. ratio in MHz/T` | `MHz T^-1` | `electromagnetic_quantum` | `42.57638543` | `42.6164059794` | `0.0939970573006` |
| `Bohr magneton in K/T` | `K T^-1` | `quantum_atomic` | `0.67171381472` | `0.671215544388` | `0.0741789614576` |
| `electron to shielded helion magn. moment ratio` | `` | `dimensionless_ratio` | `864.058255` | `864.631981083` | `0.0663990048371` |
| `Hartree energy in eV` | `eV` | `quantum_atomic` | `27.211386246` | `27.2003526253` | `0.0405478081132` |
| `alpha particle relative atomic mass` | `` | `dimensionless_ratio` | `4.00150617913` | `4.00292583835` | `0.0354781213001` |
| `shielding difference of d and p in HD` | `` | `dimensionless_ratio` | `1.9877e-08` | `1.98824341344e-08` | `0.0273388054102` |
| `shielded proton gyromag. ratio` | `s^-1 T^-1` | `electromagnetic_quantum` | `267515319.4` | `267522187.08` | `0.00256720998835` |
| `Josephson constant` | `Hz V^-1` | `electromagnetic_quantum` | `4.83597848417e+14` | `4.835979e+14` | `1.06665107266e-05` |
| `atomic unit of 1st hyperpolarizablity` | `C^3 m^3 J^-2` | `quantum_atomic` | `3.20636151e-53` | `3.2063612996e-53` | `6.56195501362e-06` |
| `reduced Planck constant times c in MeV fm` | `MeV fm` | `relativity_gravity` | `197.326980459` | `197.3269788` | `8.40889816484e-07` |
| `atomic unit of charge` | `C` | `quantum_atomic` | `1.602176634e-19` | `1.602176634e-19` | `0` |
| `natural unit of action` | `J s` | `general_dimensional` | `1.05457181765e-34` | `1.05457181765e-34` | `0` |
| `natural unit of mom.um in MeV/c` | `MeV/c` | `general_dimensional` | `0.5109989461` | `0.5109989461` | `0` |
| `proton gyromagn. ratio` | `s^-1 T^-1` | `electromagnetic_quantum` | `267522187.08` | `267522187.08` | `0` |
| `unified atomic mass unit` | `kg` | `general_dimensional` | `1.66053906892e-27` | `1.66053906892e-27` | `0` |

## Final Status

The system has perfect calibrated symbolic convergence.
It does not yet have full honest predictive victory.
