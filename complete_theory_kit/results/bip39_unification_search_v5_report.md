# BIP39 Unification Search v5

This report tests whether the README constants can be rebuilt from BIP39 invariants.
The strict target is not a pretty fit; the strict target is a low-complexity, non-calibrated formula set.
Search space tested for sparse formulas: `101635` candidate monomials per physical target.

## BIP39 Invariants

| Invariant | Value |
|:--|--:|
| `bits_per_word` | `11` |
| `dictionary_size` | `2048` |
| `words_per_phrase` | `24` |
| `sha256_entropy_bits` | `256` |
| `checksum_bits` | `8` |
| `phrase_bits_total` | `264` |
| `table_rows` | `4` |
| `table_columns` | `6` |
| `derived_K` | `6.0` |

## Variant Leaderboard

| Variant | Pass | Mean log10 error | Max log10 error | Mean complexity | Verdict |
|:--|--:|--:|--:|--:|:--|
| `BIP39_EXACT_SECTOR` | 8/8 | `0` | `0` | `1` | `PASS_NUMERICALLY: requires external derivation before physics claim` |
| `BIP39_K_ONLY_ORIGINAL_GRAPH` | 9/11 | `0.0196354821867` | `0.0775901483907` | `4` | `PARTIAL_SUPPORT: promising but incomplete` |
| `BIP39_SPARSE_MONOMIAL_NO_COEFFICIENT` | 11/11 | `0.0039065798541` | `0.00769941190396` | `3` | `NUMERIC_HIT_WITH_LOOK_ELSEWHERE_RISK: no coefficients, but target-specific formula search` |
| `BIP39_TARGET_CALIBRATED` | 11/11 | `2.19165333308e-17` | `9.64327466553e-17` | `4` | `CURVE_FIT: exact target coefficients make this non-predictive` |

## Physical-Constant Details

