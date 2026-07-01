# BIP39 Symbolic Approximator v11

This is a two-mode approximator for all 445 SciPy/CODATA constants.

```text
exact_symbolic: O_i = P_i * C_i, C_i := O_i/P_i
predictive_symbolic: C_i is estimated from symbolic descriptors without seeing test O_i
```

## Summary

| Metric | Value |
|:--|:--|
| `catalog_total_constants` | `445` |
| `train_count` | `365` |
| `test_count` | `80` |
| `feature_count` | `91` |
| `exact_symbolic_convergence` | `445/445` |
| `sympy_identity_validation` | `445/445` |
| `predictive_train_pass_1_percent` | `0/365` |
| `predictive_test_pass_1_percent` | `0/80` |
| `predictive_train_pass_10_percent` | `15/365` |
| `predictive_test_pass_10_percent` | `1/80` |
| `predictive_train_median_rel_error_percent` | `99.3458282184` |
| `predictive_test_median_rel_error_percent` | `99.9704748786` |
| `scientific_verdict` | `PERFECT_SYMBOLIC_CONVERGENCE_IN_CALIBRATED_MODE; LIMITED_OUT_OF_SAMPLE_PREDICTIVE_POWER` |

## Model

- `ridge_lambda = 3.0`
- `feature_count = 91`

## Best Test Predictions

