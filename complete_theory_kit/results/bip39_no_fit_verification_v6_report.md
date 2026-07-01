# BIP39 No-Fit Verification v6

Final verdict: `PASS_README_TOLERANCE_ONLY: no fitting, but not all constants are within 1%`

## What Changed From v5

v5 searched formula space. v6 does not search.
v6 uses a frozen registry of the 11 sparse BIP39 formulas and only recomputes their predictions.
Target-calibrated coefficients are not used for prediction; they are reported only as an audit of how much exact fitting would change each result.

Frozen formula registry SHA256: `d388fa65f2b74ffde9e313ee8334b11028eca6c02255da5a5b831fd9f8a0cbdb`

## Precision Summary

- `mean_relative_error_percent = 0.899025251536`
- `max_relative_error_percent = 1.75723248969`
- `mean_exact_fit_coefficient_deviation_percent = 0.900073489509`

| Threshold | Pass |
|:--|--:|
| `README log tolerance` | 11/11 |
| `relative <= 1%` | 7/11 |
| `relative <= 0.5%` | 4/11 |
| `relative <= 0.1%` | 0/11 |

## Frozen No-Fit Formulas

| Target | Formula | Observed | Predicted | Rel error % | log10 error | README pass | <=1% | <=0.5% | <=0.1% | Exact-fit coefficient |
|:--|:--|--:|--:|--:|--:|:--|:--|:--|:--|--:|
| `alpha` | `K^-1 * lnDict^-1 * U^-1` | `0.00729735256928` | `0.00728622367155` | `0.152505961919` | `0.000662830533795` | `True` | `True` | `True` | `False` | `1.00152738898` |
| `alpha_s_mZ` | `K^-1 * bits^-1 * bip_density^-1` | `0.1181` | `0.11753902663` | `0.474998619868` | `0.00206780772142` | `True` | `True` | `True` | `False` | `1.00477265625` |
| `g_I_squared` | `K * lnDict^-1` | `0.801` | `0.786924567758` | `1.75723248969` | `0.00769941190396` | `True` | `False` | `False` | `False` | `1.01788663465` |
| `infoton_mass_micro_eV` | `m_e[micro-eV] * dict^-2 * entropy^-2 * U` | `5.6` | `5.5770980126` | `0.408964060632` | `0.00177975010307` | `True` | `True` | `True` | `False` | `1.00410643445` |
| `proton_mass_MeV` | `m_e * pi * words^2` | `938.2720813` | `924.681915252` | `1.44842485662` | `0.00633643002875` | `True` | `False` | `False` | `False` | `1.01469712538` |
| `W_mass_GeV` | `m_e[GeV] * K * entropy * f1` | `80.379` | `81.7846285063` | `1.7487509254` | `0.00752908650134` | `True` | `False` | `False` | `False` | `0.982813047733` |
| `Z_mass_GeV` | `m_e[GeV] * dict * total_bits / U` | `91.1876` | `92.0928222708` | `0.992703252198` | `0.00428999703233` | `True` | `True` | `False` | `False` | `0.990170544799` |
| `H_mass_GeV` | `m_e[GeV] * bits^2 * dict` | `125.2` | `126.629627802` | `1.14187524089` | `0.00493100149371` | `True` | `False` | `False` | `False` | `0.988710163439` |
| `sin2_thetaW` | `lnK / checksum` | `0.223` | `0.223969933654` | `0.434947826685` | `0.00188485830037` | `True` | `True` | `True` | `False` | `0.995669357767` |
| `G_F_GeV_minus2` | `1 / (pi * total_bits * f1)` | `1.1663787e-05` | `1.15713955249e-05` | `0.792122447985` | `0.00345384153998` | `True` | `True` | `False` | `False` | `1.00798447127` |
| `Lambda_QCD_GeV` | `U * bip_density / lnK` | `0.217` | `0.215835247976` | `0.536752085008` | `0.00233736323643` | `True` | `True` | `False` | `False` | `1.0053964866` |

## Calibration Audit

The branch `BIP39_TARGET_CALIBRATED` can force 11/11 by multiplying each row by a target-specific coefficient.
v6 rejects that as proof. The coefficient column above shows how close such exact-fit constants would be to 1, but they are not used.

## Scientific Status

This is the strongest current BIP39 result in the package: frozen formulas, no fitted coefficients, no search during verification.
It is still not a final physical proof because the formulas were discovered before this freeze.
The next gate is future blind prediction with this exact registry hash unchanged.