| Variant | Target | Observed | Predicted | log10 error | Tol | Pass | Complexity | Formula |
|:--|:--|--:|--:|--:|--:|:--|--:|:--|
| `BIP39_K_ONLY_ORIGINAL_GRAPH` | `alpha` | `0.00729735256928` | `0.00729807144137` | `4.27808307069e-05` | `0.002` | `True` | 4 | `2 ln(K)^2 / (pi ln(N))` |
| `BIP39_K_ONLY_ORIGINAL_GRAPH` | `alpha_s_mZ` | `0.1181` | `0.113143011172` | `0.0186221648041` | `0.03` | `True` | 4 | `pi^3 alpha / 2` |
| `BIP39_K_ONLY_ORIGINAL_GRAPH` | `g_I_squared` | `0.801` | `0.797650077694` | `0.00182010425156` | `0.01` | `True` | 4 | `2 pi alpha f1 / K` |
| `BIP39_K_ONLY_ORIGINAL_GRAPH` | `infoton_mass_micro_eV` | `5.6` | `5.60058744215` | `4.55552688144e-05` | `0.02` | `True` | 4 | `chi_I m_e/(K f1^6)` |
| `BIP39_K_ONLY_ORIGINAL_GRAPH` | `proton_mass_MeV` | `938.2720813` | `938.300000353` | `1.29225952362e-05` | `0.01` | `True` | 4 | `m_e C_p pi K f1` |
| `BIP39_K_ONLY_ORIGINAL_GRAPH` | `W_mass_GeV` | `80.379` | `80.3800085651` | `5.44932772618e-06` | `0.01` | `True` | 4 | `m_e C_W f1^2 K sqrt(K)` |
| `BIP39_K_ONLY_ORIGINAL_GRAPH` | `Z_mass_GeV` | `91.1876` | `80.9003922186` | `0.0519851583533` | `0.01` | `False` | 4 | `m_e C_Z f1^2 K sqrt(K)` |
| `BIP39_K_ONLY_ORIGINAL_GRAPH` | `H_mass_GeV` | `125.2` | `149.690582114` | `0.0775901483907` | `0.02` | `False` | 4 | `m_e C_H f1^2 K^2` |
| `BIP39_K_ONLY_ORIGINAL_GRAPH` | `sin2_thetaW` | `0.223` | `0.2146` | `0.0166751454182` | `0.02` | `True` | 4 | `fixed weak proxy` |
| `BIP39_K_ONLY_ORIGINAL_GRAPH` | `G_F_GeV_minus2` | `1.1663787e-05` | `1.13e-05` | `0.0137611366289` | `0.05` | `True` | 4 | `weak proxy from README scale` |
| `BIP39_K_ONLY_ORIGINAL_GRAPH` | `Lambda_QCD_GeV` | `0.217` | `0.2` | `0.0354297381845` | `0.05` | `True` | 4 | `QCD scale proxy` |
| `BIP39_SPARSE_MONOMIAL_NO_COEFFICIENT` | `alpha` | `0.00729735256928` | `0.00728622367155` | `0.000662830533795` | `0.002` | `True` | 3 | `1 * K^-1 * lnDict^-1 * U^-1` |
| `BIP39_SPARSE_MONOMIAL_NO_COEFFICIENT` | `alpha_s_mZ` | `0.1181` | `0.11753902663` | `0.00206780772142` | `0.03` | `True` | 3 | `1 * K^-1 * bits^-1 * bip_density^-1` |
| `BIP39_SPARSE_MONOMIAL_NO_COEFFICIENT` | `g_I_squared` | `0.801` | `0.786924567758` | `0.00769941190396` | `0.01` | `True` | 2 | `1 * K^1 * lnDict^-1` |
| `BIP39_SPARSE_MONOMIAL_NO_COEFFICIENT` | `infoton_mass_micro_eV` | `5.6` | `5.5770980126` | `0.00177975010307` | `0.02` | `True` | 5 | `5.10999e+11 * dict^-2 * entropy^-2 * U^1` |
| `BIP39_SPARSE_MONOMIAL_NO_COEFFICIENT` | `proton_mass_MeV` | `938.2720813` | `924.681915252` | `0.00633643002875` | `0.01` | `True` | 3 | `0.510999 * pi^1 * words^2` |
| `BIP39_SPARSE_MONOMIAL_NO_COEFFICIENT` | `W_mass_GeV` | `80.379` | `81.7846285063` | `0.00752908650134` | `0.01` | `True` | 3 | `0.000510999 * K^1 * entropy^1 * f1^1` |
| `BIP39_SPARSE_MONOMIAL_NO_COEFFICIENT` | `Z_mass_GeV` | `91.1876` | `92.0928222708` | `0.00428999703233` | `0.01` | `True` | 3 | `0.000510999 * dict^1 * total_bits^1 * U^-1` |
| `BIP39_SPARSE_MONOMIAL_NO_COEFFICIENT` | `H_mass_GeV` | `125.2` | `126.629627802` | `0.00493100149371` | `0.02` | `True` | 3 | `0.000510999 * bits^2 * dict^1` |
| `BIP39_SPARSE_MONOMIAL_NO_COEFFICIENT` | `sin2_thetaW` | `0.223` | `0.223969933654` | `0.00188485830037` | `0.02` | `True` | 2 | `1 * checksum^-1 * lnK^1` |
| `BIP39_SPARSE_MONOMIAL_NO_COEFFICIENT` | `G_F_GeV_minus2` | `1.1663787e-05` | `1.15713955249e-05` | `0.00345384153998` | `0.05` | `True` | 3 | `1 * pi^-1 * total_bits^-1 * f1^-1` |
| `BIP39_SPARSE_MONOMIAL_NO_COEFFICIENT` | `Lambda_QCD_GeV` | `0.217` | `0.215835247976` | `0.00233736323643` | `0.05` | `True` | 3 | `1 * lnK^-1 * U^1 * bip_density^1` |
| `BIP39_TARGET_CALIBRATED` | `alpha` | `0.00729735256928` | `0.00729735256928` | `9.64327466553e-17` | `0.002` | `True` | 4 | `C_alpha(1.00152738898) * [1 * K^-1 * lnDict^-1 * U^-1]` |
| `BIP39_TARGET_CALIBRATED` | `alpha_s_mZ` | `0.1181` | `0.1181` | `0` | `0.03` | `True` | 4 | `C_alpha_s_mZ(1.00477265625) * [1 * K^-1 * bits^-1 * bip_density^-1]` |
| `BIP39_TARGET_CALIBRATED` | `g_I_squared` | `0.801` | `0.801` | `0` | `0.01` | `True` | 3 | `C_g_I_squared(1.01788663465) * [1 * K^1 * lnDict^-1]` |
| `BIP39_TARGET_CALIBRATED` | `infoton_mass_micro_eV` | `5.6` | `5.6` | `4.82163733277e-17` | `0.02` | `True` | 6 | `C_infoton_mass_micro_eV(1.00410643445) * [5.10999e+11 * dict^-2 * entropy^-2 * U^1]` |
| `BIP39_TARGET_CALIBRATED` | `proton_mass_MeV` | `938.2720813` | `938.2720813` | `4.82163733277e-17` | `0.01` | `True` | 4 | `C_proton_mass_MeV(1.01469712538) * [0.510999 * pi^1 * words^2]` |
| `BIP39_TARGET_CALIBRATED` | `W_mass_GeV` | `80.379` | `80.379` | `0` | `0.01` | `True` | 4 | `C_W_mass_GeV(0.982813047733) * [0.000510999 * K^1 * entropy^1 * f1^1]` |
| `BIP39_TARGET_CALIBRATED` | `Z_mass_GeV` | `91.1876` | `91.1876` | `0` | `0.01` | `True` | 4 | `C_Z_mass_GeV(0.990170544799) * [0.000510999 * dict^1 * total_bits^1 * U^-1]` |
| `BIP39_TARGET_CALIBRATED` | `H_mass_GeV` | `125.2` | `125.2` | `0` | `0.02` | `True` | 4 | `C_H_mass_GeV(0.988710163439) * [0.000510999 * bits^2 * dict^1]` |
| `BIP39_TARGET_CALIBRATED` | `sin2_thetaW` | `0.223` | `0.223` | `0` | `0.02` | `True` | 3 | `C_sin2_thetaW(0.995669357767) * [1 * checksum^-1 * lnK^1]` |
| `BIP39_TARGET_CALIBRATED` | `G_F_GeV_minus2` | `1.1663787e-05` | `1.1663787e-05` | `0` | `0.05` | `True` | 4 | `C_G_F_GeV_minus2(1.00798447127) * [1 * pi^-1 * total_bits^-1 * f1^-1]` |
| `BIP39_TARGET_CALIBRATED` | `Lambda_QCD_GeV` | `0.217` | `0.217` | `4.82163733277e-17` | `0.05` | `True` | 4 | `C_Lambda_QCD_GeV(1.0053964866) * [1 * lnK^-1 * U^1 * bip_density^1]` |

## Exact BIP39 Sector

| Target | Observed | Predicted | Formula | Pass |
|:--|--:|--:|:--|:--|
| `bits_per_word` | `11` | `11` | `2K-1` | `True` |
| `dictionary_size` | `2048` | `2048` | `2^(2K-1)` | `True` |
| `words_per_phrase` | `24` | `24` | `4K` | `True` |
| `sha256_entropy_bits` | `256` | `256` | `4*2^K` | `True` |
| `checksum_bits` | `8` | `8` | `K+2` | `True` |
| `phrase_bits_total` | `264` | `264` | `4K(2K-1)` | `True` |
| `table_rows` | `4` | `4` | `4` | `True` |
| `table_columns` | `6` | `6` | `K` | `True` |

## Scientific Reading

BIP39 exactly reproduces its own eight structural numbers from K=6.
That is a real arithmetic identity, but it is not by itself a derivation of particle physics.
The sparse non-calibrated variant is the most interesting result: it hits all listed targets without fitted coefficients.
However, because each target was allowed to choose its own sparse monomial from a search space, this is still a look-elsewhere risk.
The next scientific gate is to freeze a single generative rule for choosing each formula before seeing new targets.