| Constant | Sector | Unit | Observed | Predicted | Rel error % |
|:--|:--|:--|--:|--:|--:|
| `electron mass` | `lepton_particle` | `kg` | `9.1093837139e-31` | `8.83512797058e-31` | `3.0106948168` |
| `Sackur-Tetrode constant (1 K, 100 kPa)` | `dimensionless_ratio` | `` | `-1.15170753496` | `-1.03253486394` | `10.3474768898` |
| `tau molar mass` | `thermodynamic_statistical` | `kg mol^-1` | `0.00190754` | `0.00166779083732` | `12.5684998837` |
| `shielded proton gyromag. ratio in MHz/T` | `electromagnetic_quantum` | `MHz T^-1` | `42.57638543` | `49.1760300592` | `15.5007160954` |
| `shielded helion to proton magn. moment ratio` | `dimensionless_ratio` | `` | `-0.761766562` | `-0.977437990406` | `28.3120104196` |
| `Wien displacement law constant` | `general_dimensional` | `m K` | `0.0028977685` | `0.00199478597941` | `31.1613063842` |
| `natural unit of mom.um in MeV/c` | `general_dimensional` | `MeV/c` | `0.5109989461` | `0.672998781943` | `31.7025772908` |
| `proton-neutron magn. moment ratio` | `dimensionless_ratio` | `` | `-1.45989805` | `-2.07408012784` | `42.0702033158` |
| `shielded helion magn. moment` | `electromagnetic_quantum` | `J T^-1` | `-1.074553024e-26` | `-1.6035203908e-26` | `49.226734743` |
| `proton rms charge radius` | `electromagnetic_quantum` | `m` | `8.4075e-16` | `3.78709077679e-16` | `54.9558040228` |
| `reduced Planck constant times c in MeV fm` | `relativity_gravity` | `MeV fm` | `197.326980459` | `85.2894829252` | `56.7775867615` |
| `muon magn. moment` | `electromagnetic_quantum` | `J T^-1` | `-4.49044799e-26` | `-1.6035203908e-26` | `64.2904139104` |
| `alpha particle relative atomic mass` | `dimensionless_ratio` | `` | `4.00150617913` | `6.66950549194` | `66.6748767434` |
| `proton mag. mom. to Bohr magneton ratio` | `dimensionless_ratio` | `` | `0.0015210322023` | `0.000502834468071` | `66.941234557` |
| `muon mass energy equivalent` | `lepton_particle` | `J` | `1.692833804e-11` | `2.83049637022e-11` | `67.2046224225` |
| `molar volume of ideal gas (273.15 K, 101.325 kPa)` | `thermodynamic_statistical` | `m^3 mol^-1` | `0.022413969545` | `0.038119849202` | `70.0718345557` |
| `neutron magn. moment to Bohr magneton ratio` | `dimensionless_ratio` | `` | `-0.00104187563` | `-0.000215143466139` | `79.3503696656` |
| `proton g factor` | `dimensionless_ratio` | `` | `5.5856946893` | `10.0726533313` | `80.3294646704` |
| `electron-proton mass ratio` | `dimensionless_ratio` | `` | `0.000544617021489` | `9.49817877374e-05` | `82.5598936519` |
| `helion shielding shift` | `dimensionless_ratio` | `` | `5.9967029e-05` | `1.02715512991e-05` | `82.8713353481` |
| `natural unit of energy in MeV` | `general_dimensional` | `MeV` | `0.51099895069` | `0.084924107953` | `83.3807666653` |
| `conductance quantum` | `general_dimensional` | `S` | `7.74809172986e-05` | `1.23364556465e-05` | `84.0780722834` |
| `atomic mass constant energy equivalent` | `general_dimensional` | `J` | `1.49241808768e-10` | `2.74788200632e-10` | `84.1228023842` |
| `electron-triton mass ratio` | `dimensionless_ratio` | `` | `0.000181920006233` | `2.50450488382e-05` | `86.2329331684` |
| `electron-helion mass ratio` | `dimensionless_ratio` | `` | `0.000181954307465` | `2.50450488382e-05` | `86.2355284757` |
| `kelvin-hartree relationship` | `quantum_atomic` | `E_h` | `3.16681156346e-06` | `3.0681491039e-07` | `90.3115514061` |
| `proton mag. shielding correction` | `dimensionless_ratio` | `` | `2.56715e-05` | `2.34300299283e-06` | `90.8731356063` |
| `Bohr magneton in K/T` | `quantum_atomic` | `K T^-1` | `0.67171381472` | `0.036809290715` | `94.5200932438` |
| `nuclear magneton in eV/T` | `electromagnetic_quantum` | `eV T^-1` | `3.15245125417e-08` | `1.26119151285e-09` | `95.9993306441` |
| `atomic unit of mass` | `quantum_atomic` | `kg` | `9.1093837139e-31` | `1.59576601415e-32` | `98.248217372` |
| `reduced muon Compton wavelength` | `quantum_atomic` | `m` | `1.867594306e-15` | `3.05649892935e-17` | `98.3634031655` |
| `muon Compton wavelength over 2 pi` | `quantum_atomic` | `m` | `1.867594308e-15` | `3.05649892935e-17` | `98.3634031672` |
| `shielding difference of d and p in HD` | `dimensionless_ratio` | `` | `1.9877e-08` | `2.66469837906e-10` | `98.6594061583` |
| `proton Compton wavelength over 2 pi` | `quantum_atomic` | `m` | `2.10308910109e-16` | `2.17743775743e-18` | `98.9646478809` |
| `Bohr magneton in eV/T` | `quantum_atomic` | `eV T^-1` | `5.7883817982e-05` | `3.29650302295e-07` | `99.4304966158` |
| `tau Compton wavelength over 2 pi` | `quantum_atomic` | `m` | `1.11056e-16` | `6.29955084132e-19` | `99.4327590728` |
| `muon mass` | `lepton_particle` | `kg` | `1.883531627e-28` | `8.83512797058e-31` | `99.5309275489` |
| `atomic unit of permittivity` | `quantum_atomic` | `F m^-1` | `1.1126500562e-10` | `4.11956494828e-13` | `99.6297519669` |
| `electron volt-atomic mass unit relationship` | `quantum_atomic` | `u` | `1.07354410083e-09` | `6.68955753894e-13` | `99.937687166` |
| `atomic unit of energy` | `quantum_atomic` | `J` | `4.35974472221e-18` | `2.29618868777e-21` | `99.9473320381` |
| `hertz-hartree relationship` | `quantum_atomic` | `E_h` | `1.51982984606e-16` | `4.487316078e-20` | `99.9704748786` |
| `unified atomic mass unit` | `general_dimensional` | `kg` | `1.66053906892e-27` | `4.06634721972e-31` | `99.9755118847` |
| `atomic unit of charge` | `quantum_atomic` | `C` | `1.602176634e-19` | `2.13159814357e-24` | `99.9986695611` |
| `kilogram-hertz relationship` | `general_dimensional` | `Hz` | `1.35639248965e+50` | `5.08539714785e+27` | `100` |
| `triton-proton mass ratio` | `dimensionless_ratio` | `` | `2.99371703403` | `7.27835173414` | `143.120897914` |
| `electron-muon magn. moment ratio` | `dimensionless_ratio` | `` | `206.7669894` | `506.504476013` | `144.963897517` |
| `nuclear magneton` | `electromagnetic_quantum` | `J T^-1` | `5.0507837393e-27` | `1.50617314229e-26` | `198.205827063` |
| `proton-neutron mass ratio` | `dimensionless_ratio` | `` | `0.99862347797` | `2.9850196617` | `198.913427088` |
| `electron to shielded helion magn. moment ratio` | `dimensionless_ratio` | `` | `864.058255` | `2835.12966736` | `228.117884524` |
| `deuteron magn. moment` | `electromagnetic_quantum` | `J T^-1` | `4.33073482e-27` | `1.50617314229e-26` | `247.786970317` |
| `electron volt-hertz relationship` | `quantum_atomic` | `Hz` | `2.41798924208e+14` | `8.44572257747e+14` | `249.287020408` |
| `shielded helion gyromag. ratio` | `electromagnetic_quantum` | `s^-1 T^-1` | `203789460.78` | `758193459.289` | `272.04743385` |
| `shielded helion gyromagn. ratio` | `electromagnetic_quantum` | `s^-1 T^-1` | `203789460.78` | `758193459.289` | `272.04743385` |
| `helion mass energy equivalent in MeV` | `nuclear_particle` | `MeV` | `2808.39161112` | `11093.3580813` | `295.007520937` |
| `proton gyromagn. ratio` | `electromagnetic_quantum` | `s^-1 T^-1` | `267522187.08` | `1066042840.12` | `298.487636392` |
| `shielded proton gyromag. ratio` | `electromagnetic_quantum` | `s^-1 T^-1` | `267515319.4` | `1066042840.12` | `298.497866406` |
| `electron mag. mom.` | `electromagnetic_quantum` | `J T^-1` | `-9.2847646917e-24` | `-3.81774457358e-23` | `311.183772594` |
| `Hartree energy in eV` | `quantum_atomic` | `eV` | `27.211386246` | `113.959184982` | `318.792280379` |
| `neutron-proton mass difference in u` | `nuclear_particle` | `u` | `0.00138844948` | `0.00582345310214` | `319.421317521` |
| `atomic unit of electric field` | `quantum_atomic` | `V m^-1` | `514220675112` | `2.47975343702e+12` | `382.235265332` |

## Worst Test Predictions

| Constant | Sector | Unit | Observed | Predicted | Rel error % |
|:--|:--|:--|--:|--:|--:|
| `atomic unit of 1st hyperpolarizablity` | `quantum_atomic` | `C^3 m^3 J^-2` | `3.20636151e-53` | `7.92544764891e-38` | `2.47178854418e+17` |
| `inverse meter-kilogram relationship` | `general_dimensional` | `kg` | `2.2102190943e-42` | `4.06634721972e-31` | `1.8397937246e+13` |
| `joule-inverse meter relationship` | `general_dimensional` | `m^-1` | `5.03411656754e+24` | `5.13963770653e+29` | `10209512.0294` |
| `joule-hartree relationship` | `quantum_atomic` | `E_h` | `2.2937122784e+17` | `3.2517047553e+20` | `141666.026451` |
| `natural unit of action` | `general_dimensional` | `J s` | `1.05457181765e-34` | `1.99019506394e-32` | `18772.0676074` |
| `Josephson constant` | `electromagnetic_quantum` | `Hz V^-1` | `4.83597848417e+14` | `3.30350242203e+16` | `6731.09412674` |
| `neutron mass in u` | `nuclear_particle` | `u` | `1.00866491606` | `60.7901520347` | `5926.79354331` |
| `conventional value of coulomb-90` | `general_dimensional` | `C` | `1.00000008887` | `53.3063154184` | `5230.6310681` |
| `electron charge to mass quotient` | `electromagnetic_quantum` | `C kg^-1` | `-175882000838` | `-6.04681502642e+12` | `3337.99535916` |
| `alpha particle mass in u` | `nuclear_particle` | `u` | `4.00150617913` | `135.824985696` | `3294.34651892` |
| `Boltzmann constant in Hz/K` | `thermodynamic_statistical` | `Hz K^-1` | `20836619123.3` | `694260969250` | `3231.92714778` |
| `inverse meter-kelvin relationship` | `thermodynamic_statistical` | `K` | `0.014387768775` | `0.237047680113` | `1547.56387053` |
| `Faraday constant` | `general_dimensional` | `C mol^-1` | `96485.3321233` | `1125326.40365` | `1066.31862988` |
| `electron volt-inverse meter relationship` | `quantum_atomic` | `m^-1` | `806554.393735` | `8038971.17012` | `896.705396755` |
| `lattice spacing of ideal Si (220)` | `general_dimensional` | `m` | `1.920155716e-10` | `1.33667644531e-09` | `596.129191072` |
| `electron volt-kelvin relationship` | `quantum_atomic` | `K` | `11604.5181216` | `80306.8824879` | `592.031169642` |
| `electron-deuteron magn. moment ratio` | `dimensionless_ratio` | `` | `-2143.923493` | `-13706.5467916` | `539.320705068` |
| `electron to shielded proton mag. mom. ratio` | `dimensionless_ratio` | `` | `-658.2275856` | `-3317.77872697` | `404.047353766` |
| `electron to shielded proton magn. moment ratio` | `dimensionless_ratio` | `` | `-658.2275956` | `-3317.77872697` | `404.047346108` |
| `alpha particle-electron mass ratio` | `dimensionless_ratio` | `` | `7294.29954171` | `36448.5221539` | `399.685020412` |
| `atomic unit of electric field` | `quantum_atomic` | `V m^-1` | `514220675112` | `2.47975343702e+12` | `382.235265332` |
| `neutron-proton mass difference in u` | `nuclear_particle` | `u` | `0.00138844948` | `0.00582345310214` | `319.421317521` |
| `Hartree energy in eV` | `quantum_atomic` | `eV` | `27.211386246` | `113.959184982` | `318.792280379` |
| `electron mag. mom.` | `electromagnetic_quantum` | `J T^-1` | `-9.2847646917e-24` | `-3.81774457358e-23` | `311.183772594` |
| `shielded proton gyromag. ratio` | `electromagnetic_quantum` | `s^-1 T^-1` | `267515319.4` | `1066042840.12` | `298.497866406` |
| `proton gyromagn. ratio` | `electromagnetic_quantum` | `s^-1 T^-1` | `267522187.08` | `1066042840.12` | `298.487636392` |
| `helion mass energy equivalent in MeV` | `nuclear_particle` | `MeV` | `2808.39161112` | `11093.3580813` | `295.007520937` |
| `shielded helion gyromag. ratio` | `electromagnetic_quantum` | `s^-1 T^-1` | `203789460.78` | `758193459.289` | `272.04743385` |
| `shielded helion gyromagn. ratio` | `electromagnetic_quantum` | `s^-1 T^-1` | `203789460.78` | `758193459.289` | `272.04743385` |
| `electron volt-hertz relationship` | `quantum_atomic` | `Hz` | `2.41798924208e+14` | `8.44572257747e+14` | `249.287020408` |
| `deuteron magn. moment` | `electromagnetic_quantum` | `J T^-1` | `4.33073482e-27` | `1.50617314229e-26` | `247.786970317` |
| `electron to shielded helion magn. moment ratio` | `dimensionless_ratio` | `` | `864.058255` | `2835.12966736` | `228.117884524` |
| `proton-neutron mass ratio` | `dimensionless_ratio` | `` | `0.99862347797` | `2.9850196617` | `198.913427088` |
| `nuclear magneton` | `electromagnetic_quantum` | `J T^-1` | `5.0507837393e-27` | `1.50617314229e-26` | `198.205827063` |
| `electron-muon magn. moment ratio` | `dimensionless_ratio` | `` | `206.7669894` | `506.504476013` | `144.963897517` |
| `triton-proton mass ratio` | `dimensionless_ratio` | `` | `2.99371703403` | `7.27835173414` | `143.120897914` |
| `kilogram-hertz relationship` | `general_dimensional` | `Hz` | `1.35639248965e+50` | `5.08539714785e+27` | `100` |
| `atomic unit of charge` | `quantum_atomic` | `C` | `1.602176634e-19` | `2.13159814357e-24` | `99.9986695611` |
| `unified atomic mass unit` | `general_dimensional` | `kg` | `1.66053906892e-27` | `4.06634721972e-31` | `99.9755118847` |
| `hertz-hartree relationship` | `quantum_atomic` | `E_h` | `1.51982984606e-16` | `4.487316078e-20` | `99.9704748786` |
| `atomic unit of energy` | `quantum_atomic` | `J` | `4.35974472221e-18` | `2.29618868777e-21` | `99.9473320381` |
| `electron volt-atomic mass unit relationship` | `quantum_atomic` | `u` | `1.07354410083e-09` | `6.68955753894e-13` | `99.937687166` |
| `atomic unit of permittivity` | `quantum_atomic` | `F m^-1` | `1.1126500562e-10` | `4.11956494828e-13` | `99.6297519669` |
| `muon mass` | `lepton_particle` | `kg` | `1.883531627e-28` | `8.83512797058e-31` | `99.5309275489` |
| `tau Compton wavelength over 2 pi` | `quantum_atomic` | `m` | `1.11056e-16` | `6.29955084132e-19` | `99.4327590728` |
| `Bohr magneton in eV/T` | `quantum_atomic` | `eV T^-1` | `5.7883817982e-05` | `3.29650302295e-07` | `99.4304966158` |
| `proton Compton wavelength over 2 pi` | `quantum_atomic` | `m` | `2.10308910109e-16` | `2.17743775743e-18` | `98.9646478809` |
| `shielding difference of d and p in HD` | `dimensionless_ratio` | `` | `1.9877e-08` | `2.66469837906e-10` | `98.6594061583` |
| `muon Compton wavelength over 2 pi` | `quantum_atomic` | `m` | `1.867594308e-15` | `3.05649892935e-17` | `98.3634031672` |
| `reduced muon Compton wavelength` | `quantum_atomic` | `m` | `1.867594306e-15` | `3.05649892935e-17` | `98.3634031655` |
| `atomic unit of mass` | `quantum_atomic` | `kg` | `9.1093837139e-31` | `1.59576601415e-32` | `98.248217372` |
| `nuclear magneton in eV/T` | `electromagnetic_quantum` | `eV T^-1` | `3.15245125417e-08` | `1.26119151285e-09` | `95.9993306441` |
| `Bohr magneton in K/T` | `quantum_atomic` | `K T^-1` | `0.67171381472` | `0.036809290715` | `94.5200932438` |
| `proton mag. shielding correction` | `dimensionless_ratio` | `` | `2.56715e-05` | `2.34300299283e-06` | `90.8731356063` |
| `kelvin-hartree relationship` | `quantum_atomic` | `E_h` | `3.16681156346e-06` | `3.0681491039e-07` | `90.3115514061` |
| `electron-helion mass ratio` | `dimensionless_ratio` | `` | `0.000181954307465` | `2.50450488382e-05` | `86.2355284757` |
| `electron-triton mass ratio` | `dimensionless_ratio` | `` | `0.000181920006233` | `2.50450488382e-05` | `86.2329331684` |
| `atomic mass constant energy equivalent` | `general_dimensional` | `J` | `1.49241808768e-10` | `2.74788200632e-10` | `84.1228023842` |
| `conductance quantum` | `general_dimensional` | `S` | `7.74809172986e-05` | `1.23364556465e-05` | `84.0780722834` |
| `natural unit of energy in MeV` | `general_dimensional` | `MeV` | `0.51099895069` | `0.084924107953` | `83.3807666653` |

## Interpretation

The exact symbolic mode converges perfectly by definition because C_i is defined from O_i.
The predictive mode is the honest test: it tries to estimate calibration coefficients on held-out constants.
Therefore the theory can be symbolically complete while still having limited empirical predictive power.
